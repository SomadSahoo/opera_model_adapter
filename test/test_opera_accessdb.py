from minio import Minio

import sys
sys.path.append("..\opera-model-adapter")

from tno.aimms_adapter.model.opera_accessdb.opera_access_importer import OperaAccessImporter, copy_clean_access_database
from tno.aimms_adapter.model.opera_esdl_parser.esdl_parser import OperaESDLParser
from tno.shared.log import get_logger

logger = get_logger(__name__)


oai = OperaAccessImporter()
parser = OperaESDLParser()

path="opera-test/MACRO 16.esdl"
logger.info(f"Loading ESDL from Inter Model Storage (Minio) at {path}")

minio_client = Minio(endpoint="localhost:9000", access_key="admin", secret_key="password", secure=False)

bucket = path.split("/")[0]
rest_of_path = "/".join(path.split("/")[1:])
response = minio_client.get_object(bucket,rest_of_path)



input_esdl_bytes = response.data
if input_esdl_bytes is None:
    logger.error(f"Error retrieving {path} from Minio")
else:
    input_esdl = input_esdl_bytes.decode('utf-8')

esdl_in_dataframe, carriers = parser.parse(esdl_string=input_esdl)

copy_clean_access_database("./test/opera/clean_db/Opties_mmvib.mdb", "./test/opera/Opera_20221212/Opties_mmvib.mdb")
logger.info("Importing ESDL into Opera database")

oai.start_import(esdl_data_frame= esdl_in_dataframe, carriers=carriers, access_database="./test/opera/Opera_20221212/Opties_mmvib.mdb")