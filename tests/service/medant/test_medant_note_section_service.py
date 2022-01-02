from unittest import TestCase

from app.service.medeant.medant_note_section_service import MedantNoteSectionService


class TestMedantNoteSectionService(TestCase):

    def test__get_subjective_sections__should_return_correct_sections__given_note_with_subjective_section(self):
        medant_note_service = MedantNoteSectionService()
        test_text_1 = "Subjective\n this is subjective \n\n Something else: some other text \n\n Exam: this is exam " \
                      "\n\n "
        sections = medant_note_service.get_subjective_sections(test_text_1)
        expected_section_1_text = " this is subjective "
        expected_section_2_text = " this is exam "

        assert sections[0].group() == expected_section_1_text
        assert sections[0].start() == 11
        assert sections[0].end() == 31

        assert sections[1].group() == expected_section_2_text
        assert sections[1].start() == 74
        assert sections[1].end() == 88

        test_text_1 = "Subjective\n this is subjective \n\n Something else: some other text"
        sections = medant_note_service.get_subjective_sections(test_text_1)
        expected_section_1_text = " this is subjective "

        assert sections[0].group() == expected_section_1_text
        assert sections[0].start() == 11
        assert sections[0].end() == 31

    def test__get_subjective_sections__should_return_correct_sections__given_note_with_session_notes_section(self):
        medant_note_service = MedantNoteSectionService()
        test_text_1 = "Session notes:\n this is subjective \n\n Progress Notes: some other text \n\n Progress Notes: " \
                      "this is progress \n\n "
        sections = medant_note_service.get_subjective_sections(test_text_1)
        expected_section_1_text = "\n this is subjective \n\n "
        expected_section_2_text = " some other text "
        expected_section_3_text = " this is progress "

        assert sections[0].group() == expected_section_1_text
        assert sections[0].start() == 14
        assert sections[0].end() == 38

        assert sections[1].group() == expected_section_2_text
        assert sections[1].start() == 53
        assert sections[1].end() == 70

        assert sections[2].group() == expected_section_3_text
        assert sections[2].start() == 88
        assert sections[2].end() == 106

        test_text_1 = "Session notes:\n this is subjective \n\n Other  Notes: some other text \n\n Other Notes: this " \
                      "is other \n\n "
        sections = medant_note_service.get_subjective_sections(test_text_1)
        expected_section_1_text = "\n this is subjective "

        assert sections[0].group() == expected_section_1_text
        assert sections[0].start() == 14
        assert sections[0].end() == 35

    def test__get_subjective_sections__should_return_empty__given_note_with_no_subjective_section(self):
        test_text_1 = "notes:\n this is subjective \n\n Other  Notes: some other text \n\n Other Notes: this " \
                      "is other \n\n "
        sections = MedantNoteSectionService().get_subjective_sections(test_text_1)

        assert len(sections) == 0
