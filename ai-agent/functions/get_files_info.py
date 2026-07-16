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
            content = os.listdir(target_dir_path)
            res = ""
            for c in content:
                 size = os.path.getsize(os.path.join(target_dir_path, c))
                 isdir = os.path.isdir(os.path.join(target_dir_path, c))
                 res += f"- {c}: file_size={size} bytes, is_dir={isdir}\n"
                 
            return res.strip()

    except Exception as e:
            return f'Error: {e}'
        
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
