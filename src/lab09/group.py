import csv
from pathlib import Path

from src.lab04.io_txt_csv import write_csv
from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student


def save_students(path: str | Path, students: list[dict]) -> None:
    """
    Перезаписывает файл целиком: заголовок и все записи из списка students.
    Использует общую функцию write_csv.
    """
    # Валидация записей
    for student in students:
        validate_student(student)

    # Превращаем список словарей в список списков (последовательностей),
    # вытаскивая значения по ключам из STUDENT_FIELDS в нужном порядке
    rows = [
        [student[field] for field in STUDENT_FIELDS]
        for student in students
    ]

    # Используем готовую универсальную функцию записи CSV
    write_csv(rows, path, header=STUDENT_FIELDS)


def ensure_storage(path: str | Path) -> None:
    """
    Создаёт хранилище, если его ещё нет: файл с одной строкой-заголовком
    fio,birthdate,group,gpa (и все недостающие каталоги на пути к нему).
    Если файл уже существует, ничего не делает.
    """
    path = Path(path)

    if path.exists():
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    save_students(path, [])  # пустой список студентов = файл только с заголовком


def load_students(path: str | Path) -> list[dict]:
    """
    Читает всех студентов из CSV-файла и возвращает список словарей.

    Каждая строка проходит через student_from_dict из ЛР8: значения
    приводятся к нужным типам и проверяются.
    Если хранилища ещё нет, оно создаётся (пустое, только с заголовком).

    ValueError, если:
    - в файле нет заголовка или он не равен fio,birthdate,group,gpa
      (отсутствующие или лишние колонки);
    - в какой-то строке больше значений, чем колонок;
    - какая-то строка не проходит валидацию (в сообщении номер строки файла).
    """
    ensure_storage(path)

    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError(f"В файле {path} нет строки-заголовка")

        if tuple(reader.fieldnames) != STUDENT_FIELDS:
            raise ValueError(f"Неверный заголовок в файле {path}")

        students = []
        # строка 1 - заголовок, поэтому данные начинаются со строки 2
        for line_number, row in enumerate(reader, start=2):
            # DictReader кладёт лишние значения строки под ключ None
            if None in row:
                raise ValueError(f"В строке {line_number} файла {path} больше значений, чем колонок")

            try:
                students.append(student_from_dict(row))
            except (ValueError, TypeError) as error:
                raise ValueError(f"Строка {line_number} файла {path}: {error}") from error

    return students


def add_student(path: str | Path, student: dict) -> None:
    """
    Добавляет студента в конец файла. Запись сначала валидируется:
    если она некорректна, ValueError/TypeError и файл не меняется.
    """
    validate_student(student)

    students = load_students(path)
    students.append(dict(student))  # копия, чтобы не хранить ссылку на чужой словарь
    save_students(path, students)


def list_students(path: str | Path, sort_by: str | None = None) -> list[dict]:
    """
    Возвращает всех студентов. sort_by:
    - None - в том порядке, в котором они лежат в файле;
    - "fio" - по ФИО (по алфавиту);
    - "gpa" - по среднему баллу (по возрастанию).
    Любое другое значение sort_by - ValueError.
    """
    if sort_by not in (None, "fio", "gpa"):
        raise ValueError(f"Неизвестное поле сортировки")

    students = load_students(path)

    if sort_by == "fio":
        return sorted(students, key=lambda s: s["fio"])
    if sort_by == "gpa":
        return sorted(students, key=lambda s: s["gpa"])
    return students


def find_students(path: str | Path, substr: str) -> list[dict]:
    """
    Возвращает всех студентов, у которых substr входит в ФИО (без учёта регистра).
    Пустая подстрока подходит всем.
    """
    needle = substr.lower()
    students = load_students(path)

    return [s for s in students if needle in s["fio"].lower()]


def remove_student(path: str | Path, fio: str) -> int:
    """
    Удаляет ВСЕ записи с точно таким же ФИО и возвращает, сколько записей удалено.
    Если таких нет, файл не перезаписывается и возвращается 0.
    """
    students = load_students(path)

    kept = [s for s in students if s["fio"] != fio]
    removed = len(students) - len(kept)

    if removed > 0:
        save_students(path, kept)

    return removed


def update_student(path: str | Path, fio: str, **fields) -> bool:
    """
    Обновляет поля первой записи с таким ФИО, например:
    update_student(path, "Иванов Иван", gpa=4.5, group="БИВТ-26-6-2").

    - неизвестное имя поля - KeyError;
    - результат валидируется;
    - возвращает True, если запись найдена и обновлена, иначе False.
    """
    for name in fields:
        if name not in STUDENT_FIELDS:
            raise KeyError(f"Неизвестное поле: {name}")

    students = load_students(path)

    for i, student in enumerate(students):
        if student["fio"] == fio:
            updated = dict(student)
            updated.update(fields)
            validate_student(updated)

            students[i] = updated
            save_students(path, students)
            return True

    return False