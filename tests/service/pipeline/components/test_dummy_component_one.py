from unittest import TestCase

from app.service.pipeline.components.dummy_component_one import DummyComponentOne


class TestDummyComponentOne(TestCase):
    def test__run__should_return_correct_response__given_correct_input(self):
        result = DummyComponentOne().run({"text": "dummy"})
        assert result[0].message == "dummy"
