import logging

def convert_package_name_to_provider(package_name):
    return ".".join(package_name.split('.')[-2:])

logger = logging.getLogger(convert_package_name_to_provider(__package__))
logger.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging_handler.setFormatter(formatter)
logger.addHandler(logging_handler)
