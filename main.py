import os
import subprocess


def install_nbconvert():
    # Check if pip is installed
    try:
        subprocess.run(["pip", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("pip is not installed. Cannot proceed with installing nbconvert.")
        return False

    answer = input("jupyter nbconvert is not installed. Do you want to install it now? (yes/no) ").strip().lower()
    if answer == "yes":
        try:
            subprocess.run(["pip", "install", "nbconvert"], check=True)
            print("jupyter nbconvert installed successfully!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error installing jupyter nbconvert.")
            return False
    else:
        return False


def is_nbconvert_installed():
    try:
        subprocess.run(["jupyter", "nbconvert", "--version"], check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_notebooks_to_html_batch(root_dir="."):
    for root, _, files in os.walk(root_dir):
        for file in files:
            # Check if the file is a notebook
            if file.endswith(".ipynb"):
                full_path = os.path.join(root, file)
                output_file = os.path.join(root, file.replace(".ipynb", ".html"))

                # Check if the output file already exists
                if os.path.exists(output_file):
                    answer = input(
                        f"Output file {output_file} already exists. Do you want to overwrite it? (yes/no) ").strip().lower()
                    if answer != "yes":
                        print(f"Skipping {full_path}.")
                        continue

                print(f"Converting: {full_path}")
                cmd = [
                    "jupyter",
                    "nbconvert",
                    "--to", "html",
                    "--TemplateExporter.exclude_input=True",
                    full_path
                ]

                try:
                    subprocess.run(cmd, check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print(f"Error converting {full_path}. Moving on to next notebook.")


def get_directory_from_user():
    # Get directory path from user
    dir_input = input("Enter the directory path (or press Enter to use the current directory): ").strip()

    # If the user did not enter anything, use the current directory
    if not dir_input:
        return "."

    # Check if the path is valid
    if not os.path.exists(dir_input) or not os.path.isdir(dir_input):
        print(f"Error: The path '{dir_input}' is not a valid directory.")
        return None

    return dir_input


# Main script
if __name__ == "__main__":
    if not is_nbconvert_installed():
        if not install_nbconvert():
            print("Exiting script as jupyter nbconvert is not available.")
            exit()

    directory = get_directory_from_user()
    if directory:
        convert_notebooks_to_html_batch(directory)
    else:
        print("Operation aborted due to invalid directory.")

