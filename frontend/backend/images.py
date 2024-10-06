import cv2
import os 
import random

#AI prompt each time Describe this with one short concise sentence
dict_images = {
    "img11.jpg": "A breathtaking peninsula is silhouetted against a vibrant golden sunset, with its bright glow reflecting off the cloud cover and the ocean surrounding it.",
    "img10.jpg": "A snowy, mountainous landscape is illuminated by a bright sunset. ",
    "img9.jpg" : "A close-up view of a tangled web of branches and vines.",
    "img8.jpg" : "A waterfall flows into a lake in front of a mountain under a starry sky with an aurora borealis.",
    "img7.jpg": "An arboreal landscape imparting a sense of fall, set against the background of tall, snow-covered mountain peaks." ,
    "img6.jpg" :"A nighttime scene with silhouetted evergreens against a deep red sky.",
    "img5.jpg": " a serene sunset ocean scene with a striking pink and orange sky, a small cove, an ocean wave crash, and a rock formation.",
    "img4.jpg": "hills with grasses, shrubs, and a small waterfall up ahead, at the center, thriving in a laid-back environment.",
    "img3.jpg": "A frozen lake is surrounded by fir and spruce trees and snow-covered cliffs in this remote wintertime scene.",
    "img2.jpg": "A serene sunset over a body of water with vapors that appear to be wet and reflective and scattered clouds abroad.",
    "img1.jpg": "serene lakeside scene, likely predawn or dusk, with the gentle reflection of tall evergreen trees on the water's surface.",
    "winter.jpg": "an empty parking lot with a flat surface, where it has been lightly snowing or sleeting.",
    "clouds.png":"Amusingly distorted, rippled clouds cast a darkening grey sky in the background above a line of tall-steety lampposts.",
    "creepy_hallway.png": "a long and dimly lit hallway featuring green carpeting and clean walls, with recessed lights and emergency signs.",
    "snow_stair.png": "a snowy landscape with some steps or steps leading some where.",
    "liminal_japan.png": "a long, dimly-lit industrial corridor.",
    "red_moon.png": "a serene grassy field at night, illuminated by the faint glow of the moon beyond, creating an ethereal atmosphere.",
    "home_stairs.png": "a living room, stairwell, and hallway from the perspective of the home's second-floor landing."

}
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





