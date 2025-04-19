import matplotlib.pyplot as plt
import numpy as np
import math


def dual_function(x, n):
    if not (isinstance(x, (int, float)) and isinstance(n, (int, float))):
        raise TypeError("x and n must be numbers")
    if x < n:
        return x - 1 / x + (x ** 2) / 10
    else:
        return 1 / (x ** 2 - 4) + math.sqrt(abs(x))


def plot_dual_function(n, x_range=(-5, 5), num_points=1000):
    x_values = np.linspace(x_range[0], x_range[1], num_points)
    y_values = []

    for x in x_values:
        try:
            y = dual_function(x, n)
            y_values.append(y)
        except (ZeroDivisionError, ValueError):
            y_values.append(np.nan)  # Разрыв

    # Разделение на левую и правую части для разных стилей
    x_left = x_values[x_values < n]
    y_left = [dual_function(x, n) if x != 0 else np.nan for x in x_left]

    x_right = x_values[x_values >= n]
    y_right = [dual_function(x, n) if x ** 2 != 4 else np.nan for x in x_right]

    # Построение графика
    plt.figure(figsize=(10, 6))

    # Левая часть (x < n)
    plt.plot(x_left, y_left, color='blue', label=f'Левая часть (x < {n})')

    # Правая часть (x ≥ n)
    plt.plot(x_right, y_right, color='red', label=f'Правая часть (x ≥ {n})')

    # Точка перехода x = n
    if n in x_range:
        y_transition = dual_function(n, n)
        plt.scatter(n, y_transition, color='green', zorder=5, label=f'Переход при x={n}')

    # Настройки графика
    plt.title(f"График dual_function для n={n}", fontsize=14)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.ylim(-10, 10)  # Ограничение по y для наглядности

    plt.tight_layout()
    plt.show()


# Примеры вызова
plot_dual_function(n=0)  # Разрывы при x=0, x=±2
plot_dual_function(n=3)  # Точка перехода при x=3