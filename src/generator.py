import os

from src.block_conversions import markdown_to_html_node
from src.file_manager import read_project_file, write_project_file, find_root_dir_r


def extract_title(markdown):
    title = ""

    for line in markdown.split("\n\n"):
        if line.startswith("# "):
            title = line.lstrip("#").strip()
            break

    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        md = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_files = os.listdir(dir_path_content)

    for f in content_files:
        realpath = os.path.join(dir_path_content, f)
        if os.path.isdir(realpath):
            generate_pages_recursive(dir_path_content+"/"+f, template_path, dest_dir_path+"/"+f)
        else:
            generate_page(dir_path_content+"/"+f, template_path, dest_dir_path+"/"+f.replace(".md", ".html"))
