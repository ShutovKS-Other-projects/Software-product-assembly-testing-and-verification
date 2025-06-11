# tests/test_dual_function.py
import math
import unittest

from src.dualfunc import dual_function


class TestDualFunction(unittest.TestCase):

    def test_left_function_values(self):
        # Тесты для левой функции (x < n)
        test_cases = [
            # (x, n, expected_y)
            (2, 3, 1.9),
            (-1, 0, 0.1),
            (0.5, 1, 0.5 - 2 + 0.025)  # 0.5 - 1/0.5 + 0.25/10
        ]
        for x, n, expected in test_cases:
            with self.subTest(msg="Left function", x=x, n=n):
                self.assertAlmostEqual(dual_function(x, n), expected)

    def test_right_function_values(self):
        # Тесты для правой функции (x >= n)
        test_cases = [
            # (x, n, expected_y)
            (3, 3, 1 / (9 - 4) + math.sqrt(3)),  # Граничное значение
            (5, 2, 1 / (25 - 4) + math.sqrt(5)),
            (-3, -2, 1 / (9 - 4) + math.sqrt(3)),  # x > n
        ]
        for x, n, expected in test_cases:
            with self.subTest(msg="Right function", x=x, n=n):
                self.assertAlmostEqual(dual_function(x, n), expected)

    def test_sensitive_points_zero_division(self):
        # Тесты для "чувствительных" точек, где происходит деление на ноль
        # Левая функция падает при x = 0
        with self.assertRaises(ZeroDivisionError):
            dual_function(0, 1)

        # Правая функция падает при x = 2 и x = -2
        with self.assertRaises(ZeroDivisionError):
            dual_function(2, 0)
        with self.assertRaises(ZeroDivisionError):
            dual_function(-2, -3)

    def test_invalid_input_type(self):
        # Проверка некорректного ввода (нечисловые данные)
        # Ожидаем "естественный" TypeError, а не тот, что мы вызывали сами
        with self.assertRaises(TypeError):
            dual_function("a", 3)
        with self.assertRaises(TypeError):
            dual_function(2, "string")
        with self.assertRaises(TypeError):
            dual_function(None, 5)
