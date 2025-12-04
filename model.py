# Importing required libs
from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image
import tensorflow as tf

# Ensure we stay in eager mode, even in threaded/greenlet contexts (Locust)
tf.config.run_functions_eagerly(True)

# Loading model
model = load_model("digit_model.h5")


# Preparing and pre-processing the image
def preprocess_img(img_path):
    op_img = Image.open(img_path)
    img_resize = op_img.resize((224, 224))
    img2arr = img_to_array(img_resize) / 255.0
    img_reshape = img2arr.reshape(1, 224, 224, 3)
    return img_reshape


# Predicting function
def predict_result(predict):
    """
    Run a prediction on the preprocessed image array and
    return the predicted class index.
    """
    # Use model(...) instead of model.predict(...) to avoid graph-mode issues
    pred = model(predict, training=False)  # returns a Tensor
    pred = np.array(pred)                  # convert to ndarray if needed
    pred = model.predict(predict)
    return np.argmax(pred[0], axis=-1)
