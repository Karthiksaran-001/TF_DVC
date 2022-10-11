from ast import arg
from src.utils.all_utils import read_yaml   , create_directory , get_VGG16_model
from src.utils.models import get_VGG16_model
import argparse
import pandas as pd
import os
from tqdm import tqdm
import logging



def prepare_base_model(config_path , params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts = config["artifacts"]
    artifacts_dir = artifacts["artifacts_dir"]
    base_model_dir = artifacts["Base_model_dir"]
    Base_model_name = artifacts["Base_model_name"]
    Base_model_dir_path = os.path.join(artifacts_dir , base_model_dir)
    create_directory([Base_model_dir_path])
    base_model_path = os.path.join(Base_model_dir_path ,Base_model_name)

    model = get_VGG16_model(input_size = params["Image_Size"] , model_path = base_model_path)




    



if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config" , "-c" , default= "config/config.yaml")
    args.add_argument("--params" , "-p" , default= "params.yaml")


    parsed_args = args.parse_args()
    try:
        logging.info("stage two is started")
        prepare_base_model(config_path=parsed_args.config , params_path =parsed_args.params)
        logging.info("stage two completed and data are prepare BaseModel")
    except Exception as e:
        logging.exception(e)
