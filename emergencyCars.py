import time
from object_detection.utils import label_map_util
import tensorflow as tf
import numpy as np
from PIL import Image
import glob
import os
import warnings
import matplotlib.pyplot as plt
from matplotlib import patches
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings

# PATHS AND VARIABLES
API_PATH = "C://Users/ABRA/Desktop/Projects/ObjectDetection/models/research/object_detection/"
PATH_TO_SAVED_MODEL =  API_PATH + "moodel85/saved_model/"
PATH_TO_LABELS = API_PATH + "data/emergency_labelmap.pbtxt"
MAX_BOXES_TO_DRAW = 10
THRESHOLD = 0.55

print('Loading model...', end='')
start_time = time.time()

# Load saved model and build the detection function
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds'.format(elapsed_time))

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)

# TEST IMAGES' PATHS
PATHS = glob.glob("./testImages/*.jpg")


for image_path in PATHS:

  print('Running inference for {}... '.format(image_path), end='')

  FLAG = False

  image_np = np.array(Image.open(image_path))
  input_tensor = tf.convert_to_tensor(image_np)
  input_tensor = input_tensor[tf.newaxis, ...]

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


  os.system("cls")
  image_np_with_detections = image_np.copy()

  fig, ax = plt.subplots()

  boxes, scores, classes = detections['detection_boxes'], detections['detection_scores'], detections['detection_classes']
  boxes, scores, classes = boxes[:MAX_BOXES_TO_DRAW], scores[:MAX_BOXES_TO_DRAW], classes[:MAX_BOXES_TO_DRAW]
  h, w = image_np_with_detections.shape[:2]
  ax.imshow(image_np_with_detections)
  for index, score in enumerate(scores):
    if score > THRESHOLD  :
        FLAG = True
        xmin, ymin, xmax, ymax = boxes[index]
        xmin, xmax = xmin * w, xmax * w
        ymin, ymax = ymin * h, ymax * h

  if FLAG:
    plt.title("EMERGENCY CAR DETECTED")
  else:
    plt.title("EMERGENCY CAR NOT DETECTED")

  plt.xticks([])
  plt.yticks([])
  plt.show()
  
print('Done')