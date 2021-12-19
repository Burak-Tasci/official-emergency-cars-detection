import glob
import augly.image as imaugs
import argparse
import random
from PIL import Image
from IPython import display

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", help="Path of dataset directory", required=True)
ap.add_argument("-o", "--output", help="Path of augmented data/output directory", required=True)
ap.add_argument("-d", "--depth", help="Count of augmentation on every image", required=False)
args = vars(ap.parse_args())


def random_value():
    return random.random()*2 + 10e-5

def main():
    source = args["source"]
    output = args["output"]
    if args["depth"] is None:
        depth=1
    else:
        depth = int(args["depth"])

    

    augmentations = [
        imaugs.HFlip(), imaugs.RandomAspectRatio(), 
        imaugs.RandomBlur(), imaugs.RandomBrightness(),
        imaugs.RandomNoise(), imaugs.RandomPixelization(),
        imaugs.Saturation(random_value()), imaugs.Contrast(random_value()),
        imaugs.ShufflePixels(0.2),
        ]

    images = glob.glob(source+"\\*.jpg") + \
             glob.glob(source+"\\*.jpeg") + \
             glob.glob(source+"\\*.png")

    print(len(images))

    for count,file in enumerate(images):
        img = Image.open(file)
        for i in range(depth):
            augmented = augmentations[random.randint(0,len(augmentations)-1)](img)
            augmented.save(output+"\\"+str(count)+str(i)+"."+file.split(".")[-1])







if __name__ == "__main__":
    main()
