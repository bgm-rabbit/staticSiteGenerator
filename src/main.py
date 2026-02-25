import os
import shutil
from gencontent import generate_pages_recursive
from copystatic import copy_files_recursive

def main():
    dest_dir = "./public"
    source_dir = "./static"
    content_dir = "./content"
    template_path = "./template.html"

    print("Cleaning public directory...")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    print("Copying static assets...")
    copy_files_recursive(source_dir, dest_dir)
    
    print("Generating pages...")
    # This now handles the entire content tree!
    generate_pages_recursive(content_dir, template_path, dest_dir)

if __name__ == "__main__":
    main()