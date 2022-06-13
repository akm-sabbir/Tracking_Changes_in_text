from unittest import TestCase
from unittest.mock import Mock

from app.service.medeant.medant_note_section_service import MedantNoteSectionService
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent


class TestSubjectiveSectionExtractorComponent(TestCase):
    def test__run__should_return_correct_response__given_correct_input(self):
        extractor_component = SubjectiveSectionExtractorComponent()

        mock_section_1 = Mock()
        mock_section_1.group = Mock()
        mock_section_1.start = Mock()
        mock_section_1.end = Mock()
        mock_section_1.group.return_value = "section 1"
        mock_section_1.start.return_value = 20
        mock_section_1.end.return_value = 29

        mock_section_2 = Mock()
        mock_section_2.group = Mock()
        mock_section_2.start = Mock()
        mock_section_2.end = Mock()
        mock_section_2.group.return_value = "section 2"
        mock_section_2.start.return_value = 100
        mock_section_2.end.return_value = 109

        mock_note_section_service = Mock(MedantNoteSectionService)
        mock_note_section_service.get_subjective_sections = Mock()
        mock_note_section_service.get_subjective_sections.return_value = [mock_section_1, mock_section_2]
        extractor_component.note_section_service = mock_note_section_service

        subjective_section = extractor_component.run(annotation_results={"text": "some text"})[0]
        assert subjective_section.text == "section 1. section 2."

        assert subjective_section.subjective_sections[0].text == "section 1. "
        assert subjective_section.subjective_sections[0].start == 20
        assert subjective_section.subjective_sections[0].end == 29
        assert subjective_section.subjective_sections[0].relative_start == 0
        assert subjective_section.subjective_sections[0].relative_end == 11

        assert subjective_section.subjective_sections[1].text == "section 2."
        assert subjective_section.subjective_sections[1].start == 100
        assert subjective_section.subjective_sections[1].end == 109
        assert subjective_section.subjective_sections[1].relative_start == 11
        assert subjective_section.subjective_sections[1].relative_end == 21

    def test__run__should_return_correct_response__given_input_with_no_subjective_part(self):
        extractor_component = SubjectiveSectionExtractorComponent()

        mock_note_section_service = Mock(MedantNoteSectionService)
        mock_note_section_service.get_subjective_sections = Mock()
        mock_note_section_service.get_subjective_sections.return_value = []

        subjective_section = extractor_component.run(annotation_results={"text": "some text"})[0]

        assert subjective_section.subjective_sections[0].text == "some text"
        assert subjective_section.subjective_sections[0].start == 0
        assert subjective_section.subjective_sections[0].end == 9
        assert subjective_section.subjective_sections[0].relative_start == 0
        assert subjective_section.subjective_sections[0].relative_end == 9

    def test__run_should_return_correct_response__given_large_text_input(self):
        extractor_component = SubjectiveSectionExtractorComponent()
        annotation_results = {}
        annotation_results["text"] = "\n\n***** Note: Pt is here due to a Hospital visit, Pt was told she had C-Diff."\
        "she is also getting staples\nremoved on R-shoulder on **********.\n\nDate: **********\nWas the patient queried " \
        "about smoking behavior? Yes No\nDoes the patient currently smoke? Smoking: Patient has never smoked - (********)." \
        "\n\nHas pt had any testing done since last visit? Yes No IN hospital\nHas pt seen any specialist since last visit? " \
        "Yes No\nHas pt been to the Hospital or ** since last visit?\n\n" \
        "Yes No ********** in ******\n\nSubjective\nCC: Patient presents for a Transitional " \
        "Care Management exam.\n\nDate Admitted: **********\nDate Discharged: **********\n" \
        "Living Environment: Patient lives with relatives her mum is currently home here with " \
        "***\nLimitations: Patient has physical de-condition No. Is the patient's hearing okay? " \
        "Yes. Is the patient's\nvision okay? Yes. Is the patient's mental status okay? " \
        "Yes. Does the patient have any dementia? No\nHome Care Services: none\nPhysical/Occupational therapy:\nAmbulation " \
        "Status:\nContinence:\n\nHPI: s/p elective excisiion og bilateral suppurative hydradenitis, surgery was complicated by sepsis from\nc diffle she was admited for 3 days, she now feels much , no more fever, no diarrhea, no\nbreathlessness and the surgial side is healing , but the rt side is leaking some, clear liquid with no smell\nROS:\nConst: Denies chills, fever and sweats.\nEyes: Denies a recent change in visual acuity and watery or itching eyes.\nENMT: Denies congestion, excessive sneezing and postnasal drip.\nCV: Denies chest pain, orthopnea, palpitations and swelling of ankles.\nResp: Denies cough, PND, SOB, sputum production and wheezing.\nGI: Denies abdominal pain, constipation, diarrhea, hematemesis, melena, nausea and vomiting.\nGU: Urinary: denies dysuria, frequency, hematuria and change in urine odor.\nSkin: Denies rashes.\nNeuro: Denies headache, loss of consciousness and vertigo.\n\nCurrent Meds Prior to Visit: Sulfamethoxazole/Trimethoprim DS 800-160 mg\nAllergies: NKDA\n\nPMH:\n(Health Maintenance)\n(Childhood Illness)\nMedical Problems:\nObesity\n\n\n\n\n\n(Accidents/Injuries)\nSurgical Hx:\nbilateral excision of axillary skin\nReviewed and updated.\nFH:\nHypertension\nHeart Disease.\nFather:\nHeart Disease.\nMother:\nHypertension.\nReviewed, no changes.\nSH:\nSleep: Reports normal sleep activity.Barriers to Care: Education Status - masters in mental health\ncounselling, Family Responsibilities - lives alone, Financial hardship - no, ****************************,\nInsurance Status - commercial, Language - english, Motivation - yes, Pressing health needs - weight loss,\nPriorities - weight loss, Transportation, Work hours - full time.\nPersonal Habits: Cigarette Use: Never Smoked Cigarettes.Alcohol: Rarely consumes wine.Drug\nUse: Never Used Drugs.Daily Caffeine: 1 cup per week.\nReviewed, no changes.\n\nObjective\nHt: 62\" 5'2\" Wt: 183lb Wt Prior: 190lb as of ******** Wt Dif: -7lb BP: 109/71 T: 98.4 Pulse: 59 Resp:\n18 BMI: 33.5 IBW: 110\n\nExam:\nConst: Appears moderately overweight. No signs of apparent distress present.\nHead/Face: Normal on inspection.\nENMT: External Ears: Inspection reveals normal ears. Canals WNL. Nasopharynx: Normal to\ninspection. Dentition is normal. Gums appear healthy. Palate normal in appearance.\nNeck: Normal to inspection. Normal to palpation. No masses appreciated. No JVD. Carotids: no\nbruits.\nResp: Inspection of chest reveals no chest wall deformity. Percussion is resonant and equal. Lungs\nare clear bilaterally. Chest is normal to inspection and palpation.\nCV: No lifts or thrills. PMI is not displaced. S1 is normal. S2 is normal. No extra sounds. No heart\nmurmur appreciated. Extremities: No clubbing, cyanosis or edema.\nAbdomen: Abdomen is soft, nontender, and nondistended without guarding, rigidity or rebound\ntenderness. No abdominal masses. No pulsatile masses present. Abdominal wall is soft. No\npalpable hernias. No palpable hepatosplenomegaly. Kidneys are not palpable.\nMusculo: Walks with a normal gait. Upper Extremities: Normal to inspection and palpation. Lower\nExtremities: Normal to inspection and palpation.\nSkin: Skin is warm and dry. Hair appears normal. healing axilla\n\nMedication Review Completed : Yes No N/A\n\n\n\n\n\nPain Screening: Yes No N/A\nLevel\n\nBMI\nAssessment #1: A04.72 Enterocolitis due to Clostridium difficile, not specified as recurrent\nCare Plan:\nMed New : Florastor 250 mg 1 by mouth twice a day\n\nAssessment #2: L73.2 Hidradenitis suppurativa\nCare Plan:\n\nPlan Other:\n\nTreatment Plan discussed with patient.\nMedications have been reviewed and discussed with patient.\nPatient verbalizes understanding of discussion.\n\nSeen by:\n\nElectronically signed by ***************, MD on ********** at  8:22 pm\n\n\n"
        subjective_section = extractor_component.run(annotation_results)[0]
        print(len(subjective_section.subjective_sections))
        #print(subjective_section.subjective_sections[1].text)
        print(subjective_section.text)