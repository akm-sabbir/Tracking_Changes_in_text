from unittest import TestCase

from app.service.medeant.medant_note_section_service import MedantNoteSectionService


class TestMedantNoteSectionService(TestCase):

    def test__get_subjective_sections__should_return_correct_sections__given_note_with_subjective_section(self):
        medant_note_service = MedantNoteSectionService()
        test_text_1 = "Problem List:\n this is subjective (Health Maintenance)\n\n " \
                      "Medical Problems: Something else: some other text (Accidents/Injuries)\n\n " \
                      "HPI: this is exam ROS:" \
                      "\n\n "
        sections = medant_note_service.get_subjective_sections(test_text_1)
        expected_section_1_text = 'Medical Problems: Something else: some other text '
        expected_section_2_text = 'Problem List:\n this is subjective '
        expected_section_3_text = " this is exam "

        assert sections[0].group() == expected_section_1_text
        assert sections[0].start() == 57
        assert sections[0].end() == 107

        assert sections[1].group() == expected_section_2_text
        assert sections[1].start() == 0
        assert sections[1].end() == 34

        assert sections[2].group() == expected_section_3_text
        assert sections[2].start() == 134
        assert sections[2].end() == 148

    def test__get_subjective_sections__should_return_empty__given_note_with_no_subjective_section(self):
        test_text_1 = "notes:\n this is subjective \n\n Other  Notes: some other text \n\n Other Notes: this " \
                      "is other \n\n "
        sections = MedantNoteSectionService().get_subjective_sections(test_text_1)

        assert len(sections) == 0

    def test__get_family_history_sections__should_return_correct_sections__given_note_with_family_history_section(self):
        medant_note_service = MedantNoteSectionService()
        test_text_1 = "FH:\n this is family history \n\n Something else: some other text \n\n Exam: this is exam " \
                      "\n\n "
        expected_section_text = " this is family history "

        sections = medant_note_service.get_family_history_sections(test_text_1)

        assert sections[0].start == 4
        assert sections[0].end == 28
        assert test_text_1[4:28] == expected_section_text

        test_text_2 = "FH:\n this is family history \nSH:\n this is SH section \n Something else: some other text" \
                      "\n\n "
        sections = medant_note_service.get_family_history_sections(test_text_2)
        expected_section_text2 = " this is family history \n"

        assert sections[0].start == 4
        assert sections[0].end == 29
        assert test_text_2[4:29] == expected_section_text2

        test_text_3 = "FH:\n this is family history \nObjective:\n this is SH section \n Something else: some other text" \
                      "\n\n "
        sections = medant_note_service.get_family_history_sections(test_text_3)
        expected_section_text3 = " this is family history \n"

        assert sections[0].start == 4
        assert sections[0].end == 29
        assert test_text_3[4:29] == expected_section_text3

    def test__get_family_history_sections__should_return_empty__given_note_with_no_family_history_section(self):
        medant_note_service = MedantNoteSectionService()
        test_text_1 = "note:\n this is family history \n\n Something else: some other text \n\n Exam: this is exam " \
                      "\n\n "

        sections = medant_note_service.get_family_history_sections(test_text_1)

        assert len(sections) == 0

    def test__get_medication_sections__should_return_correct_sections__given_note_with_medication_sections(self):
        medant_note_service = MedantNoteSectionService()
        test_text_1 = "Current meds prior to visit:\n this is medication section \n\n " \
                      "Allergies: some other text \n\n Medication reviewed: this is exam " \
                      "\n\n "
        expected_section_text = ":\n this is medication section \n\n "

        sections = medant_note_service.get_medication_sections(test_text_1)

        assert sections[0].start() == 27
        assert sections[0].end() == 60
        assert sections[0].group() == expected_section_text

        test_text_2 = "Med New:\n this is medication section \ncorrespond\'s:\n " \
                      "this is correspond section \n Something else: some other text" \
                      "\n\n "
        sections = medant_note_service.get_medication_sections(test_text_2)
        expected_section_text2 = "\n this is medication section \n"

        assert sections[0].start() == 8
        assert sections[0].end() == 38
        assert sections[0].group() == expected_section_text2

        test_text_3 = "Med Current:\n this is medication section \nReferral:\n this is SH section \n Something else: some other text" \
                      "\n\n "
        sections = medant_note_service.get_medication_sections(test_text_3)
        expected_section_text3 = "\n this is medication section \n"

        assert sections[0].start() == 12
        assert sections[0].end() == 42
        assert sections[0].group() == expected_section_text3

    def test__get_medication_sections__should_return_empty__given_note_with_no_medication_sections(self):
        medant_note_service = MedantNoteSectionService()
        test_text_1 = "note:\n this is medication section \n\n Something else: some other text \n\n Exam: this is exam " \
                      "\n\n "

        sections = medant_note_service.get_medication_sections(test_text_1)

        assert len(sections) == 0
