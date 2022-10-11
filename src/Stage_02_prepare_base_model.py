from ast import arg
from src.utils.all_utils import read_yaml   , create_directory
from src.utils.models import get_VGG16_model , prepare_final_layer
import argparse
import io
import os
import logging

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


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

    model = get_VGG16_model(input_size = params["IMAGE_SIZE"] , model_path = base_model_path)

    full_model = prepare_final_layer(
        model,
        Class = params["Classes"],
        freeze_all = True,
        freeze_till = None,
        learning_rate =params["LEARNING_RATE"],
    )

    updated_base_model_path = os.path.join(Base_model_dir_path , artifacts["Updated_Base_model_name"])

    def _log_model_summary(full_model):
        with io.StringIO() as stream:
            full_model.summary(print_fn=lambda x: stream.write(f"{x}\n"))
            summary_str = stream.getvalue()
        return summary_str
    logging.info(f"Model Summary : \n{_log_model_summary(full_model)}")

    full_model.save(updated_base_model_path)




    



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
