import tensorflow as tf
import os
import logging
from src.utils.all_utils import get_timestamp

def get_VGG16_model(input_size , model_path):
    logging.info(f"Start Using VGG16")
    model = tf.keras.applications.vgg16.VGG16(
        input_shape = input_size,
        weights="imagenet",
        include_top=False)
    model.save(model_path)
    logging.info(f"VGG16 is saved in {model_path}")
    return model

def prepare_final_layer(model , Class , freeze_all , freeze_till , learning_rate):
    if freeze_all:
        for layer in model.layers:
            layer.trainable = False
    elif (freeze_till is not None) and (freeze_till > 1):
        for layer in model.layers[:-freeze_till]:
            layer.trainable = False
    ## add our layers to the base model
    flatten_in = tf.keras.layers.Flatten()(model.output)

    prediction = tf.keras.layers.Dense(
        units=Class,
        activation="softmax"
    )(flatten_in)

    full_model = tf.keras.models.Model(
        inputs = model.input,
        outputs = prediction
    )

    full_model.compile(
        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate),
        loss = tf.keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"]
    )

    logging.info("custom model is compiled and ready to be trained")

    return full_model

def load_full_model(untrained_full_model_path):
    model = tf.keras.models.load_model(untrained_full_model_path)
    logging.info(f"untrained model is read from: {untrained_full_model_path}")
    return model

def get_unique_path_to_save_model(trained_model_dir, model_name="model"):
    timestamp = get_timestamp(model_name)
    unique_model_name = f"{timestamp}_.h5"
    unique_model_path = os.path.join(trained_model_dir, unique_model_name)
    return unique_model_path

