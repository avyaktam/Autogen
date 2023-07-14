#imagegenerate.py
import os
import openai
import time
import requests
import random
import sys
from artists import artists

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv('OPENAI_API_KEY')

# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
# Add path to sys.path to import artists from artists.py
sys.path.append('C:/Users/teo_t/Desktop/Autogen')

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

    previous_prompt = ""
    image_number = 1  # separate image number tracker
    # For each paragraph in the text file
    for paragraph in paragraphs:

        # Ignore empty paragraphs
        if not paragraph.strip():
            continue

        # Create the prompt
        prompt = f"A painting in the style of {selected_artist}, depicting a scene inspired by: '{paragraph}'"

        # Generate image using OpenAI API
        try:
            response = openai.Image.create(
                prompt=prompt, 
                n=1,
                size="1024x1024"
            )
            previous_prompt = prompt  # Update previous prompt if current prompt is successful
        except openai.error.InvalidRequestError:
            print("Current prompt was rejected by the safety system. Using previous prompt...")
            if previous_prompt == "":
                print("No previous prompt available. Creating a fallback image...")
                # Extract the base name of the text file (without extension) as a fallback prompt
                fallback_prompt = os.path.splitext(text_file)[0].replace("_", " ")
                prompt = f"A painting in the style of {selected_artist}, depicting a scene inspired by: '{fallback_prompt}'"
                try:
                    response = openai.Image.create(
                        prompt=prompt,  # Using fallback prompt here
                        n=1,
                        size="1024x1024"
                    )
                except openai.error.InvalidRequestError:
                    print("Fallback prompt was also rejected. Creating a default image...")
                    prompt = f"A painting in the style of {selected_artist}, depicting a random scene"
                    response = openai.Image.create(
                        prompt=prompt,  # Using 'random scene' prompt here
                        n=1,
                        size="1024x1024"
                    )

        # Print the prompt
        print(f"Generated image from prompt: {prompt}")

        # Get the URL of the generated image
        image_url = response['data'][0]['url']

        # Save the image to a file
        image_path = f"{image_folder_path}{text_file.split('.')[0]}_image_{image_number}.png"
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as out_file:
                out_file.write(response.content)

        image_number += 1  # increment the image number for each iteration

        # Respect rate limit
        time.sleep(1)  # Adjust this based on your specific rate limit

    print(f"Processed {text_file}")
