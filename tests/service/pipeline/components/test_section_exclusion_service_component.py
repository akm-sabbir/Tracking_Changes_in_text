from unittest import TestCase
from unittest.mock import Mock

from app.dto.pipeline.excluded_sections.family_history_excluded_section import FamilyHistorySection
from app.service.medeant.medant_note_section_service import MedantNoteSectionService
from app.service.pipeline.components.section_exclusion_service_component import SectionExclusionServiceComponent


class TestSectionExclusionServiceComponent(TestCase):
    def test__run__should_return_correct_response__given_correct_input(self):
        exclusion_component = SectionExclusionServiceComponent()

        mock_section_1 = Mock(FamilyHistorySection)
        mock_section_1.start = 20
        mock_section_1.end = 29

        mock_section_2 = Mock(FamilyHistorySection)
        mock_section_2.start = 100
        mock_section_2.end = 109

        mock_note_section_service = Mock(MedantNoteSectionService)
        mock_note_section_service.get_family_history_sections = Mock()
        mock_note_section_service.get_family_history_sections.return_value = [mock_section_1, mock_section_2]
        exclusion_component.note_section_service = mock_note_section_service

        family_history_section = exclusion_component.run(annotation_results={"text": "some text"})

        assert family_history_section[0].start == 20
        assert family_history_section[0].end == 29

        assert family_history_section[1].start == 100
        assert family_history_section[1].end == 109

        mock_note_section_service.get_family_history_sections.assert_called_once()
        mock_note_section_service.get_family_history_sections.assert_called_once_with("some text")

    def test__run__should_return_correct_response__given_input_with_no_family_history_section(self):
        exclusion_component = SectionExclusionServiceComponent()

        mock_note_section_service = Mock(MedantNoteSectionService)
        mock_note_section_service.get_family_history_sections = Mock()
        mock_note_section_service.get_family_history_sections.return_value = []
        exclusion_component.note_section_service = mock_note_section_service

        family_history_section = exclusion_component.run(annotation_results={"text": "some text"})

        assert len(family_history_section) == 0

        mock_note_section_service.get_family_history_sections.assert_called_once()
        mock_note_section_service.get_family_history_sections.assert_called_once_with("some text")

