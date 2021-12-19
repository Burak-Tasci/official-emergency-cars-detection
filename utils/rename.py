import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-src","--source",required=True,
                    help="Source path of dataset directory to rename its images")
args = vars(ap.parse_args())
def main():
   
    folder = args["source"]
    for count, filename in enumerate(os.listdir(folder)):
        if filename.endswith(".jpg"):
            dst = f"{str(count)}.jpg"
        elif filename.endswith(".jpeg"):
            dst = f"{str(count)}.jpg"
        elif filename.endswith(".png"):
            dst = f"{str(count)}.png"
        else:
            continue
        src =f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
        dst =f"{folder}/{dst}"
        # rename() function will
        # rename all the files
        os.rename(src, dst)
 
# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()