from detecto.core import Model
import glob
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image
import pandas as pd
import numpy as np
from utils.Color import ColorRecogniser

colorsData = "./data/COLORS.csv"
colorRecogniser = ColorRecogniser(colorsData)
model = Model.load('./models/licence-model.pth', ['licence'])
testImages = glob.glob("./testImages/*.jpg")
ImagesAndColors = pd.read_csv(colorsData)

for imagePath in testImages:
    image_colors = []
    bg_colors = []
    img = Image.open(imagePath)
    img_np = np.array(img)

    top_border = img_np[:1,:]
    left_border = img_np[:,:1]
    right_border = img_np[:,-2:-1]

    borders = [top_border, left_border, right_border]

    labels, boxes, scores = model.predict(img)
    boxes = boxes.numpy()
    try:
        xmin, ymin, xmax, ymax = boxes[0][0],boxes[0][1],boxes[0][2],boxes[0][3]
        print("PLATE FOUND!")
    except:
        print("THERE IS NO PLATE!")
        continue
    cropped_img = np.array(img.crop((xmin, ymin, xmax, ymax)))
    
    
    for border in borders:
        # LEFT BORDER
        dominants = colorRecogniser.getColors(border)
        b,g,r = dominants[0]
        bg_colors.append(colorRecogniser.getColorName(b,g,r))
        b,g,r = dominants[1]
        bg_colors.append(colorRecogniser.getColorName(b,g,r))

    
    dominants = colorRecogniser.getColors(cropped_img)
    b,g,r = dominants[0]
    image_colors.append(colorRecogniser.getColorName(b,g,r))
    b,g,r = dominants[1]
    image_colors.append(colorRecogniser.getColorName(b,g,r))

    

    bg = colorRecogniser.getSyncColor(image_colors, bg_colors)
    cloth_color = colorRecogniser.diff(bg,image_colors)

    color_df = ImagesAndColors[ImagesAndColors["Name"] == cloth_color]
    rgb = color_df.loc[:,["Red (8 bit)","Green (8 bit)","Blue (8 bit)"]]

    color = np.ones([256,256,3], dtype=np.uint8) * rgb.loc[:,["Red (8 bit)","Green (8 bit)","Blue (8 bit)"]].values


    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(img_np)

    # Create a Rectangle patch
    rect = patches.Rectangle((xmin, ymin), int(xmax-xmin), int(ymax-ymin), linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    if "blue" in cloth_color or  "Licorice" in cloth_color or "Granite Gray" in cloth_color or "Pale silver" in cloth_color:
        plt.title("OFFICAL PLATE")
    else:
        plt.title("UNOFFICIAL PLATE")
    plt.xticks([])
    plt.yticks([])
    plt.show()

