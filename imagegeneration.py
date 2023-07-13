import os
import openai
import time
import requests
import random
import sys

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv('OPENAI_API_KEY')

# Add path to sys.path to import artists from artists.py
sys.path.append('C:/Users/teo_t/Desktop/Autogen')

from artists import artists

# Define path to text files
text_folder_path = "C:\\Users\\teo_t\\Desktop\\Autogen\\Texts\\"

# Define path for saving generated images
image_folder_path = "C:\\Users\\teo_t\\Desktop\\Autogen\\Images\\"

# List of text files
text_files = [f for f in os.listdir(text_folder_path) if f.endswith('.txt')]

# Select a random artist - moved outside of the loops
selected_artist = random.choice(artists)

# For each text file
for i, text_file in enumerate(text_files, start=1):

    # Construct the full path to the text file
    text_file_path = os.path.join(text_folder_path, text_file)

    # Read the content of the text file
    with open(text_file_path, 'r') as file:
        text = file.read()

    # Split the text into paragraphs
    paragraphs = text.split("\n\n")

    # For each paragraph in the text file
    for j, paragraph in enumerate(paragraphs, start=1):

        # Ignore empty paragraphs
        if not paragraph.strip():
            continue

        # Create the prompt
        prompt = f"A painting in the style of {selected_artist}, depicting a scene inspired by: '{paragraph}'"

        # Generate image using OpenAI API
        response = openai.Image.create(
            prompt=prompt, 
            n=1,
            size="1024x1024"
        )

        # Print the prompt
        print(f"Generated image from prompt: {prompt}")

        # Get the URL of the generated image
        image_url = response['data'][0]['url']

        # Save the image to a file
        image_path = f"{image_folder_path}{text_file.split('.')[0]}_image_{j}.png"
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as out_file:
                out_file.write(response.content)

        # Respect rate limit
        time.sleep(1)  # Adjust this based on your specific rate limit

    print(f"Processed {text_file}")
