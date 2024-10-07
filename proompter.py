import openai
import json

with open('.api_key.json') as f:
    data = json.load(f)
# Set up your OpenAI API key
openai.api_key = data["key"]

def rankings2images(image_names):

    image_vibes = curate_images(image_names)

    general_vibe = summarize_vibe(descriptions=image_vibes)

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
    prompt = "Based on these descriptions, summarize the overall vibe or feeling of the combination of these five images: "
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
    # Example descriptions (you can load these from a file or any other source)
    descriptions = [
        "A picturesque canal lined with cherry blossom trees, adorned with vibrant pink blossoms that stretch above the water, creating a breathtaking scene.",
        "A starry night above a desert landscape, with a vast sandy expanse stretching out before a distant raised sand dune, evoking a sense of peaceful isolation.",
        "A waterfall flows into a lake in front of a mountain under a starry sky with an aurora borealis.",
        "A breathtaking peninsula silhouetted against a vibrant golden sunset, with its bright glow reflecting off the cloud cover and the ocean surrounding it.",
        "A serene sunset ocean scene with a striking pink and orange sky, a small cove, an ocean wave crash, and a rock formation."
    ]

    # Step 1: Summarize the vibe from the descriptions
    vibe_summary = summarize_vibe(descriptions)
    print("Vibe Summary:")
    print(vibe_summary)

    # Step 2: Generate a prompt for a text-to-image generator based on the vibe summary
    # text_image_prompt = generate_text_image_prompt(vibe_summary)
    # print("Text-to-Image Prompt:")
    # print(text_image_prompt)
