<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" version="18" description="MMvIB macro use case version 3.3" id="3beab53e-f956-45ac-9fd0-05ba03fb3b84" name="MMvIB Macro use case 3.4" esdlVersion="v2102">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="1b789820-f90f-459f-87b2-59fc4a385d58">
    <dataSources xsi:type="esdl:DataSources" id="144a4661-4496-4904-b00a-fa2a9ffb66d5">
      <dataSource xsi:type="esdl:DataSource" description="dfsdf_asda" id="91ce2a4f-0b8e-4114-b163-ef35ef9365a0" name="NewDataSource"/>
    </dataSources>
    <carriers xsi:type="esdl:Carriers" id="44d8eb44-4d6a-4f33-855a-cbf3ef9283e4">
      <carrier xsi:type="esdl:GasCommodity" id="3cc3baa0-f1bd-44ba-bf75-2263a2432207" name="Natural Gas">
        <cost xsi:type="esdl:SingleValue" value="40.0" id="396aa714-2852-49e4-b367-1b2d7a767a1b">
          <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="bbf3c069-e51a-4b5d-b8e4-7393052e48d9" perUnit="JOULE" description="Cost in EUR/J" unit="EURO" physicalQuantity="COST"/>
        </cost>
      </carrier>
      <carrier xsi:type="esdl:GasCommodity" id="b2418fd5-d4f8-451f-ae4e-6171b1e71103" name="Hydrogen">
        <cost xsi:type="esdl:SingleValue" value="5.0" id="8ddad72b-ce13-4253-9bed-931e6de9c500">
          <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="58ad229c-4dd5-4ea9-bc72-1c67f28772d0" perUnit="JOULE" description="Cost in EUR/J" unit="EURO" physicalQuantity="COST"/>
        </cost>
      </carrier>
      <carrier xsi:type="esdl:ElectricityCommodity" id="67d4305b-4a8c-4163-be55-087bb77a3663" name="Electricity">
        <cost xsi:type="esdl:SingleValue" value="50.0" id="69f7e706-d147-450a-af8e-95d3bc7ccd1f">
          <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="30d481bf-2f98-462f-a171-50d54c3028c7" perUnit="WATTHOUR" description="Cost in EUR/MWh" perMultiplier="MEGA" unit="EURO" physicalQuantity="COST"/>
        </cost>
      </carrier>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="1cb40fb5-7c19-43b0-b88d-406aaaf2fbd3">
    <date xsi:type="esdl:InstanceDate" date="2050-01-01T00:00:00.000000"/>
    <area xsi:type="esdl:Area" id="nl2019" name="Nederland">
      <asset xsi:type="esdl:GasNetwork" name="GasNetwork_3447" id="34470ca7-9895-4118-9232-3fbf2f790c7a">
        <geometry xsi:type="esdl:Point" lat="52.09000176954296" lon="5.063838958740235"/>
        <port xsi:type="esdl:InPort" id="635530e4-fd2a-421d-919e-b4dbb1492297" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="7e6d62b5-a72a-4b3c-b298-c9b7cef7cda0 32b20da2-37cb-4b2d-aa63-43c17b2328d4" name="In"/>
        <port xsi:type="esdl:OutPort" id="a377b420-d1fc-4ae2-ab0d-888ff069faad" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="f40d4744-986c-4277-a17e-5189a1e4c030 8cfc5e6d-90c6-488b-8980-1aabf70ebb4f cc1a6805-75e8-4197-b0e4-1911cccfd71b db34035e-cf1b-4eee-8b9a-a5cd978d0c88" name="Out"/>
      </asset>
      <asset xsi:type="esdl:MobilityDemand" name="MobilityDemand_7a45" efficiency="1.35454" type="CAR" id="7a45670d-5aba-405a-94e6-47ce6c141435" fuelType="HYDROGEN" aggregated="true" technicalLifetime="13.0" originalIdInSource="transport_car_using_hydrogen">
        <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset/blob/master/nodes_source_analyses/energy/transport/transport_car_using_hydrogen.converter.xlsx"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="52.08894703028796" lon="5.060577392578126"/>
        <port xsi:type="esdl:InPort" id="646708fc-a862-4526-b0fd-4a45eea18c38" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="ab3a0854-1a7b-4a8a-a244-8ba413561f31" name="In"/>
      </asset>
      <asset xsi:type="esdl:MobilityDemand" name="MobilityDemand_c7a5" efficiency="1.34274" type="TRUCK" id="c7a59334-5290-41dc-98b4-95a842344741" fuelType="HYDROGEN" aggregated="true" technicalLifetime="12.0" originalIdInSource="transport_truck_using_hydrogen">
        <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset/blob/master/nodes_source_analyses/energy/transport/transport_truck_using_hydrogen.converter.xlsx"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="52.091900237373906" lon="5.060706138610841"/>
        <port xsi:type="esdl:InPort" id="db34035e-cf1b-4eee-8b9a-a5cd978d0c88" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="0797fe1d-bd98-4fec-a7c2-e48fd5a89690" name="In"/>
      </asset>
      <asset xsi:type="esdl:Battery" chargeEfficiency="0.9" name="Battery" id="casfd934-5290-41dc-98b4-95a842344741" technicalLifetime="12.0" capacity="12300000.0" fillLevel="0.5">
        <geometry xsi:type="esdl:Point" lat="52.09241439184352" lon="5.064139366149903"/>
        <port xsi:type="esdl:InPort" id="db34035e-cf1b-4eee-8b9a-a5cd978d0c88" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="a377b420-d1fc-4ae2-ab0d-888ff069faad" name="In"/>
      </asset>
      <asset xsi:type="esdl:MobilityDemand" name="MobilityDemand_ac31" efficiency="0.03104" type="VAN" id="ac31f9cb-9168-4b42-b620-e5d90e6c738d" fuelType="HYDROGEN" aggregated="true" technicalLifetime="12.0" originalIdInSource="transport_van_using_hydrogen">
        <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset/blob/master/nodes_source_analyses/energy/transport/transport_van_using_hydrogen.converter.xlsx"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="52.091952971438346" lon="5.066542625427247"/>
        <port xsi:type="esdl:InPort" id="aa9ffbfb-dd77-46cf-b253-7f2217495cf4" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="c7cf9c47-c265-41b8-911c-b867bffbb1ef" name="In"/>
      </asset>
      <asset xsi:type="esdl:Electrolyzer" name="Electrolyzer_b243" id="b243c807-ce6a-4625-8d24-7c2b57ac1ce3" power="10000000.0" efficiency="0.66" technicalLifetime="25.0" originalIdInSource="energy_hydrogen_flexibility_p2g_electricity">
        <costInformation xsi:type="esdl:CostInformation">
          <investmentCosts xsi:type="esdl:SingleValue" name="Initial investment (excl CCS)" interpolationMethod="NONE" value="10000000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR" unit="EURO" physicalQuantity="COST"/>
          </investmentCosts>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" name="Fixed operation and maintenance costs (per year)" interpolationMethod="NONE" value="126000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perTimeUnit="YEAR" description="EUR / year" unit="EURO" physicalQuantity="COST"/>
          </fixedOperationalAndMaintenanceCosts>
          <marginalCosts xsi:type="esdl:SingleValue" value="23.58" id="06f22f1d-a0df-4cb5-bc78-dbf6b207bc00">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" id="137354af-6812-4d74-aa0a-4a1ebb53f205" perUnit="WATTHOUR" description="Cost in EUR/MWh" perMultiplier="MEGA" unit="EURO"/>
          </marginalCosts>
        </costInformation>
        <constraint xsi:type="esdl:RangedConstraint" attributeReference="power" id="9fa772e4-bbe6-4dc5-9273-b740ba19766a" name="NewRangedConstraint">
          <range xsi:type="esdl:Range" name="NewRange" id="2c97beb4-155d-47d2-a390-74d4712da7a9" maxValue="19000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" multiplier="MEGA" id="06a28a85-15fb-4555-91db-b1a9ffac84a3" description="Power" unit="WATT" physicalQuantity="POWER"/>
          </range>
        </constraint>
        <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset-public/blob/master/nodes_source_analyses/energy/energy/energy_hydrogen_flexibility_p2g_electricity.converter.xlsx"/>
        <geometry xsi:type="esdl:Point" lat="52.08849875855484" lon="5.064654350280763"/>
        <port xsi:type="esdl:InPort" id="0700e32c-5105-4596-b15e-7b8d37269a2f" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" connectedTo="09e86001-e21f-4733-b815-9d44b1ec6d1a 6bdbdc20-1bc9-4f3f-8106-7b0fa3283e8a" name="In"/>
        <port xsi:type="esdl:OutPort" id="d530c592-ce26-478b-b736-a55104b2ac61" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="5959232b-a2fa-4139-95ec-ecee0f720475" name="Out"/>
      </asset>
      <asset xsi:type="esdl:GasConversion" name="GasConversion_bb6f" id="bb6f51a0-812f-4d9e-b23f-5259c54181d4" power="369.0" efficiency="0.81" technicalLifetime="25.0" type="SMR" originalIdInSource="energy_hydrogen_steam_methane_reformer">
        <costInformation xsi:type="esdl:CostInformation">
          <investmentCosts xsi:type="esdl:SingleValue" name="Initial investment (excl CCS)" interpolationMethod="NONE" value="222000000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR" unit="EURO" physicalQuantity="COST"/>
          </investmentCosts>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" name="Fixed operation and maintenance costs (per year)" interpolationMethod="NONE" value="9000000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perTimeUnit="YEAR" description="EUR / year" unit="EURO" physicalQuantity="COST"/>
          </fixedOperationalAndMaintenanceCosts>
          <marginalCosts xsi:type="esdl:SingleValue" value="66.2" id="306f1033-d4ed-4d69-9e5d-499fd8580639">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" id="e8be0c9e-7e91-4794-94eb-5398d1ca6374" perUnit="WATTHOUR" description="Cost in EUR/MWh" perMultiplier="MEGA" unit="EURO"/>
          </marginalCosts>
        </costInformation>
        <constraint xsi:type="esdl:RangedConstraint" attributeReference="power" id="8722dfeb-eff4-4439-99b1-60a0c9c036a1" name="NewRangedConstraint">
          <range xsi:type="esdl:Range" name="NewRange" id="f4d62923-23ec-4291-afe2-2b137dca7b82" maxValue="11716.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" multiplier="MEGA" unit="WATT" physicalQuantity="POWER" id="f62593ee-8c2a-4cc3-910f-b8215d98b106"/>
          </range>
        </constraint>
        <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset-public/blob/master/nodes_source_analyses/energy/energy/energy_hydrogen_steam_methane_reformer.xlsx"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="52.08952713996354" lon="5.069932937622071"/>
        <port xsi:type="esdl:InPort" id="a1342064-9cec-4b8f-9a6b-5813cb834871" carrier="3cc3baa0-f1bd-44ba-bf75-2263a2432207" connectedTo="fffb6031-e803-4bc2-a93e-5d1c0c13a8d4" name="In"/>
        <port xsi:type="esdl:OutPort" id="ede122aa-ae9b-46e2-a96b-ba685059171a" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="3b8a3d44-8b8d-4468-949f-ec70dbdddd13" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Import" power="5000.0" fullLoadHours="2000" name="Import_a3ac" id="a3ac6459-54f5-4345-95bd-3384d1a976e1">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="52.089975401365436" lon="5.0737953186035165"/>
        <port xsi:type="esdl:OutPort" id="1d054f21-810e-4456-8a5e-6abeff51aff3" carrier="3cc3baa0-f1bd-44ba-bf75-2263a2432207" connectedTo="a8af95f5-79e3-472f-8947-9c8f39dc8f06" name="Out"/>
      </asset>
      <asset xsi:type="esdl:WindTurbine" power="3000000.0" surfaceArea="200000" fullLoadHours="3000" name="WindTurbine_6411" id="64119197-a2d1-49d9-971a-08b978b99448" technicalLifetime="25.0" originalIdInSource="energy_power_wind_turbine_inland or energy_power_wind_turbine_coastal">
        <costInformation xsi:type="esdl:CostInformation">
          <investmentCosts xsi:type="esdl:SingleValue" name="Initial investment (excl CCS)" interpolationMethod="NONE" value="4175962.5">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR" unit="EURO" physicalQuantity="COST"/>
          </investmentCosts>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" name="Fixed operation and maintenance costs (per year)" interpolationMethod="NONE" value="147579.9">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perTimeUnit="YEAR" description="EUR / year" unit="EURO" physicalQuantity="COST"/>
          </fixedOperationalAndMaintenanceCosts>
          <marginalCosts xsi:type="esdl:SingleValue" id="f36f6a1e-b9a2-472c-80f1-57f4db27d891">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" id="ae21edee-07d1-4df1-86c5-8a4233d30404" perUnit="WATTHOUR" description="Cost in EUR/MWh" perMultiplier="MEGA" unit="EURO"/>
          </marginalCosts>
        </costInformation>
        <constraint xsi:type="esdl:RangedConstraint" attributeReference="power" id="d0e08b2b-390a-4489-accd-fe639e424676" name="NewRangedConstraint">
          <range xsi:type="esdl:Range" name="NewRange" id="8bdf07f1-f43f-42c0-a4bc-e7ff73915312" maxValue="20000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" multiplier="MEGA" unit="WATT" id="b02625ac-c951-491a-87eb-c09b816493aa"/>
          </range>
        </constraint>
        <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset-public/blob/master/nodes_source_analyses/energy/energy/energy_power_wind_turbine_inland.central_producer.xlsx"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="52.08615185068389" lon="5.067787170410157"/>
        <port xsi:type="esdl:OutPort" id="9b34bc49-f9f0-4335-9ac0-3b6ac2cc8575" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" connectedTo="f408706e-33ae-40dc-9baf-7de5dce19282" name="Out"/>
      </asset>
      <asset xsi:type="esdl:PVPark" power="11332800.0" surfaceArea="113328" name="PVPark_37e4" id="37e43704-0b9e-49a3-97da-99f25c50ff7e" technicalLifetime="25.0" panelEfficiency="0.17" originalIdInSource="energy_power_solar_pv_solar_radiation">
        <costInformation xsi:type="esdl:CostInformation">
          <investmentCosts xsi:type="esdl:SingleValue" value="17420000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" description="EUR" unit="EURO" physicalQuantity="COST"/>
          </investmentCosts>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="318000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perTimeUnit="YEAR" description="EUR / year" unit="EURO" physicalQuantity="COST"/>
          </fixedOperationalAndMaintenanceCosts>
          <marginalCosts xsi:type="esdl:SingleValue" id="f93bd4b0-ac0e-43b0-aa32-f05749fa04e2">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" id="fd953877-77e1-4e88-b5f9-ddef5d0d11e8" perUnit="WATTHOUR" description="Cost in EUR/MWh" perMultiplier="MEGA" unit="EURO"/>
          </marginalCosts>
        </costInformation>
        <constraint xsi:type="esdl:RangedConstraint" attributeReference="power" name="NewRangedConstraint" id="ea241389-19bf-41ac-bf7f-cc676a02a251" description="Power range based on 2 scenario's">
          <range xsi:type="esdl:Range" name="NewRange" id="58ea2161-1ca1-4b16-a5a1-c458ea63deae" maxValue="66918.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" multiplier="MEGA" unit="WATT" physicalQuantity="POWER" id="af9b6a59-1862-436b-ba43-b70143891e7b"/>
          </range>
        </constraint>
        <dataSource xsi:type="esdl:DataSource" name="ETM" reference="https://github.com/quintel/etdataset-public/blob/master/nodes_source_analyses/energy/energy/energy_chp_local_engine_biogas.xlsx"/>
        <geometry xsi:type="esdl:Polygon" CRS="WGS84">
          <exterior xsi:type="esdl:SubPolygon">
            <point xsi:type="esdl:Point" lat="52.08692706351441" lon="5.059525966644288"/>
            <point xsi:type="esdl:Point" lat="52.087494398998096" lon="5.0632596015930185"/>
            <point xsi:type="esdl:Point" lat="52.0835228991396" lon="5.0630879402160645"/>
            <point xsi:type="esdl:Point" lat="52.08418264120317" lon="5.05798101425171"/>
          </exterior>
        </geometry>
        <port xsi:type="esdl:OutPort" id="40f4bd95-b5f4-41fe-bc8e-1e8fe92b982e" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" connectedTo="4bd2386b-71c0-4528-b901-468fe57ade32" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_d5ec" id="d5ec770e-f602-4a53-b94e-c36965328141" length="284.9">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.09000176954296" lon="5.063838958740235"/>
          <point xsi:type="esdl:Point" lat="52.091952971438346" lon="5.066542625427247"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="f40d4744-986c-4277-a17e-5189a1e4c030" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="a377b420-d1fc-4ae2-ab0d-888ff069faad" name="In"/>
        <port xsi:type="esdl:OutPort" id="c7cf9c47-c265-41b8-911c-b867bffbb1ef" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="aa9ffbfb-dd77-46cf-b253-7f2217495cf4" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_6385" id="63856b13-fe23-43d8-9bc4-964b16bd1157" length="300.6">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.09000176954296" lon="5.063838958740235"/>
          <point xsi:type="esdl:Point" lat="52.091900237373906" lon="5.060706138610841"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="8cfc5e6d-90c6-488b-8980-1aabf70ebb4f" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="a377b420-d1fc-4ae2-ab0d-888ff069faad" name="In"/>
        <port xsi:type="esdl:OutPort" id="0797fe1d-bd98-4fec-a7c2-e48fd5a89690" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="db34035e-cf1b-4eee-8b9a-a5cd978d0c88" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_a827" id="a8276ff2-7d30-4c55-89c1-0aced8e9d665" length="251.8">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.09000176954296" lon="5.063838958740235"/>
          <point xsi:type="esdl:Point" lat="52.08894703028796" lon="5.060577392578126"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="cc1a6805-75e8-4197-b0e4-1911cccfd71b" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="a377b420-d1fc-4ae2-ab0d-888ff069faad" name="In"/>
        <port xsi:type="esdl:OutPort" id="ab3a0854-1a7b-4a8a-a244-8ba413561f31" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="646708fc-a862-4526-b0fd-4a45eea18c38" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_6a5b" id="6a5b3b24-6a8c-4439-a8d2-fcf89f23a94c" length="176.2">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08849875855484" lon="5.064654350280763"/>
          <point xsi:type="esdl:Point" lat="52.09000176954296" lon="5.063838958740235"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="5959232b-a2fa-4139-95ec-ecee0f720475" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="d530c592-ce26-478b-b736-a55104b2ac61" name="In"/>
        <port xsi:type="esdl:OutPort" id="7e6d62b5-a72a-4b3c-b298-c9b7cef7cda0" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="635530e4-fd2a-421d-919e-b4dbb1492297" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_5493" id="5493e0de-e01e-472d-86a3-78f4f4521c83" length="268.5">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.089975401365436" lon="5.0737953186035165"/>
          <point xsi:type="esdl:Point" lat="52.08952713996354" lon="5.069932937622071"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="a8af95f5-79e3-472f-8947-9c8f39dc8f06" carrier="3cc3baa0-f1bd-44ba-bf75-2263a2432207" connectedTo="1d054f21-810e-4456-8a5e-6abeff51aff3" name="In"/>
        <port xsi:type="esdl:OutPort" id="fffb6031-e803-4bc2-a93e-5d1c0c13a8d4" carrier="3cc3baa0-f1bd-44ba-bf75-2263a2432207" connectedTo="a1342064-9cec-4b8f-9a6b-5813cb834871" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_a04d" id="a04de3de-dc1b-4445-b2a2-0ec14dc82504" length="419.7">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08952713996354" lon="5.069932937622071"/>
          <point xsi:type="esdl:Point" lat="52.09000176954296" lon="5.063838958740235"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="3b8a3d44-8b8d-4468-949f-ec70dbdddd13" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="ede122aa-ae9b-46e2-a96b-ba685059171a" name="In"/>
        <port xsi:type="esdl:OutPort" id="32b20da2-37cb-4b2d-aa63-43c17b2328d4" carrier="b2418fd5-d4f8-451f-ae4e-6171b1e71103" connectedTo="635530e4-fd2a-421d-919e-b4dbb1492297" name="Out"/>
      </asset>
      <asset xsi:type="esdl:ElectricityCable" name="ElectricityCable_db12" id="db123570-87af-4faf-84f2-67ed97eaf1e2" length="420.6">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08542385533057" lon="5.0610690837579435"/>
          <point xsi:type="esdl:Point" lat="52.08849875855484" lon="5.064654350280763"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="4bd2386b-71c0-4528-b901-468fe57ade32" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" connectedTo="40f4bd95-b5f4-41fe-bc8e-1e8fe92b982e" name="In"/>
        <port xsi:type="esdl:OutPort" id="09e86001-e21f-4733-b815-9d44b1ec6d1a" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" connectedTo="0700e32c-5105-4596-b15e-7b8d37269a2f" name="Out"/>
      </asset>
      <asset xsi:type="esdl:ElectricityCable" name="ElectricityCable_8a30" id="8a303406-2b79-4835-ba41-917510362149" length="337.5">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08615185068389" lon="5.067787170410157"/>
          <point xsi:type="esdl:Point" lat="52.08849875855484" lon="5.064654350280763"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="f408706e-33ae-40dc-9baf-7de5dce19282" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" connectedTo="9b34bc49-f9f0-4335-9ac0-3b6ac2cc8575" name="In"/>
        <port xsi:type="esdl:OutPort" id="6bdbdc20-1bc9-4f3f-8106-7b0fa3283e8a" carrier="67d4305b-4a8c-4163-be55-087bb77a3663" connectedTo="0700e32c-5105-4596-b15e-7b8d37269a2f" name="Out"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
