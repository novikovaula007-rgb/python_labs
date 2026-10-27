import timeit
from collections import deque
from src.lab04.io_txt_csv import write_csv
from src.lab10.linked_list import ll_prepend


def pop_all_list(lst: list) -> None:
    """Снимает все элементы с начала обычного списка: n раз lst.pop(0)."""
    for _ in range(len(lst)):
        lst.pop(0)


def pop_all_deque(dq: deque) -> None:
    """Снимает все элементы с начала deque: n раз dq.popleft()."""
    for _ in range(len(dq)):
        dq.popleft()


def insert_front_list(n: int) -> None:
    """Вставляет n элементов в начало обычного списка: n раз lst.insert(0, x)."""
    lst = []
    for i in range(n):
        lst.insert(0, i)


def prepend_linked_list(n: int) -> None:
    """Вставляет n элементов в начало связного списка: n раз head = ll_prepend(head, x)."""
    head = None
    for i in range(n):
        head = ll_prepend(head, i)


def measure(prepare, run, repeats: int = 1) -> float:
    """Время run(data) в секундах."""
    best = None
    for _ in range(repeats):
        data = prepare()
        t = timeit.timeit(lambda: run(data), number=1)
        if best is None or t < best:
            best = t
    return best


def main() -> None:
    """Запускает бенчмарки, выводит таблицу в консоль и сохраняет её в CSV."""
    csv_rows: list[tuple[str, int, str, str, str]] = []

    for n in [10_000, 100_000]:
        # 1. Очередь: n раз list.pop(0) против n раз deque.popleft()
        t_list = measure(lambda: list(range(n)), pop_all_list)
        t_deque = measure(lambda: deque(range(n)), pop_all_deque, repeats=5)
        csv_rows.append(("queue_pop_front", n, f"{t_list:.6f}", f"{t_deque:.6f}", f"{t_list / t_deque:.1f}"))

        # 2. Вставка в начало: n раз list.insert(0, x) против n раз ll_prepend
        t_list = measure(lambda: n, insert_front_list)
        t_ll = measure(lambda: n, prepend_linked_list, repeats=5)
        csv_rows.append(("insert_front", n, f"{t_list:.6f}", f"{t_ll:.6f}", f"{t_list / t_ll:.1f}"))

    header = ("operation", "n", "list", "deque_ll", "ratio")
    write_csv(csv_rows, "data/lab10/bench.csv", header=header)

    print(f"{'Operation':<16} | {'N':<8} | {'List':<10} | {'Deque/LL':<10} | {'Ratio':<8}")
    print("-" * 64)
    for operation, n, t_list, t_other, ratio in csv_rows:
        print(f"{operation:<16} | {n:<8} | {t_list:<10} | {t_other:<10} | {ratio:<8}")


if __name__ == "__main__":
    main()