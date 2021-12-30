import time
from unittest import TestCase

from spacy.lang.en import English

from app.dto.core.trie_structure import Trie
from app.dto.pipeline.subjective_section import SubjectiveText
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.settings import Settings
from app.util.english_dictionary import EnglishDictionary


class TestNegationProcesingComponent(TestCase):

    def test__run__should_return_correct_response__given_correct_input(self, ):
        start_time = time.time()
        word = ["new", "dizziness", "anxiety", "appropriate", "breathlessness", "normal", "nothing"]
        root = Trie()
        eng_dict = EnglishDictionary()
        for each_word in word:
            eng_dict.insert_in(each_word, root)
        Settings.set_settings_dictionary(root)
        Settings.set_settings_tokenizer(English())
        print("--- %s seconds ---" % (time.time() - start_time))
        component = NegationHandlingComponent()
        start_time = time.time()
        test_data = "46-year-old male presenting for follow up of his blood pressure. Since his last visit a month ago," \
                    "he has been exercising, going out for walks every other day, compliant with medications. " \
                    " Nonew complaints for today. PAST MEDICAL HISTORY: Obesity, Hypertension, " \
                    "History of glucose intolerance ,Mild hyperlipidemia. MEDICATIONS: Lisinopril 40 mg q.d., " \
                    "Procardia XL 90 mg q.d. PHYSICAL EXAMINATION: Blood pressure today initially 190/108. Subsequently," \
                    " 170/110. Rest of exam was deferred as he had an exam a month ago. ASSESSMENT & PLAN: (1) " \
                    "Hypertension. Outpatient readings support todays reading as the patient as an " \
                    "automatic blood pressure machine. " \
                    "Will add hydrochlorothiazide 25 mg q.d. and come back in 4 days."

        result = component.run({"text": test_data,
                                "acm_cached_result": None, "changed_words": {},
                                SubjectiveSectionExtractorComponent: [SubjectiveText(test_data, [])]})
        print("--- %s seconds ---" % (time.time() - start_time))
        #print(result)
        assert result[0].text.lower().find("no new") != -1
        #assert "no anxiety" in tokens



