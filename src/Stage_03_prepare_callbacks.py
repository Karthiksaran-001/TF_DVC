from ast import arg
from src.utils.all_utils import read_yaml   , create_directory
import argparse
import pandas as pd
import os
from tqdm import tqdm
import shutil ## Help to copy files
import logging

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a",
)

def get_callbacks(config_path , params_path):
   config = read_yaml(config_path)
   params = read_yaml(params_path)
   


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config" , "-c" , default= "config/config.yaml")
    args.add_argument("--params" , "-p" , default= "params.yaml")



    parsed_args = args.parse_args()
    try:
        logging.info("stage Three is started")
        get_callbacks(config_path=parsed_args.config , params_path =parsed_args.params)
        logging.info("stage three completed and callbacks are saved as  binary")
    except Exception as e:
        logging.exception(e)
