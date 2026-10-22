import argparse
import sys

from src.lab04.io_txt_csv import read_text
from src.lib.text import normalize, tokenize, count_freq, top_n


def read_input(path: str) -> str:
    """
    Читает текстовый файл (в кодировке UTF-8) и возвращает его содержимое.

    Если файл не найден или не читается как UTF-8 - печатает понятное
    сообщение об ошибке (в stderr) и завершает программу с кодом 1.
    """
    try:
        return read_text(path)
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {path}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Ошибка: не удалось прочитать файл {path} в кодировке UTF-8", file=sys.stderr)
        sys.exit(1)


def run_cat(args: argparse.Namespace) -> None:
    """
    Подкоманда cat: выводит содержимое файла построчно.
    Если указан флаг -n - перед каждой строкой печатается её номер.
    """
    text = read_input(args.input)

    # splitlines() режет текст на строки (без символов переноса)
    lines = text.splitlines()

    for number, line in enumerate(lines, start=1):
        if args.n:
            print(f"{number}: {line}")
        else:
            print(line)


def run_stats(args: argparse.Namespace) -> None:
    """
    Подкоманда stats: считает частоты слов в файле (функции из ЛР3)
    и печатает общее число слов, число уникальных слов и топ слов.
    """
    text = read_input(args.input)

    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{args.top}:")
    for word, count in top_n(freq, n=args.top):
        print(f"{word}: {count}")
    

def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI-утилиты для работы с текстовыми файлами"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # подкоманда cat
    cat_parser = subparsers.add_parser(
        "cat",
        help="вывести содержимое файла",
        description="Выводит содержимое файла построчно.",
    )
    cat_parser.add_argument("--input", required=True, help="путь к текстовому файлу")
    cat_parser.add_argument("-n", action="store_true", help="нумеровать строки")

    # подкоманда stats
    stats_parser = subparsers.add_parser(
        "stats",
        help="частоты слов в тексте",
        description="Считает частоты слов в тексте и выводит самые частые.",
    )
    stats_parser.add_argument("--input", required=True, help="путь к текстовому файлу")
    stats_parser.add_argument(
        "--top", type=int, default=5, help="сколько слов показать (по умолчанию 5)"
    )

    args = parser.parse_args()

    if args.command == "cat":
        run_cat(args)
    elif args.command == "stats":
        if args.top <= 0:
            parser.error("--top должен быть положительным числом")
        run_stats(args)


if __name__ == "__main__":
    main()