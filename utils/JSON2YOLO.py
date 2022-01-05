import glob
import json
from progress.bar import IncrementalBar

CLASSES = ["Ambulance", "Police", "Fire Service"]
LABELS_DIR = "./official-emergency/emergency/labels/"
OUTPUT_DIR = "./official-emergency/emergency/YOLO-labels/"


def formatToYolo(points, boundingBox, tag, size):
    
    # xs and ys of region
    xs = [points[i]["x"] for i in range(4)]
    ys = [points[i]["y"] for i in range(4)]
    xmin = min(xs)
    ymin = min(ys)
    # Bounding box / image widths and heights 
    bbWidth = boundingBox["width"]
    bbHeight = boundingBox["height"]
    absHeight = size["height"]
    absWidth = size["width"]
    # Xcenter and YCenter 
    xCenter = xmin + (bbWidth / 2)
    yCenter = ymin + (bbHeight / 2)
    xCenter = xCenter / absWidth
    yCenter = yCenter / absHeight
    # Class label
    cls = CLASSES.index(*tag)
    # width and height for region
    width = bbWidth / absWidth
    height = bbHeight / absHeight

    return [cls, xCenter, yCenter, width, height]
    


def main():

    files = glob.glob(LABELS_DIR+"*.json")
    bar = IncrementalBar('Converting...', max = len(files))

    for file in files:
        data = json.load(open(file))
        regions = data["regions"]
        size = data["asset"]["size"]
        filename = data["asset"]["name"][:-4]
        print(f"Processing json file: {filename}",end="\r")
        filename = filename  + ".txt"
        labelFile = open(OUTPUT_DIR+filename,"w+")
        for region in regions:
            # Extracting attributes
            attributes = formatToYolo(region["points"], region["boundingBox"], region["tags"], size)
            attributes = " ".join(str(item) for item in attributes) + "\n"
            # Writing to file
            labelFile.write(attributes)
        labelFile.close()
        bar.next()
    bar.finish()





if __name__ == "__main__":
    main()