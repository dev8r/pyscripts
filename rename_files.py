import os
import re

def rename_files(root_dir, old_text, new_text):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if old_text in filename:
                old_path = os.path.join(dirpath, filename)
                new_filename = filename.replace(old_text, new_text)
                new_path = os.path.join(dirpath, new_filename)
                os.rename(old_path, new_path)
                print(f'Renamed: {old_path} -> {new_path}')

def rename_files_rx(root_dir, pattern):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            old_text = filename
            new_text = clean_string(old_text, pattern)
            old_path = os.path.join(dirpath, filename)
            new_filename = filename.replace(old_text, new_text)
            new_path = os.path.join(dirpath, new_filename)
            os.rename(old_path, new_path)
            print(f'Renamed: {old_path} -> {new_path}')

def clean_string(old_string, pattern):
    """
    Removes the part of old_string that matches the given regex pattern.
    
    Parameters:
        old_string (str): The original string.
        pattern (str): The regex pattern to remove.
    
    Returns:
        str: The cleaned string.
    """
    return re.sub(pattern, "", old_string).strip()

# Example usage:
# Replace 'oldpart' with 'newpart' in all filenames under '/path/to/directory'

rename_files('C:\\repos\database\\Release Scripts\\some_dir', 'Abc123-', '')
