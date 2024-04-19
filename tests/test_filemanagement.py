"""Tests for file management module"""
import os
from pathlib import Path
import logging
import unittest
#from unittest.mock import patch

from yui.filemanagement import ImageFile, File


#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger(__name__)


class TestFileManager(unittest.TestCase):
    """Tests for utils.filemanagement.FileManager class"""

    @classmethod
    def setUpClass(cls):
        tests_data_dir = os.path.join(os.getcwd(), "tests/data")

        Path(os.path.join(tests_data_dir, "hello_world")).unlink(missing_ok=True)

        if not FileManager.has_file(tests_data_dir, "hello world"):
            Path(os.path.join(tests_data_dir, "hello world")).touch()

    @classmethod
    def tearDownClass(cls):
        tests_data_dir = os.path.join(os.getcwd(), "tests/data")

        Path(os.path.join(tests_data_dir, "hello_world")).unlink(missing_ok=True)

    def test_has_file(self):
        """Test has file function"""

        tests_data_dir = os.path.join(os.getcwd(), "tests/data")

        # With relative path
        self.assertTrue(FileManager.has_file("./tests/data/", "hello world"))
        # With abs path
        self.assertTrue(FileManager.has_file(tests_data_dir, "hello world"))

    def test_normalize_filenames(self):
        """Test filenames normalization"""

        tests_data_dir = os.path.join(os.getcwd(), "tests/data")

        # 1 test
        print("1 test")
        # Check if the file is in the directory
        self.assertTrue(FileManager.has_file(tests_data_dir, "hello world"))
        # In local dir
        FileManager.normalize_filenames("./tests/data/")
        # Check if file has been renamed in the directory
        self.assertTrue(FileManager.has_file(tests_data_dir, "hello_world"))
        # 2 test
        print("2 test")
        # Remove file renamed from the prev test
        Path(os.path.join(tests_data_dir, "hello_world")).unlink(missing_ok=True)
        # Add another file with bad symbols in names for the next text
        if not FileManager.has_file(tests_data_dir, "hello world"):
            Path(os.path.join(tests_data_dir, "hello world")).touch()

        # Check if the file is in the directory
        self.assertTrue(FileManager.has_file(tests_data_dir, "hello world"))
        # In specified directory
        FileManager.normalize_filenames(tests_data_dir, is_abs=True)

        # Check if file has been renamed in the directory
        self.assertTrue(FileManager.has_file(tests_data_dir, "hello_world"))


class TestFile(unittest.TestCase):
    """Tests for utils.filemanagement.File class, the virtual file"""

    @classmethod
    def setUpClass(cls):
        tests_data_dir = os.path.join(os.getcwd(), "tests/data")

        Path(os.path.join(tests_data_dir, "renamed_file")).unlink(missing_ok=True)

        if not os.path.isfile(os.path.join(tests_data_dir, "test_file")):
            Path(os.path.join(tests_data_dir, "test_file")).touch()

    @classmethod
    def tearDownClass(cls):

        Path(os.path.join(os.getcwd(), "renamed_file")).unlink(missing_ok=True)

    def setUp(self):
        tests_data_dir = "./tests/data/"
        self.file           = File(tests_data_dir + "test_file")
        self.file_w_ext     = File(tests_data_dir + "test_file.ext")
        self.file_nonemtpy  = File(tests_data_dir + "test_file_nonempty.ext")

        # later
        #self.image_file = ImageFile("test_file")
        #self.image_file = ImageFile("test_file")

    def tearDown(self):
        pass

    def test_init(self):
        """Test file constructor / instance initiation"""

        with self.assertRaises(ValueError):
            File("")
            ImageFile("")

        with self.assertRaises(OSError):
            File("...")
            ImageFile("...")

    def test_get_base_name(self):
        """Test get base name of file function"""

        self.assertEqual(self.file.get_base_name(),             "test_file")
        self.assertEqual(self.file_w_ext.get_base_name(),       "test_file")
        self.assertEqual(self.file_nonemtpy.get_base_name(),    "test_file_nonempty")

    def test_get_name(self):
        """Test get file name w/o extension function"""

        self.assertEqual(self.file.get_name(),
                         "/home/yuri/src/scripts/utils/tests/data/test_file")
        self.assertEqual(self.file_w_ext.get_name(),
                         "/home/yuri/src/scripts/utils/tests/data/test_file")
        self.assertEqual(self.file_nonemtpy.get_name(),
                         "/home/yuri/src/scripts/utils/tests/data/test_file_nonempty")

    def test_get_extension(self):
        """Test get file extension function"""

        self.assertEqual(self.file.get_extension(),             None)
        self.assertEqual(self.file_w_ext.get_extension(),       ".ext")
        self.assertEqual(self.file_nonemtpy.get_extension(),    ".ext")

    def test_get_abspath(self):
        """Test get absolute path of file function"""

        self.assertEqual(self.file.get_abspath(),
                         "/home/yuri/src/scripts/utils/tests/data/test_file")
        self.assertEqual(self.file_w_ext.get_abspath(),
                         "/home/yuri/src/scripts/utils/tests/data/test_file.ext")
        self.assertEqual(self.file_nonemtpy.get_abspath(),
                         "/home/yuri/src/scripts/utils/tests/data/test_file_nonempty.ext")

    def test_rename(self):
        """Test File's rename function

        - [ ] add speed test
        """

        tests_data_dir = os.path.join(os.getcwd(), "tests/data")

        # Check if the file is in the directory
        self.assertTrue(os.path.isfile(os.path.join(tests_data_dir, "test_file")))
        # Check virtual abs path of the file instance
        self.assertEqual(self.file.get_abspath(),
                         "/home/yuri/src/scripts/utils/tests/data/test_file")
        # Rename file
        self.file.rename("renamed_file")

        # Check virtual abs path being renamed
        self.assertEqual(self.file.get_abspath(),
                         "/home/yuri/src/scripts/utils/tests/data/renamed_file")
        # Check if file has been renamed in the directory
        self.assertTrue(os.path.isfile(os.path.join(tests_data_dir, "renamed_file")))


class TestImageFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_crop(self):
        pass


if __name__ == "__main__":
    unittest.main()
