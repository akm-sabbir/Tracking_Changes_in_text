import glob
import importlib
import os
import pathlib
import sys


class ImportUtil:
    @staticmethod
    def import_modules_from_directory_as_list(module_directory: str) -> list:
        sys.path.append(module_directory)
        py_files: list = glob.glob(os.path.join(module_directory, '*.py'))
        modules: list = []
        for py_file in py_files:
            module_name = pathlib.Path(py_file).stem
            if module_name == '__init__':
                continue
            else:
                modules.append(importlib.import_module(module_name))
        return modules
