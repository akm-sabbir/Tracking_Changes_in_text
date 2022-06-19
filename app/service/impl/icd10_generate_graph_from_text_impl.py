from collections import OrderedDict
from typing import Optional

from app.dto.core.util.Span import Span
from app.dto.core.util.TokenNode import TokenNode
from app.dto.pipeline.tokenization_component_result import TokenizationResult
from app.service.icd10_generate_graph_from_text import ICD10GenerateGraphFromText

""" Following class helps to track the changes in text by keeping the relationship between original text and extrapolated
text."""


class ICD10GenerateGraphFromTextImpl(ICD10GenerateGraphFromText):
    ROOT_LOCATION: Optional[int] = None

    def __init__(self, ):
        self.token_dict = OrderedDict()

    """ Following function takes a list of token along with its span and generate all form of meta data.
    the utility of this information is indespensible"""

    def process_token_to_create_graph(self, spanned_info: TokenizationResult) -> dict:
        for each_span in spanned_info.token_container:
            node = self.get_new_node_for_token(pos_list=[Span(each_span.start_of_span, each_span.end_of_span, 0)],
                                               length=len(each_span.token))
            node.pos_tracking = each_span.start_of_span
            if self.token_dict.get(each_span.token, None) is None:
                self.token_dict[each_span.token] = {}
            self.token_dict[each_span.token][each_span.start_of_span] = node
        return self.token_dict

    """Following function helps to create a new object of type TokenNode and initialize it with differetn 
    type of information. It helps to create data structure"""

    def get_new_node_for_token(self, parent_key: str = "", is_root=True, pos_list: list = [], length: int = 0):
        new_node = TokenNode()
        new_node.pos_tracking = ICD10GenerateGraphFromTextImpl.ROOT_LOCATION
        new_node.pos_list = pos_list
        new_node.is_root = is_root
        new_node.length = length
        new_node.parent_token = parent_key
        return new_node
