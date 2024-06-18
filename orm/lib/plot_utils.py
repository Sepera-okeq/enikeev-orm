"""
Модуль для построения и сохранения графиков.

Импорты:
    - Импортируется модуль matplotlib.pyplot для построения графиков.

Функции:
    - save_plot: Построение и сохранение графика с несколькими линиями.
"""

import matplotlib.pyplot as plt

def save_plot(x_values, y_values, labels, title, xlabel, ylabel, filename, formats=('png',), figsize=(10, 6)):
    """
    Построение и сохранение графика с несколькими линиями.

    :param x_values: Список значений по оси X.
    :param y_values: Список списков значений по оси Y для каждой линии.
    :param labels: Список меток для каждой линии.
    :param title: Название графика.
    :param xlabel: Подпись оси X.
    :param ylabel: Подпись оси Y.
    :param filename: Имя файла для сохранения графика (без расширения).
    :param formats: Форматы для сохранения (например, ['png', 'svg']).
    :param figsize: Размер фигуры графика.
    """
    
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*']
    plt.figure(figsize=figsize)

    for i, (y, label) in enumerate(zip(y_values, labels)):
        linestyle = linestyles[i % len(linestyles)]
        marker = markers[i % len(markers)] if len(x_values) > 10 else None
        plt.plot(x_values, y, label=label, linestyle=linestyle, marker=marker)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    for fmt in formats:
        plt.savefig(f'{filename}.{fmt}')
    
    plt.close()