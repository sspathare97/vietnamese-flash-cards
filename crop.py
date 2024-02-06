import os
import subprocess

# Directory path
directory = 'cards'

rows_per_page = 5
width = 1240
height = 701

# List to store PDF filenames
pdf_files = []

# Iterate over the files in the directory
for filename in os.listdir(directory):
    # Check if the file ends with ".pdf"
    if filename.endswith('.pdf'):
        # Add PDF filename to the list
        pdf_files.append(filename)

# Sort the list of PDF filenames
pdf_files.sort()

# Iterate over sorted PDF filenames and print them
for filename in pdf_files:
    lesson = filename[:-4]
    
    lesson_directory = os.path.join(directory, 'images')
    # lesson_directory = os.path.join(directory, lesson)
    
    if not os.path.exists(lesson_directory):
        # Create the directory
        os.makedirs(lesson_directory)
    
    input_filepath = os.path.join(directory, filename)

    # Define the command to run for each PDF file
    pages_command = "pdfinfo " + input_filepath + " | awk '/^Pages:/ {print $2}'"
    
    # Run the command using subprocess
    result = subprocess.run(pages_command, shell=True, capture_output=True, text=True)
    
    # Check if the command was successful (return code 0)
    if result.returncode != 0:
        # Print an error message if the command failed
        print(f"Error running command for {filename}")
        print(result.stderr)
    else:
        # Convert the output to a number
        pages_count = int(result.stdout.strip())
        
        # Use the output_number as needed
        print(f"Pages for {filename}: {pages_count}")

        card_index = 1
        
        for page in range(1, pages_count + 1):

            for row in range(1, rows_per_page + 1):
                y_offset = (row - 1) * height

                output_filename = f'Vietnamese-L{lesson}-C{card_index:02d}'
                output_filepath = os.path.join(lesson_directory, output_filename)

                print(f"lesson: {lesson}, card: {card_index:02d}")

                # front
                crop_command = f'pdftoppm {input_filepath} {output_filepath}-Front -png -f {page} -singlefile -r 300 -x 0 -y {y_offset} -W {width} -H {height}'
                subprocess.run(crop_command, shell=True)

                # back
                crop_command = f'pdftoppm {input_filepath} {output_filepath}-Back -png -f {page} -singlefile -r 300 -x {width} -y {y_offset} -W {width} -H {height}'
                subprocess.run(crop_command, shell=True)

                card_index += 1
