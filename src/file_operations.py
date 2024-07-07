import sys
from pathlib import Path
import logging

def write_file(filepath:Path, data:str)-> None:
    
    logging.basicConfig(filename="5paisa.log",format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    with open(filepath, "w+") as f:
        logger.info(f"started writing token")
        f.write(data)
        f.close()
        logger.info("token written to file")