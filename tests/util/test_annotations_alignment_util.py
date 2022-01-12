from unittest import TestCase
from unittest.mock import Mock

from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.changed_word_annotation import ChangedWordAnnotation
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.pipeline.medication_section import MedicationText, MedicationSection
from app.dto.pipeline.negation_component_result import NegationResult
from app.dto.pipeline.rxnorm_annotation import RxNormAnnotation
from app.dto.pipeline.rxnorm_annotation_result import RxNormAnnotationResult
from app.dto.pipeline.subjective_section import SubjectiveSection, SubjectiveText
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.util.annotations_alignment_util import AnnotationAlignmentUtil


class TestAnnotationsAlignmentUtil(TestCase):
    def test__align_start_and_end_notes_from_annotations__given_correct_ontology__should_align_notes(self):
        paragraph1 = Paragraph("some text", 0, 10)
        paragraph2 = Paragraph("pneumonia some other text", 11, 20)

        paragraph3 = Paragraph("medication text", 21, 30)
        paragraph4 = Paragraph("flurosemide some other text", 31, 40)

        text = paragraph1.text + paragraph2.text
        section_1 = SubjectiveSection(paragraph1.text, 90, 100, 0, 30)
        section_2 = SubjectiveSection(paragraph2.text, 200, 209, 60, 100)

        subjective_text = SubjectiveText(text, [section_1, section_2])

        text = paragraph3.text + paragraph4.text
        section_3 = MedicationSection(paragraph3.text, 90, 100, 0, 30)
        section_4 = MedicationSection(paragraph4.text, 200, 209, 60, 100)

        medication_text = MedicationText(text, [section_3, section_4])

        mock_annotation_results = {
            MedicationSectionExtractorComponent: [medication_text],
            SubjectiveSectionExtractorComponent: [subjective_text],
            NegationHandlingComponent: [
                NegationResult(paragraph1.text + "\n\n" + paragraph2.text.replace("pneumonia", "Pneumonia")),
                NegationResult(paragraph3.text + "\n\n" + paragraph4.text.replace("flurosemide", "Flurosemide")),
            ],
            "changed_words": {"Pneumonia": [ChangedWordAnnotation("pneumonia", "Pneumonia", 11, 20)],
                              "Flurosemide": [ChangedWordAnnotation("flurosemide", "Flurosemide", 31, 40)]}
        }

        mock_acm_result = Mock()
        mock_acm_result.rxnorm_annotations = self.__get_dummy_rxnorm_annotation_result()
        mock_acm_result.icd10_annotations = self.__get_dummy_icd10_annotation_result()

        AnnotationAlignmentUtil.align_start_and_end_notes_from_annotations("ICD10-CM", mock_acm_result,
                                                                           mock_annotation_results)

        AnnotationAlignmentUtil.align_start_and_end_notes_from_annotations("RxNorm", mock_acm_result,
                                                                           mock_annotation_results)

        assert mock_acm_result.rxnorm_annotations[0].begin_offset == 101
        assert mock_acm_result.rxnorm_annotations[0].end_offset == 110
        assert mock_acm_result.rxnorm_annotations[1].begin_offset == 102
        assert mock_acm_result.rxnorm_annotations[1].end_offset == 114

        assert mock_acm_result.icd10_annotations[0].begin_offset == 99
        assert mock_acm_result.icd10_annotations[0].end_offset == 108
        assert mock_acm_result.icd10_annotations[1].begin_offset == 210
        assert mock_acm_result.icd10_annotations[1].end_offset == 240

    def test__set_annotation_condition__given_correct_ontology__should_assign_condition(self):
        rxnorm_annotation = Mock(RxNormAnnotationResult)
        rxnorm_annotation.medication = "clonidine"

        icd10_annotation = Mock(ICD10AnnotationResult)
        icd10_annotation.medical_condition = "pneumonia"

        mock_rxnorm_matched_value = "Clonidine"
        mock_icd10_matched_value = "Pneumonia"

        AnnotationAlignmentUtil._AnnotationAlignmentUtil__set_annotation_condition("RxNorm", rxnorm_annotation,
                                                                                   mock_rxnorm_matched_value)
        AnnotationAlignmentUtil._AnnotationAlignmentUtil__set_annotation_condition("ICD10-CM", icd10_annotation,
                                                                                   mock_icd10_matched_value)

        assert rxnorm_annotation.medication == mock_rxnorm_matched_value
        assert icd10_annotation.medical_condition == mock_icd10_matched_value

    def test__get_annotation_text__given_incorrect_ontology__should_raise_exception(self):
        with self.assertRaises(ValueError) as error:
            AnnotationAlignmentUtil._AnnotationAlignmentUtil__get_annotation_text("some text", [])
        assert error.exception.args[0] == "Unknown note to align!"

    def __get_dummy_icd10_annotation_result(self):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=70,
                                                          end_offset=100, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_3 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="Pneumonia", begin_offset=11, end_offset=20,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4],
                                                          raw_acm_response={"data": "data"})

        return [icd10_annotation_result_1, icd10_annotation_result_2]

    def __get_dummy_rxnorm_annotation_result(self):
        rxnorm_annotation_1 = RxNormAnnotation(code="2599", description="Clonidine Hydrochloride 0.2 MG Oral Tablet",
                                               score=0.7)
        rxnorm_annotation_2 = RxNormAnnotation(code="884187",
                                               description="Clonidine Hydrochloride 0.2 MG Oral Tablet [Catapres]",
                                               score=0.54)
        rxnorm_annotation_result_1 = RxNormAnnotationResult(medication="Clonidine", begin_offset=12,
                                                            end_offset=24, is_negated=False,
                                                            suggested_codes=[rxnorm_annotation_1, rxnorm_annotation_2],
                                                            raw_acm_response={"data": "data"})

        rxnorm_annotation_3 = RxNormAnnotation(code="3456",
                                               description="lisdexamfetamine dimesylate 50 MG Oral Capsule [Vyvanse]",
                                               score=0.89)
        rxnorm_annotation_4 = RxNormAnnotation(code="348953",
                                               description="lisdexamfetamine dimesylate 50 MG Chewable Tablet [Vyvanse]",
                                               score=0.45)

        rxnorm_annotation_result_2 = RxNormAnnotationResult(medication="Flurosemide", begin_offset=11,
                                                            end_offset=20,
                                                            is_negated=False,
                                                            suggested_codes=[rxnorm_annotation_3, rxnorm_annotation_4],
                                                            raw_acm_response={"data": "data"})

        return [rxnorm_annotation_result_1, rxnorm_annotation_result_2]
