from unittest import TestCase
from unittest.mock import patch, Mock

from scispacy.linking_utils import KnowledgeBase

from app.util.scispacy_custom_umls import UMLS2021KnowledgeBase


class TestUMLS2021KnowledgeBase(TestCase):
    @patch.object(KnowledgeBase, '__init__', lambda x, y: None)
    @patch('app.util.scispacy_custom_umls.ConfigManager.get_specific_config')
    @patch('app.util.scispacy_custom_umls.os.path.join')
    def test__creation_of_scispacy_custom_umls_object__should_create_object__given_correct_parameters(self,
                                                                                                      mock_file_path: Mock,
                                                                                                      mock_json_file_path: Mock):
        mock_file_path.return_value = "some path"
        mock_json_file_path.return_value = "some json file name"

        custom_umls = UMLS2021KnowledgeBase()

        mock_file_path.assert_called()
        mock_json_file_path.assert_called_once()
