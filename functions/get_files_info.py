import os

def get_files_info(working_directory, directory="."):
    # gives us the target path by combining working and the relative directry
    full_tar_path = os.path.join(working_directory, directory)
    
    # bot 5 lines are used to check if the abs_target is inside the abs_working dir.
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(full_tar_path)
    prefix = abs_working if abs_working.endswith(os.sep) else abs_working + os.sep
    if not (abs_target == abs_working or abs_target.startswith(prefix)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # checks to see if the provided directory is indeed a directory
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'
    
    # prints out the formatted text
    try:
        entries = os.listdir(abs_target)
        lines = []
        for entry in entries:
            entry_path = os.path.join(abs_target, entry)
            size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            lines.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"
    