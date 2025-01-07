from dataclasses import dataclass
from typing import Tuple, Union, Optional, List
from datetime import timedelta

from esdl.esdl_handler import EnergySystemHandler
from .unit import convert_to_unit, POWER_IN_GW, ENERGY_IN_PJ, COST_IN_MEur, POWER_IN_W, COST_IN_Eur_per_MWh, \
    ENERGY_IN_J, UnitException, COST_IN_MEur_per_GW, COST_IN_MEur_per_GW_per_year, COST_IN_MEur_per_PJ, \
    COST_IN_Eur_per_GJ
import esdl
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# current asset types that are not supported by this parser or Opera import
IGNORED_ASSETS_TUPLE = (esdl.Transport, esdl.Export)


class OperaESDLParser:
    def __init__(self):
        self.esh = EnergySystemHandler()

    def get_energy_system_Handler(self) -> EnergySystemHandler:
        return self.esh

    def parse(self, esdl_string: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Extracts Cost, ranges of production and values of demand
        :param esdl_string:
        :return: Tuple of 2 dataframes: assets and carriers
        """
        print(f"Power unit : {POWER_IN_GW.description}")
        print(f"Energy unit: {ENERGY_IN_PJ.description}")
        print(f"CAPEX Cost unit: {COST_IN_MEur_per_GW.description}")
        print(f"OPEX Cost unit: {COST_IN_MEur_per_GW_per_year.description}")
        print(f"Variable OPEX Cost unit: {COST_IN_MEur_per_PJ.description}")
        print(f"Marginal Cost unit: {COST_IN_Eur_per_MWh.description}")

        self.esh.load_from_string(esdl_string)
        energy_assets = self.esh.get_all_instances_of_type(esdl.EnergyAsset)
        df = pd.DataFrame({'category': pd.Series(dtype='str'),
                           'id': pd.Series(dtype='str'),
                           'esdlType': pd.Series(dtype='str'),
                           'name': pd.Series(dtype='str'),
                           'power_min': pd.Series(dtype='float'),
                           'power_max': pd.Series(dtype='float'),
                           'power': pd.Series(dtype='float'),
                           'efficiency': pd.Series(dtype='float'),
                           'investment_cost': pd.Series(dtype='float'),
                           'o_m_cost': pd.Series(dtype='float'),
                           'variable_o_m_cost': pd.Series(dtype='float'),
                           'marginal_cost': pd.Series(dtype='float'),
                           'carrier_in': pd.Series(dtype='str'),
                           'carrier_out': pd.Series(dtype='str'),
                           'profiles_in': pd.Series(dtype='str'),
                           'profiles_out': pd.Series(dtype='str'),
                           'storage_capacity': pd.Series(dtype='float'),
                           'storage_charge_efficiency': pd.Series(dtype='float'),
                           'storage_discharge_efficiency': pd.Series(dtype='float'),
                           'storage_slow_loadtime': pd.Series(dtype='float'),
                           'storage_fast_loadtime': pd.Series(dtype='float'),
                           'storage_slow_unloadtime': pd.Series(dtype='float'),
                           'storage_fast_unloadtime': pd.Series(dtype='float'),
                           'storage_losses_perhour': pd.Series(dtype='str'),
                           'opera_equivalent': pd.Series(dtype='str')
                           })
        for asset in energy_assets:
            max_power = None
            try:
                if not isinstance(asset, IGNORED_ASSETS_TUPLE) and asset.state != esdl.AssetStateEnum.DISABLED:
                    asset: esdl.EnergyAsset = asset
                    print(f'Converting {asset.name}:')
                    category = esdl_category(asset)

                    power_range, unit = extract_range(asset, 'power')
                    if power_range:
                        print("\t- Power range: ", power_range)
                        power_range = tuple([convert_to_unit(v, unit, POWER_IN_GW) for v in power_range])
                    if hasattr(asset, 'power'):
                        max_power = convert_to_unit(asset.power, POWER_IN_W, POWER_IN_GW) if asset.power else None
                    # if not power_range and max_power:
                    #     # use max power as range
                    #     power_range = (max_power, max_power)

                    capacity_range, unit = extract_range(asset, 'capacity')
                    if capacity_range:
                        print("\t- Capacity range: ", capacity_range)
                        # a bit of a hack to use power range instead of capacity range (with diferent Unit)
                        power_range = tuple([convert_to_unit(v, unit, ENERGY_IN_PJ) for v in capacity_range])

                    efficiency = extract_efficiency(asset)
                    costs = extract_costs(asset)
                    carrier_in_list, carrier_out_list = extract_carriers(asset)
                    carrier_in = ", ".join(carrier_in_list)
                    carrier_out = ", ".join(carrier_out_list)
                    singlevalue_profiles_in, singlevalue_profiles_out = extract_port_singlevalue_profiles(asset, ENERGY_IN_PJ)
                    profiles_in = ", ".join([str(p) for p in singlevalue_profiles_in])
                    profiles_out = ", ".join([str(p) for p in singlevalue_profiles_out])
                    #print(f"profiles: {singlevalue_profiles_in} and out {singlevalue_profiles_out}")
                    sa = StorageAttributes()
                    if isinstance(asset, esdl.Storage):
                        sa = extract_storage_attributes(asset)
                    opera_equivalent = find_opera_equivalent(asset)
                    print(f'\t- {asset.eClass.name}, {asset.name}, power_range={power_range}, power={max_power}, costs={costs}' )
                    s = [category, asset.id, asset.eClass.name, asset.name,
                         power_range[0] if power_range else None, power_range[1] if power_range else None,
                         max_power, efficiency, costs[0], costs[1], costs[2], costs[3],
                         carrier_in, carrier_out, profiles_in, profiles_out,
                         sa.capacity, sa.chargeEfficiency, sa.disChargeEfficiency, sa.slowLoadTime, sa.fastLoadTime,
                         sa.slowUnloadTime, sa.fastUnloadTime, sa.lossesPerHour,
                         opera_equivalent]
                    df.loc[len(df)] = s
            except UnitException as ue:
                print(f"Error parsing input: asset {asset.name} not configured correctly: {ue}")
                raise ue

        #print(df)
        df.to_csv('output.csv')

        # carrier prices
        df_carriers = pd.DataFrame({'name': pd.Series(dtype='str'),
                                    'id': pd.Series(dtype='str'),
                                    'cost': pd.Series(dtype='float'),
                                    'unit': pd.Series(dtype='str'),
                                    })
        carrier_list: List[esdl.Carrier] = self.esh.get_all_instances_of_type(esdl.Carrier)
        for carrier in carrier_list:
            if carrier.cost:
                price = extract_singlevalue(carrier.cost)
                if carrier.cost.profileQuantityAndUnit:
                    qau = carrier.cost.profileQuantityAndUnit
                    target_unit = COST_IN_Eur_per_GJ
                    if isinstance(carrier, esdl.ElectricityCommodity):
                        target_unit = COST_IN_Eur_per_MWh
                    price = convert_to_unit(price, qau, target_unit)
            carrier_df = pd.DataFrame([{'name': carrier.name, 'id': carrier.id, 'cost': price, 'unit': target_unit.description}])
            #df_carriers = df_carriers.append({'name': carrier.name, 'id': carrier.id, 'cost': price, 'unit': target_unit.description}, ignore_index=True)
            df_carriers = pd.concat([df_carriers, carrier_df], ignore_index=True)
            print(f'Carrier {carrier.name} has cost {price} {target_unit.description}')

        print(df_carriers)
        return df, df_carriers

    def parse_2(self, esdl_string) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Extracts kpis information and hourly electricity prices
        """
        self.esh.load_from_string(esdl_string)
        df_kpis = pd.DataFrame({'name': pd.Series(dtype='str'),
                            'id': pd.Series(dtype='str'),
                            'demand': pd.Series(dtype='float'),
                            'unit': pd.Series(dtype='str'),
                            'carrier': pd.Series(dtype='str'),
                            })
        kpi_list: List[esdl.DoubleKPI] = self.esh.get_all_instances_of_type(esdl.DoubleKPI)
        
        kpi_data = []

        for kpi in kpi_list:
            if kpi.quantityAndUnit and kpi.quantityAndUnit.description is not None and kpi.quantityAndUnit.description != "Warmte":
                    qau = kpi.quantityAndUnit
                    demand = kpi.value
                    target_unit = ENERGY_IN_PJ
                    demand = convert_to_unit(demand, qau, target_unit)
                    kpi_data.append({'name': kpi.name, 'id': kpi.id, 'demand': demand, 'unit': target_unit.description,
                                    'carrier': kpi.quantityAndUnit.description})
                   
                    # print(f'KPI {kpi.name} has cost {demand} {target_unit.description}')
        df_kpis = pd.concat([df_kpis, pd.DataFrame(kpi_data)], ignore_index=True)
        print(df_kpis)
        
        # Extract Electricity hourly prices
        df_electricity = pd.DataFrame({'date': pd.Series(dtype='str'),
                                       'time': pd.Series(dtype='str'),
                                       'hour': pd.Series(dtype='int'),
                                       'price': pd.Series(dtype='float'),
                                       'unit': pd.Series(dtype='str'),
                                       })
        electricity_prices: List[esdl.TimeSeriesProfile] = self.esh.get_all_instances_of_type(esdl.TimeSeriesProfile)
        
        electricity_import_price = []
        
        for electricity_price in electricity_prices:
            date_time = electricity_price.startDateTime
            print(date_time)
            date = date_time.date()
            time = date_time.time()
            print(f"Date: {date}, Time: {time}")

            hour = 0
            for time_series in electricity_price.values:
                date_time += timedelta(hours=1)
                date = date_time.date()
                time = date_time.time()
                hour += 1
                price = time_series
                # date = time_series.start
                # time = time_series.duration
                # price = time_series.value
                if electricity_price.profileQuantityAndUnit is not None:
                    qau = electricity_price.profileQuantityAndUnit
                    target_unit = COST_IN_Eur_per_GJ
                    # price = convert_to_unit(price, qau, target_unit) # commented out as the conversion does not seem
                    # to be working properly
                    price = price / 3.6 # conversion from €/MWh to €/GJ
                    unit = target_unit.description
                electricity_import_price.append({'date': date, 'time': time, 'hour': hour,'price': price, 'unit': unit})

        df_electricity = pd.concat([df_electricity, pd.DataFrame(electricity_import_price)], ignore_index=True)
        print(df_electricity)
        # print(df_kpis)
        return df_kpis, df_electricity


class ParseException(Exception):
    pass


def extract_range(asset: esdl.EnergyAsset, attribute_name: str) -> Tuple[
    Tuple[float, float] | None, esdl.QuantityAndUnitType | None]:
    """
    Returns the Range constraint of this energy asset as a tuple, plus the unit of the range, e.g. (0,20), PowerInGW
    Returns None, None if nothing is found
    :param attribute_name: the name of the attribute, e.g. 'power' or 'capacity'
    :param asset:
    :return:
    """
    constraints = asset.constraint
    for c in constraints:
        if isinstance(c, esdl.RangedConstraint):
            rc: esdl.RangedConstraint = c
            if rc.attributeReference.lower() == attribute_name.lower():
                constraint_range: esdl.Range = rc.range
                if constraint_range.profileQuantityAndUnit is None:
                    print(f"No unit specified for constraint of asset {asset.name}, assuming WATT")
                    constraint_range.profileQuantityAndUnit = POWER_IN_W
                return (constraint_range.minValue, constraint_range.maxValue), constraint_range.profileQuantityAndUnit
            #else:
            #    raise ParseException(f'Can\'t find an Ranged constrained for asset {asset.name} with attribute name {attribute_name}')
    return None, None # make sure unpacking works


@dataclass(init=False)
class StorageAttributes:
    capacity: float = None # in PJ
    fastLoadTime: float = None  # in hours
    slowLoadTime: float = None  # in hours
    fastUnloadTime: float = None
    slowUnloadTime: float = None
    chargeEfficiency: float = None  # factor
    disChargeEfficiency: float = None  # factor
    lossesPerHour: float = None

def extract_storage_attributes(asset: esdl.Storage) -> StorageAttributes:
    sa = StorageAttributes()
    sa.capacity = convert_to_unit(asset.capacity, ENERGY_IN_J, ENERGY_IN_PJ)
    # fast load Time in hour = (maxChargeRate (W) = (J/s * 3600) = 1 J
    # 22PJ / 8800TW =
    # next four Unit = hours
    sa.fastLoadTime = asset.capacity / (asset.maxChargeRate * 3600) if asset.maxChargeRate != 0.0 else None
    sa.slowLoadTime = asset.capacity / (asset.maxChargeRate * 3600) if asset.maxChargeRate != 0.0 else None
    sa.fastUnloadTime = asset.capacity / (asset.maxDischargeRate * 3600) if asset.maxDischargeRate != 0.0 else None
    sa.slowUnloadTime = asset.capacity / (asset.maxDischargeRate * 3600) if asset.maxDischargeRate != 0.0 else None
    sa.chargeEfficiency = asset.chargeEfficiency  # for charger Effect
    sa.disChargeEfficiency = asset.dischargeEfficiency  # for discharger Effect
    # self distchargeRate (J/s * 3600) = J/h
    # Verlies per uur is in PJ/uur?
    sa.lossesPerHour = convert_to_unit(asset.selfDischargeRate * 3600, ENERGY_IN_J, ENERGY_IN_PJ)  # for storage

    return sa


def extract_singlevalue(profile: esdl.GenericProfile) -> Optional[float]:
    """
    Returns the value of a SingleValue profile or 0 if not found.
    :param profile:
    :return:
    """
    if profile is not None and isinstance(profile, esdl.SingleValue):
        single_value: esdl.SingleValue = profile
        # check for units here!
        # single_value.profileQuantityAndUnit
        return single_value.value
    print(f"Cannot convert profile {profile.name} of {profile.eContainer()} to a SingleValue")
    return None


def extract_efficiency(asset: esdl.EnergyAsset) -> float:
    # todo: Storage has charge & discharge efficiencies
    # Conversion: AbstractBasicConversion has efficiency
    # HeatPump has COP...
    if hasattr(asset, 'efficiency'):
        efficiency = asset.efficiency
        return efficiency
    else:
        return 1.0


def extract_costs(asset: esdl.EnergyAsset):
    o_m_cost_normalized = None
    investment_costs_normalized = None
    marginal_cost_normalized = None
    variable_om_costs_normalized = None
    costinfo: esdl.CostInformation = asset.costInformation
    if costinfo:
        investment_costs_profile: esdl.GenericProfile = costinfo.investmentCosts
        if investment_costs_profile:
            investment_costs = extract_singlevalue(investment_costs_profile)
            investment_costs_normalized = convert_to_unit(investment_costs, investment_costs_profile.profileQuantityAndUnit, COST_IN_MEur_per_GW)
        o_m_costs_profile:esdl.GenericProfile = costinfo.fixedOperationalAndMaintenanceCosts
        if o_m_costs_profile:
            o_m_costs = extract_singlevalue(o_m_costs_profile)
            o_m_cost_normalized = convert_to_unit(o_m_costs, o_m_costs_profile.profileQuantityAndUnit, COST_IN_MEur_per_GW_per_year)
        variable_om_costs_profile = costinfo.variableOperationalAndMaintenanceCosts
        if variable_om_costs_profile:
            variable_om_costs = extract_singlevalue(variable_om_costs_profile)
            variable_om_costs_normalized = convert_to_unit(variable_om_costs, variable_om_costs_profile.profileQuantityAndUnit, COST_IN_MEur_per_PJ)
        marginal_cost_profile: esdl.GenericProfile = costinfo.marginalCosts
        if marginal_cost_profile:
            marginal_cost = extract_singlevalue(marginal_cost_profile)
            marginal_cost_normalized = convert_to_unit(marginal_cost, marginal_cost_profile.profileQuantityAndUnit, COST_IN_Eur_per_MWh)
    return investment_costs_normalized, o_m_cost_normalized, variable_om_costs_normalized, marginal_cost_normalized


def extract_carriers(asset: esdl.EnergyAsset) -> Tuple[List[str], List[str]]:
    ports = asset.port
    carrier_in_list = []
    carrier_out_list = []
    for p in ports:
        p: esdl.Port = p
        if p.carrier:
            if isinstance(p, esdl.InPort):
                carrier_in_list.append(p.carrier.name)
            else:
                carrier_out_list.append(p.carrier.name)

    return carrier_in_list, carrier_out_list


def extract_port_singlevalue_profiles(asset: esdl.EnergyAsset, target_unit:esdl.QuantityAndUnitType) -> Tuple[List[str], List[str]]:
    ports = asset.port
    singlevalue_in_list = []
    singlevalue_out_list = []
    for p in ports:
        p: esdl.Port = p
        if p.profile and len(p.profile) > 0:
            profile: esdl.GenericProfile = p.profile[0]  # TODO: only uses first profile!
            if isinstance(profile, esdl.SingleValue):
                if isinstance(p, esdl.InPort):
                    singlevalue_in_list.append(convert_to_unit(extract_singlevalue(profile), profile.profileQuantityAndUnit, target_unit))
                else:
                    singlevalue_out_list.append(convert_to_unit(extract_singlevalue(profile), profile.profileQuantityAndUnit, target_unit))
            else:
                print(f"Unsupported profile type for Opera parser {profile.eClass.name}: {profile}, ignoring")
            if len(p.profile) > 1:
                print(f"Multiple profiles per port are currently not supported")

    return singlevalue_in_list, singlevalue_out_list

# TODO extract KPIs' information
def extract_kpi(asset: esdl.DoubleKPI) -> Tuple[List[str], List[str], List[float]]: # we extract the values related to name, description, and value
    kpi_values = asset.kpi
    for kpi_value in kpi_values:
        pass



def find_opera_equivalent(asset: esdl.EnergyAsset) -> str | None:
    if isinstance(asset, esdl.Electrolyzer):
        return "H2 Large-scale electrolyser"
    elif isinstance(asset, esdl.MobilityDemand):
        # todo check for carrier
        md: esdl.MobilityDemand = asset
        if md.fuelType and md.fuelType == esdl.MobilityFuelTypeEnum.HYDROGEN:
            if esdl.VehicleTypeEnum.CAR in md.type:
                return " H2 auto"  # mind the space
            elif esdl.VehicleTypeEnum.VAN in md.type:
                return "H2 van"  # mind the space
            elif esdl.VehicleTypeEnum.TRUCK in md.type:
                return "H2 truck with energy consumption reduction"
        else:
            return "REF Finale vraag verkeer th"  # not sure if this is ok, as it is Final demand...
    elif isinstance(asset, esdl.GasConversion):
        gconv: esdl.GasConversion = asset
        if gconv.type == esdl.GasConversionTypeEnum.SMR:
            return "H2 uit SMR met CCS plus"
        elif gconv.type == esdl.GasConversionTypeEnum.ATR:
            print(f"Cannot map {asset.name} of type ATR to an Opera equivalent")
            return None
        else:
            return "H2 uit SMR met CCS plus"
    elif isinstance(asset, esdl.WindTurbine) or isinstance(asset, esdl.WindPark):
        # WindPark is a subtype of WindTurbine
        windturbine: esdl.WindTurbine = asset
        if windturbine.type == esdl.WindTurbineTypeEnum.WIND_ON_LAND:
            return "Wind op Land band 1"
        elif windturbine.type == esdl.WindTurbineTypeEnum.WIND_AT_SEA:
            return "Wind op Zee band 1"
        else:
            print(f"Unmapped type {windturbine.type} for {asset.name}, mapping to Wind op Zee for Opera equivalent")
            return "Wind op Zee band 1"
    elif isinstance(asset, esdl.PVPanel): # superclass of PVPark and PVInstallation
        # todo handle sector information here to map to right sector PV production
        panel: esdl.PVPanel = asset
        return "Solar-PV Residential" # or "Solar -PV industry" # mind the space!
    elif isinstance(asset, esdl.Import):
        carrier: str = None
        for port in asset.port:
            if isinstance(port, esdl.OutPort):
                carrier = port.carrier.name if port.carrier else None
        if carrier:
            if carrier.lower().startswith("elec"):
                # electricity import
                return "REF E import Flexnet"
            elif carrier.lower().startswith("h2") or carrier.lower().startswith("waterstof") or  carrier.lower().startswith("hydrogen"):
                return "Import H2 to H2 domestic"
            elif carrier.lower().startswith("aardgas") or carrier.lower().startswith("natural gas"):
                return "REF Gaswinning en -import"
            else:
                return None
    elif isinstance(asset, esdl.Export):
        # TODO: adapt to carriers as with import
        return "H2 domestic to export"
    elif isinstance(asset, esdl.PowerPlant):
        asset: esdl.PowerPlant
        if asset.fuel == esdl.PowerPlantFuelEnum.URANIUM:
            #return "Nuclear energy Gen IV - Electricity production"
            return "REF Kernenergie  IBO 7500u 2017"
        else:
            print(f"Cannot map {asset.name} to an Opera equivalent")
            return None
    else:
        print(f"Cannot map {asset.name} to an Opera equivalent")
        return None


'''
$ SELECT DISTINCT(Energiedrager) FROM [Opties]

                 Energiedrager
0                         None
1                      Aardgas
2                      Benzine
3              Biobrandstoffen
4           Biobrandstoffen FT
5                  Bio-ethanol
6                       biogas
7   Biomassa (hout binnenland)
8   Biomassa (hout buitenland)
9                       Diesel
10               Elektriciteit
11                Heat100to200
12                    Methanol
13                      Warmte
14                   Waterstof


                        DoelProduct
0                              None
1                           Aardgas
2                 Aardgas feedstock
3                           Benzine
4                   Biobrandstoffen
5                            biogas
6                            BioHFO
7                       Biokerosine
8              Bio-LNG for shipping
9                   Biomassa (hout)
10     Brandstofmix personenvervoer
11                           Diesel
12                    Elektriciteit
13                     Heat100to200
14                     Heat200to400
15                  HeatDir200to400
16                        HeatHT400
17                              HFO
18                              HVC
19                         Methanol
20                           Naphta
21            Plastic Pyrolysis oil
22  Synthetic methanol for shipping
23                           warmte
24                        Waterstof

'''
def map_esdl_carrier_to_opera_equivalent(carrier: str):
    if carrier:
        carrier = carrier.lower().strip()
        if carrier == "electriciteit" or carrier == "electricity":
            return "Elektriciteit"
        elif carrier == "waterstof" or carrier == 'hydrogen' or carrier == 'h2':
            return "Waterstof"
        elif carrier == "aardgas" or carrier == "natural gas" or carrier == "gas":
            return "Aardgas"
        elif carrier == 'warmte' or carrier == "heat":
            return "Warmte"
        elif carrier == 'biomassa' or carrier == 'biomass':
            return "Biomassa (hout binnenland)"
        elif carrier == 'biogas':
            return "biogas"
        else:
            print(f"Don't know how to map carrier {carrier} to an Opera equivalent")
            return carrier

def esdl_category(asset: esdl.EnergyAsset):
    """
    :param asset: esdl EnergyAsset
    :return: Producer, Consumer, Storage, Transport, Conversion
    """
    super_types = [eclass.name for eclass in asset.eClass.eAllSuperTypes()]
    return super_types[super_types.index(esdl.EnergyAsset.eClass.name) - 1]



