import cv2
import os 
import random

def generate_unique_random_numbers(x, n=50):
    # Generate 50 unique random numbers between 0 and x
    return random.sample(range(0, x+1), n)

# Example usage:
x = 100  # Set x to any value you prefer
random_numbers = generate_unique_random_numbers(x)

dir = "/Users/victorwong/Desktop/mindpixels/frontend/backend/Food Images/Food Images/"


for img in os.listdir(dir):
    path = os.path.join(dir, img)
    path = str(path)
    image = cv2.imread(path)
    cv2.imshow("image", image)

    if cv2.waitKey() == ord('a'):
        print("pressed a")
        break

    cv2.waitKey(0)





