import openai
import json
import requests
import base64
import io
from PIL import Image
import os
import uuid
import time

text2ImageModel = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
image2VidModel = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-video-diffusion"

headers = {
    "Authorization": "Bearer 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",
    "Accept": "application/json",
}

with open('.api_key.json') as f:
    data = json.load(f)
# Set up your OpenAI API key
openai.api_key = data["key"]

def rankings2images(image_names, doimage=False, bypass=True):

    image_vibes = curate_images(image_names)

    general_vibe = summarize_vibe(descriptions=image_vibes)

    print(f'General vibe is: {general_vibe}')
#    'output//video_dcb22e7c-1cfb-4521-a9ce-0ccec6190adc.mp4'
    if bypass:
        return general_vibe, 'output/video_805e38e4-bb12-4e96-ad91-9a646c570f56.mp4', 'video'
    

    resized_image, imgpath = vibe2image(general_vibe)
    if doimage:
        return general_vibe, imgpath, 'image'
    else:
        videopath = image2video(resized_image, image_type="jpeg", seed=2441322616, cfg_scale=1.8)
        return general_vibe, videopath, 'video'

from img_data import dict_images
def curate_images(image_names) -> list[str]:
    vibes2return = []
    for img in image_names:
        vibes2return.append(dict_images[img])
    return vibes2return

def summarize_vibe(descriptions):
    """
    Function to summarize the overall vibe of the provided descriptions
    using OpenAI's latest API syntax.
    
    :param descriptions: A list of image descriptions
    :return: A vibe summary string
    """
    prompt = "Based on these descriptions, summarize the overall vibe or feeling of the combination of these five images. Respond only with the vibe as a description of an image to generate from this vibe. Be detailed but vague. The image described must be photorealistic. The description of this vibe should include many visual components. Do not reference the images."
    prompt += " ".join(descriptions)
    
    # Call the OpenAI API using the latest `chat` or `completion` endpoints
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use other models like `gpt-4` if available
        max_tokens=100,
        temperature=0.7,
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": prompt
        }
        ]
        
    )
    return response.choices[0].message.content

def vibe2image(prompt="Serene lake with sunset and purple wind", cfg_scale=5, seed=0, steps=50, negative_prompt=""):
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
        print( f"Image request failed with status {imageResponse.status_code} {imageResponse.text}" )
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
    image_path = os.path.join(os.path.dirname(__file__), 'output', f'image_{uuid.uuid4()}.jpg')
    with open(image_path, 'wb') as f:
        f.write(buffered.getvalue())
    
    resized_image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return resized_image_data, image_path

def image2video(image_data, image_type="jpeg", seed=2441322616, cfg_scale=1.8):

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
    video_path = os.path.join(os.path.dirname(__file__), 'output', f'video_{uuid.uuid4()}.mp4')
    with open(video_path, 'wb') as f:
        f.write(video_bytes)

    return video_path

if __name__ == "__main__":
    img, image_path = vibe2image(prompt="An enchanting landscape at twilight, where nature's beauty harmonizes with architectural marvels, creating a serene and mystical atmosphere. The scene features a grand cliffside overlooking the shimmering ocean, adorned with a magnificent building perched atop a rugged stone ledge. A lush tree gracefully drapes over the glowing lights and swirling waters below, where boats, canoes, and ducks glide peacefully. In the distance, a bridge and a neatly trimmed hedge frame a long walkway leading to a short dock.")
    print("cool")