import tensorflow as tf
from ast import arg
from src.utils.all_utils import read_yaml   , create_directory
from src.utils.models import load_full_model 
from src.utils.callbacks import get_callbacks
import argparse
import os
import logging

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a",
)


def get_train(config_path , params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    artifacts = config["artifacts"]
    artifacts_dir = artifacts["artifacts_dir"]

    train_model_dir_path = os.path.join(artifacts_dir , artifacts["Trained_model_dir"])
    create_directory([train_model_dir_path])

    untrained_full_model = os.path.join(artifacts_dir , artifacts["Base_model_dir"] , artifacts["Updated_Base_model_name"])
    

    model = load_full_model(untrained_full_model)

    callbacks_dir_path = os.path.join(artifacts_dir , artifacts["CALLBACKS_DIR"])
    callbacks = get_callbacks(callbacks_dir_path)

    
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config" , "-c" , default= "config/config.yaml")
    args.add_argument("--params" , "-p" , default= "params.yaml")



    parsed_args = args.parse_args()
    try:
        logging.info("stage Four is started")
        get_train(config_path=parsed_args.config , params_path =parsed_args.params)
        logging.info("stage four completed and model is trained and saved as  binary")
    except Exception as e:
        logging.exception(e)