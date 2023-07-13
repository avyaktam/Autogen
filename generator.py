import subprocess
import time

# Path to your scripts
scripts = [
    "C:/Users/teo_t/Desktop/Autogen/TextGenerate.py",
    "C:/Users/teo_t/Desktop/Autogen/audiogenerate.py",
    "C:/Users/teo_t/Desktop/Autogen/imagegenerate.py",
    "C:/Users/teo_t/Desktop/Autogen/moviegenerate.py"
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
