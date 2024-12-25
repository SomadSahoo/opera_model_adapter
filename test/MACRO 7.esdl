<?xml version='1.0' encoding='UTF-8'?>
  <esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" description="Solar panel" esdlVersion="v2102" id="3beab53e-f956-45ac-9fd0-05ba03fb3b84" name="Solar panel" version="17">
    <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="1b789820-f90f-459f-87b2-59fc4a385d58">
      <carriers xsi:type="esdl:Carriers" id="44d8eb44-4d6a-4f33-855a-cbf3ef9283e4">
        <carrier xsi:type="esdl:GasCommodity" id="3cc3baa0-f1bd-44ba-bf75-2263a2432207" name="Natural Gas">
          <cost xsi:type="esdl:SingleValue" id="396aa714-2852-49e4-b367-1b2d7a767a1b" value="40.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" id="bbf3c069-e51a-4b5d-b8e4-7393052e48d9" description="Cost in EUR/J" perUnit="JOULE" unit="EURO"/>
          </cost>
        </carrier>
        <carrier xsi:type="esdl:GasCommodity" id="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Hydrogen">
          <cost xsi:type="esdl:SingleValue" id="8ddad72b-ce13-4253-9bed-931e6de9c500" value="5.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" id="58ad229c-4dd5-4ea9-bc72-1c67f28772d0" description="Cost in EUR/J" perUnit="JOULE" unit="EURO"/>
          </cost>
        </carrier>
        <carrier xsi:type="esdl:ElectricityCommodity" id="67d4305b-4a8c-4163-be55-087bb77a3663" name="Electricity">
          <cost xsi:type="esdl:SingleValue" id="69f7e706-d147-450a-af8e-95d3bc7ccd1f" value="46.24885079184887">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" description="eur/MWh" perMultiplier="MEGA" perUnit="WATTHOUR" unit="EURO"/>
          </cost>
        </carrier>
      </carriers>
      <dataSources xsi:type="esdl:DataSources" id="144a4661-4496-4904-b00a-fa2a9ffb66d5">
        <dataSource xsi:type="esdl:DataSource" description="dfsdf_asda" id="91ce2a4f-0b8e-4114-b163-ef35ef9365a0" name="NewDataSource"/>
      </dataSources>
    </energySystemInformation>
    <instance xsi:type="esdl:Instance" id="1cb40fb5-7c19-43b0-b88d-406aaaf2fbd3">
      <date xsi:type="esdl:InstanceDate" date="2050-01-01T00:00:00.000000"/>
      <area xsi:type="esdl:Area" id="nl2019" name="Nederland">
        <asset xsi:type="esdl:GasNetwork" id="34470ca7-9895-4118-9232-3fbf2f790c7a" name="GasNetwork_3447">
          <geometry xsi:type="esdl:Point" lon="5.063838958740235" lat="52.09000176954296"/>
          <port xsi:type="esdl:InPort" id="635530e4-fd2a-421d-919e-b4dbb1492297" connectedTo="7e6d62b5-a72a-4b3c-b298-c9b7cef7cda0 32b20da2-37cb-4b2d-aa63-43c17b2328d4" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="In"/>
          <port xsi:type="esdl:OutPort" id="a377b420-d1fc-4ae2-ab0d-888ff069faad" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Out" connectedTo="f40d4744-986c-4277-a17e-5189a1e4c030 8cfc5e6d-90c6-488b-8980-1aabf70ebb4f cc1a6805-75e8-4197-b0e4-1911cccfd71b"/>
        </asset>
        <asset xsi:type="esdl:MobilityDemand" aggregated="true" fuelType="HYDROGEN" originalIdInSource="transport_car_using_hydrogen" name="MobilityDemand_7a45" type="CAR" id="7a45670d-5aba-405a-94e6-47ce6c141435" technicalLifetime="13.0" efficiency="1.35454" power="162737037.48245242">
          <geometry xsi:type="esdl:Point" lat="52.08894703028796" CRS="WGS84" lon="5.060577392578126"/>
          <port xsi:type="esdl:InPort" id="646708fc-a862-4526-b0fd-4a45eea18c38" connectedTo="ab3a0854-1a7b-4a8a-a244-8ba413561f31" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="In">
            <profile xsi:type="esdl:SingleValue" value="5132075214046532.0" name="Yearly demand">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" unit="JOULE"/>
            </profile>
          </port>
          <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset/blob/master/nodes_source_analyses/energy/transport/transport_car_using_hydrogen.converter.xlsx"/>
        </asset>
        <asset xsi:type="esdl:MobilityDemand" aggregated="true" fuelType="HYDROGEN" originalIdInSource="transport_truck_using_hydrogen" name="MobilityDemand_c7a5" type="TRUCK" id="c7a59334-5290-41dc-98b4-95a842344741" technicalLifetime="12.0" efficiency="1.34274" power="1346560876.7453334">
          <geometry xsi:type="esdl:Point" lat="52.091900237373906" CRS="WGS84" lon="5.060706138610841"/>
          <port xsi:type="esdl:InPort" id="db34035e-cf1b-4eee-8b9a-a5cd978d0c88" connectedTo="0797fe1d-bd98-4fec-a7c2-e48fd5a89690" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="In">
            <profile xsi:type="esdl:SingleValue" value="4.2465143809040104e+16" name="Yearly demand">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" unit="JOULE"/>
            </profile>
          </port>
          <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset/blob/master/nodes_source_analyses/energy/transport/transport_truck_using_hydrogen.converter.xlsx"/>
        </asset>
        <asset xsi:type="esdl:MobilityDemand" aggregated="true" fuelType="HYDROGEN" originalIdInSource="transport_van_using_hydrogen" name="MobilityDemand_ac31" type="VAN" id="ac31f9cb-9168-4b42-b620-e5d90e6c738d" technicalLifetime="12.0" efficiency="0.03104" power="547974648.266366">
          <geometry xsi:type="esdl:Point" lat="52.091952971438346" CRS="WGS84" lon="5.066542625427247"/>
          <port xsi:type="esdl:InPort" id="aa9ffbfb-dd77-46cf-b253-7f2217495cf4" connectedTo="c7cf9c47-c265-41b8-911c-b867bffbb1ef" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="In">
            <profile xsi:type="esdl:SingleValue" value="1.728092850772782e+16" name="Yearly demand">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" unit="JOULE"/>
            </profile>
          </port>
          <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset/blob/master/nodes_source_analyses/energy/transport/transport_van_using_hydrogen.converter.xlsx"/>
        </asset>
        <asset xsi:type="esdl:Electrolyzer" originalIdInSource="energy_hydrogen_flexibility_p2g_electricity" power="10000000.0" efficiency="0.66" id="b243c807-ce6a-4625-8d24-7c2b57ac1ce3" technicalLifetime="25.0" fullLoadHours="2989" name="Electrolyzer_b243">
          <constraint xsi:type="esdl:RangedConstraint" name="NewRangedConstraint" attributeReference="power" id="9fa772e4-bbe6-4dc5-9273-b740ba19766a">
            <range xsi:type="esdl:Range" minValue="42000000000.0" id="2c97beb4-155d-47d2-a390-74d4712da7a9" name="NewRange" maxValue="51000000000.0">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" id="06a28a85-15fb-4555-91db-b1a9ffac84a3" description="Power" multiplier="MEGA" unit="WATT"/>
            </range>
          </constraint>
          <geometry xsi:type="esdl:Point" lon="5.064654350280763" lat="52.08849875855484"/>
          <costInformation xsi:type="esdl:CostInformation">
            <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="126000.0" name="Fixed operation and maintenance costs (per year)" interpolationMethod="NONE">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR / year" unit="EURO" physicalQuantity="COST" perTimeUnit="YEAR"/>
            </fixedOperationalAndMaintenanceCosts>
            <investmentCosts xsi:type="esdl:SingleValue" value="10000000.0" name="Initial investment (excl CCS)" interpolationMethod="NONE">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR" physicalQuantity="COST" unit="EURO"/>
            </investmentCosts>
            <marginalCosts xsi:type="esdl:SingleValue" id="06f22f1d-a0df-4cb5-bc78-dbf6b207bc00" value="23.58">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" id="137354af-6812-4d74-aa0a-4a1ebb53f205" description="Cost in EUR/MWh" perMultiplier="MEGA" perUnit="WATTHOUR" unit="EURO"/>
            </marginalCosts>
          </costInformation>
          <port xsi:type="esdl:InPort" id="0700e32c-5105-4596-b15e-7b8d37269a2f" connectedTo="09e86001-e21f-4733-b815-9d44b1ec6d1a 6bdbdc20-1bc9-4f3f-8106-7b0fa3283e8a" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" name="In"/>
          <port xsi:type="esdl:OutPort" id="d530c592-ce26-478b-b736-a55104b2ac61" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Out" connectedTo="5959232b-a2fa-4139-95ec-ecee0f720475">
            <profile xsi:type="esdl:InfluxDBProfile" database="energy_profiles" host="http://influxdb" profileType="POWER_IN_MW" field="E3B" id="d883ec8a-dc1a-47bf-b9ab-8bee87dfdcf5" port="8086" name="energy_hydrogen_flexibility_p2g_electricity" measurement="standard_profiles_point"/>
          </port>
          <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset-public/blob/master/nodes_source_analyses/energy/energy/energy_hydrogen_flexibility_p2g_electricity.converter.xlsx"/>
        </asset>
        <asset xsi:type="esdl:GasConversion" originalIdInSource="energy_hydrogen_steam_methane_reformer" power="369.0" id="bb6f51a0-812f-4d9e-b23f-5259c54181d4" technicalLifetime="25.0" type="SMR" efficiency="81.0" name="GasConversion_bb6f">
          <constraint xsi:type="esdl:RangedConstraint" name="NewRangedConstraint" attributeReference="power" id="8722dfeb-eff4-4439-99b1-60a0c9c036a1">
            <range xsi:type="esdl:Range" id="f4d62923-23ec-4291-afe2-2b137dca7b82" name="NewRange" maxValue="11716.0">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" multiplier="MEGA" id="f62593ee-8c2a-4cc3-910f-b8215d98b106" physicalQuantity="POWER" unit="WATT"/>
            </range>
          </constraint>
          <geometry xsi:type="esdl:Point" lat="52.08952713996354" CRS="WGS84" lon="5.069932937622071"/>
          <costInformation xsi:type="esdl:CostInformation">
            <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="9000000.0" name="Fixed operation and maintenance costs (per year)" interpolationMethod="NONE">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR / year" unit="EURO" physicalQuantity="COST" perTimeUnit="YEAR"/>
            </fixedOperationalAndMaintenanceCosts>
            <investmentCosts xsi:type="esdl:SingleValue" value="222000000.0" name="Initial investment (excl CCS)" interpolationMethod="NONE">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR" physicalQuantity="COST" unit="EURO"/>
            </investmentCosts>
            <marginalCosts xsi:type="esdl:SingleValue" id="306f1033-d4ed-4d69-9e5d-499fd8580639" value="66.2">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" id="e8be0c9e-7e91-4794-94eb-5398d1ca6374" description="Cost in EUR/MWh" perMultiplier="MEGA" perUnit="WATTHOUR" unit="EURO"/>
            </marginalCosts>
          </costInformation>
          <port xsi:type="esdl:InPort" id="a1342064-9cec-4b8f-9a6b-5813cb834871" connectedTo="fffb6031-e803-4bc2-a93e-5d1c0c13a8d4" carrier="3cc3baa0-f1bd-44ba-bf75-2263a2432207" name="In"/>
          <port xsi:type="esdl:OutPort" id="ede122aa-ae9b-46e2-a96b-ba685059171a" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Out" connectedTo="3b8a3d44-8b8d-4468-949f-ec70dbdddd13"/>
          <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset-public/blob/master/nodes_source_analyses/energy/energy/energy_hydrogen_steam_methane_reformer.xlsx"/>
        </asset>
        <asset xsi:type="esdl:Import" fullLoadHours="2000" id="a3ac6459-54f5-4345-95bd-3384d1a976e1" power="5000.0" name="Import_a3ac">
          <geometry xsi:type="esdl:Point" lat="52.089975401365436" CRS="WGS84" lon="5.0737953186035165"/>
          <port xsi:type="esdl:OutPort" id="1d054f21-810e-4456-8a5e-6abeff51aff3" carrier="3cc3baa0-f1bd-44ba-bf75-2263a2432207" name="Out" connectedTo="a8af95f5-79e3-472f-8947-9c8f39dc8f06"/>
        </asset>
        <asset xsi:type="esdl:WindTurbine" originalIdInSource="energy_power_wind_turbine_inland or energy_power_wind_turbine_coastal" fullLoadHours="3000" id="64119197-a2d1-49d9-971a-08b978b99448" technicalLifetime="25.0" surfaceArea="200000" power="3000000.0" name="WindTurbine_6411">
          <constraint xsi:type="esdl:RangedConstraint" name="NewRangedConstraint" attributeReference="power" id="d0e08b2b-390a-4489-accd-fe639e424676">
            <range xsi:type="esdl:Range" minValue="20000000000.0" id="8bdf07f1-f43f-42c0-a4bc-e7ff73915312" name="NewRange" maxValue="20000000000.0">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" multiplier="MEGA" id="b02625ac-c951-491a-87eb-c09b816493aa" physicalQuantity="POWER" unit="WATT"/>
            </range>
          </constraint>
          <geometry xsi:type="esdl:Point" lat="52.08615185068389" CRS="WGS84" lon="5.067787170410157"/>
          <costInformation xsi:type="esdl:CostInformation">
            <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="147579.9" name="Fixed operation and maintenance costs (per year)" interpolationMethod="NONE">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR / year" unit="EURO" physicalQuantity="COST" perTimeUnit="YEAR"/>
            </fixedOperationalAndMaintenanceCosts>
            <investmentCosts xsi:type="esdl:SingleValue" value="4175962.5" name="Initial investment (excl CCS)" interpolationMethod="NONE">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR" physicalQuantity="COST" unit="EURO"/>
            </investmentCosts>
            <marginalCosts xsi:type="esdl:SingleValue" id="f36f6a1e-b9a2-472c-80f1-57f4db27d891">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" id="ae21edee-07d1-4df1-86c5-8a4233d30404" description="Cost in EUR/MWh" perMultiplier="MEGA" perUnit="WATTHOUR" unit="EURO"/>
            </marginalCosts>
          </costInformation>
          <port xsi:type="esdl:OutPort" id="9b34bc49-f9f0-4335-9ac0-3b6ac2cc8575" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" name="Out" connectedTo="f408706e-33ae-40dc-9baf-7de5dce19282"/>
          <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset-public/blob/master/nodes_source_analyses/energy/energy/energy_power_wind_turbine_inland.central_producer.xlsx"/>
        </asset>
        <asset xsi:type="esdl:PVPark" originalIdInSource="energy_power_solar_pv_solar_radiation" fullLoadHours="867" id="37e43704-0b9e-49a3-97da-99f25c50ff7e" technicalLifetime="25.0" surfaceArea="113328" power="11332800.0" panelEfficiency="0.17" name="PVPark_37e4">
          <constraint xsi:type="esdl:RangedConstraint" attributeReference="power">
            <range xsi:type="esdl:Range" minValue="57600000000.0" maxValue="66918000000.0"/>
          </constraint>
          <geometry xsi:type="esdl:Polygon" CRS="WGS84">
            <exterior xsi:type="esdl:SubPolygon">
              <point xsi:type="esdl:Point" lon="5.059525966644288" lat="52.08692706351441"/>
              <point xsi:type="esdl:Point" lon="5.0632596015930185" lat="52.087494398998096"/>
              <point xsi:type="esdl:Point" lon="5.0630879402160645" lat="52.0835228991396"/>
              <point xsi:type="esdl:Point" lon="5.05798101425171" lat="52.08418264120317"/>
            </exterior>
          </geometry>
          <costInformation xsi:type="esdl:CostInformation">
            <marginalCosts xsi:type="esdl:SingleValue">
              <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" description="Cost in EUR/MWh" perMultiplier="MEGA" perUnit="WATTHOUR" unit="EURO"/>
            </marginalCosts>
          </costInformation>
          <port xsi:type="esdl:OutPort" id="40f4bd95-b5f4-41fe-bc8e-1e8fe92b982e" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" name="Out" connectedTo="4bd2386b-71c0-4528-b901-468fe57ade32"/>
          <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset-public/blob/master/nodes_source_analyses/energy/energy/energy_chp_local_engine_biogas.xlsx"/>
        </asset>
        <asset xsi:type="esdl:Pipe" capacity="100000000.0" length="284.9" id="d5ec770e-f602-4a53-b94e-c36965328141" name="Pipe_d5ec">
          <geometry xsi:type="esdl:Line" CRS="WGS84">
            <point xsi:type="esdl:Point" lon="5.063838958740235" lat="52.09000176954296"/>
            <point xsi:type="esdl:Point" lon="5.066542625427247" lat="52.091952971438346"/>
          </geometry>
          <port xsi:type="esdl:InPort" id="f40d4744-986c-4277-a17e-5189a1e4c030" connectedTo="a377b420-d1fc-4ae2-ab0d-888ff069faad" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="In"/>
          <port xsi:type="esdl:OutPort" id="c7cf9c47-c265-41b8-911c-b867bffbb1ef" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Out" connectedTo="aa9ffbfb-dd77-46cf-b253-7f2217495cf4"/>
        </asset>
        <asset xsi:type="esdl:Pipe" capacity="100000000.0" length="300.6" id="63856b13-fe23-43d8-9bc4-964b16bd1157" name="Pipe_6385">
          <geometry xsi:type="esdl:Line" CRS="WGS84">
            <point xsi:type="esdl:Point" lon="5.063838958740235" lat="52.09000176954296"/>
            <point xsi:type="esdl:Point" lon="5.060706138610841" lat="52.091900237373906"/>
          </geometry>
          <port xsi:type="esdl:InPort" id="8cfc5e6d-90c6-488b-8980-1aabf70ebb4f" connectedTo="a377b420-d1fc-4ae2-ab0d-888ff069faad" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="In"/>
          <port xsi:type="esdl:OutPort" id="0797fe1d-bd98-4fec-a7c2-e48fd5a89690" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Out" connectedTo="db34035e-cf1b-4eee-8b9a-a5cd978d0c88"/>
        </asset>
        <asset xsi:type="esdl:Pipe" capacity="100000000.0" length="251.8" id="a8276ff2-7d30-4c55-89c1-0aced8e9d665" name="Pipe_a827">
          <geometry xsi:type="esdl:Line" CRS="WGS84">
            <point xsi:type="esdl:Point" lon="5.063838958740235" lat="52.09000176954296"/>
            <point xsi:type="esdl:Point" lon="5.060577392578126" lat="52.08894703028796"/>
          </geometry>
          <port xsi:type="esdl:InPort" id="cc1a6805-75e8-4197-b0e4-1911cccfd71b" connectedTo="a377b420-d1fc-4ae2-ab0d-888ff069faad" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="In"/>
          <port xsi:type="esdl:OutPort" id="ab3a0854-1a7b-4a8a-a244-8ba413561f31" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Out" connectedTo="646708fc-a862-4526-b0fd-4a45eea18c38"/>
        </asset>
        <asset xsi:type="esdl:Pipe" capacity="100000000.0" length="176.2" id="6a5b3b24-6a8c-4439-a8d2-fcf89f23a94c" name="Pipe_6a5b">
          <geometry xsi:type="esdl:Line" CRS="WGS84">
            <point xsi:type="esdl:Point" lon="5.064654350280763" lat="52.08849875855484"/>
            <point xsi:type="esdl:Point" lon="5.063838958740235" lat="52.09000176954296"/>
          </geometry>
          <port xsi:type="esdl:InPort" id="5959232b-a2fa-4139-95ec-ecee0f720475" connectedTo="d530c592-ce26-478b-b736-a55104b2ac61" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="In"/>
          <port xsi:type="esdl:OutPort" id="7e6d62b5-a72a-4b3c-b298-c9b7cef7cda0" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Out" connectedTo="635530e4-fd2a-421d-919e-b4dbb1492297"/>
        </asset>
        <asset xsi:type="esdl:Pipe" capacity="100000000.0" length="268.5" id="5493e0de-e01e-472d-86a3-78f4f4521c83" name="Pipe_5493">
          <geometry xsi:type="esdl:Line" CRS="WGS84">
            <point xsi:type="esdl:Point" lon="5.0737953186035165" lat="52.089975401365436"/>
            <point xsi:type="esdl:Point" lon="5.069932937622071" lat="52.08952713996354"/>
          </geometry>
          <port xsi:type="esdl:InPort" id="a8af95f5-79e3-472f-8947-9c8f39dc8f06" connectedTo="1d054f21-810e-4456-8a5e-6abeff51aff3" carrier="3cc3baa0-f1bd-44ba-bf75-2263a2432207" name="In"/>
          <port xsi:type="esdl:OutPort" id="fffb6031-e803-4bc2-a93e-5d1c0c13a8d4" carrier="3cc3baa0-f1bd-44ba-bf75-2263a2432207" name="Out" connectedTo="a1342064-9cec-4b8f-9a6b-5813cb834871"/>
        </asset>
        <asset xsi:type="esdl:Pipe" capacity="100000000.0" length="419.7" id="a04de3de-dc1b-4445-b2a2-0ec14dc82504" name="Pipe_a04d">
          <geometry xsi:type="esdl:Line" CRS="WGS84">
            <point xsi:type="esdl:Point" lon="5.069932937622071" lat="52.08952713996354"/>
            <point xsi:type="esdl:Point" lon="5.063838958740235" lat="52.09000176954296"/>
          </geometry>
          <port xsi:type="esdl:InPort" id="3b8a3d44-8b8d-4468-949f-ec70dbdddd13" connectedTo="ede122aa-ae9b-46e2-a96b-ba685059171a" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="In"/>
          <port xsi:type="esdl:OutPort" id="32b20da2-37cb-4b2d-aa63-43c17b2328d4" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Out" connectedTo="635530e4-fd2a-421d-919e-b4dbb1492297"/>
        </asset>
        <asset xsi:type="esdl:ElectricityCable" length="420.6" id="db123570-87af-4faf-84f2-67ed97eaf1e2" name="ElectricityCable_db12" capacity="100000000.0">
          <geometry xsi:type="esdl:Line" CRS="WGS84">
            <point xsi:type="esdl:Point" lon="5.0610690837579435" lat="52.08542385533057"/>
            <point xsi:type="esdl:Point" lon="5.064654350280763" lat="52.08849875855484"/>
          </geometry>
          <port xsi:type="esdl:InPort" id="4bd2386b-71c0-4528-b901-468fe57ade32" connectedTo="40f4bd95-b5f4-41fe-bc8e-1e8fe92b982e" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" name="In"/>
          <port xsi:type="esdl:OutPort" id="09e86001-e21f-4733-b815-9d44b1ec6d1a" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" name="Out" connectedTo="0700e32c-5105-4596-b15e-7b8d37269a2f"/>
        </asset>
        <asset xsi:type="esdl:ElectricityCable" length="337.5" id="8a303406-2b79-4835-ba41-917510362149" name="ElectricityCable_8a30" capacity="100000000.0">
          <geometry xsi:type="esdl:Line" CRS="WGS84">
            <point xsi:type="esdl:Point" lon="5.067787170410157" lat="52.08615185068389"/>
            <point xsi:type="esdl:Point" lon="5.064654350280763" lat="52.08849875855484"/>
          </geometry>
          <port xsi:type="esdl:InPort" id="f408706e-33ae-40dc-9baf-7de5dce19282" connectedTo="9b34bc49-f9f0-4335-9ac0-3b6ac2cc8575" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" name="In"/>
          <port xsi:type="esdl:OutPort" id="6bdbdc20-1bc9-4f3f-8106-7b0fa3283e8a" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" name="Out" connectedTo="0700e32c-5105-4596-b15e-7b8d37269a2f"/>
        </asset>
      </area>
    </instance>
    </esdl:EnergySystem>