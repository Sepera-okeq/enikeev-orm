"""
Модуль для построения и сохранения графиков с помощью matplotlib.
"""

import matplotlib.pyplot as plt

def save_plot(x_values, y_values, labels, title, xlabel, ylabel, filename, formats=('png',), figsize=(10, 6)):
    """
    Построение и сохранение графика с несколькими линиями.

    :param x_values: Список списков значений по оси X для каждой линии.
    :param y_values: Список списков значений по оси Y для каждой линии.
    :param labels: Список меток для каждой линии.
    :param title: Название графика.
    :param xlabel: Подпись оси X.
    :param ylabel: Подпись оси Y.
    :param filename: Имя файла для сохранения графика (без расширения).
    :param formats: Список форматов для сохранения (например, ['png', 'svg']).
    :param figsize: Размер фигуры графика.
    """
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*']
    plt.figure(figsize=figsize)

    for i, (x, y, label) in enumerate(zip(x_values, y_values, labels)):
        linestyle = linestyles[i % len(linestyles)]
        marker = markers[i % len(markers)] if len(x) < 10 else None
        plt.plot(x, y, label=label, linestyle=linestyle, marker=marker)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    for fmt in formats:
        plt.savefig(f'{filename}.{fmt}')
    
    plt.close()