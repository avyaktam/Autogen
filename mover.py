import os
import shutil

# Define the source and target directories
src_dir = r"C:\Users\teo_t\Desktop\Autogen\Processed"
img_target_dir = r"C:\Users\teo_t\Desktop\Autogen\Images"
text_target_dir = r"C:\Users\teo_t\Desktop\Autogen\Texts"

# List all files in the source directory
files = os.listdir(src_dir)

# Iterate over all files
for file_name in files:
    # Construct the full file path
    file_path = os.path.join(src_dir, file_name)

    # Check if the file is a PNG image
    if file_name.endswith('.png'):
        # Move the file to the image target directory
        shutil.move(file_path, img_target_dir)
    else:
        # Move the file to the text target directory
        shutil.move(file_path, text_target_dir)
