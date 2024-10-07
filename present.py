import cv2
import os
import random
import requests
import base64
import io
from PIL import Image

text2ImageModel = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
image2VidModel = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-video-diffusion"

headers = {
    # Replace the API key after Bearer with your own API key
    "Authorization": "Bearer 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",
    "Accept": "application/json",
}

# Edit path to image folder
dir = "../../assets/scenery"
    
def run_opencv_presentation(count=50):
    used = set()
    images = os.listdir(dir)
    for i in range(count):

        # Get random non duplicated image
        idx = random.randint(0, len(images)-1)
        while idx in used:
            idx = random.randint(0, len(images)-1)   
        used.add(idx)         
        img = images[idx]
        path = os.path.join(dir, img)
        print(path)
        image = cv2.imread(path)

        # Insert marker

        # Show the image and wait for 1 second
        cv2.imshow("image", image)
        cv2.waitKey(1000)

def data_to_image(prompt="Serene lake with sunset and purple wind", cfg_scale=5, seed=0, steps=50, negative_prompt=""):
    imagePayload = {
        "prompt": prompt,
        "cfg_scale": cfg_scale,
        "aspect_ratio": "16:9",
        "seed": seed,
        "steps": steps,
        "negative_prompt": negative_prompt
    }

    # Get image from text-to-image model
    imageResponse = requests.post(text2ImageModel, headers=headers, json=imagePayload)
    if imageResponse.status_code != 200:
        return f"Image request failed with status {imageResponse.status_code} {imageResponse.text}", imageResponse.status_code
    
    image_data = imageResponse.json().get('image')
    
    # Decode the base64 image data
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))

    # Ensure the image size is below 200KB before re-enconding
    buffered = io.BytesIO()
    quality = 85
    image.save(buffered, format="JPEG", quality=quality)
    while buffered.tell() > 200 * 1024 and quality > 10: 
        quality -= 5
        buffered.seek(0)
        buffered.truncate()
        image.save(buffered, format="JPEG", quality=quality)

    # Save the image locally
    image_path = os.path.join(os.path.dirname(__file__), 'output', 'image.jpg')
    with open(image_path, 'wb') as f:
        f.write(buffered.getvalue())
    
    resized_image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return resized_image_data, image_path

def image_to_video(image_data, image_type="jpeg", seed=2441322616, cfg_scale=1.8):
    vidPayload = {
        "image": f"data:image/{image_type};base64,{image_data}",  
        "seed": seed,
        "cfg_scale": cfg_scale,
    }

    # Get video from image-to-video model
    vidResponse = requests.post(image2VidModel, headers=headers, json=vidPayload)
    if vidResponse.status_code != 200:
        return f"Video request failed with status {vidResponse.status_code} {vidResponse.text}", vidResponse.status_code

    video_data = vidResponse.json().get('video') 

    # Decode and save the video content locally 
    video_bytes = base64.b64decode(video_data)
    video_path = os.path.join(os.path.dirname(__file__), 'output', 'video.mp4')
    with open(video_path, 'wb') as f:
        f.write(video_bytes)

    return video_path


if __name__ == "__main__":
    run_opencv_presentation(3)