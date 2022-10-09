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


def copy_file(source_data_dir , local_data_dir):
    list_of_files = os.listdir(source_data_dir)
    N = len(list_of_files)
    for file in tqdm(list_of_files , total=N , desc= "copy files from {source_data_dir} To {local_data_dir}" , colour="red"):
        src = os.path.join(source_data_dir , file)
        dest = os.path.join(local_data_dir , file)
        shutil.copy(src , dest)


def get_data(config_path):
    config = read_yaml(config_path)
    source_data_dirs = config["source_data_dirs"]
    local_data_dirs = config["local_data_dirs"]

    for source_data_dir , local_data_dir in tqdm(zip(source_data_dirs , local_data_dirs) , total=2 , desc= "list of folders" , colour="green"):
        create_directory([local_data_dir])
        copy_file(source_data_dir , local_data_dir)

   



if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config" , "-c" , default= "config/config.yaml")

    parsed_args = args.parse_args()
    try:
        logging.info("stage one is started")
        get_data(config_path=parsed_args.config)
        logging.info("stage one completed and data are stored in local")
    except Exception as e:
        logging.exception(e)
