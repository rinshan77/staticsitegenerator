# src/main.py
import sys

from copy_static import copy_directory
from generate_page import generate_pages_recursive 

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    out_dir = "docs"

    copy_directory("static", out_dir)
    generate_pages_recursive("content", "template.html", out_dir, "/staticsitegenerator/")

if __name__ == "__main__":
    main()
