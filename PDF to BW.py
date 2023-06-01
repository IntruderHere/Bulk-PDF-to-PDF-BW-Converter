import os
from pdf2image import convert_from_path

def convert_to_bw(pdf_path, output_path):
    images = convert_from_path(pdf_path)

    # Create an empty list to store the black and white images
    bw_images = []

    for image in images:
        # Convert the image to black and white
        bw_image = image.convert('L')
        bw_images.append(bw_image)

    # Create the directory for the output file if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the black and white images to a PDF file
    bw_images[0].save(output_path, save_all=True, append_images=bw_images[1:], optimize=True)

def process_file(input_path, output_path):
    try:
        # Convert the file to black and white
        convert_to_bw(input_path, output_path)
        print(f'Converted file: {input_path}')
        return True
    except Exception as e:
        print(f'Error processing file: {input_path}. {str(e)}')
        return False

def process_folder(input_folder, output_folder):
    converted_count = 0  # Counter for the converted files

    # Iterate over all files and subfolders in the input folder
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Determine the input and output file paths
            relative_path = os.path.relpath(os.path.join(root, file), input_folder)
            input_path = os.path.join(input_folder, relative_path)
            output_path = os.path.join(output_folder, relative_path)

            # Process the file
            if process_file(input_path, output_path):
                converted_count += 1

    return converted_count

# Get the absolute path to the current directory where the .py file is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Create the input and output folders in the current directory
input_folder = os.path.join(current_directory, 'input_files')
output_folder = os.path.join(current_directory, 'output_files')

# Create the input folder directory if it doesn't exist
os.makedirs(input_folder, exist_ok=True)

# Call the function to process all files in the folder structure
converted_count = process_folder(input_folder, output_folder)
print(f'Number of converted files: {converted_count}')