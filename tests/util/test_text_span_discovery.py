from unittest import TestCase

from app.service.icd10_text_token_span_gen_service import ICD10TextTokenAndSpanGeneration
from app.util.TextSpanDiscovery import TextSpanDiscovery
from app.service.impl.icd10_text_token_span_gen_service_impl import ICD10TextAndSpanGenerationServiceImpl
from app.service.impl.icd10_generate_graph_from_text_impl import ICD10GenerateGraphFromTextImpl

class TestSpanDiscovery(TestCase):
    get_dummy_dictionary = {
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
                             "swolling" : [("swolling", "swell")],
                            "hisheadache": [("his", "his"), ("headache", "headache")],
                            "haveshingles": [("have", "have"), ("shingles", "shingles")],
                            "giveshim": [("gives", "gives"), ("him", "him")],
                            "lowbuttock": [("low", "low"), ("buttock", "buttock")],
                            "buttock": [("buttock", "butock")],
                            "butock": [("butock", "butox")]
                          }
    text_span_discovery_tool: TextSpanDiscovery

    def test__get_icd_10_codes_with_relevant_spans__should_return_correct_response__given_correct_input_setone(self,):
        self.text_span_discovery_tool = TextSpanDiscovery(self.get_dummy_dictionary)
        token_generator_with_span = ICD10TextAndSpanGenerationServiceImpl()
        graph_generator = ICD10GenerateGraphFromTextImpl()
        text = "this is a wellwriten? sentence? we are going to analyz it. this was wellwriten policy. " \
           "so thanks. we have a broadview on this topic."
        ts = token_generator_with_span.get_token_with_span(text)
        nodes = graph_generator.process_token_to_create_graph(ts)
        updated_token_dict, _ = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, ts)
        assert updated_token_dict["broadview"].get(108, None) != None
        assert updated_token_dict["broadview"][108].parent_token == ""
        assert updated_token_dict["broad"][115].parent_token == "broadview"
        assert updated_token_dict["broad"][115].pos_tracking[115] == 108

    def test__get_icd_10_codes_with_relevant_spans_should_return_correct_response__give_correct_input_settwo(self):

        self.text_span_discovery_tool = TextSpanDiscovery(self.get_dummy_dictionary)
        token_generator_with_span = ICD10TextAndSpanGenerationServiceImpl()
        graph_generator = ICD10GenerateGraphFromTextImpl()
        text3 = "He has alot going on, he continues to drinks, daily, " \
                "and he has been feeling dizzy with some fall,he was in the er recently " \
                "and he had a head CT, he still smokes, coughing wheezying breathless, withsputum, " \
                "he stil has urinary incontinent, he has been confirmed to have colon cancer, " \
                "he am not sure he has hallucinations, he not sleeping well, he has chronic urinary and bowel incontinent, " \
                "he also chronic diarrheafrom time to time,  the absence of recurrent leg cramps is obvious"
        ts = token_generator_with_span.get_token_with_span(text3)
        nodes = graph_generator.process_token_to_create_graph(ts)
        updated_token_dict, _ = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, ts)
        assert updated_token_dict["diarrhea"][407].parent_token == "diarrheafrom"
        assert updated_token_dict["diarrhea"][407].pos_tracking[407] == 405
        assert updated_token_dict["diarrhea"][407].is_root == False
        assert updated_token_dict["diarrhea"][407].length == 8

    def test__get_icd_10_codes_with_relevant_spans_should_return_correct_response__given_correct_input_setthree(self):
        self.text_span_discovery_tool = TextSpanDiscovery(self.get_dummy_dictionary)
        token_generator_with_span = ICD10TextAndSpanGenerationServiceImpl()
        graph_generator = ICD10GenerateGraphFromTextImpl()
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
        ts = token_generator_with_span.get_token_with_span(text4)
        nodes = graph_generator.process_token_to_create_graph(ts)
        updated_token_dict, _ = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, ts)
        assert updated_token_dict["swolling"][202].parent_token == "noswolling"
        assert updated_token_dict["swolling"][202].pos_tracking[202] == 199

    def test__get_icd_10_codes_with_relevant_spans_should_return_correct_response__given_correct_input_setfour(self):
        self.text_span_discovery_tool = TextSpanDiscovery(self.get_dummy_dictionary)
        token_generator_with_span = ICD10TextAndSpanGenerationServiceImpl()
        graph_generator = ICD10GenerateGraphFromTextImpl()
        text5 = "She has hx of dm, cad, cops, depression, and morbid obesity, she is currently having alot of lowbuttock pain, " \
            "the pain is worse at night, she cant seat or put pressure on her buttock, " \
            "there has been noswolling, it is hard to work to tingling no numbness, duration month, "
        ts = token_generator_with_span.get_token_with_span(text5)
        nodes = graph_generator.process_token_to_create_graph(ts)
        updated_token_dict, new_ts = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, ts)
        assert updated_token_dict["buttock"].__contains__(175) == True
        assert updated_token_dict["buttock"][97].parent_token == "lowbuttock"
        assert updated_token_dict["buttock"][97].sub_word == 'buttock'
        assert updated_token_dict["buttock"][175].sub_word == ""
        assert len([each for each in new_ts if each[0] == 'butock']) == 1
        assert len([each for each in new_ts if each[0] == 'butox']) == 0
        updated_token_dict, new_ts = self.text_span_discovery_tool.generate_metainfo_for_changed_text(updated_token_dict, new_ts)
        (span_info, root) = self.text_span_discovery_tool.get_start_end_pos_span(updated_token_dict, "swell", 200, "")
        assert span_info == 201
        assert root == 8
        (span_info, root) = self.text_span_discovery_tool.get_start_end_pos_span(updated_token_dict, "swell", 201, "")
        assert span_info == -1
        assert  root == None
        (span_info, root) = self.text_span_discovery_tool.get_start_end_pos_span(updated_token_dict, "swelled", 201, "")
        assert  span_info == -1
        assert  root == None
        assert len([each for each in new_ts if each[0] == 'butock']) == 1
        assert len([each for each in new_ts if each[0] == 'butox']) == 1
        assert updated_token_dict["swolling"][202].parent_token == "noswolling"
        assert updated_token_dict["swolling"][202].pos_tracking[202] == 199
        assert updated_token_dict["swell"][200].parent_token == "swolling"
        assert updated_token_dict["swell"][200].pos_tracking[200] == 202