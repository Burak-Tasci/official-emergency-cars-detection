import os
import cv2
import random

def __intercect_of_union(image1, image2):
    pass

def visualize_detections(image, boxes, scores, classes, label_dict, max_boxes_to_draw, threshold):
    
    for index, score in enumerate(scores):
        if score > threshold:
            
            xmin, ymin, xmax, ymax = boxes[index]
            label_id = classes[index]
            label = label_dict[label_id]

            cv2.rectangle(image, (xmin,ymin), (xmax, ymax), color=(0,255,0),thickness=1)

    cv2.imshow("image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




