import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    # gives us the target path by combining working and the file_path
    full_tar_path = os.path.join(working_directory, file_path)
    
    # bot 5 lines are used to check if the abs_target is inside the abs_working file path.
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(full_tar_path)
    prefix = abs_working if abs_working.endswith(os.sep) else abs_working + os.sep
    if not (abs_target == abs_working or abs_target.startswith(prefix)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # checks to see if the provided directory is indeed a file
    if not os.path.isfile(abs_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # prints out the formatted text
    try:
        with open(abs_target, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(abs_target) > MAX_CHARS:
                file_content_string = file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'

            return file_content_string

    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="reads the content of the specified file up to a certain number of characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that we want to read, relative to the working directory.",
            ),
        },
    ),
)