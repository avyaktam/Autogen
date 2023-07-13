import openai
import os
import random
from storyobjects import story_objects
import re

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define a function to generate a story given a prompt
def generate_story(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",  # Use the most cost-effective GPT-3.5-turbo model
      messages=[
            {"role": "system", "content": "You are a narrator specializing in crafting short, concise, engaging texts. Your text needs to start with a title. The text needs to be about 100 words long."},
            {"role": "user", "content": prompt}
        ],
      temperature=0.6,  # Adjust this to change the randomness of the output
      max_tokens=800,    # Adjust this based on how long you want your story to be
      stop=["The End"]  # Stop generating further tokens when "The End" is generated
    )
    return response.choices[0].message['content'].strip()

# List of object names
object_names = story_objects

# Select a random object name from the list
object_name = random.choice(object_names)

# Create the prompt
story_prompt = f"Write a short informative text about {object_name}."

# Generate a story
story = generate_story(story_prompt)
print(story)


def create_paragraphs(text, min_length=150):
    """
    Split text into paragraphs that are not shorter than min_length
    """
    sentences = re.split('(?<=[.!?]) +', text)
    paragraphs = []
    current_paragraph = ""
    for sentence in sentences:
        if len(current_paragraph + sentence) > min_length:
            paragraphs.append(current_paragraph.strip())
            current_paragraph = sentence
        else:
            current_paragraph += " " + sentence
    # Add the last paragraph if it's not empty
    if current_paragraph:
        paragraphs.append(current_paragraph.strip())
    return paragraphs

# Assuming `story` is your generated story
# Split the story into paragraphs
paragraphs = story.split("\n\n")

# Extract title and remove it from paragraphs
title = paragraphs.pop(0)

# Process each paragraph to create chunks that are not too short or too long
chunks = [title]  # Start with title
for paragraph in paragraphs:
    chunks.extend(create_paragraphs(paragraph))

# Your directory path
directory = "C:\\Users\\teo_t\\Desktop\\Autogen\\Texts"

# Generate a filename from the title
# Replace spaces with underscores and remove any non-alphanumeric characters
filename = re.sub(r'\W+', '', title.replace(' ', '_')) + '.txt'

# Combine directory path and filename
filename = os.path.join(directory, filename)

# Open a text file in write mode
with open(filename, 'w') as f:
    # For each chunk in the list of chunks
    for chunk in chunks:
        # Write the chunk to the file
        f.write(chunk + '\n\n')  # Added '\n\n' to separate chunks by a blank line

# Open the file in read mode, read the content
with open(filename, 'r') as f:
    content = f.read()

# Replace consecutive newlines with a single newline
content = re.sub('\n{3,}', '\n\n', content)

# Open the file in write mode, write the modified content back
with open(filename, 'w') as f:
    f.write(content)
