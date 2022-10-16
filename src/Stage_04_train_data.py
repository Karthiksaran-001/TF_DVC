import tensorflow as tf
from ast import arg
from src.utils.all_utils import read_yaml   , create_directory
from src.utils.models import load_full_model , get_unique_path_to_save_model
from src.utils.callbacks import get_callbacks
from src.utils.data_management import train_valid_generator
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

    train_generator, valid_generator = train_valid_generator(
        data_dir=artifacts["DATA_DIR"],
        IMAGE_SIZE=tuple(params["IMAGE_SIZE"][:-1]),
        BATCH_SIZE=params["BATCH_SIZE"],
        do_data_augmentation=params["AUGMENTATION"]
    )

    steps_per_epoch = train_generator.samples // train_generator.batch_size
    validation_steps = valid_generator.samples // valid_generator.batch_size

    model.fit(
        train_generator,
        validation_data=valid_generator,
        epochs=params["EPOCHS"], 
        steps_per_epoch=steps_per_epoch, 
        validation_steps=validation_steps,
        callbacks=callbacks
    )

    logging.info(f"training completed")

    trained_model_dir = os.path.join(artifacts_dir, artifacts["Trained_model_dir"])
    create_directory([trained_model_dir])

    model_file_path = get_unique_path_to_save_model(trained_model_dir)
    model.save(model_file_path)
    logging.info(f"trained model is saved at: {model_file_path}")

    
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