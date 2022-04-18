import logging

from app.dto.core.util.TokenNode import TokenNode
from app.dto.core.util.Span import Span
from collections import OrderedDict, defaultdict
from app.exception.service_exception import ServiceException


class TextSpanDiscovery:

    def __init__(self, changed_token_dict):
        self.dictionary = changed_token_dict
        self.token_dict = OrderedDict()
        self.global_offset = 0

    def get_start_end_pos_span(self, graph: dict, child_node: str, location: int, sub_word: str):
        if graph.get(child_node, None) is not None:
            node = graph.get(child_node)
            inner_node = node.get(location, None)
            if inner_node == None :
                return (-1, None)
            if inner_node != None and inner_node.is_root is True:
                span_to_return = location + (child_node.find(sub_word) if sub_word != '' else 0)
                return (span_to_return, len(sub_word) if sub_word!='' else len(child_node))
            else:
                return self.get_start_end_pos_span(
                    graph, inner_node.parent_token, inner_node.pos_tracking[location], inner_node.sub_word
                )
        return (-1, None)

    """Global_offset is an importan pointer that track how many places text are shifting towards either left or right through
    expansion and shrinking"""
    def reset_global_offset(self):
        self.global_offset = 0

    """Following function is used to create a complex objec  of type TokenNode"""
    def get_new_node_(self, parent_: str = "", is_root=True, sub_word: str = "", length: int = 0):
        node = TokenNode()
        node.pos_tracking = defaultdict(int)
        node.sub_word = sub_word
        node.is_root = is_root
        node.track_pos = 0
        node.length = length
        node.parent_token = parent_
        return node

    """In The following function we first check whether the dictionary base is initialzied or not. If it is not initialized
    in that case we are going return Code 500 internal server error, the error will be logged in log file. If everythign
    is properly initialized then we proceed to track the changes in text position"""
    def track_the_changes_in_text(self, token_dict, text_span):
        new_span = []
        for index, (key, value1, value2) in enumerate(text_span):
            corrected_key = self.dictionary.get(key, None)
            if corrected_key is not None:
                for index, each_tups in enumerate(corrected_key):
                    start = key.find(each_tups[0]) + value1
                    self.global_offset += (1 if index > 0 else 0)
                    new_node = self.get_new_node_(key, is_root=False, length=len(each_tups[1]), sub_word=
                                                  each_tups[0] if len(key) != len(each_tups[0]) else "")
                    new_node.pos_tracking[start + self.global_offset] = value1
                    new_span.append([each_tups[1], start + self.global_offset, start + self.global_offset + len(each_tups[1])])
                    if token_dict.get(each_tups[1], None) is None:
                        token_dict[each_tups[1]] = {}
                    token_dict[each_tups[1]][start + self.global_offset] = new_node
                    self.global_offset += (len(each_tups[1]) - len(each_tups[0]))
            else:
                new_span.append([key, value1 + self.global_offset, value2 + self.global_offset])
        return (token_dict, new_span)

    """This is the function externally visible. It takes graph dictionary and text span information as parameter and return
    updated graph dictionary with new text positional information"""
    def generate_metainfo_for_changed_text(self, token_dict: dict, spanned_info: dict) -> dict:
        self.reset_global_offset()
        token_dict2 = self.track_the_changes_in_text(token_dict, spanned_info)
        return token_dict2