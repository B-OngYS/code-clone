from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself. The default value is '.'",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file up to 10_000 max characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working dirctory",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working dirctory",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative tto the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file"
            ),
        },


    ),
)
