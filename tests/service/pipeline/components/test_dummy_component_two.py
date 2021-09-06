from unittest import TestCase

from app.service.pipeline.components.dummy_component_two import DummyComponentTwo


class TestDummyComponentTwo(TestCase):
    def test__run__should_return_correct_response__given_correct_input(self):
        result = DummyComponentTwo().run({})
        assert result[0].message == "dummy two"
