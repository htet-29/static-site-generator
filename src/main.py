import os
import sys
import shutil
from blocknode import markdown_to_html_node
from pathlib import Path


def copy_static_files(src_path, dest_path: str):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    recursively_copy_files(src_path, dest_path)


def recursively_copy_files(src_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    if not os.path.exists(src_path):
        raise ValueError("there is no source directory")
    files = os.listdir(src_path)
    for file in files:
        file_path = os.path.join(src_path, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest_path)
        else:
            new_dst_path = os.path.join(dest_path, file)
            recursively_copy_files(file_path, new_dst_path)


def extract_title(markdown: str):
    lines = markdown.split("\n\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise Exception("There is no title text")


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    dest_path = Path(dest_dir_path)
    dest_path.mkdir(parents=True, exist_ok=True)
    dirs = os.listdir(dir_path_content)
    for dir in dirs:
        content_path = os.path.join(dir_path_content, dir)
        if not os.path.isfile(content_path):
            new_dest_path = os.path.join(dest_dir_path, dir)
            generate_page_recursive(
                content_path, template_path, new_dest_path, base_path
            )
        else:
            content_file = Path(content_path)
            md_content = content_file.read_text()
            template_file = Path(template_path)
            template_content = template_file.read_text()
            html_content = markdown_to_html_node(md_content).to_html()
            title = extract_title(md_content)
            template_content = template_content.replace("{{ Title }}", title)
            template_content = template_content.replace("{{ Content }}", html_content)
            template_content = template_content.replace('href="/', f'href="{base_path}')
            template_content = template_content.replace('src="/', f'src="{base_path}')
            write_file = Path(os.path.join(dest_path, "index.html"))
            write_file.write_text(template_content)


def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    copy_static_files("static", "docs")
    generate_page_recursive("content", "template.html", "docs", base_path)


main()
