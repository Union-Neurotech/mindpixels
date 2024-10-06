import cv2
import os 
import random
# from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

# Edit path to image folders
dir = "../../assets/scenery"

def randImages(count=10):
    used = set()
    images = os.listdir(dir)
    for i in range(count):
        # Get random non duplicated image
        idx = random.randint(0, len(images)-1)
        while idx in used:
            idx = random.randint(0, len(images)-1)   
        used.add(idx)         
        img = images[idx]

        # Show the image and wait for 1 second
        path = os.path.join(dir, img)
        print(path)
        image = cv2.imread(path)
        # BoardShim.insert_marker(board_shim, i)
        cv2.imshow("image", image)
        cv2.waitKey(1000)

if __name__ == "__main__":
    randImages(3)




