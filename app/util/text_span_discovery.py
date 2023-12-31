from app.dto.core.util.TokenNode import TokenNode
from collections import OrderedDict
from typing import Optional
from app.dto.core.service.Tokens import TokenInfo


class TextSpanDiscovery:
    ROOT_LOCATION: Optional[int] = None

    def __init__(self, changed_token_dict=None):
        self.dictionary = changed_token_dict
        self.token_dict = OrderedDict()
        self.global_offset = 0

    def set_changed_text_dictionary(self, dict__):
        self.dictionary = dict__

    def get_start_end_pos_span(self, graph: dict, child_node: str, location: int, sub_word: str):
        if graph.get(child_node, None) is not None:
            node = graph.get(child_node)
            inner_node = node.get(location, None)
            if inner_node == None:
                return (-1, None)
            if inner_node != None and inner_node.is_root is True:
                span_to_return = location + (child_node.find(sub_word) if sub_word != '' else 0)
                return (span_to_return, sub_word if sub_word != '' else child_node)
            else:
                return self.get_start_end_pos_span(
                    graph, inner_node.parent_token, inner_node.pos_tracking, inner_node.sub_word
                )
        return (-1, None)

    """Global_offset is an importan pointer that track how many places text are shifting towards either left or right through
    expansion and shrinking"""

    def reset_global_offset(self):
        self.global_offset = 0

    """Following function is used to create a complex objec  of type TokenNode"""

    def get_new_node_(self, parent_: str = "", is_root=True, sub_word: str = "", length: int = 0):
        node = TokenNode()
        node.pos_tracking = TextSpanDiscovery.ROOT_LOCATION
        node.sub_word = sub_word
        node.is_root = is_root
        node.length = length
        node.parent_token = parent_
        return node

    def get_new_nodes(self, key: str, corrected_key: list, start_of_span: int, new_span: list, token_dict: dict):
        for index, each_tuple in enumerate(corrected_key):
            start = key.find(each_tuple[0]) + start_of_span
            is_space_needed = 1 if index > 0 else 0
            self.global_offset += is_space_needed
            subword = each_tuple[0] if len(key) != len(each_tuple[0]) else ""
            new_node = self.get_new_node_(key, is_root=True if key == "" else False, length=len(each_tuple[1]),
                                          sub_word=subword)
            new_node.pos_tracking = start_of_span
            new_span.append(TokenInfo(token=each_tuple[1], start_of_span=start + self.global_offset,
                                      end_of_span=start + self.global_offset + len(each_tuple[1])))
            if token_dict.get(each_tuple[1], None) is None:
                token_dict[each_tuple[1]] = {}
            if token_dict[each_tuple[1]].get(start + self.global_offset, None) is None:
                 token_dict[each_tuple[1]][start + self.global_offset] = new_node
            self.global_offset += (len(each_tuple[1]) - len(each_tuple[0]))

    """In The following function we first check whether the dictionary base is initialzied or not. If it is not initialized
    in that case we are going return Code 500 internal server error, the error will be logged in log file. If everythign
    is properly initialized then we proceed to track the changes in text position"""

    def track_the_changes_in_text(self, token_dict, text_span) -> tuple:
        new_span = []
        for index, token_object in enumerate(text_span):
            key = token_object.token
            start_of_span = token_object.start_of_span
            corrected_key = self.dictionary.get(key, None)
            if corrected_key != None:
                self.get_new_nodes(key, corrected_key, start_of_span, new_span, token_dict)
            else:
                self.get_new_nodes(key, [(key, key)], start_of_span, new_span, token_dict)

        return token_dict, new_span

    def improved_text_reconstruction(self, new_text: list) -> str:
        new_token_list = [""] * len(new_text)
        for index in range(len(new_text) - 1):
            if new_text[index + 1].token not in {':', ';', '!', '?', '.', ','}:
                new_token_list[index] = new_text[index].token + " "
            else:
                new_token_list[index] = new_text[index].token
        new_token_list[-1] = new_text[-1].token
        return "".join([each_elem for each_elem in new_token_list])

    """This is the function externally visible. It takes graph dictionary and text span information as parameter and return
    updated graph dictionary with new text positional information"""

    def generate_metainfo_for_changed_text(self, token_dict: dict, spanned_info: dict) -> tuple:
        self.reset_global_offset()
        updated_tokenize_dict, new_span = self.track_the_changes_in_text(token_dict, spanned_info)
        return updated_tokenize_dict, new_span
