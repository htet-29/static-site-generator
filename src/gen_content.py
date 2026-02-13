import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def extract_title(markdown: str):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise ValueError("no title found")


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)
    for filename in files:
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if not os.path.isfile(from_path):
            generate_page_recursive(from_path, template_path, dest_path, basepath)
        else:
            generate_page(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = Path(from_path)
    md_content = from_file.read_text()

    template_file = Path(template_path)
    template = template_file.read_text()

    html = markdown_to_html_node(md_content).to_html()

    title = extract_title(md_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)

    dest_path = Path(dest_dir_path)
    dest_path.mkdir(parents=True, exist_ok=True)

    write_file = Path(os.path.join(dest_path, "index.html"))
    write_file.write_text(template)
