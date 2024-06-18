#!/bin/bash

# Проверяем, передана ли папка как аргумент
if [ -z "$1" ]; then
  echo "Использование: $0 <папка>"
  exit 1
fi

# Проверяем, существует ли папка
if [ ! -d "$1" ]; then
  echo "Ошибка: Папка '$1' не найдена."
  exit 1
fi

# Создаем выходной файл (можно изменить название)
output_file="combined_files.txt"

# Проходим по всем файлам в папке (рекурсивно)
find "$1" -type f -print0 | while IFS= read -r -d $'\0' file; do

  # Получаем относительный путь до файла
  relative_path="${file#$1/}"

  # Добавляем информацию о файле и его содержимое в выходной файл
  echo "Файл ${relative_path}:" >> "$output_file"
  echo "" >> "$output_file"
  cat "$file" >> "$output_file"
  echo "" >> "$output_file"

done

echo "Готово! Все файлы скомпилированы в '$output_file'."