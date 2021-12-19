import glob
import augly.image as imaugs
import argparse
import random
from PIL import Image
from progress.bar import IncrementalBar

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

    total = len(images) * depth
    bar = IncrementalBar('Augmentation', max = total)

    for count,file in enumerate(images):
        img = Image.open(file)
        random_indexes = random.sample(range(len(augmentations)), 3)
        for i, index in enumerate(random_indexes):
            augmented = augmentations[index](img)
            augmented.save(output+"\\augmented"+str(count)+str(i)+"."+file.split(".")[-1])
            bar.next()

    bar.finish()

if __name__ == "__main__":
    main()


