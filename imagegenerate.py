import requests
import os
import time
import random
import json
import sys
import io
import base64
from PIL import Image, PngImagePlugin  # import PngImagePlugin
from artists import artists

current_dir = os.path.dirname(os.path.abspath(__file__))
text_folder_path = os.path.join(current_dir, "Texts")
image_folder_path = os.path.join(current_dir, "Images")
text_files = [f for f in os.listdir(text_folder_path) if f.endswith('.txt')]
selected_artist = random.choice(artists)
api_url = "http://127.0.0.1:7860"

def generate_image_with_sd2_api(prompt):
    payload = {
        "prompt": prompt,
        "steps": 50,
        "cfg_scale": 7.0,
        "sampler_name": "DPM++ 2M SDE Karras",  # Use DPM2 sampler by Karras
        "negative_prompt": "cropped, nudity, explicit, sexual, naked, nude, undressed, unclothed, topless, explicit content, adult content, mature content, sexual content, NSFW, text, children, boobs, tits, bad anatomy, bad proportions, deformed",
        "width": 768,
        "height": 1024
        # Add more parameters here as needed
    }
    response = requests.post(url=f'{api_url}/sdapi/v1/txt2img', json=payload)
    response_data = response.json()

    # Print the entire response to see what it looks like
    #print(f"Response data: {response_data}")

    for i in response_data['images']:
        image_data = i.split(",",1)
        if len(image_data) < 2:
            image_data = ["", i]  # Assume that missing data type means it's a PNG image
        try:
            image = Image.open(io.BytesIO(base64.b64decode(image_data[1])))
        except Exception as e:
            print(f"Error decoding base64 string: {e}")
            continue

        # Get PNG info
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{api_url}/sdapi/v1/png-info', json=png_payload)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", json.dumps(response2.json().get("info"), indent=4))
        image.save('output.png', pnginfo=pnginfo)

        return image  # Return the generated image
    return None  # Return None if no valid image was found

for i, text_file in enumerate(text_files, start=1):
    text_file_path = os.path.join(text_folder_path, text_file)

    with open(text_file_path, 'r') as file:
        text = file.read()

    paragraphs = text.split("\n\n")
    previous_prompt = ""
    image_number = 1
    title = None  # Added line to initialize title

    for paragraph in paragraphs:
        if not paragraph.strip():
            continue

        # If title is not yet set, set it as the current paragraph
        if title is None:
            title = paragraph

        prompt = f"masterpiece, {selected_artist}, depicting: '{title}, {paragraph}, 8k, detailed'"

        try:
            image = generate_image_with_sd2_api(prompt)
            if image is None:  # Check if image is None before saving
                print(f"Failed to generate image for prompt: {prompt}")
                continue
            previous_prompt = prompt
        except Exception as e:
            print(f"Error generating image: {e}")
            continue

        print(f"Generated image from prompt: {prompt}")
        new_image_path = os.path.join(image_folder_path, f"{text_file.split('.')[0]}_image_{image_number}.png")
        image.save(new_image_path)

        image_number += 1
        time.sleep(1)

    print(f"Processed {text_file}")