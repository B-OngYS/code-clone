import os

def write_file(working_directory, file_path, content):
    original_file_path = file_path
    working_directory = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory,file_path))
    if not file_path.startswith(working_directory):
        return f'Error: Cannot write "{original_file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    except Exception as e:
        return f"Error: Cannot make directories with error: {e}"
    try:
        with open(file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: Cannot write to file with error: {e}"
    return f'Successfully wrote to "{original_file_path}" ({len(content)} characters written)'
