from unittest import TestCase
from unittest.mock import patch

from app.util.import_util import ImportUtil


def mock_import_module(module_name):
    return "some module"


def mock_sys_path_append(some_data):
    return


def mock_glob(some_path):
    return ["somefile.py", "someotherfile.py"]


def mock_os_path_join(path, path_to_join):
    return path + path_to_join


class TestImportUtil(TestCase):
    @patch("importlib.import_module", mock_import_module)
    @patch("sys.path", [])
    @patch("glob.glob", mock_glob)
    @patch("os.path.join", mock_os_path_join)
    def test_import_modules_from_directory_as_list__given_path__should_call_proper_library_functions(self):
        modules = ImportUtil.import_modules_from_directory_as_list("some/path")
        assert modules == ['some module', 'some module']
