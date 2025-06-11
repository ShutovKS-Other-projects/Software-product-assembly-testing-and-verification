# src/dualfunc/main.py
import math

import matplotlib.pyplot as plt
import numpy as np


def dual_function(x, n):
    if x < n:
        return x - 1 / x + (x ** 2) / 10
    else:
        return 1 / (x ** 2 - 4) + math.sqrt(abs(x))


def plot_dual_function(n, x_range=(-5, 5), num_points=1000):
    """Строит график сдвоенной функции для заданного n."""
    x_values = np.linspace(x_range[0], x_range[1], num_points)
    y_values = []

    # Вычисляем значения y, обрабатывая точки разрыва
    for x in x_values:
        try:
            y = dual_function(x, n)
            y_values.append(y)
        except (ZeroDivisionError, ValueError):
            y_values.append(np.nan)

    x_left = x_values[x_values < n]
    y_left = [y for x, y in zip(x_values, y_values) if x < n]

    x_right = x_values[x_values >= n]
    y_right = [y for x, y in zip(x_values, y_values) if x >= n]

    plt.figure(figsize=(10, 6))

    plt.plot(x_left, y_left, color='blue', label=f'y = x - 1/x + x²/10 (при x < {n})')
    plt.plot(x_right, y_right, color='red', label=f'y = 1/(x²-4) + √|x| (при x ≥ {n})')

    if x_range[0] < n < x_range[1]:
        try:
            y_transition = dual_function(n, n)
            plt.scatter(n, y_transition, color='green', zorder=5, s=100,
                        label=f'Точка перехода при x = {n}')
        except ZeroDivisionError:
            plt.axvline(x=n, color='green', linestyle='--', label=f'Разрыв в точке перехода x = {n}')

    plt.title(f"График сдвоенной функции для n = {n}", fontsize=14)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.ylim(-10, 10)  # Ограничение по y для наглядности

    plt.tight_layout()
    plt.show()
