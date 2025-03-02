import matplotlib.pyplot as plt
import numpy as np
from dual_function import dual_function


def plot_dual_function(n, x_range=(-10, 10), num_points=400):
    x_values = np.linspace(x_range[0], x_range[1], num_points)
    y_values = []
    for x in x_values:
        try:
            y_values.append(dual_function(x, n))
        except Exception:
            y_values.append(float('nan'))
    plt.figure()
    plt.plot(x_values, y_values, label=f"dual_function при n={n}")
    plt.title(f"График dual_function для n={n}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # Построение графиков для двух разных значений n
    plot_dual_function(n=0)
    plot_dual_function(n=3)
