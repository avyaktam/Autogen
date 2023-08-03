# moviegenerate.py
import os
import shutil
import textwrap
import random
from moviepy.config import change_settings
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.fx.resize import resize
from moviepy.video.VideoClip import ColorClip
from moviepy.video.fx.all import crop
from natsort import natsorted

change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

project_folder = os.path.dirname(os.path.abspath(__file__))
audio_parent_folder_path = os.path.join(project_folder, "Texts")
image_folder_path = os.path.join(project_folder, "Images")
output_video_folder = os.path.join(project_folder, "Videos")
processed_dir = os.path.join(project_folder, "Processed")
audio_tracks_folder_path = os.path.join(project_folder, "audiotracks")

audio_folders = [f for f in os.listdir(audio_parent_folder_path) if os.path.isdir(os.path.join(audio_parent_folder_path, f))]

audio_tracks = [f for f in os.listdir(audio_tracks_folder_path) if f.endswith('.mp3')]

for audio_folder in audio_folders:
    audio_folder_path = os.path.join(audio_parent_folder_path, audio_folder)
    audio_files = natsorted([f for f in os.listdir(audio_folder_path) if f.endswith('.mp3')])

    clips = []

    text_file_name = f"{audio_folder.replace('1_', '')}.txt"
    text_file_path = os.path.join(audio_parent_folder_path, text_file_name)

    with open(text_file_path, 'r') as file:
        text = file.read()

    paragraphs = text.split("\n\n")

    fps = 24
    video_width = 1080 # 1080p vertical video
    video_height = 1920 # 1080p vertical video
    image_max_height = int(video_height * 2 / 3)

    for idx, audio_file in enumerate(audio_files):
        audio_file_path = os.path.join(audio_folder_path, audio_file)
        image_file_name = audio_file.replace('1_', '', 1).replace('paragraph', 'image').replace('.mp3', '.png')
        image_file_path = os.path.join(image_folder_path, image_file_name)

        print(f"Processing {audio_file}")
        print(f"Image Path: {image_file_path}")
        print(f"Audio Path: {audio_file_path}")

        if not os.path.isfile(image_file_path) or not os.path.isfile(audio_file_path):
            print(f"Files do not exist for {audio_file}")
            continue

        audio = AudioFileClip(audio_file_path)
        audio_duration = audio.duration

        images = [image_file_path for _ in range(int(audio_duration*fps))]
        durations = [1/fps for _ in range(int(audio_duration*fps))]

        image_clip = ImageSequenceClip(images, durations=durations)
        zoom_factor = 1.1  # Adjust this value as needed
        zoomed_width = int(video_width * zoom_factor)
        zoomed_height = int(video_height * zoom_factor)
        image_clip = image_clip.resize(height=zoomed_height) # zoom in
        image_clip = image_clip.fx(crop, x_center=zoomed_width/2, y_center=zoomed_height/2, width=video_width, height=video_height)  # center crop back to original size

        image_clip = image_clip.set_position(('center', 'center')) # center the image
        image_clip.fps = fps
        image_clip.audio = audio

        fontsize = 50


        def text_position(t):
            return ('center', video_height * 1 / 2 + fontsize - 0) # place text just below the image with an offset of -200 pixels
        if idx < len(paragraphs):
            wrapped_text = '\n'.join(textwrap.wrap(paragraphs[idx], width=50))

            print(f"Index: {idx}, Wrapped text: {wrapped_text}")

            if wrapped_text.strip() == "":
                print("The wrapped text is empty. Skipping this iteration.")
                continue

            text = TextClip(wrapped_text, fontsize=fontsize, color='red', stroke_color='black', stroke_width=2, size=(video_width, None))
            text = text.set_duration(audio_duration).set_position(text_position).margin(left=int(video_width*0.05), right=int(video_width*0.05)) # add left and right margin

        background = ColorClip((video_width, video_height), col=[0,0,0]).set_duration(audio_duration)
        clip = CompositeVideoClip([background, image_clip, text.set_start(0).crossfadein(0.5).set_position(text_position).set_duration(audio_duration)])

        clips.append(clip)

        print(f"Processed {audio_file}")

    final_clip = concatenate_videoclips(clips)

    random_audio_track_file_path = os.path.join(audio_tracks_folder_path, random.choice(audio_tracks))

    backtrack = AudioFileClip(random_audio_track_file_path)

    if backtrack.duration < final_clip.duration:
        backtrack = backtrack.fx(vfx.loop, duration=final_clip.duration)

    backtrack = backtrack.subclip(0, final_clip.duration)

    backtrack = backtrack.volumex(0.3)

    final_clip.audio = CompositeAudioClip([final_clip.audio, backtrack])

    final_output_path = os.path.join(output_video_folder, f"{audio_folder}.mp4")
    final_clip.write_videofile(final_output_path, fps=fps, codec='libx264')

    image_files = [f for f in os.listdir(image_folder_path) if f.startswith(audio_folder.replace('1_', '', 1))]
    for image_file in image_files:
        shutil.move(os.path.join(image_folder_path, image_file), processed_dir)

    shutil.move(audio_folder_path, os.path.join(processed_dir, audio_folder))
    shutil.move(text_file_path, processed_dir)

    print("Video creation completed!")
