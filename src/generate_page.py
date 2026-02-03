import os

from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("##"):
            title = stripped[2:].strip()
            if title:
                return title
            break
    raise Exception("No h1 header found")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", content_html
    )

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    """
    Walk dir_path_content recursively.
    For each .md file, generate a matching .html file under dest_dir_path,
    preserving the directory structure.
    """
    # Ensure destination root exists
    os.makedirs(dest_dir_path, exist_ok=True)

    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)

        # If it's a directory, recurse into it
        if os.path.isdir(src_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(src_path, template_path, new_dest_dir)
            continue

        # If it's a markdown file, generate html
        if os.path.isfile(src_path) and entry.endswith(".md"):
            filename_no_ext = entry[:-3]  # remove ".md"
            dest_path = os.path.join(dest_dir_path, f"{filename_no_ext}.html")
            generate_page(src_path, template_path, dest_path)
