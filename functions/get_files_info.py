import os

def get_files_info(working_directory, directory=None):
    files_info=[]
    if directory:
        working_directory = os.path.abspath(working_directory)
        directory = os.path.abspath(os.path.join(working_directory, directory))
        if not directory.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not (len(directory) == len(working_directory) or 
        directory[len(working_directory)] == '/'):
            return f'Error: Cannot list "{directory} as it is outside the permiteed working directory'
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
        for content in os.listdir(directory):
            if str(content) in ["__pycache__", "venv"]:
                continue
            name = str(content)
            content_path = os.path.join(directory, name)
            size = os.path.getsize(content_path)
            is_dir = os.path.isdir(content_path)
            files_info.append(f"- {name}: file_size:{size} bytes, is_dir={is_dir}")
    return "\n".join(files_info)
