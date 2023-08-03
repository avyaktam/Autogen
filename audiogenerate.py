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

# Define a list of voice codes
voices = [
    'en-AU-Neural2-A', 'en-AU-Neural2-B', 'en-AU-Neural2-C', 'en-AU-Neural2-D', 'en-AU-News-E', 
    'en-AU-News-F', 'en-AU-News-G', 'en-AU-Polyglot-1', 'en-AU-Standard-A', 'en-AU-Standard-B', 
    'en-AU-Standard-C', 'en-AU-Standard-D', 'en-AU-Wavenet-A', 'en-AU-Wavenet-B', 'en-AU-Wavenet-C', 
    'en-AU-Wavenet-D', 'en-IN-Standard-A', 'en-IN-Standard-B', 'en-IN-Standard-C', 'en-IN-Standard-D', 
    'en-IN-Wavenet-A', 'en-IN-Wavenet-B', 'en-IN-Wavenet-C', 'en-IN-Wavenet-D', 'en-GB-Neural2-A', 
    'en-GB-Neural2-B', 'en-GB-Neural2-C', 'en-GB-Neural2-D', 'en-GB-Neural2-F', 'en-GB-News-G', 
    'en-GB-News-H', 'en-GB-News-I', 'en-GB-News-J', 'en-GB-News-K', 'en-GB-News-L', 'en-GB-News-M', 
    'en-GB-Standard-A', 'en-GB-Standard-B', 'en-GB-Standard-C', 'en-GB-Standard-D', 'en-GB-Standard-F', 
    'en-GB-Wavenet-A', 'en-GB-Wavenet-B', 'en-GB-Wavenet-C', 'en-GB-Wavenet-D', 'en-GB-Wavenet-F', 
    'en-US-Neural2-A', 'en-US-Neural2-C', 'en-US-Neural2-D', 'en-US-Neural2-E', 'en-US-Neural2-F', 
    'en-US-Neural2-G', 'en-US-Neural2-H', 'en-US-Neural2-I', 'en-US-Neural2-J', 'en-US-News-K', 
    'en-US-News-L', 'en-US-News-M', 'en-US-News-N', 'en-US-Polyglot-1', 'en-US-Standard-A', 
    'en-US-Standard-B', 'en-US-Standard-C', 'en-US-Standard-D', 'en-US-Standard-E', 'en-US-Standard-F', 
    'en-US-Standard-G', 'en-US-Standard-H', 'en-US-Standard-I', 'en-US-Standard-J', 'en-US-Studio-M', 
    'en-US-Studio-O', 'en-US-Wavenet-A', 'en-US-Wavenet-B', 'en-US-Wavenet-C', 'en-US-Wavenet-D', 
    'en-US-Wavenet-E', 'en-US-Wavenet-F', 'en-US-Wavenet-G', 'en-US-Wavenet-H', 'en-US-Wavenet-I', 
    'en-US-Wavenet-J'
]  # Add your voice codes here

# Randomly choose a voice for the voice
voice_choice = random.choice(voices)

# Set the language code and voice name
language = voice_choice.split('-')[0] + '-' + voice_choice.split('-')[1]  # The first two parts of the voice code
voice_name = voice_choice  # The full voice code
print(f"Selected language: {language}, Selected voice: {voice_name}")  # Add this line

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

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=paragraph)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            name=voice_name,
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
