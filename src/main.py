import sys
from copy_static import copy_static_files
from gen_content import generate_page_recursive


def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    copy_static_files("static", "docs")
    generate_page_recursive("content", "template.html", "docs", base_path)


main()
