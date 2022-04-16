import re

from app.service.icd10_generate_graph_from_text import ICD10GenerateGraphFromText
from collections import OrderedDict
from collections import defaultdict
import string
from app.dto.core.util.Span import Span
from app.dto.core.util.TokenNode import TokenNode


class ICD10GenerateGraphFromTextImpl(ICD10GenerateGraphFromText):

    def __init__(self, changed_token_dict):
        self.dictionary = changed_token_dict
        self.token_dict = OrderedDict()
        self.global_offset = 0

    def get_start_end_pos_span(self, graph: dict, child_node: str, marker: int):
        if graph.get(child_node, None) is not None:
            node = graph.get(child_node)
            if node.is_root is True:
                span_to_return = node.pos_list[node.track_pos].start if marker == 0 else node.pos_list[
                    node.track_pos].end
                node = self.position_tracker_repositioning(node)
                return span_to_return
            else:
                return self.get_start_end_pos_span(
                    graph, node.parent_token, marker
                )
        return -1

    def position_tracker_repositioning(self, node: dict):
        node.track_pos += 1
        node.track_pos = node.track_pos % len(node.pos_list)
        return node

    def reset_global_offset(self):
        self.global_offset = 0

    def process_token_to_create_graph(self, spanned_info: list) -> TokenNode:
        for each_span in spanned_info:
            punctuation_list = re.findall("[" + string.punctuation + "]+", each_span[0])
            if len(punctuation_list) > 0 and len( each_span[0]) == 1:
                continue
            if self.token_dict.get(each_span[0], None) is None:
                node = self.get_new_node_for_token(pos_list=[Span(each_span[1], each_span[2], 0)],
                                                   length=len(each_span[0]))
                node.pos_tracking[each_span[1]] = each_span[1]
                self.token_dict[each_span[0]] = node
            else:
                self.token_dict[each_span[0]].pos_list.append(Span(each_span[1], each_span[2], 0))
                self.token_dict[each_span[0]].pos_tracking[each_span[1]] = each_span[1]
        return self.token_dict

    def get_new_node_for_token(self, parent_key: str = "", is_root=True, pos_list: list = [], length: int = 0):
        new_node = TokenNode()
        new_node.pos_tracking = defaultdict(int)
        new_node.pos_list = pos_list
        new_node.is_root = is_root
        new_node.track_pos = 0
        new_node.length = length
        new_node.parent_token = parent_key
        return new_node

    def track_change_in_text(self, token_dict, text_span):

        new_dict = OrderedDict()
        for index, (key, value1, value2) in enumerate(text_span):
            corrected_key = self.dictionary.get(key, None)
            if corrected_key is not None:
                node = token_dict[key]
                for index, each_tups in enumerate(corrected_key):
                    new_node = self.get_new_node_for_token(key, is_root=False, length=len(each_tups[1]))
                    start = key.find(each_tups[0]) + node.pos_list[node.track_pos].start
                    self.global_offset += (1 if index > 0 else 0)
                    new_node.pos_list.append(Span(start, start + len(each_tups[1]), self.global_offset))
                    new_node.pos_tracking[start + self.global_offset] = start
                    new_dict[each_tups[1]] = new_node
                    self.global_offset += len(each_tups[1]) - len(each_tups[0])
                node.track_pos += 1
                if node.track_pos == len(node.pos_list):
                    node.track_pos = 0
                new_text = [each_tups[1] for each_tups in corrected_key]
                text_span[index][0] = " ".join(new_text)
        return {**token_dict, **new_dict}

    def generate_metainfo_for_changed_text(self, spanned_info: dict) -> dict:
        token_dict = self.process_token_to_create_graph(spanned_info)
        self.reset_global_offset()
        token_dict2 = self.track_change_in_text(token_dict, spanned_info)
        return token_dict2