from unittest import TestCase

from spacy.lang.en import English

from app.dto.core.trie_structure import Trie
from app.dto.pipeline.medication_section import MedicationText
from app.dto.pipeline.subjective_section import SubjectiveText
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.settings import Settings
from app.util.english_dictionary import EnglishDictionary


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
        assert first_test_result[0].token_container[10].token == 'clonidine'
        assert first_test_result[0].token_container[10].start_of_span == 44
        assert first_test_result[0].token_container[10].end_of_span == 53
        assert first_test_result[0].token_container[10].offset == 0
        assert first_test_result[0].token_container[17].token == '1'
        assert first_test_result[0].token_container[17].token == '1'
        test_data3 = ": Sulfamethoxazole/Trimethoprim DS 800-160 mg\n. : Florastor 250 mg 1 by mouth twice a day"

        third_test_result = component.run({"text": test_data3,
                                           "acm_cached_result": None, "changed_words": {},
                                           SubjectiveSectionExtractorComponent: [SubjectiveText(test_data3, [])],
                                           MedicationSectionExtractorComponent: [MedicationText(test_data3, [])],
                                           })
        assert third_test_result[0].token_container[2].token == 'or'
        assert third_test_result[0].token_container[3].token == 'trimethoprim'
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
        assert second_test_result[0].token_container[11].token == "since"

        test_data4 = "CC: Patient presents for a Transitional Care Management exam." \
                     "Date Admitted: **********\n" \
                    "Date Discharged: **********\n"\
                    "Living Environment: Patient lives with relatives her mum is currently home here with ***\n"
        "Limitations: Patient has physical de-condition No. Is the patient's hearing okay? Yes. Is the patient's\n"
        "vision okay? Yes. Is the patient's mental status okay? Yes. Does the patient have any dementia? No"\
        "Home Care Services: none\n"
        "Physical/Occupational therapy:\n"
        "Ambulation Status:\n"
        "Continence:\n\n"
        "HPI: s/p elective excisiion og bilateral suppurative hydradenitis, surgery was complicated by sepsis from"
        "c diffle she was admited for 3 days, she now feels much , no more fever, no diarrhea, no\n"
        "breathlessness and the surgial side is healing , but the rt side is leaking some, clear liquid with no smell\n"
        "ROS:\n"
        "Const: Denies chills, fever and sweats.\n"
        "Eyes: Denies a recent change in visual acuity and watery or itching eyes.\n"
        "ENMT: Denies congestion, excessive sneezing and postnasal drip.\n"
        "CV: Denies chest pain, orthopnea, palpitations and swelling of ankles.\n"
        "Resp: Denies cough, PND, SOB, sputum production and wheezing.\n"
        "GI: Denies abdominal pain, constipation, diarrhea, hematemesis, melena, nausea and vomiting.\n"
        "GU: Urinary: denies dysuria, frequency, hematuria and change in urine odor.\n"
        "Skin: Denies rashes.\n"
        "Neuro: Denies headache, loss of consciousness and vertigo.\n\n."
        "Const: Appears moderately overweight. No signs of apparent distress present.\n"
        "Head/Face: Normal on inspection.\n"
        "ENMT: External Ears: Inspection reveals normal ears. Canals WNL. Nasopharynx: Normal to\n"
        "inspection. Dentition is normal. Gums appear healthy. Palate normal in appearance.\n"
        "Neck: Normal to inspection. Normal to palpation. No masses appreciated. No JVD. Carotids: no\n"
        "bruits.\n"
        "Resp: Inspection of chest reveals no chest wall deformity. Percussion is resonant and equal. Lungs\n"
        "are clear bilaterally. Chest is normal to inspection and palpation.\n"
        "CV: No lifts or thrills. PMI is not displaced. S1 is normal. S2 is normal. No extra sounds. No heart\n"
        "murmur appreciated. Extremities: No clubbing, cyanosis or edema.\n"
        "Abdomen: Abdomen is soft, nontender, and nondistended without guarding, rigidity or rebound\n"
        "tenderness. No abdominal masses. No pulsatile masses present. Abdominal wall is soft. No\n"
        "palpable hernias. No palpable hepatosplenomegaly. Kidneys are not palpable.\n"
        "Musculo: Walks with a normal gait. Upper Extremities: Normal to inspection and palpation. Lower\n"
        "Extremities: Normal to inspection and palpation.\n"
        "Skin: Skin is warm and dry. Hair appears normal. healing axilla\n\n."

    def test__run__should_return_empty__given_cache_present(self):
        component = TextTokenizationComponent()
        result = component.run({"text": "some text.\n\nSome other text", 'acm_cached_result': ["some data"]})
        assert result == []