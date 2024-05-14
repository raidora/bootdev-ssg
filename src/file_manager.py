import os
import shutil

from src.config import SHOW_DEBUG_INFO


def build_public_dir() -> None:
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    project_root_path = find_root_dir_r(current_file_path)
    static_files_path = os.path.join(project_root_path, 'static')
    public_dir_path = os.path.join(project_root_path, 'public')

    if os.path.exists(public_dir_path):
        if SHOW_DEBUG_INFO:
            print(f"Existing public dir found. Deleting.")
        shutil.rmtree(public_dir_path)

    if not os.path.isdir(static_files_path):
        raise Exception(f"copy_filetree_r requires a directory as root_path. Current argument {static_files_path} is "
                        f"not a directory.")

    copy_filetree_r(static_files_path, public_dir_path)


def find_root_dir_r(current_dir: str) -> str:
    if SHOW_DEBUG_INFO:
        print(f"Looking for project root in: {os.path.realpath(current_dir)}")

    if not os.path.exists(current_dir):
        raise FileNotFoundError(f"{current_dir} is not a valid path.")

    if os.path.isdir(current_dir):
        potential_static = os.path.realpath(os.path.join(current_dir, "static"))
        potential_gitignore = os.path.realpath(os.path.join(current_dir, ".gitignore"))

        if os.path.exists(potential_static) and os.path.exists(potential_gitignore):
            return os.path.realpath(current_dir)

        os_root = os.path.abspath(os.sep)
        if os.path.realpath(current_dir) == os_root:
            raise FileNotFoundError("Project root could not be found.")

    return find_root_dir_r(os.path.join(current_dir, ".."))


def copy_filetree_r(root_path: str, target_path: str, current_relative_path: str = "") -> None:
    root_full = os.path.join(root_path, current_relative_path)
    target_full = os.path.join(target_path, current_relative_path)

    if not os.path.exists(root_full):
        raise FileNotFoundError(f"{root_full} is not a valid path.")

    if os.path.isfile(os.path.join(root_path, current_relative_path)):
        if SHOW_DEBUG_INFO:
            print(f"Copying {root_path}{os.sep}{current_relative_path} to "
                  f"{target_path}{os.sep}{current_relative_path}")
        shutil.copy(root_full, target_full)
        return

    else:
        dir_contents = os.listdir(os.path.join(root_path, current_relative_path))

        if not os.path.exists(target_full) and len(dir_contents) > 0:
            if SHOW_DEBUG_INFO:
                print(f"Creating directory {target_full}")
            os.mkdir(target_full)

        for node in dir_contents:
            copy_filetree_r(root_path, target_path, os.path.join(current_relative_path, node))
