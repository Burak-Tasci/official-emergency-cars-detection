import time
from object_detection.utils import label_map_util
import tensorflow as tf
import numpy as np
from visualize import visualize_detections
from PIL import Image
import os
import warnings
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings

API_PATH = "C://Users/ABRA/Desktop/Projects/ObjectDetection/models/research/object_detection/"
PATH_TO_SAVED_MODEL =  API_PATH + "trained_model/saved_model/"
PATH_TO_LABELS = API_PATH + "data/emergency_labelmap.pbtxt"

print('Loading model...', end='')
start_time = time.time()

# Load saved model and build the detection function
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds'.format(elapsed_time))

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)

def load_image_into_numpy_array(path):
    """Load an image from file into a numpy array.

    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.

    Args:
      path: the file path to the image

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3)
    """
    return np.array(Image.open(path))

image_path = API_PATH + "test_images/5.jpg"

print('Running inference for {}... '.format(image_path), end='')

image_np = load_image_into_numpy_array(image_path)

# The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
input_tensor = tf.convert_to_tensor(image_np)
# The model expects a batch of images, so add an axis with `tf.newaxis`.
input_tensor = input_tensor[tf.newaxis, ...]

# input_tensor = np.expand_dims(image_np, 0)
detections = detect_fn(input_tensor)

# All outputs are batches tensors.
# Convert to numpy arrays, and take index [0] to remove the batch dimension.
# We're only interested in the first num_detections.
num_detections = int(detections.pop('num_detections'))
detections = {key: value[0, :num_detections].numpy()
                for key, value in detections.items()}
detections['num_detections'] = num_detections

# detection_classes should be ints.
detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

image_np_with_detections = image_np.copy()

os.system("cls")
print(detections["detection_scores"])
print(detections["detection_boxes"])
print(detections["detection_classes"])
visualize_detections(image_np_with_detections, 
                    detections["detection_boxes"],
                    detections["detection_scores"],
                    detections['detection_classes'],
                    category_index)



print('Done')

