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
    
    # Устанавливаем стили линий и маркеров для графика
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*']
    plt.figure(figsize=figsize)

    # Проходимся по каждому набору данных и строим линии
    for i, (y, label) in enumerate(zip(y_values, labels)):
        linestyle = linestyles[i % len(linestyles)]
        marker = markers[i % len(markers)] if len(x_values) < 10 else None
        plt.plot(x_values, y, label=label, linestyle=linestyle, marker=marker)

    # Устанавливаем заголовок, подписи осей и легенду, включаем сетку
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    # Сохраняем график в указанных форматах
    for fmt in formats:
        plt.savefig(f'{filename}.{fmt}')
    
    # Закрываем фигуру
    plt.close()