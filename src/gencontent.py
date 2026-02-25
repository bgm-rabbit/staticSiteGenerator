import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    # Convert Markdown to HTML string
    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()
    
    # Get the title
    title = extract_title(markdown_content)
    
    # Inject into template
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Ensure destination directory exists
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(full_html)
