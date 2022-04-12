import string
import random
from typing import List
from unittest import TestCase
from app.util import TextSpanDiscovery

class TestSpanDiscovery(TestCase):
    __get_dummy_dictionary = {"this": [("this", "these")],
                          "wellwriten": [("well", "well"), ("writen", "written")],
                          "analyz": [("analyz", "analyze")],
                          "broadview": [("broad", "broad"), ("view", "view")],
                          "baddest": [("baddest", "worst")],
                          "hart": [("hart", "heard")],
                          "diarrheafrom": [("diarrhea", "diarrhea"), ("from", "from")],
                          "withsputum": [("with", "with"), ("sputum", "sputum")],
                          "stil": [("stil", "still")],
                          "noswolling": [("no", "no"), ("swolling", "swolling")],
                          "hisheadache": [("his", "his"), ("headache", "headache")],
                          "haveshingles": [("have", "have"), ("shingles", "shingles")],
                          "giveshim": [("gives", "gives"), ("him", "him")]
                          }

    def test__get_icd_10_codes_with_relevant_spans__should_return_correct_response__given_correct_input(self):
        mock_icd10_annotations = self.__get_dummy_dictionary()
        no_of_components_in_algorithm = 3

        icd10_filtered_annotations = TextSpanDiscovery().get_icd_10_codes_with_relevant_spans(mock_icd10_annotations,
                                                                                         no_of_components_in_algorithm,
                                                                                         mock_medant_note)


        assert icd10_filtered_annotations[0].begin_offset == 0
        assert icd10_filtered_annotations[0].end_offset == 7

        assert icd10_filtered_annotations[1].begin_offset == 8
        assert icd10_filtered_annotations[1].end_offset == 10

        assert icd10_filtered_annotations[2].begin_offset == 50
        assert icd10_filtered_annotations[2].end_offset == 130

        assert icd10_filtered_annotations[3].begin_offset == 300
        assert icd10_filtered_annotations[3].end_offset == 900

        assert icd10_filtered_annotations[3].suggested_codes[0].code == 'A15.0'
        assert icd10_filtered_annotations[3].suggested_codes[1].code == 'J12.89'
        assert icd10_filtered_annotations[3].suggested_codes[2].code == 'A15.9'

        assert icd10_filtered_annotations[0].medical_condition == mock_medant_note[0:7]
        assert icd10_filtered_annotations[1].medical_condition == mock_medant_note[8:10]
        assert icd10_filtered_annotations[2].medical_condition == mock_medant_note[50:130]
        assert icd10_filtered_annotations[3].medical_condition == mock_medant_note[300:900]
