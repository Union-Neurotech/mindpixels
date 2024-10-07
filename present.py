import cv2
import os
import random
import requests
import base64
import io
from PIL import Image
from brainflow import BoardShim
import numpy as np

text2ImageModel = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
image2VidModel = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-video-diffusion"

headers = {
    # Replace the API key after Bearer with your own API key
    "Authorization": "Bearer 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",
    "Accept": "application/json",
}

# Edit path to image folder
dir = "assets/"

def run_opencv_presentation(board:BoardShim, image_folder:str="images/", display_time:int=2, screen_resolution=(1920, 1080)):
    """
    Displays images in fullscreen with markers and returns EEG data.
    
    Parameters:
    - board: EEG board object (for streaming data and inserting markers).
    - image_folder: Path to the folder containing images.
    - display_time: Time (in seconds) each image should be displayed.
    
    Returns:
    - EEG data collected during the session.
    - the board you passed in
    """
    # Get list of image files from the specified folder
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if image_files == []: print("NO IMAGE FILES, did you remember to add them?")

    # Sort the images to ensure a specific order if needed
    image_files.sort()

    # Create a fullscreen window for OpenCV
    window_name = "Image Presentation"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Start the EEG stream (assuming the stream is not already started)
    board.start_stream()

    for idx, image_file in enumerate(image_files):
        # Load the image and resize to fit fullscreen (assuming 1920x1080 for simplicity)
        img = cv2.imread(image_file)
        # img = cv2.resize(img, (1920, 1080))

        # Get the dimensions of the image and the screen
        img_height, img_width = img.shape[:2]
        screen_width, screen_height = screen_resolution

        # Create a black background (same size as the screen resolution)
        background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

        x_offset = (background.shape[1] - img.shape[1]) // 2
        y_offset = (background.shape[0] - img.shape[0]) // 2
        
        
        # Ensure the image fits within the screen dimensions
        if img_width <= screen_width and img_height <= screen_height:
            # Place the image on the black background at the calculated offset
            background[y_offset:y_offset + img_height, x_offset:x_offset + img_width] = img
        else:
            # If the image is larger than the screen, resize it to fit while maintaining aspect ratio
            img = cv2.resize(img, (screen_width, screen_height), interpolation=cv2.INTER_AREA)
            background = img  # Use the resized image directly as the background
        
        # Display the image
        cv2.imshow(window_name, background)

        # Insert a marker into the EEG stream
        marker = idx + 1  # Marker could be any value; using image index here
        board.insert_marker(marker)

        # Wait for the specified display time
        cv2.waitKey(display_time * 1000)

    # Stop the stream and close the OpenCV window
    board.stop_stream()
    cv2.destroyAllWindows()

    # Get and return the EEG data
    data = board.get_board_data()
    return data, board

def run_opencv_presentation_lite(count=50):
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