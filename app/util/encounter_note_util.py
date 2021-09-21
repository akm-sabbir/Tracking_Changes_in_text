from spacy.lang.en import English
from collections import deque
from app.dto.core.paragraph import Paragraph


class EncounterNoteUtil:

    @staticmethod
    def break_note_into_paragraphs(note: str, limit: int) -> []:
        paragraphs = EncounterNoteUtil._get_paragraphs(note, limit)
        paragraph_dto = EncounterNoteUtil._map_to_paragraph_dto(paragraphs)
        return paragraph_dto

    @staticmethod
    def _get_paragraphs(note, limit):
        if len(note) < limit:
            return [note]

        sentences = EncounterNoteUtil._break_note_into_sentences(note)
        queue = deque(sentences)
        paragraphs = []
        paragraph = ""
        sentence = ""
        while queue:
            top = queue[0]
            if len(top) >= limit:
                long_sentence = queue.popleft()
                broken_sentences = EncounterNoteUtil._split_sentence_into_list_of_words(long_sentence, limit)
                paragraphs += broken_sentences
                continue

            if len(paragraph) + len(top) < limit:
                sentence = queue.popleft()
                paragraph += sentence
                paragraph += " "

            else:
                paragraphs.append(paragraph.rstrip())
                paragraph = ""

        if sentence:
            paragraphs.append(sentence)
        return paragraphs

    @staticmethod
    def _break_note_into_sentences(note: str) -> []:
        nlp = English()
        nlp.add_pipe('sentencizer')
        doc = nlp(note)
        sentences = [sent.text.strip() for sent in doc.sents]
        return sentences

    @staticmethod
    def _split_sentence_into_list_of_words(sentence: str, limit: int) -> []:
        return [sentence[i: i + limit] for i in range(0, len(sentence), limit)]

    @staticmethod
    def _map_to_paragraph_dto(paragraphs: []) -> []:
        paragraph_dto = []
        curr_index = 0
        for i in range(len(paragraphs)):
            text = paragraphs[i]
            start = curr_index
            end = curr_index + len(text)
            curr_index = end + 1
            dto = Paragraph(text, start, end)
            paragraph_dto.append(dto)

        return paragraph_dto
