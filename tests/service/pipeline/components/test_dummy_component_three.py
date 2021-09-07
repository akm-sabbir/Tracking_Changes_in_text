from unittest import TestCase

from app.service.pipeline.components.dummy_component_three import DummyComponentThree


class TestDummyComponentThree(TestCase):
    def test__run__should_return_correct_response__given_correct_input(self):
        result = DummyComponentThree().run({})
        assert result[0].message == "dummy three"
