import re
from typing import List

from app.dto.core.medical_ontology import MedicalOntology
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent


class AnnotationAlignmentUtil:
    @staticmethod
    def align_start_and_end_notes_from_annotations(medical_ontology_to_align_on_note: str, acm_result,
                                                   annotation_results):
        if medical_ontology_to_align_on_note == MedicalOntology.RXNORM.value:
            AnnotationAlignmentUtil.__align_start_and_text(medical_ontology_to_align_on_note,
                                                           acm_result.rxnorm_annotations,
                                                           annotation_results[MedicationSectionExtractorComponent][
                                                               0].text,
                                                           annotation_results[NegationHandlingComponent][1].text,
                                                           annotation_results['changed_words'])
            AnnotationAlignmentUtil.__align_start_end_for_medical_part(acm_result.rxnorm_annotations,
                                                                       annotation_results[
                                                                           MedicationSectionExtractorComponent][
                                                                           0].medication_sections,
                                                                       annotation_results)

        elif medical_ontology_to_align_on_note == MedicalOntology.ICD10_CM.value:
            AnnotationAlignmentUtil.__align_start_and_text(medical_ontology_to_align_on_note,
                                                           acm_result.icd10_annotations,
                                                           annotation_results[SubjectiveSectionExtractorComponent][
                                                               0].text,
                                                           annotation_results[NegationHandlingComponent][0].text,
                                                           annotation_results['changed_words'])
            AnnotationAlignmentUtil.__align_start_end_for_medical_part(acm_result.icd10_annotations, annotation_results[
                SubjectiveSectionExtractorComponent][0].subjective_sections,
                                                                       annotation_results)

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
    def __align_start_and_text(medical_ontology_to_align_on_note: str, medical_annotations: List,
                               original_text: str, changed_text: str, changed_words: dict):

        for annotation in medical_annotations:
            annotation_text = AnnotationAlignmentUtil.__get_annotation_text(medical_ontology_to_align_on_note,
                                                                            annotation)

            word_list = re.sub(r"[^\w]", " ", annotation_text).split()

            match_found = AnnotationAlignmentUtil._reassign_acm_annotation_values(medical_ontology_to_align_on_note,
                                                                                  annotation, word_list,
                                                                                  original_text, changed_text)

            if match_found:
                continue

            changed_word_list = []
            for idx, word in enumerate(word_list):
                if word in changed_words:
                    changed_word_list.append(
                        "|".join((changed_word.original_text for changed_word in changed_words[word])))
                else:
                    changed_word_list.append(word)

            consecutive_words_match_regex_changed = r"[^\w]*?".join(changed_word_list)
            AnnotationAlignmentUtil._reassign_acm_annotation_values(medical_ontology_to_align_on_note, annotation,
                                                                    word_list, original_text,
                                                                    changed_text, consecutive_words_match_regex_changed)

    @staticmethod
    def _reassign_acm_annotation_values(medical_ontology_to_align_on_note: str, annotation, words_list: List,
                                        original_text: str,
                                        changed_text: str,
                                        consecutive_words_match_regex_changed: str = None):

        consecutive_words_match_regex = r"[^\w]*?".join(words_list)
        matches_changed = (match for match in
                           re.finditer(consecutive_words_match_regex, changed_text, re.IGNORECASE))

        if consecutive_words_match_regex_changed:
            consecutive_words_match_regex = consecutive_words_match_regex_changed

        matches = [match for match in re.finditer(consecutive_words_match_regex, original_text, re.IGNORECASE)]

        match_index = 0
        match_found = False
        for idx, match in enumerate(matches_changed):
            if match.start() == annotation.begin_offset and match.end() == annotation.end_offset:
                match_index = idx
                match_found = True
                break

        if match_found and len(matches) > match_index:
            annotation.begin_offset = matches[match_index].start()
            annotation.end_offset = matches[match_index].end()
            AnnotationAlignmentUtil.__set_annotation_condition(medical_ontology_to_align_on_note, annotation,
                                                               matches[match_index].group())
            return True
        else:
            return False

    @staticmethod
    def __align_start_end_for_medical_part(acm_annotations: List,
                                           medical_sections, annotation_results):
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
