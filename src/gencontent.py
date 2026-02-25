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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Iterate over all files and directories in the content path
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            # Only process markdown files
            if filename.endswith(".md"):
                # Change extension from .md to .html
                new_filename = filename.replace(".md", ".html")
                dest_html_path = os.path.join(dest_dir_path, new_filename)
                
                # Call your existing generate_page function
                generate_page(from_path, template_path, dest_html_path)
        else:
            # If it's a directory, recurse into it
            generate_pages_recursive(from_path, template_path, dest_path)

