import argparse
import sys

from src.lab08.models import make_student, format_student
from src.lab09.group import add_student, list_students, find_students, remove_student, update_student

DEFAULT_DB = "data/lab09/samples/students.csv"


def add_db_argument(parser: argparse.ArgumentParser) -> None:
    """Добавляет подкоманде общий параметр --db (путь к CSV-хранилищу)."""
    parser.add_argument(
        "--db", default=DEFAULT_DB, help=f"путь к CSV-хранилищу (по умолчанию {DEFAULT_DB})"
    )


def build_parser() -> argparse.ArgumentParser:
    """
    Создаёт парсер с подкомандами add, list, find, remove, update.
    Параметр --db есть у каждой подкоманды и пишется после её названия.
    """
    parser = argparse.ArgumentParser(
        description="Учёт студентов в CSV-файле: добавление, список, поиск, удаление, обновление"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="добавить студента", description="Добавляет студента в хранилище.")
    add_db_argument(p_add)
    p_add.add_argument("--fio", required=True, help="ФИО (минимум фамилия и имя)")
    p_add.add_argument("--birthdate", required=True, help="дата рождения в формате YYYY-MM-DD")
    p_add.add_argument("--group", required=True, help="группа, например БИВТ-26-6-5")
    p_add.add_argument("--gpa", type=float, required=True, help="средний балл от 0.0 до 5.0")

    # list
    p_list = sub.add_parser("list", help="показать всех студентов", description="Выводит студентов по одному на строку.")
    add_db_argument(p_list)
    p_list.add_argument("--sort", choices=["fio", "gpa"], help="сортировать по ФИО или по среднему баллу")

    # find
    p_find = sub.add_parser("find", help="найти студентов по части ФИО", description="Ищет подстроку в ФИО без учёта регистра.")
    add_db_argument(p_find)
    p_find.add_argument("--q", required=True, help="подстрока для поиска в ФИО")

    # remove
    p_remove = sub.add_parser("remove", help="удалить студента по ФИО", description="Удаляет все записи с точно таким ФИО.")
    add_db_argument(p_remove)
    p_remove.add_argument("--fio", required=True, help="ФИО студента (точное совпадение)")

    # update
    p_update = sub.add_parser("update", help="обновить данные студента", description="Обновляет указанные поля первой записи с таким ФИО.")
    add_db_argument(p_update)
    p_update.add_argument("--fio", required=True, help="ФИО студента (точное совпадение)")
    p_update.add_argument("--birthdate", help="новая дата рождения YYYY-MM-DD")
    p_update.add_argument("--group", help="новая группа")
    p_update.add_argument("--gpa", type=float, help="новый средний балл")

    return parser


def run_command(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Выполняет подкоманду."""
    if args.command == "add":
        student = make_student(args.fio, args.birthdate, args.group, args.gpa)
        add_student(args.db, student)
        print(f"Добавлен: {format_student(student)}")

    elif args.command == "list":
        students = list_students(args.db, args.sort)
        if not students:
            print("Студентов нет.")
        for student in students:
            print(format_student(student))

    elif args.command == "find":
        students = find_students(args.db, args.q)
        if not students:
            print("Ничего не найдено.")
        for student in students:
            print(format_student(student))

    elif args.command == "remove":
        removed = remove_student(args.db, args.fio)
        print(f"Удалено записей: {removed}")

    elif args.command == "update":
        # берём только те поля, которые пользователь действительно указал
        fields = {}
        if args.birthdate is not None:
            fields["birthdate"] = args.birthdate
        if args.group is not None:
            fields["group"] = args.group
        if args.gpa is not None:
            fields["gpa"] = args.gpa

        if not fields:
            parser.error("укажите хотя бы одно поле для обновления: --birthdate, --group или --gpa")

        if update_student(args.db, args.fio, **fields):
            print(f"Обновлено: {args.fio}")
        else:
            print(f"Ошибка: студент не найден: {args.fio}", file=sys.stderr)
            sys.exit(1)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        run_command(parser, args)
    except (ValueError, TypeError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()