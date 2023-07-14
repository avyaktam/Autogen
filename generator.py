#generator.py
import subprocess
import time
import os

# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Relative paths to your scripts
scripts = [
    os.path.join(current_dir, "TextGenerate.py"),
    os.path.join(current_dir, "audiogenerate.py"),
    os.path.join(current_dir, "imagegenerate.py"),
    os.path.join(current_dir, "moviegenerate.py")
]

# Set the number of loops
loops = 1

# Function to execute a single script
def execute_script(script_path):
    process = subprocess.Popen(["python", "-u", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:  # If the script ended in error
        print(f"Error executing {script_path}: \n{stderr.decode('utf-8')}")
    else:  # If the script executed successfully
        print(f"Finished executing {script_path} successfully")

    try:
        print(f"Output of {script_path}: \n{stdout.decode('utf-8')}")
    except UnicodeDecodeError:
        print(f"Output of {script_path}: \nDecoding error: output not in UTF-8 format")

# Main execution loop
for i in range(loops):
    for script in scripts:
        execute_script(script)
        time.sleep(1)  # Optional: wait for 1 second between scripts
