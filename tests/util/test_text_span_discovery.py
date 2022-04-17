import string
import random
from typing import List
from unittest import TestCase
from app.util import TextSpanDiscovery
from app.service.icd10_text_token_span_gen_service import ICD10TextTokenAndSpanGeneration

class TestSpanDiscovery(TestCase):
    __get_dummy_dictionary = {
                            "this": [("this", "these")],
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
    text_span_discovery_tool: TextSpanDiscovery

    def test__get_icd_10_codes_with_relevant_spans__should_return_correct_response__given_correct_input_setone(self):
        self.text_span_discovery_tool = TextSpanDiscovery()
        span_generator = ICD10TextTokenAndSpanGeneration()
        text = "this is a wellwriten? sentence? we are going to analyz it. this was wellwriten policy. " \
           "so thanks. we have a broadview on this topic."
        ts = span_generator.get_token_with_span(text)
        self.text_span_discovery_tool.generate_metainfo_for_changed_text()

    def test__get_icd_10_codes_with_relevant_spans_should_return_correct_response__give_correct_input_settwo(self):

        self.text_span_discovery_tool = TextSpanDiscovery()
        span_generator = ICD10TextTokenAndSpanGeneration()
        text3 = "He has alot going on, he continues to drinks, daily, " \
                "and he has been feeling dizzy with some fall,he was in the er recently " \
                "and he had a head CT, he still smokes, coughing wheezying breathless, withsputum, " \
                "he stil has urinary incontinent, he has been confirmed to have colon cancer, " \
                "he am not sure he has hallucinations, he not sleeping well, he has chronic urinary and bowel incontinent, " \
                "he also chronic diarrheafrom time to time,  the absence of recurrent leg cramps is obvious"
        ts = span_generator.get_token_with_span(text3)
        self.text_span_discovery_tool.generate_metainfo_for_changed_text()

    def test__get_icd_10_codes_with_relevant_spans_should_return_correct_response__given_correct_input_setthree(self):
        self.text_span_discovery_tool = TextSpanDiscovery()
        span_generator = ICD10TextTokenAndSpanGeneration()
        text4 = "She has hx of dm, cad, cops, depression, and morbid obesity, she is currently having alot of lowbuttock pain, " \
                "the pain is worse at night, she cant seat or put pressure on her buttock, " \
                "there has been noswolling, it is hard to work to tingling no numbness, duration month, " \
                "she also lost her job during covid, she was very depressed but she is feeling better now, " \
                "but she is still smoking, coughing, with sputum inthe morining, with some wheezing, " \
                "although she did loss alot of weight, but over covid she has gained13lbs, " \
                "no tingling no numbness in her feet, no foot ulcers, " \
                "she also stoppd alot of medication hermedication becuase of financial issues He is here for " \
                "followup on his colitis and " \
                "headache.He said his ulcerative colitis flares up and giveshim a hard time doing is school work or job work." \
                "His abdominal pain, N / V comes and goes; sometiomessevere.He said his Gi dr just changed him medicine to Apriso " \
                "which helps sometimes.Hius GI dr hadplan to have his abominal surgery in the future; His Gi dr wants start him on " \
                "Xeljang but he needs to haveshingles shot; which he is not able to get because of his age; " \
                "he is wondering if his PCP can give him aShingle shot. " \
                "He said he has seen neurologist who prescribed him a sumatriptan for hisheadache / migraine and " \
                "this medication is helping him.He has no CP, SOB, coughing and wheezing." \
                "Hehas no other issues reported. Schzophrenia, Hypothyroidism"
        ts = span_generator.get_token_with_span(text4)
        self.text_span_discovery_tool.generate_metainfo_for_changed_text()