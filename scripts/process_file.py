import sys
from minio import Minio
import os
import tempfile
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/processing.log'),
        logging.StreamHandler()
    ]
)

def sanitize_filename(filename):
    # Obtener solo el nombre del archivo sin la ruta
    base_name = os.path.basename(filename)
    # Reemplazar caracteres problemáticos
    return base_name.replace('/', '_').replace('\\', '_')


def process_file(bucket_name, object_name):
    logger = logging.getLogger(__name__)
    logger.info(f"Starting processing of {bucket_name}/{object_name}")

    minio_client = Minio(
        os.getenv('MINIO_ENDPOINT', 'minio:9000'),
        access_key=os.getenv('MINIO_ACCESS_KEY', 'admin'),
        secret_key=os.getenv('MINIO_SECRET_KEY', 'password'),
        region=os.getenv('MINIO_REGION', 'eu-central-1'),
        secure=False
    )

    try:
        with tempfile.NamedTemporaryFile(suffix='.xlsx') as temp_file:
            start_time = datetime.now()
            logger.info(f"Downloading file {object_name}")

            minio_client.fget_object(bucket_name, object_name, temp_file.name)

            if object_name.endswith('.xlsx'):
                df = pd.read_excel(temp_file.name)
                logger.info(f"Excel file readed. Dimensions: {df.shape}")
                logger.info(f"Columns found: {df.columns.tolist()}")

                safe_filename = sanitize_filename(object_name)

                summary_file = f"/app/logs/summary_{safe_filename}_{start_time.strftime('%Y%m%d_%H%M%S')}.txt"
                with open(summary_file, 'w') as f:
                    f.write(f"Processing Summary:\n")
                    f.write(f"File: {object_name}\n")
                    f.write(f"Date: {start_time}\n")
                    f.write(f"Rows: {df.shape[0]}\n")
                    f.write(f"Columns: {df.shape[1]}\n")
                    f.write(f"Names of columns: {df.columns.tolist()}\n")
                    f.write(f"First 5 rows:\n{df.head().to_string()}\n")

                logger.info(f"Processing completed. Summary saved in {summary_file}")
            else:
                logger.warning(f"File {object_name} it is not an Excel file")

    except Exception as e:
        logger.error(f"Error processing file {object_name}: {e}")
        raise


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("how use: python process_file.py <bucket_name> <object_name>")
        sys.exit(1)

    bucket_name = sys.argv[1]
    object_name = sys.argv[2]
    process_file(bucket_name, object_name)
