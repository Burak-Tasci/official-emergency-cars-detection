import os
import cv2
import random

def area(xmin, xmax, ymin, ymax, h, w):
    xmin, xmax = xmin * w, xmax * w
    ymin, ymax = ymin * h, ymax * h
    bbWidth = xmax - xmin
    bbHeight = ymax - ymin
    return bbWidth * bbHeight

def visualize_detections(image, boxes, scores, classes, label_dict, max_boxes_to_draw = 10, threshold = 0.50):
    
    boxes, scores, classes = boxes[:max_boxes_to_draw], scores[:max_boxes_to_draw], classes[:max_boxes_to_draw]
    w,h = image.shape[:2]
    for index, score in enumerate(scores):
        if score > threshold  :
            
            xmin, ymin, xmax, ymax = boxes[index]
            xmin, xmax = xmin * w, xmax * w
            ymin, ymax = ymin * h, ymax * h
            label_id = classes[index]
            label = label_dict[label_id]

            image = cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0,255,0), 1)

    cv2.imshow("image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




