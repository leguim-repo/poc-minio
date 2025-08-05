import logging

logging.getLogger("THE_LOGGER")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s:%(module)s:%(lineno)d:%(funcName)s:%(message)s",
    handlers=[
        # logging.FileHandler('/app/logs/processing_fastapi.log'),
        logging.StreamHandler()
    ]
)

THE_LOGGER = logging.getLogger("THE_LOGGER")
