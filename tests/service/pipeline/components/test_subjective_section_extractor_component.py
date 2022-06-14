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
        annotation_results["text"] = "\n\nNurse Note: Pt is here for PE\n\nDate: **********\nWas the patient queried about smoking behavior? Yes No" \
                                     "\nDoes the patient currently smoke? Smoking: Patient has never smoked - (********).\n\n" \
                                     "Has pt had any testing done since last visit? Yes No\nHas pt seen any specialist since last visit? Yes No" \
                                     "\nHas pt been to the Hospital or ** since last visit?\n\nYes No\n\nDate: **********\n" \
                                     "Was the patient queried about smoking behavior? Yes No\n" \
                                     "Does the patient currently smoke? Smoking: Patient has never smoked - (********)." \
                                     "\n\nWhooley Depression Screen\n1. During the past month, have you often been bothered by feeling down, " \
                                     "depressed, or hopeless?\n\nYes No\n2. During the past month, have you often been bothered by " \
                                     "little interest or pleasure in doing\n\nthings? Yes No\n\nSubjective\nCC: " \
                                     "Patient presents for general physical exam. here as new pateint pateint, he has recent out break\nof herpes\nHPI: He had a genital herpes out break last week, his girlfriend would like suppressive therapy, he has\nasthma and he uses symbicort, which has kept his asthma under good control, no chest pains no\nbreathlessness no dizzyness\nROS:\nConst: Denies chills, fever and sweats.\nEyes: Denies a recent change in visual acuity and watery or itching eyes.\nENMT: Denies congestion, excessive sneezing and postnasal drip.\nCV: Denies chest pain, orthopnea, palpitations and swelling of ankles.\nResp: Denies cough, PND, SOB, sputum production and wheezing.\nGI: Denies abdominal pain, constipation, diarrhea, hematemesis, melena, nausea and vomiting.\nGU: Urinary: denies dysuria, frequency, hematuria and change in urine odor.\nSkin: Denies rashes.\nNeuro: Denies headache, loss of consciousness and vertigo.\n\nCurrent Meds Prior to Visit:\nAllergies:\n\nPMH:\n(Health Maintenance)\n(Childhood Illness)\nMedical Problems:\nAsthma\n(Accidents/Injuries)\nSurgical Hx:\nNo Past History of Procedure\nReviewed and updated.\n\n\n\n\n\nFH:\nAsthma\nAlcoholism.\nFather:\nAsthma.\nMother:\nNo Current Problems.\nReviewed and updated.\nSH:\nSleep: Reports normal sleep activity.Barriers to Care: Education Status - associate degree, Family\nResponsibilities - he lives with his girlfriend, Financial hardship - no, Geographic location - ****, Insurance\nStatus - commercial, Language - english, Motivation - yes, Pressing health needs - suppressive therapy\nfor genital herpes, Priorities, Transportation - he drives and has bis own car, Work hours - full time,\nSocial Determinants: None identified, Social Functioning: None identified.\nPersonal Habits: Cigarette Use: Never Smoked Cigarettes.Alcohol: consumes 7 beers per\nweek.Drug Use: Formerly used Marijuana sporadically.Daily Caffeine: Consumes on average 1 cup\nof regular coffee per day.\nReviewed and updated.\nCage-Aid Alcohol/Drug Question\n\nObjective\nHt: 69\" 5'9\" Wt: 167lb BP: 137/75 T: 98.7 Pulse: 87 BMI: 24.7 IBW: 160\n\nExam:\nConst: Appears well. No signs of apparent distress present.\nHead/Face: Normal on inspection.\nENMT: External Ears: Inspection reveals normal ears. Canals WNL. Nasopharynx: Normal to\ninspection. Dentition is normal. Gums appear healthy. Palate normal in appearance.\nNeck: Normal to inspection. Normal to palpation. No masses appreciated. No JVD. Carotids: no\nbruits.\nResp: Inspection of chest reveals no chest wall deformity. Percussion is resonant and equal. Lungs\nare clear bilaterally. Chest is normal to inspection and palpation.\nCV: No lifts or thrills. PMI is not displaced. S1 is normal. S2 is normal. No extra sounds. No heart\nmurmur appreciated. Extremities: No clubbing, cyanosis or edema.\nAbdomen: Abdomen is soft, nontender, and nondistended without guarding, rigidity or rebound\ntenderness. No abdominal masses. No pulsatile masses present. Abdominal wall is soft. No\npalpable hernias. No palpable hepatosplenomegaly. Kidneys are not palpable.\nGU: No hernias. Scrotum: Unremarkable. Testes are normal on palpation. No testicular masses\nnoted. Bladder: Non distended. Rectum: Rectal walls smooth, no masses or tenderness. Prostate:\nSymmetric, smooth w/o nodules and nontender. Hematest: negative.\nLymph: No palpable or visible regional lymphadenopathy.\nMusculo: Walks with a normal gait. Upper Extremities: Normal to inspection and palpation. Lower\nExtremities: Normal to inspection and palpation.\nSkin: Skin is warm and dry. Hair appears normal.\nNeuro: Alert and oriented x3. Mood is normal. Affect is normal.\nPsych: Language/Thought: Speech is clear and appropriate for age.\n\nSocial Functioning/Determinants of Health\n\n1. Does the patient find it difficult to interact with others or maintain an adequate social life? No\n\n\n\n\n\n2. Does the patient find it difficult to meet the daily needs of food, housing or transportation? No\n\nBarriers to Care: Education Status - associate degree, Family Responsibilities - he lives with his\ngirlfriend, Financial hardship - no, Geographic location - ****, Insurance Status - commercial, Language -\nenglish, Motivation - yes, Pressing health needs - suppressive therapy for genital herpes, Priorities,\nTransportation - he drives and has bis own car, Work hours - full time, Social Determinants: None\nidentified, Social Functioning: None identified.\n\nYes No Comments\nCommunity Resources Provided\n\nMedication Review Completed : Yes No N/A\nPain Screening: Yes No N/A\nPain Level\n\nBMI\nAssessment #1: Z00.00 Encounter for general adult medical examination without abno\nCare Plan:\nComments : balanced healthy diet,exercise, no smoking, no drinking, safe sex,\n\nAssessment #2: A60.02 Herpesviral infection of other male genital organs\nCare Plan:\nMed New : Valacyclovir HCL 500 mg 1 by mouth twice a day\n\nAssessment #3: J45.909 Unspecified asthma, uncomplicated\nCare Plan:\nComments : his current medication is controlling his asthma\n\nAssessment #4: Z70.9 Sex counseling, unspecified\nCare Plan:\nComments : educated about sex sex, abstinence is prefered\n\nuse of condom\nkeep to monogamous relationship\n\nAssessment #5: Z71.82 Exercise counseling\nCare Plan:\nComments : encouraged 1hr aerobic exercise, 3 times per week, or even walking\n\nAssessment #6: Z71.3 Dietary counseling and surveillance\nCare Plan:\nComments : educated on balanced diet, to typicall aviod, snacks, starchy food\n\nAssessment #7: Z68.24 Body mass index (BMI) 24.0-24.9, adult\nCare Plan:\n\nPlan Other:\n\nMed New : Symbicort 80-4.5 mcg/Act\n" \
                                     "inhale 2 puffs by mouth twice a day\n(rinse mouth after use)\nVentolin HFA 108 (90 Base) mcg/Act\n1-2 puff q4-6hrs as needed\n\n" \
                                     "Follow Up : see in 6 months\n\n\n\n\n\nTreatment Plan discussed with patient.\nMedications have been reviewed and discussed with patient." \
                                     "\nPatient verbalizes understanding of discussion.\nRisk Assessment\n\nOne or more Acute Unstable Illnesses Yes No\n\n" \
                                     "Three or more Chronic Medical Conditions Yes No\n\nMultiple ER Visits Yes No\n\nFinancial Difficulties Yes No\n\nLow Social Economics Yes No\n\nMental Illness Yes No" \
                                     "\n\nPoor Medical Compliance Yes No\n\nDrug Abuse or Dependence Yes No\n\nLanguage Barrier Yes No\n\nPolypharmacy Yes No\n\nRisk Low Medium High\n\n"
        subjective_section = extractor_component.run(annotation_results)[0]
        print(len(subjective_section.subjective_sections))
        #print(subjective_section.subjective_sections[1].text)