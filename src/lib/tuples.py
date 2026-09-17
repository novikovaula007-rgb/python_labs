def format_record(rec: tuple[str, str, float]) -> str:
    """Форматирует запись о студенте в текстовую строку.
    Raises:
        TypeError: Если входные данные имеют неверный тип.
        ValueError: Если ФИО содержит менее 2 слов или группа пустая.
    """
    if not isinstance(rec, tuple) or len(rec) != 3:
        raise TypeError("Запись должна быть кортежем из 3 элементов: (fio, group, gpa).")

    fio, group, gpa = rec

    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError("Поля ФИО и группа должны быть строками.")

    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise TypeError("GPA должен быть числом (float или int).")

    fio_parts = fio.split()
    if len(fio_parts) < 2:
        raise ValueError("ФИО должно содержать как минимум фамилию и имя.")

    clean_group = group.strip()
    if not clean_group:
        raise ValueError("Название группы не может быть пустым.")

    surname = fio_parts[0].capitalize()
    initials = "".join(f"{part[0].upper()}." for part in fio_parts[1:])

    return f"{surname} {initials}, гр. {clean_group}, GPA {gpa:.2f}"