from typing import Dict, Optional

import sys
sys.path.append("..\opera-model-adapter")

from tno.aimms_adapter.model.opera_esdl_parser.esdl_parser import OperaESDLParser
from tno.shared.log import get_logger

logger = get_logger(__name__)

path = "D:\\test\\ESSIM\\Adapter-ESSIM\\bedrijventerreinommoord\\Scenario_1_II3050_Nationale_Sturing\\Trial_1\\MM_workflow_run_1\\ESSIM_adapter\\HHP_KPIs.esdl"

input_esdl: str

logger.info(f"Loading ESDL from local disk at {path}")
# local file
with open(path, 'r') as file:
    input_esdl = file.read()

print('Input ESDL:', input_esdl)

parser = OperaESDLParser()
print("bla....")
try:
    esdl_in_dataframe, carriers = parser.parse(esdl_string=input_esdl)
    logger(f"esdl_in_dataframe looks like this: \n", {esdl_in_dataframe})
    logger(f"carriers are the following: \n", {carriers})
except Exception as e:
    logger.error(f"Parse exception for ESDL input: {e}")
