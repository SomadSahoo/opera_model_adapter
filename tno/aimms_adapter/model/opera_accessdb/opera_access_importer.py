import shutil
from enum import Enum
from typing import TypedDict

import pandas as pd
import pandas.io.sql as psql
import sqlalchemy as sa
import time
import gc
import pyodbc
from contextlib import contextmanager

import sys
sys.path.append("..\opera-model-adapter")

from tno.shared.log import get_logger

log = get_logger(__name__)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)


class StorageType(Enum):
    STORAGE = 0
    CHARGER = 1
    DISCHARGER = 2

class OperaStorageOption(TypedDict):
    name: str
    nr: int
    type: StorageType

def not_empty(value):
    return not (value is None or pd.isna(value) or str(value).strip() == '')

def opera_energycarrier(carrier):
    if pd.isna(carrier):
        return None
    else:
        return 'MMvIB_' + carrier


def activity_name(activity):
    return 'Activity_' + activity


def copy_clean_access_database(empty_source, target_db):
    log.info(f"Copying empty Opera DB to target {target_db}")
    try:
        shutil.copy2(empty_source, target_db)
    except IOError as e:
        print(e)


class OperaAccessImporter:
    year: int = 2030
    scenario = 'MMvIB'
    default_sector = 'Energie'


    def __init__(self, year=2030, scenario='MMvIB', default_sector="Energie"):
        self.year = year
        self.scenario = scenario
        self.default_sector = default_sector
        self.df: pd.DataFrame = None  # df with ESDL as a table
        self.carriers: pd.DataFrame = None  # df with carriers and prices
        self.df_kpi: pd.DataFrame = None  # df with electricity and NG demand for Ameland
        self.df_electricity: pd.DataFrame = None  # df with hourly import electricity prices for the Netherlands
        self.engine = None  # db engine
        self.conn = None  # db connection
        self.cursor = None  # db cursor
        self.not_consumer_options: pd.DataFrame = None
        self.consumer_options: pd.DataFrame = None


    def __enter__(self):
        """
        Enter the context: this is automatically called when using 'with'.
        """
        return self  # Return the instance itself to allow access to methods
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context: this is automatically called when leaving 'with'.
        It ensures the connection is closed even in case of an exception.
        """
        self.disconnect()

    @contextmanager
    def connect_to_access(self, access_file: str):
        #access_file = r'C:\data\git\aimms-adapter\esdl2opera_access\Opties_mmvib.mdb'
        # odbc_string = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + access_file + ';Pooling=False;'
        odbc_string = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={access_file};"
        log.info(f"Connecting to database: {access_file}")
        
        connection_url = sa.engine.URL.create(
        "access+pyodbc",
        query={"odbc_connect": odbc_string}
        )
            
        try:    
            # Create an engine for the database connection
            self.engine = sa.create_engine(connection_url)

            # Connect to the engine
            self.conn = self.engine.raw_connection() # Raw DBAPI connection
            log.info("Connection to the database established.")

            #Create a cursor
            self.cursor = self.conn.cursor()
            log.info("Cursor created successfully.")

            yield # Yield control to the block of code that uses this context manager
            
        except Exception as e:
            print(f"Error connecting to the Access database: {e}", exc_info=True)
            raise # Raising the exception so that the caller can handle it

        finally:
            self.disconnect()

    def disconnect(self): 
        log.info("Disconnecting database")
        try:
            if self.cursor:
                log.info(f"Closing cursor: {self.cursor}")
                self.cursor.close()
                self.cursor = None
                log.info("Cursor closed successfully.")
            
            if self.conn:
                log.info(f"Closing connection: {self.conn}")
                self.conn.close() #Close the raw connection
                self.conn = None
                log.info("Raw connection closed successfully.")
            
            if self.engine:
                log.info(f"Disposing engine: {self.engine}")
                self.engine.dispose() # Dispose of the engine
                self.engine = None
                log.info("Engine disposed successfully.")

            # Pause to ensure all resources are freed
            time.sleep(3) # Give some time for cleanup

        except Exception as e: 
            log.error(f"Error during disconnect: {e}", exc_info=True)
    
        # Optionally trigger garbage collection, but usually not necessary
        finally:
            garbage_collected = gc.collect()
            log.info(f'amount of garbage collected is {garbage_collected}')

    def execute_query(self, query: str):
        """Execute a single query and commit the transaction."""
        try:
            log.debug(f"Executing query: {query}")
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as ex:
            log.error(f"Failed to execute query: {query}", exc_info=True)
            raise ex  
    
    def fetch_query(self, query: str) -> pd.DataFrame:
        """Fetch data from the database using a query."""
        try:
            log.debug(f"Fetching data with query: {query}")
            return psql.read_sql(query, self.engine)
        except Exception as ex:
            log.error(f"Failed to fetch data with query: {query}", exc_info=True)
            raise ex

    def start_import(self, esdl_data_frame: pd.DataFrame, 
                     carriers: pd.DataFrame, 
                     esdl_kpi: pd.DataFrame,
                     hourly_electricity_price: pd.DataFrame,
                     access_database: str):
        """
        Connects to database file and uses esdl-dataframe to create opera database
        :param esdl_data_frame: dataframe extracting all relevant info for all the assets in the ESDL
        :param carriers: dataframe describing the carriers in the ESDL
        :param esdl_kpi: dataframe with KPI-related data obtained from the ESSIM model
        :param hourly_electricity_price: dataframe with hourly national import electricity prices (from ESSIM)
        :param access_database: the path to the access database
        :return:
        """
        self.df = esdl_data_frame
        self.carriers = carriers
        self.df_kpi = esdl_kpi
        self.df_electricity = hourly_electricity_price
        is_consumer = self.df['category'] == 'Consumer'
        self.not_consumer_options = self.df[~is_consumer]
        self.consumer_options = self.df[is_consumer]

        #self.copy_clean_access_database()
        try:
            with self.connect_to_access(access_file=access_database):
                log.info("Database connection established and cursor created successfully")

                self._create_energycarriers()
                log.info("Created energy carriers successfully")

                self._add_activities()  # first activities, then options
                log.info("Added activities successfully")

                self._add_options()
                log.info("Added options successfully")
                
                self._update_option_related_tables()
                log.info("Updated options-related tables successfully")

                self._add_demand() # this is for KPI-related demand addition
                log.info("Demand added successfully")

                self._add_electricity_import_price() # this is for adding electricity import price
                log.info("Electricity import price added successfully")
        
        except Exception as e: 
            log.error(f"Failed to connect to the Access database: {e}")           
        
        # finally:
        #    self.disconnect()
        #    log.info("Import to Opera finished")
        


    def _create_energycarriers(self):
        # TODO: use ESDL price information for carriers
        #carriers = pd.concat([self.df['carrier_in'], self.df['carrier_out']]).dropna().unique()
        for index, carrier in self.carriers.iterrows():
            #if carrier == "": continue
            carrier_name = carrier['name']
            new_carrier_name = opera_energycarrier(carrier['name'])
            sql = "SELECT * FROM [Energiedragers] WHERE [Energiedrager] = '{}'".format(new_carrier_name)
            df = psql.read_sql(sql, self.engine)
            if df.shape[0] == 0:  # not in table yet, insert
                vraagisaanbod = False
                generiek = False
                basisenergiedrager = False
                electriciteit = False
                warmte = False
                # TODO: use
                price = 0.0
                if not_empty(carrier['cost']):
                    price = float(carrier['cost'])
                    print("Using ESDL-defined energy carrier cost")
                # rest of the if statement in case no cost is assigned
                elif carrier_name.lower().startswith("ele"):
                    vraagisaanbod = True
                    generiek = True
                    basisenergiedrager = True
                    electriciteit = True
                    price = 10.11  # EUR/MWh
                elif carrier_name.lower().startswith("hydrogen") or carrier_name.lower().startswith(
                        "waterstof") or carrier_name.lower().startswith("h2"):
                    vraagisaanbod = True
                    generiek = True
                    price = 8.34  # EUR/GJ
                elif carrier_name.lower().startswith("aardgas") or carrier_name.lower().startswith("natural") or \
                        carrier_name.lower().startswith("fossil gas") or carrier_name.lower().startswith("gas"):
                    basisenergiedrager = True
                    price = 6.8  # EUR/GJ (KEV 2020 in EUR 2015)
                elif carrier_name.lower().startswith("heat") or carrier_name.lower().startswith("warmte"):
                    vraagisaanbod = True
                    generiek = True
                    warmte = True
                else:
                    print(f"EnergyCarrier {carrier_name} is not matched to a similar energy carrier in Opera, using default values")

                print(f"Inserting new Energy carrier {new_carrier_name}")
                sql = f"INSERT INTO [Energiedragers] ([Energiedrager],[Eenheid],[VraagIsAanbod], [Generiek], [Basisenergiedrager], [Elektriciteit], [Warmte]) " \
                      f" VALUES ('{new_carrier_name}', 'PJ', {vraagisaanbod}, {generiek}, {basisenergiedrager}, {electriciteit}, {warmte});"
                print(sql)
                self.cursor.execute(sql)

                if price != 0.0:
                    print(f"Inserting Energy carrier price {price} for {new_carrier_name}")
                    sql = f"INSERT INTO [EconomieNationaal(Energiedrager,Jaar,Scenario)] ([Energiedrager],[Jaar],[Scenario], [Nationale prijs]) " \
                          f" VALUES ('{new_carrier_name}', {self.year}, '{self.scenario}', {price});"
                    print(sql)
                    self.cursor.execute(sql)
                else:
                    print(f"WARNING: No price is set for {new_carrier_name}")
            else:
                print(f"Energy carrier {new_carrier_name} already present")
        self.conn.commit()

    def _add_activities(self):
        for index, row in self.consumer_options.iterrows():
            activiteiten_name = activity_name(row['name'])
            eenheid = 'PJ'
            sql = "SELECT * FROM [Activiteiten] WHERE [Activiteit] = '{}'".format(activiteiten_name)
            df = psql.read_sql(sql, self.engine)
            if df.shape[0] == 0:  # Case where new activity is NOT in table 'Activiteiten'
                print(f'Adding {activiteiten_name} to [Activiteiten]')

                sql = f"INSERT INTO [Activiteiten] ([Activiteit],[Eenheid]) VALUES ('{activiteiten_name}', '{eenheid}' )"
                self.cursor.execute(sql)
            else:
                print(f"{activiteiten_name} already in [Activiteiten]")

            # add to ActiviteitBaseline(activiteit,scenario,jaar) the annual demand
            sql = "SELECT * FROM [ActiviteitBaseline(activiteit,scenario,jaar)] WHERE [Activiteit] = '{}' AND [Scenario] = '{}' AND [Jaar] = {}" \
                .format(activiteiten_name, self.scenario, self.year)
            df = psql.read_sql(sql, self.engine)
            if df.shape[0] == 0:  # Case where new activity is NOT in table 'ActiviteitBaseline'
                print(f'Adding {activiteiten_name} to [ActiviteitBaseline]')
                #value = row['power'] if not pd.isna(row['power']) else 0.0
                # for activities: use InPort profile
                value = row['profiles_in'] if not pd.isna(row['profiles_in']) else 0.0
                sql = f"INSERT INTO [ActiviteitBaseline(activiteit,scenario,jaar)] ([Activiteit],[Scenario], [Jaar], [Waarde]) VALUES " \
                      f"('{activiteiten_name}', '{self.scenario}', {self.year}, {value} )"
                self.cursor.execute(sql)
            else:
                print(f"{activiteiten_name} already in [ActiviteitBaseline]")

        self.conn.commit()

    def _add_options(self):
        ## Add option to Opties table
        for index, row in self.df.iterrows():
            new_opt = row['name']
            sql = "SELECT * FROM [Opties] WHERE [Naam optie] = '{}'".format(new_opt)
            df = psql.read_sql(sql, self.engine)
            ref_option_name = row.opera_equivalent
            if df.shape[0] == 0:  # Case where new option is NOT in table 'Opties'
                print(f'Adding {new_opt} to [Opties]')
                if row['category'] == 'Storage':
                    self._add_storage(row)
                else:
                    sql = "SELECT * FROM [Opties] WHERE [Naam optie] = '{}'".format(ref_option_name)
                    df_ref_option = psql.read_sql(sql, self.engine)
                    if df_ref_option.empty:
                        print(f"#######################      There is no Opera equivalent defined for {new_opt}, creating a new one!  ###################")
                        df_ref_option = pd.DataFrame([{'Nr': 1}])  # create dataframe with one row.
                        df_ref_option['Doelstof'] = 'CO2'  # Default doelstof in Opera
                    df_ref_option = df_ref_option.drop('Nr', axis=1)
                    df_ref_option['Naam optie'] = '{}'.format(new_opt)
                    df_ref_option['Sector'] = 'Energie'  # use an unused sector in opera for now (see Sectoren table)
                    if row['category'] == 'Consumer':
                        df_ref_option['Unit of Capacity'] = 'PJ'
                        df_ref_option['Eenheid activiteit'] = 'PJ'
                        df_ref_option['Cap2Act'] = 1  # Cap2Act is a number in DB
                        df_ref_option['Optie onbeperkt'] = True
                        df_ref_option['Capaciteit onbeperkt'] = True
                    else:
                        df_ref_option['Unit of Capacity'] = 'GW'
                        df_ref_option['Eenheid activiteit'] = 'PJ'
                        df_ref_option['Cap2Act'] = 31.536
                        df_ref_option['Capaciteit onbeperkt'] = True   # Fix to get Opera working
                        df_ref_option['Optie onbeperkt'] = True   # Fix to get Opera working
                        #df_ref_option['ReferentieOptie'] = -1   # Fix to get Opera working
                        # df_ref_option['Landelijk beperkt'] = True   # Fix only needed for Windturbine

                    col = [[i] for i in df_ref_option.columns]
                    sql = 'INSERT INTO [Opties] ({}) VALUES ({}{})'.format(str(col)[1:-1],
                            '?,' * (len(df_ref_option.columns) - 1), '?').replace("'", "")
                    values = list(df_ref_option.itertuples(index=False, name=None))
                    print(sql)
                    print(values)
                    self.cursor.executemany(sql, values)
            else: # option already in Opties table
                print(f"{new_opt} ({df.Nr.values}) already in [Opties]")

        self.conn.commit()

    def _add_storage(self, row: pd.Series):

        lifetime = 10 # years
        # for storage 3 options are required: the storage itself, which has the same name as the asset name
        # the charger, which is postfixed with _charger
        # the discharger, which is postfixed with _discharger
        chargerName = f"{row['name']}_charger"
        dischargerName = f"{row['name']}_discharger"
        # assumption here is that if the storage is not in the options, the other 2 are also not there otherwise
        # we should check here
        # do we need to set value for: Optie onbeperkt, Landelijk beperkt, Capaciteit onbeperkt, Flexibel?

        config_storage = {'Unit of Capacity': 'PJ'}
        sql = f"INSERT INTO [Opties] ([Naam optie], [Unit of Capacity], [Eenheid activiteit], [Cap2Act], [Sector], " \
              f"[LaadOpslagOptie], [OntlaadOpslagOptie], [VoorraadOpslagOptie], [Levensduur], [Doelstof]) VALUES (" \
              f"'{row['name']}', 'PJ', 'PJ', 1, '{self.default_sector}', {False}, {False}, {True}, {lifetime}, 'CO2')"
        print(sql)
        self.cursor.execute(sql)
        storage_id = self.cursor.execute("SELECT @@Identity").fetchone()[0]
        sql = f"INSERT INTO [Opties] ([Naam optie], [Unit of Capacity], [Eenheid activiteit], [Cap2Act], [Sector], " \
              f"[LaadOpslagOptie], [OntlaadOpslagOptie], [VoorraadOpslagOptie], [Levensduur], " \
              f"[Doelstof], [ConnectorPointOption]) VALUES (" \
              f"'{chargerName}', 'GW', 'PJ', {31.536}, '{self.default_sector}', {True}, {False}, {False}, {lifetime}," \
              f" 'CO2', {True})"
        self.cursor.execute(sql)
        charger_id = self.cursor.execute("SELECT @@Identity").fetchone()[0]
        sql = f"INSERT INTO [Opties] ([Naam optie], [Unit of Capacity], [Eenheid activiteit], [Cap2Act], [Sector], " \
              f"[LaadOpslagOptie], [OntlaadOpslagOptie], [VoorraadOpslagOptie], [Levensduur], [Doelstof]) VALUES (" \
              f"'{dischargerName}','GW', 'PJ', {31.536}, '{self.default_sector}', {False}, {True}, {False}, {lifetime}, 'CO2')"
        self.cursor.execute(sql)
        discharger_id = self.cursor.execute("SELECT @@Identity").fetchone()[0]

        print(f"storage_id: {storage_id}, charger_id={charger_id}, discharger_id={discharger_id}")
        self.conn.commit()
        storage_option: OperaStorageOption = {'name': row['name'], 'nr': storage_id, 'type': StorageType.STORAGE}
        charger_option: OperaStorageOption = {'name': chargerName, 'nr': charger_id, 'type': StorageType.CHARGER}
        discharger_option: OperaStorageOption = {'name': dischargerName, 'nr': discharger_id, 'type': StorageType.DISCHARGER}
        opera_storage_options = [storage_option, charger_option, discharger_option]

        for optie in opera_storage_options:
            sql = "SELECT * FROM [Beschikbare varianten] WHERE [Nr] = {}".format(optie['nr'])
            df = psql.read_sql(sql, self.engine)

            if df.shape[0] == 0:  # Case where new option is NOT in table 'Beschikbare varianten'
                print(f"Adding new option {optie['name']} to [Beschikbare varianten]")
                # insert using defaults
                q = f"INSERT INTO [Beschikbare varianten] ([Nr], [Variant], [Beschikbaar]) VALUES ({optie['nr']}, 1, 1)"
                self.cursor.execute(q)
            else:
                print(f"Option {optie['nr']}/{optie['name']} is already in [Beschikbare varianten]")
                print(df)
        self.conn.commit()

        # Define flows in OpgelegdeToegestaneFlows
        # manual for charger -> storage and for storage -> discharger
        input_energiedrager = row['carrier_in']
        opera_energiedrager = opera_energycarrier(input_energiedrager)
        sql = "SELECT * FROM [OpgelegdeToegestaneFlows] WHERE [OptieVan] = {}".format(charger_option['nr'])
        df = psql.read_sql(sql, self.engine)
        if df.shape[0] == 0:  # Case where flow is NOT in table 'OpgelegdeToegestaneFlows'
            print(f"Adding new flow {charger_option['name']}->{storage_option['name']} to [OpgelegdeToegestaneFlows]")
            # insert using defaults
            opmerking = "Storage: Charger -> storage"
            q = f"INSERT INTO [OpgelegdeToegestaneFlows] ([Energiedrager], [OptieVan], [OptieNaar], [Match], [Opmerking]) " \
                f" VALUES ('{opera_energiedrager}', {charger_option['nr']}, {storage_option['nr']}, 1, '{opmerking}')"
            self.cursor.execute(q)
        else:
            print(f"Flow {charger_option['name']}->{storage_option['name']} is already in [OpgelegdeToegestaneFlows]")
        self.conn.commit()

        sql = "SELECT * FROM [OpgelegdeToegestaneFlows] WHERE [OptieVan] = {}".format(storage_option['nr'])
        df = psql.read_sql(sql, self.engine)
        if df.shape[0] == 0:  # Case where flow is NOT in table 'OpgelegdeToegestaneFlows'
            print(f"Adding new flow {storage_option['name']}->{discharger_option['name']} to [OpgelegdeToegestaneFlows]")
            # insert using defaults
            opmerking = "Storage: Storage -> Discharger"
            q = f"INSERT INTO [OpgelegdeToegestaneFlows] ([Energiedrager], [OptieVan], [OptieNaar], [Match], [Opmerking]) " \
                f" VALUES ('{opera_energiedrager}', {storage_option['nr']}, {discharger_option['nr']}, 1, '{opmerking}')"
            self.cursor.execute(q)
        else:
            print(f"Flow {storage_option['name']}->{discharger_option['name']} is already in [OpgelegdeToegestaneFlows]")
        self.conn.commit()

        # energiedrageraloc [EnergieDragerAlloc(Optie,Energiedrager,Var,ConstrJaar,Jaar)]
        for optie in opera_storage_options:
            sql = "SELECT * FROM [EnergieDragerAlloc(Optie,Energiedrager,Var,ConstrJaar,Jaar)] WHERE [Nr] = {}".format(optie['nr'])
            df = psql.read_sql(sql, self.engine)
            if df.shape[0] == 0:  # Case where flow is NOT in table 'OpgelegdeToegestaneFlows'
                print(f"Adding Effect of {optie['name']} to [EnergieDragerAlloc(Optie,Energiedrager,Var,ConstrJaar,Jaar)]")
                effect = -1
                if optie['type'] == StorageType.CHARGER:
                    effect = 1

                # todo if e.g. compression energy (electricity) is used when charging, add extra energiedrager with the consumption of this energy as Effect
                # todo: in esdl.InputOutputBehavior is used here, use that.
                # todo: constructiejaar is now hardcoded and same as self.year

                q = f"INSERT INTO [EnergieDragerAlloc(Optie,Energiedrager,Var,ConstrJaar,Jaar)] ([Nr], [Energiedrager], [Variant], [ConstructieJaar], [Jaar], [Effect]) " \
                    f" VALUES (" \
                    f"{optie['nr']}, '{opera_energiedrager}', 1, {self.year}, {self.year}, {effect}" \
                    f")"
                self.cursor.execute(q)
            else:
                print(f"Effect of {optie['name']} is already in [EnergieDragerAlloc(Optie,Energiedrager,Var,ConstrJaar,Jaar)]")

            # add Efficiency to [TechnischeParameters(Optie,Jaar)]
            sql = "SELECT * FROM [TechnischeParameters(Optie,Jaar)] WHERE [Nr] = {}".format(optie['nr'])
            df = psql.read_sql(sql, self.engine)
            if df.shape[0] == 0:  # Case where flow is NOT in table 'OpgelegdeToegestaneFlows'
                print(f"Adding efficiency of {optie['name']} to [TechnischeParameters(Optie,Jaar)]")
                efficiency = 1
                if optie['type'] == StorageType.CHARGER:
                    efficiency = row['storage_charge_efficiency'] if not_empty(row['storage_charge_efficiency']) else 1
                if optie['type'] == StorageType.STORAGE:
                    efficiency = row['efficiency'] if not_empty(row['efficiency']) else 1
                if optie['type'] == StorageType.DISCHARGER:
                    efficiency = row['storage_discharge_efficiency'] if not_empty(row['storage_discharge_efficiency']) else 1
                q = f"INSERT INTO [TechnischeParameters(Optie,Jaar)] ([Nr], [Jaar], [AvailabilityFactor], [Rendement]) " \
                    f" VALUES (" \
                    f"{optie['nr']}, {self.year}, 0.99, {efficiency}" \
                    f")"
                self.cursor.execute(q)
            else:
                print(f"Efficiency of {optie['name']} is already in [TechnischeParameters(Optie,Jaar)]")
            self.conn.commit()

            # add storage options to ([OpslagOpties(Optie,ConstrJr)]
            sql = "SELECT * FROM [OpslagOpties(Optie,ConstrJr)] WHERE [Nr] = {}".format(optie['nr'])
            df = psql.read_sql(sql, self.engine)
            if df.shape[0] == 0:  # Case where flow is NOT in table 'OpgelegdeToegestaneFlows'
                print(f"Adding storage options of {optie['name']} to [OpslagOpties(Optie,ConstrJr)]")
                verliesperuur = 'Null' # check if None works or 0
                slowloadtime = 'Null'
                fastloadtime = 'Null'
                if optie['type'] == StorageType.CHARGER:
                    slowloadtime = row['storage_slow_loadtime'] if not_empty(row['storage_slow_loadtime']) else 1
                    fastloadtime = row['storage_fast_loadtime'] if not_empty(row['storage_fast_loadtime']) else 1
                if optie['type'] == StorageType.STORAGE:
                    verliesperuur = row['storage_losses_perhour'] if not_empty(row['storage_losses_perhour']) else 0
                if optie['type'] == StorageType.DISCHARGER:
                    slowloadtime = row['storage_slow_unloadtime'] if not_empty(row['storage_slow_unloadtime']) else 1
                    fastloadtime = row['storage_fast_unloadtime'] if not_empty(row['storage_fast_unloadtime']) else 1
                q = f"INSERT INTO [OpslagOpties(Optie,ConstrJr)] ([Nr], [ConstructieJaar], [VerliesPerUur], [SlowLoadTime], [FastLoadTime]) " \
                    f" VALUES (" \
                    f"{optie['nr']}, {self.year}, {verliesperuur}, {slowloadtime}, {fastloadtime}" \
                    f")"
                print(q)
                self.cursor.execute(q)
            else:
                print(f"Storage options for {optie['name']} is already in [OpslagOpties(Optie,ConstrJr)]")
            self.conn.commit()


        # add Kosten, only to storage medium ([OpslagOpties(Optie,ConstrJr)] (battery for now only)
        # todo: for hydrogen, all options have cost (charger, discharger)
        sql = "SELECT * FROM [Kosten(Optie,Variant,Jaar)] WHERE [Nr] = {} AND [Jaar] = '{}'".format(
            storage_option['nr'],  self.year)
        df = psql.read_sql(sql, self.engine)
        if df.shape[0] == 0:  # Case where no kost for this option
            print(f"Adding Cost for {storage_option['name']} to [Kosten(Optie,Variant,Jaar)]")
            investerings_kosten = row['investment_cost'] if not_empty(row['investment_cost']) else 0.0
            om_kosten = row['o_m_cost'] if not_empty(row['o_m_cost']) else 0.0
            variable_kosten = row['variable_o_m_cost'] if not_empty(row['variable_o_m_cost']) else 0.0
            q = f"INSERT INTO [Kosten(Optie,Variant,Jaar)] ([Nr], [Variant], [Jaar], [InvesteringsKosten], [Overig operationeel kosten/baten], [Variabele kosten]) " \
                f" VALUES (" \
                f"{storage_option['nr']}, 1, {self.year}, {investerings_kosten}, {om_kosten}, {variable_kosten}" \
                f")"
            self.cursor.execute(q)
        else:
            print(f"Cost for {storage_option['name']} is already in [Kosten(Optie,Variant,Jaar)]")
        self.conn.commit()

        # OptieNetwerken not used for now, as we currently don't use the EnergyNetworks in Opera (e.g. HS, MS, LS, HHD, HLD)

        ## Add option to CatJaarScen table to set capacity ranges for storage options (not charge and discharger)
        sql = "SELECT * FROM [CatJaarScen(categorie,jaar,scenario)] WHERE [Categorie] = '{}' AND [Jaar] = '{}' AND [Scenario] = '{}'".format(
            storage_id, self.year, self.scenario)
        df = psql.read_sql(sql, self.engine)
        if df.shape[0] == 0:  # Case where new option is NOT in table 'CatJaarScen'
            print(f"Adding new CatJaarScen for optie {storage_id}/{storage_option['name']}")
            max_capacity = row['power_max'] if not pd.isna(row['power_max']) else 0  # None
            min_capacity = row['power_min'] if not pd.isna(row['power_min']) else 0
            # currently not filling in columns [Max aantal], [Max kosten], [Min aantal], [Min kosten],
            sql = f'INSERT INTO [CatJaarScen(categorie,jaar,scenario)] ([Categorie], [Jaar], [Scenario], ' \
                  f'[Max aantal], [Max kosten], [Min aantal], [Min kosten], ' \
                  f'[Max totale capaciteit], [Min totale capaciteit], [Min Activiteit Jaar], [Max Activiteit Jaar]) ' \
                  f"VALUES ('{storage_id}', '{self.year}', '{self.scenario}', 0,0,0,0, " \
                  f"{max_capacity}, {min_capacity}, 0, 0 );"
            self.cursor.execute(sql)
            self.conn.commit()
        else:
            print(f"Option {storage_id}/{storage_option['name']} is already present in [CatJaarScen(categorie,jaar,scenario)] with scenario {self.scenario}")

    def _update_storage_related_tables(self, row: pd.Series):
        pass

    def _update_option_related_tables(self):
        # add column to self.df with Optie number (Nr)
        self.df['Nr'] = 0
        for index, row in self.df.iterrows():
            if row['category'] == 'Storage':
                #self._update_storage_related_tables(row)
                continue  # already handled in _add_storage()
            #else:
            #    continue  # skip storage in this method, handled in _update_storage_related_tables()
            new_opt = row['name']
            print("Updating related tables for option:", new_opt)
            ref_option_name = row.opera_equivalent
            sql = "SELECT * FROM [Opties] WHERE [Naam optie] = '{}'".format(new_opt)
            df_optie = psql.read_sql(sql, self.engine)
            new_optie_nr = int(df_optie.Nr)
            row['Nr'] = new_optie_nr

            ## Add option to Beschikbare varianten table
            sql = "SELECT * FROM [Beschikbare varianten] WHERE [Nr] = {}".format(new_optie_nr)
            df = psql.read_sql(sql, self.engine)

            if ref_option_name is not None and not pd.isna(ref_option_name):
                sql = "SELECT * FROM [Opties] WHERE [Naam optie] = '{}'".format(ref_option_name)
                df_ref_option = psql.read_sql(sql, self.engine)
            else:
                df_ref_option = None

            if df.shape[0] == 0:  # Case where new option is NOT in table 'Beschikbare varianten'

                if df_ref_option is not None:
                    # copy data from the reference [Beschikbare varianten] and use that to insert new option
                    sql = "SELECT * FROM [Beschikbare varianten] WHERE [Nr] = {}".format(int(df_ref_option.Nr))
                    df3 = psql.read_sql(sql, self.engine)
                    df3.Nr = df_optie.Nr
                    col = [[i] for i in df3.columns]

                    q = 'INSERT INTO [Beschikbare varianten] ({}) VALUES ({}{})'.format(str(col)[1:-1], '?,' * (
                            len(df3.columns) - 1), '?').replace("'", "")
                    values = list(df3.itertuples(index=False, name=None))
                    print(q, values)
                    self.cursor.executemany(q, values)
                else:
                    print(f"Adding new option {df_optie['Naam optie'].values} to [Beschikbare varianten]")
                    # insert using defaults
                    q = f'INSERT INTO [Beschikbare varianten] ([Nr], [Variant], [Beschikbaar]) VALUES ({new_optie_nr}, 1, 1)'
                    print(q)
                    res = self.cursor.execute(q)
                    print(res)
                self.conn.commit()

            else:
                print(f'Option {df_optie.Nr.values}/{new_opt} is already in [Beschikbare varianten]')
                print(df)

            ## Add option to Kosten table

            sql = "SELECT * FROM [Kosten(Optie,Variant,Jaar)] WHERE [Nr] = {} AND [Jaar] = '{}'".format(new_optie_nr,
                                                                                                        self.year)
            df = psql.read_sql(sql, self.engine)

            investment_cost = row['investment_cost'] if not_empty(row['investment_cost']) else 0.0
            o_m_cost = row['o_m_cost'] if not_empty(row['o_m_cost']) else 0.0
            variable_cost = row['variable_o_m_cost'] if not_empty(row['variable_o_m_cost']) else 0.0
            no_costs_defined = investment_cost == 0.0 and o_m_cost == 0.0 and variable_cost == 0.0

            if df.shape[0] == 0 and not no_costs_defined:  # Case where new option is NOT in table 'Kosten'
                if df_ref_option is not None:
                    sql = "SELECT * FROM [Kosten(Optie,Variant,Jaar)] WHERE [Nr] = {} AND [Jaar] = '{}'".format(
                        int(df_ref_option.Nr),
                        self.year)
                    df3 = psql.read_sql(sql, self.engine)
                    if df3.empty: # if no costs are found for reference option, create new
                        df3 = pd.DataFrame({'Nr': new_optie_nr, 'Variant': 1, 'Jaar': self.year})
                    print(df3)
                    df3.Nr = df_optie.Nr
                    df3['Investeringskosten'] = float(investment_cost)
                    df3['Overig operationeel kosten/baten'] = float(o_m_cost)
                    df3['Variabele kosten'] = float(variable_cost)
                    # Do we need to add more costs (?)
                    col = [[i] for i in df3.columns]

                    sql = 'INSERT INTO [Kosten(Optie,Variant,Jaar)] ({}) VALUES ({}{})'.format(str(col)[1:-1], '?,' * (
                                len(df3.columns) - 1), '?').replace("'", "")
                    values = list(df3.itertuples(index=False, name=None))
                    print(sql)
                    print(values)
                    self.cursor.executemany(sql, values)
                else:
                    # TODO add overige kosten?
                    q = f'INSERT INTO [Kosten(Optie,Variant,Jaar)] ([Nr], [Variant], [Jaar], [Investeringskosten], [Overig operationeel kosten/baten], [Variabele kosten]) ' \
                        f'VALUES ({new_optie_nr}, 1, {self.year}, {float(investment_cost)}, {float(o_m_cost)}, {float(variable_cost)})'
                    self.cursor.execute(q)
                self.conn.commit()
            else:
                if no_costs_defined:
                    print(f"All costs are empty for {df_optie.Nr.values}/{new_opt}, not adding to [Kosten(Optie,Variant,Jaar)]")
                else:
                    print(f'Option {df_optie.Nr.values}/{new_opt} has already costs attached in [Kosten(Optie,Variant,Jaar)]')
                    print(df)

            # Add option to Energiegebruik table, update efficiency in  Effect column (x unit required for 1 unit of output)
            # first input carriers
            esdl_carrier_in = row['carrier_in']
            if esdl_carrier_in is not None and esdl_carrier_in:
                carrier_in = opera_energycarrier(esdl_carrier_in)  # convert to Opera version of this ESDL carrier
                sql = "SELECT * FROM [Energiegebruik(Optie,Energiedrager,Variant,Jaar)] WHERE [Nr] = {} AND [Jaar] = '{}' AND [Energiedrager] = '{}'".format(
                    new_optie_nr, self.year, carrier_in)
                df = psql.read_sql(sql, self.engine)
                if df.shape[0] == 0:  # Case where new option is NOT in table 'Energiegebruik'
                    print(f"Inserting efficiency for option {new_opt} and carrier_in {carrier_in}")
                    sql = f"INSERT INTO [Energiegebruik(Optie,Energiedrager,Variant,Jaar)] ([Nr],[Energiedrager],[Variant],[Jaar],[Effect]) VALUES " \
                          f"({new_optie_nr}, '{carrier_in}', {1}, {self.year}, '{1}');"  # Effect for consumption is always 1
                    print(sql)
                    self.cursor.execute(sql)
                else:
                    print(
                        f'Option {df_optie.Nr.values}/{new_opt} is already present in [Energiegebruik(Optie,Energiedrager,Variant,Jaar)]')

            carrier_out = row['carrier_out']
            if carrier_out is not None and carrier_out:
                carrier_out = opera_energycarrier(carrier_out)  # convert to opera equivalent of this ESDL carrier
                sql = "SELECT * FROM [Energiegebruik(Optie,Energiedrager,Variant,Jaar)] WHERE [Nr] = {} AND [Jaar] = '{}' AND [Energiedrager] = '{}'".format(
                    new_optie_nr, self.year, carrier_out)
                df = psql.read_sql(sql, self.engine)
                if df.shape[0] == 0:  # Case where new option is NOT in table 'Energiegebruik'
                    print(f"Inserting efficiency for option {new_opt} and carrier_out {carrier_out}")
                    # Effect is a 'Short Text' column. insert as string and use . as decimal separator instead of ,
                    effect = -row['efficiency'] if row['efficiency'] != 0.0 or not pd.isna(row['efficiency']) else -1
                    sql = f"INSERT INTO [Energiegebruik(Optie,Energiedrager,Variant,Jaar)] ([Nr],[Energiedrager],[Variant],[Jaar],[Effect]) VALUES " \
                          f"({new_optie_nr}, '{carrier_out}', {1}, {self.year}, '{str(effect)}');"
                    self.cursor.execute(sql)
                else:
                    print(
                        f'Option {df_optie.Nr.values}/{new_opt} is already present in [Energiegebruik(Optie,Energiedrager,Variant,Jaar)]')

            ## Add option to CatJaarScen table
            sql = "SELECT * FROM [CatJaarScen(categorie,jaar,scenario)] WHERE [Categorie] = '{}' AND [Jaar] = '{}' AND [Scenario] = '{}'".format(
                new_optie_nr, self.year, self.scenario)
            df = psql.read_sql(sql, self.engine)
            if df.shape[0] == 0:  # Case where new option is NOT in table 'CatJaarScen'
                df3 = pd.DataFrame()
                if df_ref_option is not None:
                    sql = "SELECT * FROM [CatJaarScen(categorie,jaar,scenario)] WHERE [Categorie] = '{}' AND [Jaar] = '{}' AND [Scenario] = '{}'".format(
                        int(df_ref_option.Nr), self.year, self.scenario)
                    df3 = psql.read_sql(sql, self.engine)
                if not df3.empty:  # can use reference option
                    print(f"Adding new CatJaarScen for optie {new_optie_nr}/{new_opt}, based on reference option {ref_option_name}")
                    df3.Categorie = new_optie_nr
                    df3['Max totale capaciteit'] = row['power_max'] if not pd.isna(row['power_max']) else None
                    df3['Min totale capaciteit'] = row['power_min'] if not pd.isna(row['power_min']) else 0
                    df3['Max Activiteit Jaar'] = 0
                    df3['Min Activiteit Jaar'] = 0
                    df3['ActiviteitMinimaalGelijkBaseline'] = False  # Fix to get Opera  working


                    col = [[i] for i in df3.columns]
                    sql = 'INSERT INTO [CatJaarScen(categorie,jaar,scenario)] ({}) VALUES ({}{})'.format(str(col)[1:-1], '?,' * (len(df3.columns) - 1), '?').replace("'", "")
                    #print(sql)
                    #print(df3)
                    #print(list(df3.itertuples(index=False, name=None)))
                    self.cursor.executemany(
                        sql,
                        list(df3.itertuples(index=False, name=None)))
                else:
                    print(f"Adding new CatJaarScen for optie {new_optie_nr}/{new_opt}")
                    max_capacity = row['power_max'] if not pd.isna(row['power_max']) else 0 #None
                    min_capacity = row['power_min'] if not pd.isna(row['power_min']) else 0
                    # currently not filling in columns [Max aantal], [Max kosten], [Min aantal], [Min kosten],
                    sql = f'INSERT INTO [CatJaarScen(categorie,jaar,scenario)] ([Categorie], [Jaar], [Scenario], ' \
                          f'[Max aantal], [Max kosten], [Min aantal], [Min kosten], ' \
                          f'[Max totale capaciteit], [Min totale capaciteit], [Min Activiteit Jaar], [Max Activiteit Jaar]) ' \
                          f"VALUES ('{new_optie_nr}', '{self.year}', '{self.scenario}', 0, 0, 0, 0, {max_capacity}, {min_capacity}, {0}, {0});"
                    #print(sql)
                    self.cursor.execute(sql)

                self.conn.commit()

            else:
                print(
                    f'Option {df_optie.Nr.values}/{new_opt} is already present in [CatJaarScen(categorie,jaar,scenario)] with scenario {self.scenario}')
                print(df)

            if row['category'] == 'Consumer':
                activiteiten_name = activity_name(row['name'])
                # TODO: OptieActiviteit(Optie,Activiteit) : connect option to activiteit.
                sql = "SELECT * FROM [OptieActiviteit(Optie,Activiteit)] WHERE [Optie] = {} AND [Activiteit] = '{}'" \
                    .format(new_optie_nr, activiteiten_name)
                df = psql.read_sql(sql, self.engine)
                if df.shape[0] == 0:  # Case where new activity is NOT in table 'ActiviteitBaseline'
                    print(f'Adding {activiteiten_name} to [OptieActiviteit]')
                    sql = f"INSERT INTO [OptieActiviteit(Optie,Activiteit)] ([Optie],[Activiteit], [Match]) VALUES " \
                          f"({new_optie_nr}, '{activiteiten_name}', {True})"
                    self.cursor.execute(sql)
                else:
                    print(f"{activiteiten_name} already in [OptieActiviteit]")

            ### A similar procedure can be done to include activities (demands)
            # following slide "Database (5)" in the file "D:\MMVIB\MMvIB\Working with OPERA_20220907.pptx"
            # It is crucial that the table 'OptieActiviteit' connect (match) the number of the included Options and an Activiteit (demand) in OPERA

        self.conn.commit()

    def _add_demand(self):
        """        
        add electricity and NG demand to the final demand of the households sector, under the assumption
        that the households sector is only responsible for the demand of these two carriers.
        """
        
        """First, for Natural Gas"""
        #query to fetch the demand value for Natural Gas from the EnergiebalansBaseline table
        query = """
                SELECT *FROM [EnergiebalansBaseline] WHERE [Baseline] = 'MMVIB' AND 
                [Sector] = 'Huishoudens' AND [Energiedrager] = 'Aardgas'
                """ 
        
        df = self.fetch_query(query)

        # Kindly ensure that there is only one matching value for the demand of Natural Gas in 'df_kpi'
        kpi_values = self.df_kpi.loc[self.df_kpi['carrier'] == 'Aardgas', 'demand']
        if kpi_values.empty:
            log.error("No matching demand values found for Aardgas")
            return
        elif len(kpi_values) > 1:
            log.error("Multiple matching demand values found for Aardgas")
            return
        
        kpi_value = kpi_values.iloc[0]

        if not df.empty:
            demand_value = df.iloc[0]['Finale vraag']
            new_value = demand_value + kpi_value
            # new_value = demand_value + 10     # for testing purposes
            log.info(f"Updating demand value for Aardgas: {demand_value} -> {new_value}")
            
            # Update the Natural Gas demand value in the EnergiebalansBaseline table
            update_query = """
                            UPDATE [EnergiebalansBaseline] 
                            SET [Finale vraag] = ? 
                            WHERE
                            [Baseline] = ? AND [Sector] = ? AND 
                            [Energiedrager] = ?
                            """
            self.cursor.execute(update_query, (new_value, 'MMVIB', 'Huishoudens', 'Aardgas'))
            log.info("Natural Gas demand updated successfully")
        self.conn.commit()

        
        """Then, for Electricity"""
        
        query = """
                SELECT *FROM [EnergiebalansBaseline] WHERE [Baseline] = 'MMVIB' AND 
                [Sector] = 'Huishoudens' AND [Energiedrager] = 'Elektriciteit'
                """
        df = self.fetch_query(query)
        log.info("Fetched Electricity demand successfully")

        # Kindly ensure that there is only one matching value for the demand of Electricity in 'df_kpi'
        kpi_values = self.df_kpi.loc[self.df_kpi['carrier'] == 'Electricity', 'demand']
        if kpi_values.empty:
            log.error("No matching demand values found for Electricity")
            return
        elif len(kpi_values) > 1:
            log.error("Multiple matching demand values found for Electricity")
            return
        
        kpi_value = kpi_values.iloc[0]

        if not df.empty:
            demand_value = df.iloc[0]['Finale vraag']
            new_value = demand_value + kpi_value
            # new_value = demand_value + 10     # for testing purposes
            log.info(f"Updating demand value for electricity: {demand_value} -> {new_value}")
            update_query = """
                        UPDATE [EnergiebalansBaseline] SET [Finale vraag] = ? 
                        WHERE 
                        [Baseline] = ? AND [Sector] = ? 
                        AND [Energiedrager] = ?
                        """
            self.cursor.execute(update_query, (new_value, 'MMVIB', 'Huishoudens', 'Elektriciteit'))
            log.info("Electricity demand updated successfully")
        self.conn.commit()
        
        # log.info(f"query: {query} \n df: {df} \n df_kpi: {self.df_kpi} \n row: {row}")

    def _add_electricity_import_price(self):
        """
        Add electricity import price to the OPERA MS access database.
        """

        # Fetch the Hourly_prices_EnergyCarriers table from the database
        query = """
                SELECT * FROM [Hourly_prices_EnergyCarriers]
                """
        df_hourly_prices = self.fetch_query(query)
        
        # Ensure the 'uuren' column is of type int64
        df_hourly_prices['uuren'] = df_hourly_prices['uuren'].astype('int64')   
        
        # Merge the DataFrame with the electricity prices with the Hourly_prices_EnergyCarriers table
        df_merged = df_hourly_prices.merge(self.df_electricity, left_on='uuren', right_on='hour', how='left')

        # Update the [Prijzen Uur] column with the 'price' column from df_electricity
        df_hourly_prices['Prijzen Uur'] = df_merged['price']

        # Update the Hourly_prices_EnergyCarriers table with the new prices
        update_query = """
                        UPDATE [Hourly_prices_EnergyCarriers] 
                        SET [Prijzen Uur] = ?
                        WHERE [uuren] = ?
                        """
        
        for _, row in df_hourly_prices.iterrows():
            self.cursor.execute(update_query, (row['Prijzen Uur'], row['uuren']))

        self.conn.commit()
