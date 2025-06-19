import os
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types
import function_schemas
from functions import get_file_content, get_files_info, write_file, run_python

client = genai.Client(api_key=api_key)

function_maps = {
        function_schemas.schema_write_file.name: write_file.write_file,
        function_schemas.schema_get_file_content.name: get_file_content.get_file_content,
        function_schemas.schema_run_python_file.name: run_python.run_python_file,
        function_schemas.schema_get_files_info.name: get_files_info.get_files_info
        }


def call_function(function_call_part, verbose=False)-> types.Content:
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    if function_call_part.name not in [function_schemas.schema_get_files_info.name, 
                                       function_schemas.schema_get_file_content.name,
                                       function_schemas.schema_run_python_file.name,
                                       function_schemas.schema_write_file.name]:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
    function_result = function_maps[function_call_part.name](working_directory="./calculator", **function_call_part.args)
    
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result},
        )
    ],
)


def chat_loop(system_prompt, messages:list[str|types.Content|None]|None=None,iteration:int=20, verbose:bool=False):
    available_functions = types.Tool(
    function_declarations=[
        function_schemas.schema_get_files_info,
        function_schemas.schema_get_file_content,
        function_schemas.schema_run_python_file,
        function_schemas.schema_write_file
    ]
)
    if not messages:
        messages = []
    if iteration==0:
        print("Max iteration hit")
        return
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    if response.function_calls:
        for function_call in response.function_calls:
            call_response = call_function(function_call_part=function_call, verbose=verbose)
            messages.append(call_response)
        return chat_loop(system_prompt, messages=messages, iteration=iteration-1,verbose=verbose)
    else:
        print(response.text)
    if response.usage_metadata and verbose:
        print(f"Messages: {messages}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories to search
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    try:
        prompt = sys.argv[1]
        chat_loop(system_prompt, messages=[prompt])
    except IndexError as indexerr:
        print(indexerr)
        exit(code=1)            
    verbose = "--verbose" in sys.argv


if __name__ == "__main__":
    main()
