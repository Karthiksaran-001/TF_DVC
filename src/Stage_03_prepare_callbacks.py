from ast import arg
from src.utils.all_utils import read_yaml   , create_directory
import argparse
import os
from src.utils.callbacks import create_save_tensorboard_callbacks, create_save_checkpoint_callbacks
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

   artifacts = config["artifacts"]
   artifacts_dir = artifacts["artifacts_dir"]
   
   tensorboard_logdir = os.path.join(artifacts_dir , artifacts["TENSORBOARD_ROOT_LOG_DIR"])
   checkpoint_dir = os.path.join(artifacts_dir , artifacts["Checkpoint_Dir"])
   callback_dir = os.path.join(artifacts_dir , artifacts["CALLBACKS_DIR"])

   create_directory([tensorboard_logdir,checkpoint_dir,callback_dir])
   create_save_tensorboard_callbacks(callback_dir , tensorboard_logdir)
   create_save_checkpoint_callbacks(callback_dir , tensorboard_logdir)
   




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
