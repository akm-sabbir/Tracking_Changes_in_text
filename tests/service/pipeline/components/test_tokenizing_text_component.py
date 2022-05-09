import time
from unittest import TestCase

from spacy.lang.en import English

from app.dto.core.trie_structure import Trie
from app.dto.pipeline.medication_section import MedicationText
from app.dto.pipeline.subjective_section import SubjectiveText
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.settings import Settings
from app.util.english_dictionary import EnglishDictionary
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent


class TestTextTokenizationComponent(TestCase):

    def test__run__should_return_correct_response__given_correct_input(self, ):
        word = ["new", "dizziness", "anxiety", "appropriate", "breathlessness", "normal", "nothing", "pain"]
        root = Trie()
        eng_dict = EnglishDictionary()
        for each_word in word:
            eng_dict.insert_in(each_word, root)
        Settings.set_settings_dictionary(root)
        Settings.set_settings_tokenizer(English())
        component = TextTokenizationComponent()
        test_data2 = "Meds : Vyvanse 50 mgs po at breakfast daily," \
                     "Clonidine 0.2 mgs -- 1 and 1 / 2 tabs po qhs nopain"

        first_test_result = component.run({"text": test_data2,
                                "acm_cached_result": None, "changed_words": {},
                                SubjectiveSectionExtractorComponent: [SubjectiveText(test_data2, [])],
                                MedicationSectionExtractorComponent: [MedicationText(test_data2, [])],
                                })
        assert first_test_result[0].token_container[4].token == 'mgs'
        assert first_test_result[0].token_container[10].token == 'Clonidine'
        assert first_test_result[0].token_container[10].start_of_span == 44
        assert first_test_result[0].token_container[10].end_of_span == 53
        assert first_test_result[0].token_container[10].offset == 0
        assert first_test_result[0].token_container[17].token == '1'
        test_data = "46-year-old male presenting for follow up of his blood pressure. Since his last visit a month ago," \
                    "he has been exercising, going out for walks every other day, compliant with medications. " \
                    " Nonew complaints for today. PAST MEDICAL HISTORY: Obesity, Hypertension, " \
                    "History of glucose intolerance ,Mild hyperlipidemia. MEDICATIONS: Lisinopril 40 mg q.d., " \
                    "Procardia XL 90 mg q.d. PHYSICAL EXAMINATION: Blood pressure today initially 190/108. Subsequently," \
                    " 170/110. Rest of exam was deferred as he had an exam a month ago. ASSESSMENT & PLAN: (1) " \
                    "Hypertension. Outpatient readings support todays reading as the patient as an " \
                    "automatic blood pressure machine. " \
                    "Will add hydrochlorothiazide 25 mg q.d. and come back in 4 days."

        second_test_result = component.run({"text": test_data,
                                "acm_cached_result": None, "changed_words": {},
                                SubjectiveSectionExtractorComponent:[SubjectiveText(test_data, [])],
                                MedicationSectionExtractorComponent:[MedicationText(test_data,[])]})

        assert second_test_result[0].token_container[0].token == '46-year-old'
        assert second_test_result[0].token_container[0].start_of_span == 0
        assert second_test_result[0].token_container[0].end_of_span == 11
        assert second_test_result[0].token_container[0].offset == 0
        assert second_test_result[0].token_container[1].token == 'male'
        assert second_test_result[0].token_container[1].start_of_span == 12
        assert second_test_result[0].token_container[1].end_of_span == 16
        assert second_test_result[0].token_container[1].offset == 0
        assert second_test_result[0].token_container[11].start_of_span == 65
        assert second_test_result[0].token_container[11].end_of_span == 70
        assert second_test_result[0].token_container[11].offset == 0
        assert second_test_result[0].token_container[11].token == "Since"