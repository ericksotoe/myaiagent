import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    # gives us the target path by combining working directory and the file_path
    full_tar_path = os.path.join(working_directory, file_path)

    # bot 5 lines are used to check if the abs_target is inside the abs_working file path.
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(full_tar_path)
    prefix = abs_working if abs_working.endswith(os.sep) else abs_working + os.sep
    if not (abs_target == abs_working or abs_target.startswith(prefix)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    try:
        # checks to see if the provided file path exists if not create it and write to it
        if not os.path.exists(abs_target):
            return f'Error: File "{file_path}" not found.'

        # checks to see if the file is an executable python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # provided file path exists and isnt a dir, overwrite it
        else:
            result = subprocess.run(
                ["python3", abs_target, *args],
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            )
            # formatting depending on the returned object
            output = []
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")

            if result.returncode != 0:
                output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs Python files with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file path, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of CLI args to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
