# Dual Function Library

Простая библиотека, созданная в рамках практической работы. Она предоставляет функцию `dual_function`, вычисляющую
значение по условию, и вспомогательную функцию `plot_dual_function` для визуализации.

## Установка

Установите пакет из PyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ dualfunc_ShutovKS
```

## Использование

### В качестве библиотеки в вашем Python-коде:

```python
from dualfunc import dual_function, plot_dual_function

# Вычислить одно значение
result = dual_function(x=2, n=3)
print(f"The result is: {result}")  # Вывод: The result is: 1.9

# Построить график функции при n=0
print("Displaying plot for n=0...")
plot_dual_function(n=0)

# Построить график функции при n=3
print("Displaying plot for n=3...")
plot_dual_function(n=3)
```
