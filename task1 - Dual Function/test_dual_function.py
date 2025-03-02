import unittest
import math
from dual_function import dual_function


class TestDualFunction(unittest.TestCase):
    def test_left_function(self):
        # Тесты для левой функции (когда x < n)
        test_cases = [
            (2, 3, 2 - 1 / 2 + (2 * 2) / 10),  # 2 - 0.5 + 0.4 = 1.9
            (-1, 0, -1 - (-1) + ((-1) * (-1)) / 10)  # (-1 + 1 + 0.1) = 0.1
        ]
        for x, n, expected in test_cases:
            with self.subTest(x=x, n=n):
                self.assertAlmostEqual(dual_function(x, n), expected)

    def test_right_function(self):
        # Тесты для правой функции (когда x >= n)
        test_cases = [
            (3, 3, 1 / (3 * 3 - 4) + math.sqrt(abs(3))),  # 1/5 + sqrt(3)
            (5, 2, 1 / (5 * 5 - 4) + math.sqrt(abs(5)))
        ]
        for x, n, expected in test_cases:
            with self.subTest(x=x, n=n):
                self.assertAlmostEqual(dual_function(x, n), expected)

    def test_invalid_input(self):
        # Проверка некорректного ввода (нечисловые данные)
        with self.assertRaises(TypeError):
            dual_function("string", 3)
        with self.assertRaises(TypeError):
            dual_function(2, "string")


if __name__ == '__main__':
    unittest.main()
