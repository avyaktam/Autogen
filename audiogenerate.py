import os
from gtts import gTTS

# Specify the path to the directory containing the text files
dir_path = "C:\\Users\\teo_t\\Desktop\\Autogen\\Texts"

# Get a list of all text files in the directory
text_files = [f for f in os.listdir(dir_path) if f.endswith('.txt')]

# Process each text file
for i, text_file in enumerate(text_files, start=1):
    # Construct the full path to the text file
    text_file_path = os.path.join(dir_path, text_file)

    # Read the content of the text file
    with open(text_file_path, 'r') as file:
        text = file.read()

    # Split the text into paragraphs
    paragraphs = text.split("\n\n")

    # Create a directory to store the audio files for this text file
    directory_name = f"{i}_{text_file.replace('.txt', '').replace(' ', '_')}"
    directory_path = os.path.join(dir_path, directory_name)
    os.makedirs(directory_path, exist_ok=True)

    # Process each paragraph
    for j, paragraph in enumerate(paragraphs, start=1):
        # Ignore empty paragraphs
        if not paragraph.strip():
            continue

        # Generate speech
        tts = gTTS(text=paragraph, lang='en', tld='ca')

        # Save the speech audio into a file
        audio_file_path = os.path.join(directory_path, f"{i}_{text_file.replace('.txt', '')}_paragraph_{j}.mp3")
        tts.save(audio_file_path)

    print(f"Processed {text_file}")
