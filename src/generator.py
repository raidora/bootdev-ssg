import os

from src.block_conversions import markdown_to_html_node
from src.file_manager import read_project_file, write_project_file


def extract_title(markdown):
    title = ""

    for line in markdown.split("\n\n"):
        if line.startswith("# "):
            title = line.lstrip("#").strip()
            break

    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md = read_project_file(from_path)

    template = read_project_file(template_path)

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    write_project_file(dest_path, page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    pass