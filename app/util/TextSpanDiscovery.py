from app.dto.core.util import TokenNode
from app.dto.core.util import Span
from collections import OrderedDict
from nltk import TreebankWordTokenizer
from nltk import sent_tokenize
import string
import re


class TextSpanDiscovery:

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