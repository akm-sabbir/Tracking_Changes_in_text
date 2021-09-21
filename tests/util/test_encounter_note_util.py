from unittest import TestCase
from app.util.encounter_note_util import EncounterNoteUtil
import math


class TestEncounterNoteUtil(TestCase):

    def test_break_note_into_sentences(self):
        note = "This is the first sentence. This is the second sentence.\n\nThis is the third sentence."
        expected = ["This is the first sentence.", "This is the second sentence.", "This is the third sentence."]

        actual = EncounterNoteUtil.break_note_into_sentences(note)

        assert type(actual) is type(expected)
        self.assertListEqual(actual, expected)

    def test_get_paragraphs_with_char_limit_30(self):
        max_limit = 30

        note = "This is the first sentence. This is the second sentence.\n\nThis is the third sentence."
        expected = ["This is the first sentence.", "This is the second sentence.", "This is the third sentence."]
        actual = EncounterNoteUtil.get_paragraphs(note, max_limit)

        assert type(actual) is type(expected)
        self.assertListEqual(actual, expected)

    def test_get_paragraphs_with_char_limit_60(self):
        max_limit = 60

        note = "This is the first sentence. This is the second sentence.\n\nThis is the third sentence."
        expected = ["This is the first sentence. This is the second sentence.", "This is the third sentence."]
        actual = EncounterNoteUtil.get_paragraphs(note, max_limit)

        assert type(actual) is type(expected)
        self.assertListEqual(actual, expected)

    def test_get_paragraphs_with_char_limit_100(self):
        max_limit = 100

        note = "This is the first sentence. This is the second sentence.\n\nThis is the third sentence."
        expected = ["This is the first sentence. This is the second sentence.\n\nThis is the third sentence."]
        actual = EncounterNoteUtil.get_paragraphs(note, max_limit)

        assert type(actual) is type(expected)
        self.assertListEqual(actual, expected)

    def test_get_paragraphs_with_long_sentence(self):
        max_limit = 50

        note = "This is the first sentence This is the second sentence \n\nThis is the third sentence."
        paragraphs = EncounterNoteUtil.get_paragraphs(note, max_limit)
        expected_no_of_paragraphs = math.ceil(len(note) / max_limit)
        actual_no_of_paragraphs = len(paragraphs)

        assert actual_no_of_paragraphs == expected_no_of_paragraphs

    def test_map_to_paragraph_dto_should_map_properly(self):
        max_limit = 30
        note = "This is the first sentence. This is the second sentence. \n\nThis is the third sentence."
        paragraphs = EncounterNoteUtil.get_paragraphs(note, max_limit)
        dto = EncounterNoteUtil.map_to_paragraph_dto(paragraphs)

        assert dto[0].text == "This is the first sentence."
        assert dto[0].start_index == 0
        assert dto[0].end_index == 27

        assert dto[2].text == "This is the third sentence."
        assert dto[2].start_index == 57
        assert dto[2].end_index == 84

    def test_break_note_into_paragraphs(self):
        max_limit = 30
        note = "This is the first sentence. This is the second sentence. \n\nThis is the third sentence."
        dto = EncounterNoteUtil.break_note_into_paragraphs(note, max_limit)

        assert dto[0].text == "This is the first sentence."
        assert dto[0].start_index == 0
        assert dto[0].end_index == 27

        assert dto[2].text == "This is the third sentence."
        assert dto[2].start_index == 57
        assert dto[2].end_index == 84
