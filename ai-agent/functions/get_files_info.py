import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_dir_path = os.path.normpath(os.path.join(working_dir_path, directory))
        valid_target_dir = os.path.commonpath([working_dir_path, target_dir_path]) == working_dir_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir_path):
            return f'Error: "{directory}" is not a directory'
        else:
            return f'Success: "{directory}" is within the working directory'

    except Exception as e:
            return f'Error: {e}'
        
