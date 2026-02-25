import os
import shutil

def copy_files_recursive(source_node, dest_node):
    if not os.path.exists(dest_node):
        os.mkdir(dest_node)

    for filename in os.listdir(source_node):
        from_path = os.path.join(source_node, filename)
        dest_path = os.path.join(dest_node, filename)
        print(f" * {from_path} -> {dest_path}")
        
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)