from unittest import TestCase
from unittest.mock import patch, Mock

from app.util.hcc.hcc_category_util import HCCCategoryUtil


class TestHCCCategoryUtil(TestCase):
    data = None
    hcc_engine = None

    @patch("app.util.hcc.hcc_category_util.ConfigManager.get_specific_config")
    @patch("app.util.hcc.hcc_category_util.HCCEngine")
    @patch("builtins.open")
    def test__get_hcc_category__should_return_correct_category__given_hcc_code(self, mock_file_open: Mock,
                                                                               mock_hcc_engine: Mock,
                                                                               mock_config: Mock):
        mock_hcc_object = Mock()
        mock_hcc_object.describe_hcc = Mock()
        mock_hcc_object.describe_hcc.return_value = {"description": "Some other category"}

        mock_hcc_engine.return_value = mock_hcc_object

        mock_config.side_effect = ["23", "file_name"]
        hcc_util = HCCCategoryUtil()
        mock_read = Mock()
        mock_read.read = Mock()
        mock_read.read.return_value = '{"HCC1": "Some category"}'
        mock_file_open.return_value = mock_read

        category = hcc_util.get_hcc_category("HCC1")
        assert category == "Some category"
        mock_file_open.assert_called()

        category = hcc_util.get_hcc_category("HCC2")
        assert category == "Some other category"
        mock_hcc_object.describe_hcc.assert_called_with("HCC2")
