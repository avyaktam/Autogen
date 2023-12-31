import os
import random
from google.cloud import texttospeech

# Set your google cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\teo_t\Desktop\Autogen\hazel-strand-393310-66038e1e9eed.json"

# Instantiate a client
client = texttospeech.TextToSpeechClient()

# Specify the relative path to the directory containing the text files
dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Texts")

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

    # Randomly choose a gender for the voice
    gender = random.choice([
        texttospeech.SsmlVoiceGender.MALE,
        texttospeech.SsmlVoiceGender.FEMALE,
    ])

    # Process each paragraph
    for j, paragraph in enumerate(paragraphs, start=1):
        # Ignore empty paragraphs
        if not paragraph.strip():
            continue

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=paragraph)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-CA",
            ssml_gender=gender,
        )

        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.1,  # Speaking rate set to 1.1
            pitch=0,
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Save the speech audio into a file
        audio_file_path = os.path.join(directory_path, f"{i}_{text_file.replace('.txt', '')}_paragraph_{j}.mp3")
        with open(audio_file_path, "wb") as out:
            out.write(response.audio_content)

    print(f"Processed {text_file}")

