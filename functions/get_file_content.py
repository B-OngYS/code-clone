import os

def get_file_content(working_directory, file_path):
    original_file_path = file_path
    working_directory = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory,file_path))
    if not file_path.startswith(working_directory):
        return f'Error: Cannot read "{original_file_path}" as it is outside the permitted working directory'
    if not os.path.commonpath([working_directory, file_path])==working_directory:
        return f'Error: Cannot read "{original_file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{original_file_path}"'
    MAX_CHARS = 10_000
    try:
        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS+1)
    except Exception as e:
        return f"Error: File cannot be read with error: {e}"
    truc_msg = f'[...File "{original_file_path}" truncated at 10000 characters]'
    if len(file_content_string)>MAX_CHARS:
        return file_content_string[:MAX_CHARS]+truc_msg
    return file_content_string
