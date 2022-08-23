from typing import List

from spacy.lang.en import English
from spacy.tokens import Span

from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.core.pipeline.sentence import Sentence


class EncounterNoteUtil:

    @staticmethod
    def break_note_into_paragraphs(note: str, limit: int) -> []:
        if len(note) <= limit:
            return [Paragraph(note, 0, len(note))]
        sentences: List[Sentence] = EncounterNoteUtil.break_note_into_sentences(note, limit)
        paragraphs: List[Paragraph] = EncounterNoteUtil.__get_paragraphs(sentences, note, limit)
        return paragraphs

    @staticmethod
    def __get_paragraphs(sentences: List[Sentence], note: str, limit: int) -> List[Paragraph]:
        text = ""
        start = 0
        end = 0
        paragraphs = []
        curr_sent = ""

        for sentence in sentences:
            curr_end = sentence.end
            curr_sent = sentence
            if curr_end - start < limit:
                text = note[start:curr_end]
                end = sentence.end
            else:
                paragraphs.append(Paragraph(text, start, end))
                start = sentence.start
                text = note[start:curr_end]
                end = curr_end
        if paragraphs[-1].end_index < len(note):
            paragraphs.append(Paragraph(note[start:curr_sent.end], start, curr_sent.end))

        return paragraphs

    @staticmethod
    def break_note_into_sentences(note: str, limit: int) -> List[Sentence]:
        nlp = English()
        nlp.add_pipe('sentencizer')
        doc = nlp(note)
        sentence_spans: List[Span] = [sent for sent in doc.sents]
        sentences: List[Sentence] = []
        for sentence_span in sentence_spans:
            if sentence_span.end_char - sentence_span.start_char > limit:
                sentences.extend(EncounterNoteUtil.__break_into_multiple_sentences(sentence_span, limit))
            else:
                sentences.append(Sentence(sentence_span.text, sentence_span.start_char, sentence_span.end_char))

        return sentences

    @staticmethod
    def __break_into_multiple_sentences(sentence_span: Span, limit: int) -> List[Sentence]:
        span = ""
        sentences = []
        text = ""
        start = 0
        end = 0
        current_tok_idx = 0
        for i in range(sentence_span.__len__() + 1):
            span = sentence_span[current_tok_idx:i]
            if len(span.text) < limit:
                text = span.text
                start = sentence_span.start_char + span.start_char
                end = sentence_span.start_char + span.end_char
            else:
                sentences.append(Sentence(text, start, end))
                current_tok_idx = i - 1
                span = sentence_span[current_tok_idx:i]
                text = span.text
                start = sentence_span.start_char + span.start_char
                end = sentence_span.start_char + span.end_char
        if sentences[-1].end != span.end_char:
            end = start + len(span.text)
            sentences.append(Sentence(span.text, start, end))
        return sentences
