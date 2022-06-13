from unittest import TestCase

from app.dto.pipeline.tokenization_component_result import TokenizationResult
from app.service.icd10_text_token_span_gen_service import ICD10TextTokenAndSpanGeneration
from app.util.text_span_discovery import TextSpanDiscovery
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
                            "butock": [("butock", "butox")],
                            "surgial": [("surgial", "surgical")],
                            "suppurative" : [("suppurative", "supportive")]
                          }
    text_span_discovery_tool: TextSpanDiscovery

    def test__get_icd_10_codes_with_relevant_spans__should_return_correct_response__given_correct_input_setone(self,):
        self.text_span_discovery_tool = TextSpanDiscovery(self.get_dummy_dictionary)
        token_generator_with_span = ICD10TextAndSpanGenerationServiceImpl()
        graph_generator = ICD10GenerateGraphFromTextImpl()
        text = "this is a wellwriten? sentence? we are going to analyz it. this was wellwriten policy. " \
           "so thanks. we have a broadview on this topic."
        ts = token_generator_with_span.get_token_with_span(text)
        nodes = graph_generator.process_token_to_create_graph(TokenizationResult(ts))
        updated_token_dict, _ = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, ts)
        assert updated_token_dict["broadview"].get(108, None) != None
        assert updated_token_dict["broadview"][108].parent_token == ""
        assert updated_token_dict["broad"][115].parent_token == "broadview"
        assert updated_token_dict["broad"][115].pos_tracking == 108

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
        nodes = graph_generator.process_token_to_create_graph(TokenizationResult(ts))
        updated_token_dict, _ = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, ts)
        assert updated_token_dict["diarrhea"][407].parent_token == "diarrheafrom"
        assert updated_token_dict["diarrhea"][407].pos_tracking == 405
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
                "but she is still smoking, coughing, with sputum inthe morining, witfgfgfe wheezing, " \
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
        nodes = graph_generator.process_token_to_create_graph(TokenizationResult(ts))
        updated_token_dict, _ = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, ts)
        assert updated_token_dict["swolling"][202].parent_token == "noswolling"
        assert updated_token_dict["swolling"][202].pos_tracking == 199

    def test__get_icd_10_codes_with_relevant_spans_should_return_correct_response__given_correct_input_setfour(self):
        self.text_span_discovery_tool = TextSpanDiscovery(self.get_dummy_dictionary)
        token_generator_with_span = ICD10TextAndSpanGenerationServiceImpl()
        graph_generator = ICD10GenerateGraphFromTextImpl()
        text5 = "She has hx of dm, cad, cops, depression, and morbid obesity, she is currently having alot of lowbuttock pain, " \
            "the pain is worse at night, she cant seat or put pressure on her buttock, " \
            "there has been noswolling, lowbuttock, it is hard to work to tingling no numbness, duration month, "
        text_span = token_generator_with_span.get_token_with_span(text5)
        nodes = graph_generator.process_token_to_create_graph(TokenizationResult(text_span))
        updated_token_dict, new_text_span = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, text_span)
        assert updated_token_dict["buttock"].__contains__(175) is True
        assert updated_token_dict["buttock"][97].parent_token == "lowbuttock"
        assert updated_token_dict["buttock"][97].sub_word == 'buttock'
        assert updated_token_dict["buttock"][175].sub_word == ""
        assert len([each for each in new_text_span if each.token == 'butock']) == 1
        assert len([each for each in new_text_span if each.token == 'butox']) == 0
        updated_token_dict, new_text_span = self.text_span_discovery_tool.generate_metainfo_for_changed_text(updated_token_dict, new_text_span)
        (start_of_span_info, root) = self.text_span_discovery_tool.get_start_end_pos_span(updated_token_dict, "swell", 200, "")
        assert start_of_span_info == 201
        assert root == "swolling"
        (start_of_span_info, root) = self.text_span_discovery_tool.get_start_end_pos_span(updated_token_dict, "swell", 201, "")
        assert start_of_span_info == -1
        assert  root == None
        (start_of_span_info, root) = self.text_span_discovery_tool.get_start_end_pos_span(updated_token_dict, "swelled", 201, "")
        assert start_of_span_info == -1
        assert root == None
        (start_of_span_info, root) = self.text_span_discovery_tool.get_start_end_pos_span(updated_token_dict, "numbness", 253, "")
        assert start_of_span_info == 257
        assert root == "numbness"
        assert len([each for each in new_text_span if each.token == 'butock']) == 2
        assert len([each for each in new_text_span if each.token == 'butox']) == 1
        assert updated_token_dict["swolling"][202].parent_token == "noswolling"
        assert updated_token_dict["swolling"][202].pos_tracking == 199
        assert updated_token_dict["swell"][200].parent_token == "swolling"
        assert updated_token_dict["swell"][200].pos_tracking == 202

    def test__icd_10_text_reconstruction_response__given_correct_ouput_setfive(self):
        self.text_span_discovery_tool = TextSpanDiscovery(self.get_dummy_dictionary)
        token_generator_with_span = ICD10TextAndSpanGenerationServiceImpl()
        graph_generator = ICD10GenerateGraphFromTextImpl()
        text5 = "She has hx of dm, cad, cops, depression, and morbid obesity, she is currently having alot of lowbuttock pain, " \
                "the pain is worse at night, she cant seat or put pressure on her buttock, " \
                "there has been noswolling, lowbuttock, it is hard to work to tingling no numbness, duration month, "
        ts = token_generator_with_span.get_token_with_span(text5)
        nodes = graph_generator.process_token_to_create_graph(TokenizationResult(ts))
        updated_token_dict, new_ts = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, ts)
        text = self.text_span_discovery_tool.improved_text_reconstruction(new_ts)
        assert text.find("buttock") == 97
        assert text.find('swolling') == 202
        updated_token_dict, new_ts = self.text_span_discovery_tool.generate_metainfo_for_changed_text(updated_token_dict, new_ts)
        text = self.text_span_discovery_tool.improved_text_reconstruction(new_ts)
        assert text.find("swell") != -1
        assert text.find("butox")
        assert text.count(',') == 12
        assert text.count("lowbuttock") == 0
        assert text.find("no swell,") != -1

    def test__icd_10_text_reconstruction_response__given_correct_output_set_six(self):
        test_text1 = "CC: Patient presents for a Transitional Care Management exam." \
                     "Date Admitted: **********\n" \
                     "Date Discharged: **********\n" \
                     "Living Environment: Patient lives with relatives her mum is currently home here with ***\n" \
        "Limitations: Patient has physical de-condition No. Is the patient's hearing okay? Yes. Is the patient's\n" \
        "vision okay? Yes. Is the patient's mental status okay? Yes. Does the patient have any dementia? No" \
        "Home Care Services: none\n" \
        "Physical/Occupational therapy:\n" \
        "Ambulation Status:\n" \
        "Continence:\n\n" \
        "HPI: s/p elective excisiion og bilateral suppurative hydradenitis, surgery was complicated by sepsis from" \
        "c diffle she was admited for 3 days, she now feels much , no more fever, no diarrhea, no\n" \
        "breathlessness and the surgial side is healing , but the rt side is leaking some, clear liquid with no smell\n" \
        "ROS:\n" \
        "Const: Denies chills, fever and sweats.\n" \
        "Eyes: Denies a recent change in visual acuity and watery or itching eyes.\n" \
        "ENMT: Denies congestion, excessive sneezing and postnasal drip.\n" \
        "CV: Denies chest pain, orthopnea, palpitations and swelling of ankles.\n" \
        "Resp: Denies cough, PND, SOB, sputum production and wheezing.\n" \
        "GI: Denies abdominal pain, constipation, diarrhea, hematemesis, melena, nausea and vomiting.\n" \
        "GU: Urinary: denies dysuria, frequency, hematuria and change in urine odor.\n" \
        "Skin: Denies rashes.\n" \
        "Neuro: Denies headache, loss of consciousness and vertigo.\n\n." \
        "Const: Appears moderately overweight. No signs of apparent distress present.\n" \
        "Head/Face: Normal on inspection.\n" \
        "ENMT: External Ears: Inspection reveals normal ears. Canals WNL. Nasopharynx: Normal to\n" \
        "inspection. Dentition is normal. Gums appear healthy. Palate normal in appearance.\n" \
        "Neck: Normal to inspection. Normal to palpation. No masses appreciated. No JVD. Carotids: no\n" \
        "bruits.\n" \
        "Resp: Inspection of chest reveals no chest wall deformity. Percussion is resonant and equal. Lungs\n" \
        "are clear bilaterally. Chest is normal to inspection and palpation.\n" \
        "CV: No lifts or thrills. PMI is not displaced. S1 is normal. S2 is normal. No extra sounds. No heart\n" \
        "murmur appreciated. Extremities: No clubbing, cyanosis or edema.\n" \
        "Abdomen: Abdomen is soft, nontender, and nondistended without guarding, rigidity or rebound\n" \
        "tenderness. No abdominal masses. No pulsatile masses present. Abdominal wall is soft. No\n" \
        "palpable hernias. No palpable hepatosplenomegaly. Kidneys are not palpable.\n" \
        "Musculo: Walks with a normal gait. Upper Extremities: Normal to inspection and palpation. Lower\n" \
        "Extremities: Normal to inspection and palpation.\n" \
        "Skin: Skin is warm and dry. Hair appears normal. healing axilla\n\n."

        self.text_span_discovery_tool = TextSpanDiscovery(self.get_dummy_dictionary)
        token_generator_with_span = ICD10TextAndSpanGenerationServiceImpl()
        graph_generator = ICD10GenerateGraphFromTextImpl()
        ts = token_generator_with_span.get_token_with_span(test_text1)
        print(len(ts))

        nodes = graph_generator.process_token_to_create_graph(TokenizationResult(ts))
        updated_token_dict, new_ts = self.text_span_discovery_tool.generate_metainfo_for_changed_text(nodes, ts)

        text = self.text_span_discovery_tool.improved_text_reconstruction(new_ts)
        updated_token_dict, new_ts = self.text_span_discovery_tool.generate_metainfo_for_changed_text(
            updated_token_dict, new_ts)
        (start_of_span_info, root) = self.text_span_discovery_tool.get_start_end_pos_span(updated_token_dict, "surgical", 717, "")
        assert updated_token_dict["surgical"][716].pos_tracking == 717
        assert updated_token_dict["surgial"][717].parent_token == ""
        assert updated_token_dict["supportive"][541].parent_token == "suppurative"