import os
import subprocess

def run_python_file(working_directory, file_path):
    original_file_path=file_path
    working_directory = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not file_path.startswith(working_directory):
        return f'Error: Cannot execute "{original_file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path):
        return f'Error: File "{original_file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{original_file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(["python3", file_path], timeout=30,cwd=working_directory, capture_output=True, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    output = ""
    if not ((completed_process.stderr.strip()) or (completed_process.stdout.strip())):
        return "No output produced."
    output+=f"STDOUT: {completed_process.stdout}\n"
    output+=f"STDERR: {completed_process.stderr}\n"

    if completed_process.returncode != 0:
        output += f" Process exited with code {completed_process.returncode}"
    return output
