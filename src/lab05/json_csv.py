import csv
import json
from pathlib import Path

from src.lab04.io_txt_csv import read_text, write_csv


def check_extension(path: str, extension: str) -> None:
    """
    Проверяет, что у файла path нужное расширение (например, ".json").
    """
    if Path(path).suffix.lower() != extension:
        raise ValueError(f"Неверный тип файла: {path} (ожидалось {extension})")


def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует JSON-файл в CSV.
    Поддерживает список словарей [{...}, {...}], заполняет отсутствующие поля пустыми строками.
    Колонки CSV - это ключи словарей: сначала ключи первого объекта,
    затем новые ключи из остальных объектов (в порядке появления).
    Если у объекта нет какого-то ключа - в ячейку пишется пустая строка.

    Raises:
        неверное расширение файла -> ValueError
        пустой JSON или не список словарей -> ValueError
        файл не найден -> FileNotFoundError (поднимает read_text из ЛР4)
        некорректный JSON -> json.JSONDecodeError (подвид ValueError)
    """
    check_extension(json_path, ".json")
    check_extension(csv_path, ".csv")

    # читаем файл функцией из ЛР4
    text = read_text(json_path)

    if text.strip() == "":
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    # превращаем текст в python-объект (список словарей)
    data = json.loads(text)

    # проверяем, что это непустой список
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    # проверяем, что каждый элемент списка - словарь
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("В JSON должен быть список словарей")

    # собираем названия колонок
    columns = []
    for item in data:
        for key in item:
            if key not in columns:
                columns.append(key)

    if len(columns) == 0:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    # превращаем каждый словарь в строку-список значений
    rows = []
    for item in data:
        row = []
        for column in columns:
            row.append(item.get(column, ""))  # нет ключа -> пустая строка
        rows.append(row)

    # записываем функцией из ЛР4
    write_csv(rows, csv_path, header=tuple(columns))


def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует CSV в JSON (список словарей).
    Заголовок обязателен, значения сохраняются как строки.

    Raises:
        неверное расширение файла -> ValueError
        CSV пустой, без заголовка или без строк с данными -> ValueError
        файл не найден -> FileNotFoundError
    """
    check_extension(csv_path, ".csv")
    check_extension(json_path, ".json")

    # DictReader превращает каждую строку CSV в словарь {колонка: значение}
    # restval="" - если в строке не хватает значений, ставим пустую строку
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, restval="")

        if not reader.fieldnames:
            raise ValueError("CSV пустой или без заголовка")

        rows = list(reader)

    if len(rows) == 0:
        raise ValueError("В CSV нет данных (есть только заголовок)")

    # создаём папку для результата, если её ещё нет
    path = Path(json_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    json_to_csv("data/lab05/samples/people.json", "data/lab05/out/people_from_json.csv")
    csv_to_json("data/lab05/samples/people.csv", "data/lab05/out/people_from_csv.json")

    print("Тест #1. Конвертации JSON <-> CSV выполнены.")

    with open("data/lab05/samples/people.json", encoding="utf-8") as f:
        count_json = len(json.load(f))
    
    with open("data/lab05/out/people_from_json.csv", encoding="utf-8", newline="") as f:
        count_csv = len(list(csv.DictReader(f)))

    # проверка: количество записей до и после конвертации совпадает

    print(f"Записей в JSON: {count_json}, строк в CSV: {count_csv}")

    json_to_csv("data/lab05/samples/students.json", "data/lab05/out/students_from_json.csv")
    csv_to_json("data/lab05/samples/students.csv", "data/lab05/out/students_from_csv.json")

    print("Тест #2. Конвертации JSON <-> CSV выполнены.")
    
    with open("data/lab05/samples/students.json", encoding="utf-8") as f:
        count_json = len(json.load(f))
        
    with open("data/lab05/out/students_from_json.csv", encoding="utf-8", newline="") as f:
        count_csv = len(list(csv.DictReader(f)))

    # проверка: количество записей до и после конвертации совпадает

    print(f"Записей в JSON: {count_json}, строк в CSV: {count_csv}")