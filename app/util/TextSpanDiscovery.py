import logging

from app.dto.core.util.TokenNode import TokenNode
from app.dto.core.util.Span import Span
from collections import OrderedDict, defaultdict
from app.exception.service_exception import ServiceException


class TextSpanDiscovery:

    def __init__(self, changed_token_dict=None):
        self.dictionary = changed_token_dict
        self.token_dict = OrderedDict()
        self.global_offset = 0
        self.__logger = logging.getLogger(__name__)

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

    def get_new_node_(self, parent_: str = "", isRoot=True, posList: list = list(), length: int = 0):
        node = TokenNode()
        node.pos_tracking = defaultdict(int)
        node.pos_list = posList
        node.is_root = isRoot
        node.track_pos = 0
        node.length = length
        node.parent_token = parent_
        return node

    def track_the_changes_in_text(self, token_dict, text_span):

        new_dict = OrderedDict()
        try:
            if self.dictionary is None:
                raise ValueError("Missing dictionary need to be initialized")
        except ValueError:
            self.__logger.error("Error while reading from dictionary not initlialzied in TextSpanDiscovery module"
                                " ", exc_info=True)
            raise ServiceException(message="Missing dictionary to generate result")
        for index, (key, value1, value2) in enumerate(text_span):
            corrected_key = self.dictionary.get(key, None)
            if corrected_key is not None:
                node = token_dict[key]
                for index, each_tups in enumerate(corrected_key):
                    new_node = self.get_new_node_(key, isRoot=False, length=len(each_tups[1]), posList=[])
                    start = key.find(each_tups[0]) + node.pos_list[node.track_pos].start
                    self.global_offset += (1 if index > 0 else 0)
                    new_node.pos_list.append(Span(start=start, end=start + len(each_tups[1]), offset=self.global_offset))
                    new_node.pos_tracking[start + self.global_offset] = start
                    new_dict[each_tups[1]] = new_node
                    self.global_offset += len(each_tups[1]) - len(each_tups[0])
                node.track_pos += 1
                if node.track_pos == len(node.pos_list):
                    node.track_pos = 0
                new_text = [each_tups[1] for each_tups in corrected_key]
                text_span[index][0] = " ".join(new_text)
        return {**token_dict, **new_dict}

    def generate_metainfo_for_changed_text(self, token_dict: dict, spanned_info: dict) -> dict:
        self.reset_global_offset()
        token_dict2 = self.track_the_changes_in_text(token_dict, spanned_info)
        return token_dict2