import os
import shutil
from gencontent import generate_page
from copystatic import copy_files_recursive

def main():
    dest_dir = "./public"
    source_dir = "./static"
    content_path = "./content/index.md"
    template_path = "./template.html"
    output_path = "./public/index.html"

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    copy_files_recursive(source_dir, dest_dir)
    
    # Generate the index page
    generate_page(content_path, template_path, output_path)

if __name__ == "__main__":
    main()
