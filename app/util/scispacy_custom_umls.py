import os

from scispacy.linking_utils import KnowledgeBase

from app.util.config_manager import ConfigManager
from data import data_base_path
from data.scispacy_cache_for_itx import umls2021ab_json_path


class UMLS2021KnowledgeBase(KnowledgeBase):
    def __init__(self):
        _umls_jsonl_file = ConfigManager.get_specific_config(section="scispacy_umls2021_ab", key="umls2021_ab")
        _file_path = os.path.join(os.path.join(os.path.dirname(data_base_path),
                                               umls2021ab_json_path),
                                  _umls_jsonl_file)
        super().__init__(_file_path)
