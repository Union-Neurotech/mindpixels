from flask import Flask, request, jsonify, render_template_string
import requests
import base64
import os
import io
from PIL import Image

app = Flask(__name__)

text2ImageModel = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
image2VidModel = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-video-diffusion"

headers = {
    # Replace the API key after Bearer with your own API key
    "Authorization": "Bearer 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",
    "Accept": "application/json",
}

imagePayload = {
    "prompt": "Serene lake with sunset and purple wind",
    "cfg_scale": 5,
    "aspect_ratio": "16:9",
    "seed": 0,
    "steps": 50,
    "negative_prompt": ""
}

@app.route('/test')
def hello():
    return "Hello World!"

# @app.route('/start_process')
def start_proc():
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
    image_path = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'resized_image.jpg')
    with open(image_path, 'wb') as f:
        f.write(buffered.getvalue())
    
    resized_image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    vidPayload = {
        "image": f"data:image/jpeg;base64,{resized_image_data}",  
        "seed": 2441322616,
        "cfg_scale": 1.8,
    }

    vidResponse = requests.post(image2VidModel, headers=headers, json=vidPayload)

    if vidResponse.status_code != 200:
        return f"Video request failed with status {vidResponse.status_code} {vidResponse.text}", vidResponse.status_code

    video_data = vidResponse.json().get('video') 

    if not video_data:
        return "Video URL not found in the response.", 500

    # Decode and save the video content locally 
    video_bytes = base64.b64decode(video_data)
    video_path = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'generated_video.mp4')
    with open(video_path, 'wb') as f:
        f.write(video_bytes)

    return video_path

@app.route('/stop_process')
def stop_proc():
    data = {"message": "Process Stopped"}
    return jsonify(data)

@app.route('/command', methods=['POST'])
def execute_command():
    command = request.json.get('command')
    
    if command == "start-inject-video":

        # run code

        # get video path
        video_path = start_proc()
        
        return jsonify({'status': 'START Command received',
                        'video': video_path})

    if command == 'start':
        # Implement your start logic here
        print("HELLO HELLO")



        return jsonify({'status': 'START Command received'})
    
    elif command == 'stop':
        # Implement your stop logic here
        return jsonify({'status': 'STOP Command received'})
    
    elif command == 'restart':
        # Implement your restart logic here
        return jsonify({'status': 'RESTART Command received'})

    else:
        return jsonify({'error': 'Unknown command'}), 400
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)