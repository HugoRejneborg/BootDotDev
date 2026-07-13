import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))
        valid_target_file = os.path.commonpath([working_dir_path, target_file_path]) == working_dir_path

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_file_path]
            if args:
                command.extend(args)

            completed_process = subprocess.run(
                command,
                cwd=working_dir_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            output = []
            if completed_process.stdout:
                output.append(f"STDOUT:\n{completed_process.stdout}")
            if completed_process.stderr:
                output.append(f"STDERR:\n{completed_process.stderr}")
            if completed_process.returncode != 0:
                output.append(f"Process exited with code {completed_process.returncode}")

            if not output:
                return "No output produced"
            return "\n".join(output)

    except Exception as e:
            return f"Error: executing Python file: {e}"
