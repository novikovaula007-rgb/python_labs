from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def make_student(fio: str, birthdate: str, group: str, gpa: float | int) -> dict:
    """Конструктор студента: проверяет входные данные и возвращает словарь-запись."""
    if not isinstance(fio, str) or not fio.strip():
        raise ValueError("ФИО должно быть непустой строкой.")
    
    if not isinstance(group, str) or not group.strip():
        raise ValueError("Группа должна быть непустой строкой.")

    fio_parts = fio.split()
    if len(fio_parts) < 2:
        raise ValueError("ФИО должно содержать как минимум фамилию и имя.")

    try:
        b_date = date.fromisoformat(birthdate)
    except ValueError:
        raise ValueError(f"Неверный формат или несуществующая дата рождения '{birthdate}'. Ожидается YYYY-MM-DD.")

    if b_date > date.today():
        raise ValueError("Дата рождения не может быть в будущем.")

    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise TypeError("GPA должен быть числом (float или int).")

    gpa_float = float(gpa)
    if not (0.0 <= gpa_float <= 5.0):
        raise ValueError("GPA должен принадлежать промежутку от 0.0 до 5.0")

    return {
        "fio": fio.strip(),
        "birthdate": birthdate.strip(),
        "group": group.strip(),
        "gpa": round(gpa_float, 2)
    }


def validate_student(rec: dict) -> None:
    """Проверяет готовый словарь-запись на соответствие структуре и правилам валидации."""
    if not isinstance(rec, dict):
        raise ValueError("Запись студента должна быть словарём.")

    expected = set(STUDENT_FIELDS) # ожидаемые ключи
    actual = set(rec.keys()) # действительные ключи

    # Проверяем ключи, если они не совпадают
    if actual != expected:
        missing = expected - actual 
        extra = actual - expected
        
        details = []
        if missing:
            details.append(f"пропущены {missing}")
        if extra:
            details.append(f"лишние {details}")
            
        raise ValueError(f"Неверный набор полей записи студента: {', '.join(details)}.")

    # Проверяем корректность значений через уже существующий конструктор
    make_student(rec["fio"], rec["birthdate"], rec["group"], rec["gpa"])


def student_age(rec: dict, today: date | None = None) -> int:
    """Вычисляет полных лет студента на дату today (по умолчанию сегодня)."""
    validate_student(rec)
    b_date = date.fromisoformat(rec["birthdate"])
    ref_date = today or date.today()
    
    if b_date > ref_date:
        raise ValueError("Дата рождения позже целевой даты.")

    age = ref_date.year - b_date.year
    if (ref_date.month, ref_date.day) < (b_date.month, b_date.day):
        age -= 1
    return age


def format_student(rec: dict) -> str:
    """Форматирует запись студента в читаемую строку с инициалами и возрастом."""
    validate_student(rec)
    
    fio_parts = rec["fio"].split()
    surname = fio_parts[0].capitalize()
    initials = "".join(f"{part[0].upper()}." for part in fio_parts[1:])
    
    age = student_age(rec)

    return f"{surname} {initials} ({rec['group']}), {age} лет, GPA {rec['gpa']}"


def student_to_dict(rec: dict) -> dict:
    """Возвращает копию записи для сериализации."""
    validate_student(rec)
    return dict(rec)


def student_from_dict(d: dict) -> dict:
    """Десериализует словарь, приводит типы и проверяет запись через валидацию."""
    if not isinstance(d, dict):
        raise ValueError("Ожидался словарь для десериализации студента.")
    
    fio = d.get("fio")
    birthdate = d.get("birthdate")
    group = d.get("group")
    gpa = d.get("gpa")

    if gpa is not None and not isinstance(gpa, bool):
        try:
            gpa = float(gpa)
        except (ValueError, TypeError):
            pass

    rec = {
        "fio": fio,
        "birthdate": birthdate,
        "group": group,
        "gpa": gpa
    }
    
    validate_student(rec)
    return rec


if __name__ == "__main__":
    # 1. Создание корректного студента
    student = make_student("Иванов Иван Иванович", "2007-05-14", "БИВТ-26-6-1", 4.3)
    print("Создан студент:", student)
    
    # 2. Форматирование
    print("Форматирование:", format_student(student))
    
    # 3. Проверка возраста
    print("Возраст:", student_age(student))
    
    # 4. Ошибка валидации
    print("Попытка создать студента с GPA = 7:")
    try:
        make_student("Петров Петр", "2006-01-01", "ИУ-5", 7.0)
    except ValueError as e:
        print(f"Перехвачена ожидаемая ошибка: {e}")