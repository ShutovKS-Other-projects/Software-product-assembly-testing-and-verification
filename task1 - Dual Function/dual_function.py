import math


def dual_function(x, n):
    """
    Вычисляет значение y по условию:
      - Если x < n, используется левая функция: x - 1/x + x^2/10.
      - Иначе используется правая функция: 1/(x^2 - 4) + sqrt(|x|).

    Примеры (doctest):
    >>> dual_function(2, 3)  # 2 < 3 -> левая функция: 2 - 1/2 + 4/10 = 2 - 0.5 + 0.4 = 1.9
    1.9
    >>> dual_function(3, 3)  # 3 >= 3 -> правая функция: 1/(9-4)+sqrt(3) = 0.2+1.7320508075688772 = 1.9320508075688772
    1.9320508075688772
    >>> dual_function("a", 3)  # некорректный тип, должно вызвать исключение
    Traceback (most recent call last):
        ...
    TypeError
    """
    if not (isinstance(x, (int, float)) and isinstance(n, (int, float))):
        raise TypeError("x and n must be numbers")
    if x < n:
        return x - 1 / x + (x * x) / 10
    else:
        return 1 / (x * x - 4) + math.sqrt(abs(x))


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
