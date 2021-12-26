from typing import List
from unittest import TestCase

from app.dto.pipeline.changed_word_annotation import ChangedWordAnnotation
from app.util.pipeline_util import PipelineUtil


class PipelineUtilTest(TestCase):

    def test_track_changed_words(self):
        mock_annotation_result = {"changed_words": {}}

        PipelineUtil.track_changed_words("breathlessnes", "breathlessness", 10, 24, mock_annotation_result)
        PipelineUtil.track_changed_words("breathlissness", "breathlessness", 50, 64, mock_annotation_result)

        changed_word_list: List[ChangedWordAnnotation] = mock_annotation_result["changed_words"]["breathlessness"]

        assert changed_word_list[0].original_text == "breathlessnes"
        assert changed_word_list[0].start == 10
        assert changed_word_list[0].end == 24

        assert changed_word_list[1].original_text == "breathlissness"
        assert changed_word_list[1].start == 50
        assert changed_word_list[1].end == 64
