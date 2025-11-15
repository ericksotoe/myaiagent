import os
from google.genai import types

def write_file(working_directory, file_path, content):
    # gives us the target path by combining working directory and the file_path
    full_tar_path = os.path.join(working_directory, file_path)
    
    # bot 5 lines are used to check if the abs_target is inside the abs_working file path.
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(full_tar_path)
    prefix = abs_working if abs_working.endswith(os.sep) else abs_working + os.sep
    if not (abs_target == abs_working or abs_target.startswith(prefix)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    
    try:
        directory_path = os.path.dirname(abs_target)
        # checks to see if the provided file path exists if not create it and write to it
        if not os.path.exists(abs_target):
            os.makedirs(directory_path, exist_ok=True)
            with open(abs_target, 'w') as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
        # checks if the provided file path is a directory
        if os.path.exists(abs_target) and os.path.isdir(abs_target):
            return f'Error: "{file_path}" is a directory, not a file'
        
        # provided file path exists and isnt a dir, overwrite it
        else:
            with open(abs_target, 'w') as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content to the provided file_path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file's location, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content that will be written to the file path, if there is no file at the destination it will be created else it will overwrite it.",
            ),
        },
    ),
)