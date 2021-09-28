import math
from typing import List
from unittest import TestCase

from app.dto.core.paragraph import Paragraph
from app.util.encounter_note_util import EncounterNoteUtil


class TestEncounterNoteUtil(TestCase):

    def test_get_paragraphs_with_char_limit_30(self):
        max_limit = 30

        note = "This is the first sentence. This is the second sentence.\n\nThis is the third sentence."
        expected_texts = ["This is the first sentence.", "This is the second sentence.",
                          "\n\nThis is the third sentence."]
        expected_starts = [0, 28, 56]
        expected_ends = [27, 56, 85]
        actual_paragraphs = EncounterNoteUtil.break_note_into_paragraphs(note, max_limit)

        self.__assert_actual_paragraph_values_with_expected(actual_paragraphs, expected_texts, expected_starts,
                                                            expected_ends)

    def test_get_paragraphs_with_char_limit_60(self):
        max_limit = 60

        note = "This is the first sentence. This is the second sentence.\n\nThis is the third sentence."
        expected_texts = ["This is the first sentence. This is the second sentence.", "\n\nThis is the third sentence."]
        expected_starts = [0, 56]
        expected_ends = [56, 85]
        actual_paragraphs = EncounterNoteUtil.break_note_into_paragraphs(note, max_limit)

        self.__assert_actual_paragraph_values_with_expected(actual_paragraphs, expected_texts, expected_starts,
                                                            expected_ends)

    def test_get_paragraphs_with_char_limit_100(self):
        max_limit = 100

        note = "This is the first sentence. This is the second sentence.\n\nThis is the third sentence."
        expected_texts = ["This is the first sentence. This is the second sentence.\n\nThis is the third sentence."]
        expected_starts = [0]
        expected_ends = [len(note)]

        actual_paragraphs = EncounterNoteUtil.break_note_into_paragraphs(note, max_limit)

        self.__assert_actual_paragraph_values_with_expected(actual_paragraphs, expected_texts, expected_starts,
                                                            expected_ends)

    def test_get_paragraphs_with_long_sentence(self):
        max_limit = 50

        note = "This is the first sentence This is the second sentence \n\nThis is the third sentence."
        paragraphs = EncounterNoteUtil.break_note_into_paragraphs(note, max_limit)
        expected_no_of_paragraphs = math.ceil(len(note) / max_limit)
        actual_no_of_paragraphs = len(paragraphs)

        assert actual_no_of_paragraphs == expected_no_of_paragraphs

    def __assert_actual_paragraph_values_with_expected(self, paragraphs: List[Paragraph], expected_texts,
                                                       expected_starts,
                                                       expected_ends):
        assert len(paragraphs) == len(expected_texts)
        for idx, paragraph in enumerate(paragraphs):
            assert paragraph.text == expected_texts[idx]
            assert paragraph.start_index == expected_starts[idx]
            assert paragraph.end_index == expected_ends[idx]
