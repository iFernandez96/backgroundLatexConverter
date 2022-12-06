import os
import time

# Set the path to the specific file that we want to monitor
file_path = "path/to/specific/file.txt"

# Create an infinite loop that will run until the script is interrupted
while True:
    # Wait until the file is modified
    while True:
        # Check if the modification time of the file is different from its creation time
        # This indicates that the file has been modified since it was last read
        if os.path.getmtime(file_path) != os.path.getctime(file_path):
            # If the file has been modified, break out of the inner loop
            break
        # Sleep for 1 second before checking the file again
        time.sleep(1)

    # Open the file and read its contents
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except IOError:
        # If there is an error reading the file, print an error message and continue
        # to the next iteration of the loop
        print(f"Could not read file {file_path}. Skipping.")
        continue

    # Wrap the file contents in LaTeX boilerplate
    # f-strings are used to insert the contents of the "content" variable into the string
    latex = f"""
    \\documentclass{{article}}
    \\begin{{document}}
    {content}
    \\end{{document}}
    """

    # Save the LaTeX to a file with the same name as the original file but with a .tex extension
    file_name = os.path.splitext(file_path)[0]
    with open(file_name + ".tex", "w") as f:
        f.write(latex)

    # Convert the LaTeX file to a PDF using pdflatex
    try:
        os.system(f"pdflatex {file_name}.tex")
    except OSError:
        # If there is an error running pdflatex, print an error message and continue
        # to the next iteration of the loop
        print(f"Could not run pdflatex on file {file_name}.tex. Skipping.")
        continue

    # Delete the LaTeX file after it has been converted to a PDF
    os.remove(file_name + ".tex")
