"""An utilities suite for UNIX file management.

TODO:
    - See /TODO

version: 0.0.1
"""
import os
import re
import logging
from pathlib import Path
from typing import TypeAlias
import numpy as np
#from skimage.io import imread, imsave
#from imageops.core import crop_image, expand_image

from .exceptions import SuspiciousFileOperation

# Setup logger
logger = logging.getLogger(__name__)

# A type that is returned by the file rename command.
RenameResult: TypeAlias = dict[str, str | tuple]


def has_file(directory, checking_filename) -> bool:
    """Returns True if directory has a filename otherwise returns False."""

    return checking_filename in os.listdir(directory)


class File():
    """Virtual file, file representation.

    TODO:
        - [ ] add lazy fields eval, maybe do it by using a decorator?
    """

    abspath: str

    def __init__(self, filename: str, create_new=False):
        # Raise on empty string
        if not filename:
            raise ValueError()

        # Evaluate file's absolute path
        self.abspath = os.path.abspath(os.path.join(os.getcwd(), filename))

        # Raise on invalid name or missing file
        if not os.path.exists(self.abspath):
            if not create_new:
                raise FileNotFoundError(f"File {self.get_abspath()} does not exist.")

    def get_abspath(self) -> str:
        """Get absolute path of this file."""

        return self.abspath

    def get_base_name(self) -> str:
        """Get base name of this file.

        path/to/file.ext -> file
        """

        return Path(self.get_abspath()).stem

    def get_root(self) -> str:
        """Get name of this file.

        path/to/file.ext -> path/to/file
        """

        file_name, _ = os.path.splitext(self.abspath)
        return file_name

    def get_name(self) -> str:
        """Get name of this file.

        path/to/file.ext -> file.ext
        """
        if self.get_extension() is not None:
            return self.get_base_name() + self.get_extension()

        return self.get_base_name()

    def get_extension(self) -> str | None:
        """Get extension of this file if any. If no ext returns None.

        path/to/file.ext -> .ext
        """

        _, file_extension = os.path.splitext(self.abspath)

        if not file_extension:
            return None

        return file_extension

    def get_parent_file_name(self) -> str:
        """Get directory name where this file is located.

        path/to/file.ext -> path/to
        """

        return os.path.dirname(self.abspath)

    def rename(self, new_name: str, force_rewrite: bool=False) -> RenameResult:
        """Rename file."""

        file_name = self.get_name()

        # Eval directory path where the file to be renamed located
        procing_dir = self.abspath[:-len(file_name)]

        # Eval new abs path with new file name
        new_abspath = procing_dir + new_name

        result: RenameResult

        # If specified `new_filename` is the same as the current file name do nothing
        if file_name == new_name:
            logger.info("%s unchanged", file_name)

            result = {"status": "unchanged",
                      "names": (file_name, file_name)}
        # If file with `new_filename` already exists do nothing except the case force set to True
        elif has_file(procing_dir, new_name) and not force_rewrite:
            logger.warning("File with name %s already exists! No changes were made.", new_name)

            result = {"status": "collision",
                      "names": (file_name, new_name)}
        # In any other case rename it
        else:
            os.rename(self.abspath, new_abspath)

            logger.info("%s -> %s", file_name, new_name)

            result = {"status": "changed",
                      "names": (file_name, new_name)}

        # Update absolute path
        self.abspath = new_abspath

        return result

    def normalize_filename(self, force_rewrite=False) -> RenameResult:
        """Remove bad symbols in the name of the file."""

        name = self.get_name()

        new_filename = name.strip().replace(" ", "_")
        new_filename = re.sub(r"(?u)[^-\w.]", "", new_filename)
        if new_filename in {"", ".", ".."}:
            raise SuspiciousFileOperation(f"Could not derive file name from '{name}'")

        return self.rename(new_filename, force_rewrite)

    def update_filename_with_version_num(self, new_name, v_num=0) -> str:
        """Updates the filename with a version number if necessary,
        without adding anything if no versioning is needed.

        Does it work?
        """

        # If file with the name already exists increment version number
        if os.path.isfile(os.path.join(self.get_parent_file_name(), new_name)):
            v_num += 1
            name = self.get_base_name() + "_" + str(v_num) + self.get_extension()
            logger.debug("Updated name %s", name)
            return self.update_filename_with_version_num(
                    os.path.join(self.get_parent_file_name(), name), v_num)

        return new_name

    def read(self, encoding="utf-8") -> str | None:
        content = ""
        if os.path.isfile(self.abspath):
            with open(self.abspath, 'r', encoding=encoding) as file:
                content = file.read()
        else:
            return None

        return content

    def __repr__(self) -> str:
        return f"Filename {self.abspath}"


class Directory(File):
    """Virtual directory class.

    An object of this class is a virtual file itself. It extends file class
    with some utilities like normalize filenames in this dir, etc.
    The object of this class contains a flat (w/o dir objects) list of its
    children files(!) just a list of abs paths as strings for now.

    I'm not sure about if it does worth it cuz having all the files in the
    dir as objects, and even before this -- instantiate every single of --
    could be expensive.
    """

    def __init__(self, filename: str):
        File.__init__(self, filename)

        if not os.path.isdir(self.get_abspath()):
            logger.warning("%s is not a directory.", self.get_abspath())
            raise NotADirectoryError(f"{self.get_abspath()} is not a directory.")

        self.file_list = os.listdir(self.get_abspath())

    def normalize_filenames(self, force_rewrite: bool | None = None) -> list[RenameResult]:
        """Normalize filenames in directory.

        This script removes 'bad' symbols from files' names in the specified
        or current directory
        """

        change_log: list[RenameResult] = []

        for filename in self.file_list:
            file = File(os.path.join(self.get_abspath(), filename))

            result = file.normalize_filename(force_rewrite=force_rewrite)

            change_log.append(result)

        return change_log

    def add_background(self, filt: str | None=None) -> None:
        """Adds background to images in directory.

        Image files to which background to be added can be filtered by regex with
        `filt` argument.
        """
        raise NotImplementedError()

    def read(self, _):
        raise IOError("You cannot read from directory file.")

    @staticmethod
    def copy_tree(source_path: str, destination_path: str) -> None:
        '''Copies directory recursively.
        Works somewhat like copy_tree. Uses `os.walk`.
        '''

        print("Inserting config... ", end='')
        for source_root, dirs, files in os.walk(source_path, topdown=True):
            new_root = source_root[len(source_path):].strip('/')

            for name in files:
                try:
                    os.replace(os.path.join(source_root, name),
                               os.path.join(destination_path, new_root, name))
                except FileNotFoundError:
                    # It says "there's no such directory". Does git delete it at
                    # some point? Not sure why is this and am lazy to figure it out.
                    pass
            for name in dirs:
                os.makedirs(os.path.join(destination_path, new_root, name),
                            exist_ok=True)
        print("Done.")

    @staticmethod
    def remove_dir_recursively(dir_path: str) -> None:
        '''Removes directory recursively (force).
        Somewhat like `rm <dir_path> -rf`.
        '''

        print(f"Deleting '{dir_path}'... ", end='')
        for disposed_root, dirs, files in os.walk(dir_path, topdown=False):
            for name in files:
                os.remove(os.path.join(disposed_root, name))
            for name in dirs:
                os.rmdir(os.path.join(disposed_root, name))
        os.rmdir(dir_path)
        print("Done.")
