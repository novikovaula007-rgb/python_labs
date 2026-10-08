import csv
from pathlib import Path
from typing import Iterable, Sequence


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """
    Читает текстовый файл целиком и возвращает его содержимое
    как одну строку.

    По умолчанию файл читается в кодировке UTF-8. Если нужен другой
    формат кодировки, можно передать его явно, например:
        read_text("data/input.txt", encoding="cp1251")

    Если файл не найден - функция не перехватывает ошибку,
    а даёт ей "всплыть" наружу как FileNotFoundError.
    Если кодировка не подходит к содержимому файла - аналогично
    всплывает UnicodeDecodeError.

    Если файл пустой - возвращается пустая строка "".
    """
    path = Path(path)
    text = path.read_text(encoding=encoding)
    return text


def write_csv(
    rows: Iterable[Sequence],
    path: str | Path,
    header: tuple[str, ...] | None = None,
) -> None:
    """
    Записывает строки rows в CSV-файл path с разделителем ",".

    Если указан header - он записывается первой строкой файла.

    Файл создаётся заново (если его не было) либо полностью
    перезаписывается (если уже существовал).

    Перед записью проверяется, что все строки в rows имеют
    одинаковую длину. Если это не так - поднимается ValueError.
    Если header задан, его длина тоже должна совпадать с длиной строк.

    Если rows пуст и header=None - создаётся пустой файл (0 строк).
    Если rows пуст, а header задан - в файле будет только заголовок.
    """
    path = Path(path)

    # превращаем rows в обычный список, чтобы можно было
    # пройтись по нему несколько раз (для проверки и для записи)
    rows_list = list(rows)

    # проверяем, что все строки одинаковой длины
    if len(rows_list) > 0:
        first_row_len = len(rows_list[0])

        for row in rows_list:
            if len(row) != first_row_len:
                raise ValueError(
                    "Все строки в rows должны иметь одинаковую длину"
                )

        if header is not None and len(header) != first_row_len:
            raise ValueError(
                "Длина header должна совпадать с длиной строк в rows"
            )

    # создаём родительскую папку, если её ещё нет
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if header is not None:
            writer.writerow(header)

        for row in rows_list:
            writer.writerow(row)


if __name__ == "__main__":
    txt = read_text("data/lab04/input.txt")
    print(txt)

    write_csv([("word", "count"), ("test", 3)], "data/lab04/check.csv")
    print("CSV создан.")