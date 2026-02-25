import unittest
import os
import shutil
import tempfile
from main import copy_files_recursive

class TestCopyStatic(unittest.TestCase):
    def setUp(self):
        # Create a unique temporary directory for this test run
        self.tmp_base = tempfile.mkdtemp()
        self.src = os.path.join(self.tmp_base, "static")
        self.dst = os.path.join(self.tmp_base, "public")
        os.mkdir(self.src)

    def tearDown(self):
        # Clean up the temporary directory after each test
        shutil.rmtree(self.tmp_base)

    def test_copy_recursive_nested(self):
        # Test 1: Deeply nested file structure
        # Setup: static/index.css and static/images/logo.png
        with open(os.path.join(self.src, "index.css"), "w") as f:
            f.write("body { color: red; }")
        
        img_dir = os.path.join(self.src, "images")
        os.mkdir(img_dir)
        with open(os.path.join(img_dir, "logo.png"), "w") as f:
            f.write("fake-binary-data")

        # Act
        copy_files_recursive(self.src, self.dst)

        # Assert
        self.assertTrue(os.path.exists(os.path.join(self.dst, "index.css")))
        self.assertTrue(os.path.exists(os.path.join(self.dst, "images/logo.png")))
        with open(os.path.join(self.dst, "index.css"), "r") as f:
            self.assertEqual(f.read(), "body { color: red; }")

    def test_copy_to_existing_dir(self):
        # Test 2: Destination directory already exists
        os.mkdir(self.dst)
        with open(os.path.join(self.src, "test.txt"), "w") as f:
            f.write("hello")
        
        copy_files_recursive(self.src, self.dst)
        
        self.assertTrue(os.path.exists(os.path.join(self.dst, "test.txt")))

    def test_copy_multiple_files(self):
        # Test 3: Multiple files in one directory
        files = ["a.txt", "b.txt", "c.txt"]
        for f_name in files:
            with open(os.path.join(self.src, f_name), "w") as f:
                f.write(f_name)
        
        copy_files_recursive(self.src, self.dst)
        
        for f_name in files:
            self.assertTrue(os.path.exists(os.path.join(self.dst, f_name)))

if __name__ == "__main__":
    unittest.main()
