import openai
import json

with open('.api_key.json') as f:
    data = json.load(f)
# Set up your OpenAI API key
openai.api_key = data["key"]

def rankings2images(image_names):

    image_vibes = curate_images(image_names)

    general_vibe = summarize_vibe(descriptions=image_vibes)

    print(f'General vibe is: {general_vibe}')

    vibe2image(general_vibe)


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
    prompt = "Based on these descriptions, summarize the overall vibe or feeling of the combination of these five images. Respond only with the vibe as a description of an image to generate from this vibe. Be detailed but vague. The description of this vibe should include many visual components. Do not reference the images."
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

def vibe2image(vibe_prompt):
    return "IMG_PATH"


if __name__ == "__main__":
    pass