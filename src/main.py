from src.file_manager import build_public_dir
from src.generator import generate_page


def main() -> None:
    build_public_dir()
    generate_page("/content/index.md", "/template.html", "/public/index.html")


main()
