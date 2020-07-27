from unittest import TestCase

from app.service.impl.calculator_service_impl import CalculatorServiceImpl


class TestCalculatorServiceImpl(TestCase):
    service: CalculatorServiceImpl = CalculatorServiceImpl()

    def test_add_numbers__given_correct_input__should_return_correct_output(self):
        assert self.service.add_numbers(3, 5) == 8

    def test_subtract_numbers__given_correct_input__should_return_correct_output(self):
        assert self.service.subtract_numbers(3, 5) == -2

    def test_multiply_numbers__given_correct_input__should_return_correct_output(self):
        assert self.service.multiply_numbers(3, 5) == 15

    def test_divide_numbers__given_correct_input__should_return_correct_output(self):
        assert self.service.divide_numbers(10, 2) == 5
