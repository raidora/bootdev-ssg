import os

from src.file_manager import build_public_dir, find_root_dir_r
from src.generator import generate_pages_recursive


def main() -> None:
    root_dir = find_root_dir_r(os.path.dirname(os.path.realpath(__file__)))
    build_public_dir()
    generate_pages_recursive(root_dir+"/content", root_dir+"/template.html", root_dir+"/public")


main()
