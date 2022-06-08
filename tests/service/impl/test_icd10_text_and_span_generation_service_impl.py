from unittest import TestCase
from unittest.mock import patch, Mock
from app.service.impl.icd10_text_token_span_gen_service_impl import ICD10TextAndSpanGenerationServiceImpl


class TestICD10TextAndSpanGenerationServiceImplTest(TestCase):
    icd10TextTokenGenerator: ICD10TextAndSpanGenerationServiceImpl

    def test__get_text_tokenized_and_span_should_return_proper_data(self) -> None:
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        test_text1 = "as the patient queried about smoking behavior? Yes No\n" \
               "Does the patient currently smoke? Smoking: Patient has never smoked - (1/21/2020).\n"
        test_result1 = self.icd10TextTokenGenerator.get_token_with_span(test_text1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        count = sum([1 if actual_test_result1[i][0] == '?' else 0 for i in range(len(actual_test_result1))])
        count_paren = sum([1 if actual_test_result1[i][0] == '(' else 0 for i in range(len(actual_test_result1))])
        count_colon = sum([1 if actual_test_result1[i][0] == ':' else 0 for i in range(len(actual_test_result1))])
        assert count == 2
        assert count_paren == 1
        assert count_colon == 1
        assert actual_test_result1[2][1] == 7
        assert actual_test_result1[2][2] == 14
        assert actual_test_result1[6][0] == "behavior"

    def test__get_text_tokenized_and_span_should_return_proper_data_second_set(self) -> None:
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        test_text1 = "He has alot going on, he continues to drinks, daily, " \
           "and he has been feeling dizzy with some fall,he was in the er recently " \
           "and he had a head CT, he still smokes, coughing wheezying breathless, withsputum, " \
           "he stil has urinary incontinent, he has been confirmed to have colon cancer, " \
           "he am not sure he has hallucinations, he not sleeping well, he has chronic urinary and bowel incontinent, " \
           "he also chronic diarrheafrom time to time,  the absence of recurrent leg cramps is obvious"
        test_result1 = self.icd10TextTokenGenerator.get_token_with_span(test_text1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        count = sum([1 if actual_test_result1[i][0] == ',' else 0 for i in range(len(actual_test_result1))])
        assert actual_test_result1[2][1] == 7
        assert actual_test_result1[2][2] == 11
        assert actual_test_result1[7][0] == "continues"
        assert  actual_test_result1[11][0] == "daily"
        assert actual_test_result1[21][0] == 'fall'
        assert actual_test_result1[50][0] == 'incontinent'
        assert count == 14

    def test__get_text_tokenized_and_span_should_return_proper_data_third_set(self):
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        test_text2= "He said his ulcerative colitis flares up and giveshim a hard time doing is school work or job work." \
        " His abdominal pain, N / V comes and goes; sometiomessevere."
        test_result2 = self.icd10TextTokenGenerator.get_token_with_span(test_text2)
        actual_test_result2 = self.icd10TextTokenGenerator.process_each_token(test_result2)
        count = sum([1 if actual_test_result2[i][0] == '/' else 0 for i in range(len(actual_test_result2))])
        assert actual_test_result2[2][1] == 8
        assert actual_test_result2[2][2] == 11
        assert actual_test_result2[30][0] == ";"
        assert count == 1

    def test_get_text_tokenized_and_span_should_return_proper_data_fourth_set(self):
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        test_text2 = "\n\n***** Note: Pt is here due to a Hospital visit, Pt was told she had C-Diff. she is also getting staples\nremoved on R-shoulder on **********." \
                     "\n\nDate: **********\nWas the patient queried about smoking behavior? Yes No" \
                     "\nDoes the patient currently smoke? Smoking: Patient has never smoked - (********)." \
                     "\n\nHas pt had any testing done since last visit? Yes No IN hospital\nHas pt seen any specialist since last visit? Yes No" \
                     "\nHas pt been to the Hospital or ** since last visit?" \
                     "\n\nYes No ********** in ******\n\nSubjective\nCC: Patient presents for a Transitional Care Management exam." \
                     "\n\nDate Admitted: **********\nDate Discharged: **********" \
                     "\nLiving Environment: Patient lives with relatives her mum is currently home here with ***" \
                     "\nLimitations: Patient has physical de-condition No. Is the patient's hearing okay? Yes. Is the patient's" \
                     "\nvision okay? Yes. Is the patient's mental status okay? Yes. Does the patient have any dementia? No" \
                     "\nHome Care Services: none\nPhysical/Occupational therapy:\nAmbulation Status:\nContinence:" \
                     "\n\nHPI: s/p elective excisiion og bilateral suppurative hydradenitis, surgery was complicated by sepsis from\n" \
                     "c diffle she was admited for 3 days, she now feels much , no more fever, no diarrhea, no" \
                     "\nbreathlessness and the surgial side is healing , but the rt side is leaking some, clear liquid with no smell\n" \
                     "ROS:\nConst: Denies chills, fever and sweats." \
                     "\nEyes: Denies a recent change in visual acuity and watery or itching eyes." \
                     "\nENMT: Denies congestion, excessive sneezing and postnasal drip.\nCV: Denies chest pain, orthopnea, " \
                     "palpitations and swelling of ankles." \
                     "\nResp: Denies cough, PND, SOB, sputum production and wheezing." \
                     "\nGI: Denies abdominal pain, constipation, diarrhea, hematemesis, melena, nausea and vomiting." \
                     "\nGU: Urinary: denies dysuria, frequency, hematuria and change in urine odor." \
                     "\nSkin: Denies rashes.\nNeuro: Denies headache, loss of consciousness and vertigo.' \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                '\n\nCurrent Meds Prior to Visit: Sulfamethoxazole/Trimethoprim DS 800-160 mg\nAllergies: NKDA\n\nPMH:\n(Health Maintenance)\n(Childhood Illness)\nMedical Problems:\nObesity\n\n\n\n\n\n(Accidents/Injuries)\nSurgical Hx:\nbilateral excision of axillary skin\nReviewed and updated.\nFH:\nHypertension\nHeart Disease.\nFather:\nHeart Disease.\nMother:\nHypertension.\nReviewed, no changes.\nSH:\nSleep: Reports normal sleep activity.Barriers to Care: Education Status - masters in mental health\ncounselling, Family Responsibilities - lives alone, Financial hardship - no, ****************************,\nInsurance Status - commercial, Language - english, Motivation - yes, Pressing health needs - weight loss,\nPriorities - weight loss, Transportation, Work hours - full time.\nPersonal Habits: Cigarette Use: Never Smoked Cigarettes.Alcohol: Rarely consumes wine.Drug\nUse: Never Used Drugs.Daily Caffeine: 1 cup per week.\nReviewed, no changes.\n\nObjective\nHt: 62\" 5'2\" Wt: 183lb Wt Prior: 190lb as of ******** Wt Dif: -7lb BP: 109/71 T: 98.4 Pulse: 59 Resp:\n18 BMI: 33.5 IBW: 110\n\nExam:\nConst: Appears moderately overweight. No signs of apparent distress present.\nHead/Face: Normal on inspection.\nENMT: External Ears: Inspection reveals normal ears. Canals WNL. Nasopharynx: Normal to\ninspection. Dentition is normal. Gums appear healthy. Palate normal in appearance.\nNeck: Normal to inspection. Normal to palpation. No masses appreciated. No JVD. Carotids: no\nbruits.\nResp: Inspection of chest reveals no chest wall deformity. Percussion is resonant and equal. Lungs\nare clear bilaterally. Chest is normal to inspection and palpation.\nCV: No lifts or thrills. PMI is not displaced. S1 is normal. S2 is normal. No extra sounds. No heart\nmurmur appreciated. Extremities: No clubbing, cyanosis or edema.\nAbdomen: Abdomen is soft, nontender, and nondistended without guarding, rigidity or rebound\ntenderness. No abdominal masses. No pulsatile masses present. Abdominal wall is soft. No\npalpable hernias. No palpable hepatosplenomegaly. Kidneys are not palpable.\nMusculo: Walks with a normal gait. Upper Extremities: Normal to inspection and palpation. Lower\nExtremities: Normal to inspection and palpation.\nSkin: Skin is warm and dry. Hair appears normal. healing axilla\n\nMedication Review Completed : Yes No N/A\n\n\n\n\n\nPain Screening: Yes No N/A\nLevel\n\nBMI\nAssessment #1: A04.72 Enterocolitis due to Clostridium difficile, not specified as recurrent\nCare Plan:\nMed New : Florastor 250 mg 1 by mouth twice a day\n\nAssessment #2: L73.2 Hidradenitis suppurativa\nCare Plan:\n\nPlan Other:\n\nTreatment Plan discussed with patient.\nMedications have been reviewed and discussed with patient.\nPatient verbalizes understanding of discussion." \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           "\n\nSeen by:\n\nElectronically signed by ***************, MD on ********** at  8:22 pm\n\n\n"
        test_result2 = self.icd10TextTokenGenerator.get_token_with_span(test_text2)
        actual_test_result2 = self.icd10TextTokenGenerator.process_each_token(test_result2)
        print(actual_test_result2)
