from typing import Type
from unittest import TestCase
from unittest.mock import patch

from injector import T

from app.util.dependency_injector import DependencyInjector


class MockInjector:
    @staticmethod
    def get(class_name: Type[T]):
        return class_name.__name__


class TestDependencyInjector(TestCase):
    @patch.object(DependencyInjector, "_DependencyInjector__injector", MockInjector())
    def test_get_instance(self):
        assert DependencyInjector.get_instance(Exception) == "Exception"
        assert DependencyInjector.get_instance(int) == "int"
