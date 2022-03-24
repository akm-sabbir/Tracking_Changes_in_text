from app.service.icd10_exclusion_service import ICD10ExclusionService
import math
from app.settings import Settings
from app.util.icd_exclusions import ICDExclusions
from app.dto.core.service.exclusion_graph import ExclusionGraph
from collections import defaultdict
from functools import partial
import operator


class Icd10CodeExclusionServiceImpl(ICD10ExclusionService):
    icd_exclusion_util: ICDExclusions
    dir_left: str = "left"
    dir_right: str = "right"

    def __init__(self, icd_exclusion_utility=None):
        self.icd_exclusion_util = icd_exclusion_utility

    def form_exclusion_graph(self, icd10_metainfo: dict):
        icd10_lists = icd10_metainfo.keys()
        list_of_nodes = []
        for key, value in icd10_metainfo.items():
            exclusion_list = self.icd_exclusion_util.get_excluded_list(key, icd10_lists)
            node = ExclusionGraph()
            node.code = key
            node.neighbors = dict()
            for each_elem in exclusion_list:
                node.neighbors[each_elem] = 0
                node.degree += 1
            list_of_nodes.append(node)
        list_of_nodes = sorted(list_of_nodes, key=lambda x: x.degree, reverse=True)
        return list_of_nodes

    def built_graph_index(self, list_of_nodes: list):
        dict_of_codes = defaultdict(str)
        for index, value in enumerate(list_of_nodes):
            dict_of_codes[value.code] = index

        return dict_of_codes

    def iterate_graph_nodes_and_exclude(self, list_of_nodes: list, dict_of_codes: dict,
                                        icd10_metainfo: dict):
        for each_node in list_of_nodes:
            if len(each_node.neighbors) != 0 and each_node.vote >= 0:
                partial_selection = partial(self.get_filtered_neighbors, list_of_nodes=list_of_nodes,
                                            dict_of_nodes=dict_of_codes)
                neighbors = list(map(partial_selection, each_node.neighbors.items()))
                neighbors = [each for each in neighbors if each is not None]
                if len(neighbors) == 0:
                    continue
                selected_codes = self.get_no_selection_icd10_vote(each_node.code, neighbors,
                                                                  icd10_metainfo, list_of_nodes, dict_of_codes )
                for each_neighbor in each_node.neighbors.keys():
                    if selected_codes is self.dir_left:
                        list_of_nodes = self.set_reset_voting(each_node.code, each_neighbor, list_of_nodes, dict_of_codes)
                    else:
                        list_of_nodes = self.set_reset_voting(each_neighbor, each_node.code, list_of_nodes, dict_of_codes)
        return list_of_nodes

    def set_reset_voting(self, voter_code: str, reciever_code: str, list_of_nodes: list, dict_of_codes: dict):
        index_of_voter = dict_of_codes[voter_code]
        index_of_reciever = dict_of_codes[reciever_code]
        list_of_nodes[index_of_voter].neighbors[reciever_code] = 1
        list_of_nodes[index_of_reciever].vote -= 1
        for each_node in list(list_of_nodes[index_of_reciever].neighbors.keys()):
            if list_of_nodes[index_of_reciever].neighbors[each_node] == 1:
                list_of_nodes[dict_of_codes[each_node]].vote += 1
                list_of_nodes[index_of_reciever].neighbors[each_node] = 0
        return list_of_nodes

    def get_icd10_code_exclusion_decision_based_graph(self, icd10_metainfo: dict) -> dict:
        list_of_nodes = self.form_exclusion_graph(icd10_metainfo)
        dict_of_codes = self.built_graph_index(list_of_nodes)
        for each_index, each_value in enumerate(list_of_nodes):
            print(each_value.code)
            print(each_value.neighbors)
        list_of_nodes = self.iterate_graph_nodes_and_exclude(list_of_nodes, dict_of_codes,
                                        icd10_metainfo)
        for each_node in list_of_nodes:
            if each_node.vote < 0:
                icd10_metainfo[each_node.code].remove = True
        return icd10_metainfo

    def get_filtered_neighbors(self, neighbors: tuple, list_of_nodes: list, dict_of_nodes: dict ):
        node_key, node_value = neighbors
        if node_value == 0 and list_of_nodes[dict_of_nodes[node_key]].vote >= 0:
            return node_key

    def get_no_selection_icd10_vote(self, key_code: str, neighbors_: list, icd10_metainfo: dict, list_of_nodes: list,
                                    dict_of_nodes: dict):

        if len(icd10_metainfo.get(key_code).hcc_map) != 0 and \
                self.get_exclusion_list_hccmap(neighbors_, icd10_metainfo) is True \
                and sum([1 if (len(icd10_metainfo.get(each_elem).hcc_map) != 0 )  else 0 for each_elem in neighbors_]) \
                > 1:
            return self.dir_right
        if len(icd10_metainfo.get(key_code).hcc_map) != 0 and \
                self.get_exclusion_list_hccmap(neighbors_, icd10_metainfo) is True:
            return self.dir_left if (self.get_decision_on_choice(icd10_metainfo, key_code, neighbors_)[0] == key_code) else \
                self.dir_right

        if len(icd10_metainfo.get(key_code).hcc_map) != 0 and \
                self.get_exclusion_list_hccmap(neighbors_, icd10_metainfo) is False:
            return self.dir_left

        if len(icd10_metainfo.get(key_code).hcc_map) == 0 and \
                self.get_exclusion_list_hccmap(neighbors_, icd10_metainfo) is True:
            return self.dir_right

        return self.dir_left if (self.get_decision_on_choice(icd10_metainfo, key_code, neighbors_)[0] == key_code) else \
            self.dir_right

    def get_exclusion_list_hccmap(self, exclusion_list: list, meta_info: dict):
        for each_elem in exclusion_list:
            if meta_info.get(each_elem) is not None and len(meta_info.get(each_elem).hcc_map) != 0:
                return True
        return False

    def __get_avg_acm_score(self, exclusion_list: list, icd10_metainfo: dict):
        scores = [icd10_metainfo[elem].score for elem in exclusion_list]
        return sum(scores) / len(scores)

    def __get_avg_acm_icd10code_len(self, exclusion_list: list):
        return sum([len(element) for element in exclusion_list]) / len(exclusion_list)

    def get_decision_on_choice(self, icd10_metainfo: dict, key: str, exclusion_list: list):
        if (math.fabs(
                icd10_metainfo.get(key).score - self.__get_avg_acm_score(exclusion_list, icd10_metainfo)) > 0.15):
            if icd10_metainfo.get(key).score > self.__get_avg_acm_score(exclusion_list, icd10_metainfo):
                return [key]
            else:
                return exclusion_list
        if len(key) > self.__get_avg_acm_icd10code_len(exclusion_list):
            return [key]
        if len(key) < self.__get_avg_acm_icd10code_len(exclusion_list):
            return exclusion_list

        score_ = sum([icd10_metainfo.get(exclusion_list[each_ind]).score
                      for each_ind in range(len(exclusion_list))])/len(exclusion_list)
        if icd10_metainfo.get(key).score > score_:
            return [key]
        else:
            return exclusion_list

    def get_not_selected_icd10_list(self, key: str, exclusion_list: list, icd10_metainfo: dict) -> list:

        if len(icd10_metainfo.get(key).hcc_map) != 0 and \
                self.get_exclusion_list_hccmap(exclusion_list, icd10_metainfo) is True \
                and sum([1 if len(icd10_metainfo.get(each_elem).hcc_map) != 0 else 0 for each_elem in exclusion_list]) \
                > 1:
            return exclusion_list
        if len(icd10_metainfo.get(key).hcc_map) != 0 and \
                self.get_exclusion_list_hccmap(exclusion_list, icd10_metainfo) is True:
            return self.get_decision_on_choice(icd10_metainfo, key, exclusion_list)

        if len(icd10_metainfo.get(key).hcc_map) != 0 and \
                self.get_exclusion_list_hccmap(exclusion_list, icd10_metainfo) is False:
            return [key]

        if len(icd10_metainfo.get(key).hcc_map) == 0 and \
                self.get_exclusion_list_hccmap(exclusion_list, icd10_metainfo) is True:
            return exclusion_list

        return self.get_decision_on_choice(icd10_metainfo, key, exclusion_list)
