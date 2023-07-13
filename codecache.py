import os
import shutil
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips

# Specify the paths to the parent directories containing the audio and image folders
audio_parent_folder_path = "C:\\Users\\teo_t\\Desktop\\Autogen\\Texts"
image_folder_path = "C:\\Users\\teo_t\\Desktop\\Autogen\\Images"
output_video_folder = "C:\\Users\\teo_t\\Desktop\\Autogen\\Videos"
processed_dir = "C:\\Users\\teo_t\\Desktop\\Autogen\\Processed"

# Get a list of all the directories within the audio parent folder
audio_folders = [f for f in os.listdir(audio_parent_folder_path) if os.path.isdir(os.path.join(audio_parent_folder_path, f))]

# Process each audio directory
for audio_folder in audio_folders:
    audio_folder_path = os.path.join(audio_parent_folder_path, audio_folder)

    # Get a list of all audio files in the directory
    audio_files = [f for f in os.listdir(audio_folder_path) if f.endswith('.mp3')]

    # Prepare a list to store individual clips
    clips = []

    # Process each audio file
    for audio_file in sorted(audio_files):
        # Construct the full paths to the audio file and corresponding image
        audio_file_path = os.path.join(audio_folder_path, audio_file)
        image_file_name = audio_file.replace('1_', '', 1).replace('paragraph', 'image').replace('.mp3', '.png')
        image_file_path = os.path.join(image_folder_path, image_file_name)

        print(f"Processing {audio_file}")
        print(f"Image Path: {image_file_path}")
        print(f"Audio Path: {audio_file_path}")

        # Check if both files exist
        if not os.path.isfile(image_file_path) or not os.path.isfile(audio_file_path):
            print(f"Files do not exist for {audio_file}")
            continue

        # Load audio file and get its duration
        audio = AudioFileClip(audio_file_path)
        audio_duration = audio.duration

        # Create a movie clip
        clip = ImageSequenceClip([image_file_path], durations=[audio_duration]) # duration is set to audio duration
        clip.fps = 24  # define the fps for the clip
        clip.audio = audio # set the audio for the clip

        # Append the clip to the list of clips
        clips.append(clip)

        print(f"Processed {audio_file}")

    # Concatenate all clips into a single video
    final_clip = concatenate_videoclips(clips)

    # Extract the story name from the first audio file and format it
    story_name = "_".join(audio_files[0].split('_')[1:-1])  # assumes file names are like "1_The_Forgotten_Treasure_Map_paragraph1.mp3"

    # Save the final video to a file
    final_output_path = os.path.join(output_video_folder, f"{story_name}.mp4")
    final_clip.write_videofile(final_output_path)

    # Move processed audio and image folders and text
    shutil.move(audio_folder_path, os.path.join(processed_dir, audio_folder))
    text_file_name = f"{audio_folder}.txt"
    text_file_path = os.path.join(audio_parent_folder_path, f"{audio_folder}.txt")
    if os.path.isfile(text_file_path):
        shutil.move(text_file_path, processed_dir)

    print(f"Completed processing for {audio_folder}")
