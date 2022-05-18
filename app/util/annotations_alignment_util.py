import re
from typing import List

from app.dto.core.medical_ontology import MedicalOntology
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.service.impl.icd10_text_token_span_gen_service_impl import ICD10TextAndSpanGenerationServiceImpl
from app.dto.core.service.Tokens import TokenInfo
from app.util.text_span_discovery import TextSpanDiscovery


class AnnotationAlignmentUtil:

    tokenize_and_span_gen = ICD10TextAndSpanGenerationServiceImpl()
    text_span_discoverer = TextSpanDiscovery()

    @staticmethod
    def align_start_and_end_notes_from_annotations(medical_ontology_to_align_on_note: str, acm_result,
                                                   annotation_results, token_node_graph: dict) -> None:
        if medical_ontology_to_align_on_note == MedicalOntology.RXNORM.value:
            AnnotationAlignmentUtil.__align_start_and_text(medical_ontology_to_align_on_note,
                                                           acm_result.rxnorm_annotations,
                                                           token_node_graph)

            AnnotationAlignmentUtil.__align_start_end_for_medical_part(acm_result.rxnorm_annotations,
                                                                       annotation_results[
                                                                           MedicationSectionExtractorComponent][
                                                                           0].medication_sections)

        elif medical_ontology_to_align_on_note == MedicalOntology.ICD10_CM.value:
            AnnotationAlignmentUtil.__align_start_and_text(medical_ontology_to_align_on_note,
                                                           acm_result.icd10_annotations, token_node_graph)

            AnnotationAlignmentUtil.__align_start_end_for_medical_part(acm_result.icd10_annotations, annotation_results[
                SubjectiveSectionExtractorComponent][0].subjective_sections)

    @staticmethod
    def __get_annotation_text(medical_ontology_to_align_on_note: str, annotation):
        if medical_ontology_to_align_on_note == MedicalOntology.RXNORM.value:
            return annotation.medication
        elif medical_ontology_to_align_on_note == MedicalOntology.ICD10_CM.value:
            return annotation.medical_condition

        raise ValueError("Unknown note to align!")

    @staticmethod
    def __set_annotation_condition(medical_ontology_to_align_on_note: str, annotation, matched_value):
        if medical_ontology_to_align_on_note == MedicalOntology.RXNORM.value:
            annotation.medication = matched_value
        elif medical_ontology_to_align_on_note == MedicalOntology.ICD10_CM.value:
            annotation.medical_condition = matched_value

    @staticmethod
    def __align_start_and_text(medical_ontology_to_align_on_note: str, medical_annotations: List, token_node_graph: dict):

        for annotation in medical_annotations:
            annotation_text = AnnotationAlignmentUtil.__get_annotation_text(medical_ontology_to_align_on_note,
                                                                            annotation)

            token_list: List[TokenInfo] = AnnotationAlignmentUtil.tokenize_and_span_gen.get_token_with_span(annotation_text)
            pos, root_word = AnnotationAlignmentUtil.text_span_discoverer.get_start_end_pos_span(token_node_graph,
                                                                token_list[0].token, token_list[0].start_of_span, "")
            if medical_ontology_to_align_on_note == MedicalOntology.RXNORM.value:
                annotation.medication = root_word
            else:
                annotation.medical_condition = root_word
            annotation.begin_offset = pos
            annotation.end_offset = pos + len(root_word)

    @staticmethod
    def __align_start_end_for_medical_part(acm_annotations: List, medical_sections):
        section_index = 0
        annotation_index = 0
        acm_annotations.sort(key=lambda x: x.begin_offset)

        while not annotation_index == len(acm_annotations):
            annotation = acm_annotations[annotation_index]
            current_section = medical_sections[section_index]
            if annotation.begin_offset >= current_section.relative_start and annotation.end_offset <= current_section.relative_end:
                annotation.begin_offset = annotation.begin_offset - current_section.relative_start + current_section.start
                annotation.end_offset = annotation.end_offset - current_section.relative_start + current_section.start
                annotation_index = annotation_index + 1
            else:
                section_index = section_index + 1
