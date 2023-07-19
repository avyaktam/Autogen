#moviegenerate.py
import os
import shutil
import textwrap
import random
from moviepy.config import change_settings
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.audio.AudioClip import CompositeAudioClip
from natsort import natsorted

change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

# Specify the relative paths to the parent directories
project_folder = os.path.dirname(os.path.abspath(__file__))
audio_parent_folder_path = os.path.join(project_folder, "Texts")
image_folder_path = os.path.join(project_folder, "Images")
output_video_folder = os.path.join(project_folder, "Videos")
processed_dir = os.path.join(project_folder, "Processed")
audio_tracks_folder_path = os.path.join(project_folder, "audiotracks")

# Get a list of all the directories within the audio parent folder
audio_folders = [f for f in os.listdir(audio_parent_folder_path) if os.path.isdir(os.path.join(audio_parent_folder_path, f))]

# Get a list of all audio tracks in the directory
audio_tracks = [f for f in os.listdir(audio_tracks_folder_path) if f.endswith('.mp3')]

# Process each audio directory
for audio_folder in audio_folders:
    audio_folder_path = os.path.join(audio_parent_folder_path, audio_folder)

    # Get a list of all audio files in the directory
    audio_files = natsorted([f for f in os.listdir(audio_folder_path) if f.endswith('.mp3')])

    # Prepare a list to store individual clips
    clips = []

    # Load the text file and split it into paragraphs
    text_file_name = f"{audio_folder.replace('1_', '')}.txt"  # Adjusted to remove '1_' prefix
    text_file_path = os.path.join(audio_parent_folder_path, text_file_name)

    with open(text_file_path, 'r') as file:
        text = file.read()

    paragraphs = text.split("\n\n")

    # Define fps
    fps = 24

    # Process each audio file
    for idx, audio_file in enumerate(audio_files):
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
    
        # Create a list of images and a corresponding duration list
        images = [image_file_path for _ in range(int(audio_duration*fps))]
        durations = [1/fps for _ in range(int(audio_duration*fps))]
    
        # Create a movie clip
        clip = ImageSequenceClip(images, durations=durations)  # duration is set to audio duration
        clip.fps = fps  # define the fps for the clip
        clip.audio = audio  # set the audio for the clip
    
        # Specify a smaller font size if necessary
        fontsize = 38
    
        # Define text position (e.g., center the text both horizontally and vertically)
        text_position = ('center', 'bottom')
    
        # Create a text clip for each paragraph and overlay it on the movie clip
        if idx < len(paragraphs):
            # Use textwrap to split long text into multiple lines
            wrapped_text = '\n'.join(textwrap.wrap(paragraphs[idx], width=50))  # Adjust width as necessary
    
            # Add a print statement to print the wrapped_text and idx
            print(f"Index: {idx}, Wrapped text: {wrapped_text}")
    
            # If the wrapped text is empty, print a message and continue with the next iteration
            if wrapped_text.strip() == "":
                print("The wrapped text is empty. Skipping this iteration.")
                continue
            
            text = TextClip(wrapped_text, fontsize=fontsize, color='red')  # adjust properties as needed
            text = text.set_duration(audio_duration).set_pos(text_position)
            clip = CompositeVideoClip([clip, text.set_start(0).crossfadein(0.5).set_duration(clip.duration)])
    
        # Append the clip to the list of clips
        clips.append(clip)
    
        print(f"Processed {audio_file}")


    # Concatenate all clips into a single video
    final_clip = concatenate_videoclips(clips)

    # Select a random audio track
    random_audio_track_file_path = os.path.join(audio_tracks_folder_path, random.choice(audio_tracks))
    
    # Load the audio track
    backtrack = AudioFileClip(random_audio_track_file_path)
    
    # Loop the backtrack to match the duration of the video
    if backtrack.duration < final_clip.duration:
        backtrack = backtrack.fx(vfx.loop, duration=final_clip.duration)
    
    # Now cut the backtrack to match the exact duration of the video
    backtrack = backtrack.subclip(0, final_clip.duration)
    
    # Lower the volume of the backtrack
    backtrack = backtrack.volumex(0.4)
    
    # Set the audio of the final clip
    final_clip.audio = CompositeAudioClip([final_clip.audio, backtrack])

    # Save the final clip
    final_output_path = os.path.join(output_video_folder, f"{audio_folder}.mp4")
    final_clip.write_videofile(final_output_path, fps=fps, codec='libx264')

    # Now, move the processed image files to the processed directory
    image_files = [f for f in os.listdir(image_folder_path) if f.startswith(audio_folder.replace('1_', '', 1))]
    for image_file in image_files:
        shutil.move(os.path.join(image_folder_path, image_file), processed_dir)

    # Move processed audio and image folders and text
    shutil.move(audio_folder_path, os.path.join(processed_dir, audio_folder))
    shutil.move(text_file_path, processed_dir)

    print("Video creation completed!")