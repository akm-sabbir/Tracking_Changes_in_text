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

    def tokenize_with_span(self, text):
        ss = sent_tokenize(text)
        ts = [(src[start:end], start, end) for tok, src in zip(TreebankWordTokenizer().span_tokenize_sents(ss), ss) for
              start, end in tok]
        return ts

    def tokenize_with_span_for_text(self, text):
        ts = [[text[start:end], start, end] for start, end in TreebankWordTokenizer().span_tokenize(text)]
        return ts

    def get_start_end_pos_span(self, graph :dict, child_node :str, marker: int):
        if graph.get(child_node, None) is not None:
            node = graph.get(child_node)
            if node.is_root is True:
                span_to_return = node.pos_list[node.track_pos].start if marker == 0 else node.pos_list[node.track_pos].end
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

    def process_each_token(self, spanned_info) -> TokenNode:
        for each_span in spanned_info:
            punctuation_list = re.findall("[" + string.punctuation + "]+", each_span[0])
            key = each_span[0][0:-1] if len(punctuation_list) > 0 else each_span[0]
            each_span[2] = (each_span[2] - 1) if len(punctuation_list) > 0 else each_span[2]
            if self.token_dict.get(key, None) is None:
                node = TokenNode()
                node.parent_token = None
                node.length = len(key)
                node.is_root = True
                node.track_pos = 0
                node.pos_list = [Span(each_span[1], each_span[2], 0)]
                self.token_dict[key] = node
            else:
                self.token_dict[key].pos_list.append(Span(each_span[1], each_span[2], 0))
        return self.token_dict

    def text_structuring(self, text):
        ts = self.tokenize_with_span_for_text(text)
        token_dict = self.process_each_token(ts)
        new_dict = OrderedDict()
        for key, value1, value2 in ts:
            corrected_key = self.dictionary.get(key, None)
            if corrected_key is not None:
                node = token_dict[key]
                for index, each_tups in enumerate(corrected_key):
                    new_node = TokenNode()
                    print("old text: " + each_tups[0])
                    start = key.find(each_tups[0]) + node.pos_list[node.track_pos].start
                    print("old pos: " + str(start))
                    print("new text: " + each_tups[1])
                    self.global_offset += (1 if index > 0 else 0)
                    print("new pos: " + str(start + self.global_offset))
                    new_node.pos_list.append(Span(start, start + len(each_tups[1]), self.global_offset))
                    self.global_offset += len(each_tups[1]) - len(each_tups[0])
                    new_node.is_root = False
                    new_node.track_pos = 0
                    new_node.parent_token = key
                    new_dict[each_tups[1]] = new_node
                node.track_pos += 1
                if node.track_pos == len(node.pos_list):
                    node.track_pos = 0
        print("End of Processing")
        return {**token_dict, **new_dict}