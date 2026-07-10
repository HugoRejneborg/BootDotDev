import os
from config import MAX_READ_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))
        valid_target_file = os.path.commonpath([working_dir_path, target_file_path]) == working_dir_path

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_file_path, 'r') as file:
                content = file.read(MAX_READ_CHARS)
                if file.read(1):
                     content += f'[...File "{file_path}" truncated at {MAX_READ_CHARS} characters]'
            return content

    except Exception as e:
            return f'Error: {e}'
