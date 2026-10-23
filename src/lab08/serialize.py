import json
from pathlib import Path

from src.lab04.io_txt_csv import read_text
from src.lab05.json_csv import check_extension
from src.lab08.models import student_from_dict, student_to_dict


def students_to_json(students: list[dict], path: str | Path) -> None:
    """Сохраняет список записей студентов в JSON-файл с предварительной валидацией."""
    check_extension(str(path), ".json")
    
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Каждую запись пропускаем через student_to_dict для проверки и создания копии
    validated_list = [student_to_dict(s) for s in students]
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(validated_list, f, ensure_ascii=False, indent=2)


def students_from_json(path: str | Path) -> list[dict]:
    """Загружает список студентов из JSON-файла со строгой валидацией каждой записи.

    Политика обработки битых записей:
    - Строгая (strict): первая же битая запись вызывает ValueError с указанием индекса и причины.
    """
    check_extension(str(path), ".json")
    
    text = read_text(path)

    if text.strip() == "":
        raise ValueError(f"Файл пуст: {path}")

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"Некорректный формат JSON в файле {path}")

    if not isinstance(data, list):
        raise ValueError("Содержимое JSON-файла должно быть списком.")

    students = []

    for idx, item in enumerate(data):
        try:
            # Десериализация и строгая валидация через модель студента
            student = student_from_dict(item)
            students.append(student)
        except:
            raise ValueError(f"Ошибка в записи под индексом {idx}")

    return students


if __name__ == "__main__":    
    input_file = "data/lab08/samples/students_input.json"
    output_file = "data/lab08/out/students_output.json"
    bad_file = "data/lab08/samples/students_bad.json"

    # 1. Чтение корректного файла и запись в новый
    print(f"1. Чтение из {input_file} и сохранение в {output_file}:")
    try:
        students_list = students_from_json(input_file)
        print(f"Успешно загружено записей: {len(students_list)}") 
        students_to_json(students_list, output_file)
    except Exception as e:
        print(f"Ошибка: {e}")

    # 2. Проверка строгой валидации на битом файле
    print(f"2. Попытка загрузить файл с ошибками ({bad_file}):")
    try:
        students_from_json(bad_file)
    except ValueError as e:
        print(f"Ошибка: {e}")
