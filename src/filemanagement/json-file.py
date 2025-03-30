from .core import File
import json


class JsonFile(File):
    """ """

    def convert_to_dict(self) -> dict:
        """Convert JSON content of this file into Python dictionary form."""

        with open(self.get_abspath(), 'r', encoding="utf-8") as f_in:
            return json.load(f_in)
