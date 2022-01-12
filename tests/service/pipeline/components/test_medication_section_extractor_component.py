from unittest import TestCase
from unittest.mock import Mock

from app.service.medeant.medant_note_section_service import MedantNoteSectionService
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent


class TestMedicationSectionExtractorComponent(TestCase):
    def test__run__should_return_correct_response__given_correct_input(self):
        extractor_component = MedicationSectionExtractorComponent()

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
        mock_note_section_service.get_medication_sections = Mock()
        mock_note_section_service.get_medication_sections.return_value = [mock_section_1, mock_section_2]
        extractor_component.note_section_service = mock_note_section_service

        subjective_section = extractor_component.run(annotation_results={"text": "some text"})[0]

        assert subjective_section.text == "section 1section 2"

        assert subjective_section.medication_sections[0].text == "section 1"
        assert subjective_section.medication_sections[0].start == 20
        assert subjective_section.medication_sections[0].end == 29
        assert subjective_section.medication_sections[0].relative_start == 0
        assert subjective_section.medication_sections[0].relative_end == 9

        assert subjective_section.medication_sections[1].text == "section 2"
        assert subjective_section.medication_sections[1].start == 100
        assert subjective_section.medication_sections[1].end == 109
        assert subjective_section.medication_sections[1].relative_start == 9
        assert subjective_section.medication_sections[1].relative_end == 18

    def test__run__should_return_correct_response__given_input_with_no_subjective_part(self):
        extractor_component = MedicationSectionExtractorComponent()

        mock_note_section_service = Mock(MedantNoteSectionService)
        mock_note_section_service.get_medication_sections = Mock()
        mock_note_section_service.get_medication_sections.return_value = []

        subjective_section = extractor_component.run(annotation_results={"text": "some text"})[0]

        assert subjective_section.medication_sections[0].text == "some text"
        assert subjective_section.medication_sections[0].start == 0
        assert subjective_section.medication_sections[0].end == 9
        assert subjective_section.medication_sections[0].relative_start == 0
        assert subjective_section.medication_sections[0].relative_end == 9

