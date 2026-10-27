class Node:
    """Узел односвязного списка: значение и ссылка на следующий узел (или None)."""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def ll_from_list(values: list) -> Node | None:
    """
    Собирает связный список из обычного списка и возвращает его голову.

    ll_from_list([1, 2, 3]) -> [1] -> [2] -> [3] -> None
    ll_from_list([]) -> None
    """
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def ll_to_list(head: Node | None) -> list:
    """Возвращает значения узлов от головы к хвосту обычным списком."""
    result = []
    cur = head
    while cur is not None:
        result.append(cur.value)
        cur = cur.next
    return result


def ll_length(head: Node | None) -> int:
    """Количество узлов (проходом от головы, O(n))."""
    count = 0
    cur = head
    while cur is not None:
        count += 1
        cur = cur.next
    return count


def ll_prepend(head: Node | None, value) -> Node:
    """
    Добавляет элемент в начало за O(1) и возвращает новую голову.
    Ничего не сдвигается: новый узел просто указывает на старую голову.
    """
    return Node(value, head)


def ll_append(head: Node | None, value) -> Node:
    """
    Добавляет элемент в конец (проходом от головы, O(n)) и возвращает голову.
    Для пустого списка возвращается новый единственный узел.
    """
    new_node = Node(value)

    if head is None:
        return new_node

    cur = head
    while cur.next is not None:   # идём до последнего узла
        cur = cur.next
    cur.next = new_node

    return head


def ll_insert(head: Node | None, idx: int, value) -> Node:
    """
    Вставляет элемент так, чтобы он оказался на позиции idx, и возвращает голову.
    Допустимо 0 <= idx <= длина списка (idx == 0 - вставка в начало,
    idx == длине - вставка в конец). 
    """
    if idx < 0 or idx > ll_length(head):
        raise IndexError(f"Индекс {idx} вне диапазона для списка длины {ll_length(head)}")

    if idx == 0:
        return ll_prepend(head, value)

    # идём к узлу, который будет стоять перед новым (позиция idx - 1)
    prev = head
    for _ in range(idx - 1):
        prev = prev.next

    prev.next = Node(value, prev.next)
    return head


def ll_remove(head: Node | None, value) -> Node | None:
    """
    Удаляет первое вхождение value и возвращает голову (она может смениться,
    а у списка из одного элемента станет None).
    """
    if head is not None and head.value == value:
        return head.next

    prev = head
    while prev is not None and prev.next is not None:
        if prev.next.value == value:
            prev.next = prev.next.next
            return head
        prev = prev.next

    raise ValueError(f"Значения {value} нет в списке")


def ll_reverse(head: Node | None) -> Node | None:
    """
    Разворачивает список на месте (без копирования значений), тремя ссылками
    prev / cur / nxt, и возвращает новую голову (бывший последний узел).
    Использовать надо так: head = ll_reverse(head)
    """
    prev = None
    cur = head

    while cur is not None:
        nxt = cur.next    # запоминаем следующий узел, пока не потеряли
        cur.next = prev   # разворачиваем ссылку назад
        prev = cur        # сдвигаем prev и cur на шаг вперёд
        cur = nxt

    return prev


def ll_repr(head: Node | None) -> str:
    """
    Строковое представление: "[1] -> [2] -> [3] -> None"; для пустого списка "None".
    """
    parts = []
    cur = head
    while cur is not None:
        parts.append(f"[{cur.value}]")
        cur = cur.next

    if not parts:
        return "None"
    return " -> ".join(parts) + " -> None"


if __name__ == "__main__":
    head = ll_from_list([1, 2, 3])
    print("from_list([1, 2, 3]):", ll_repr(head))
    print("to_list:", ll_to_list(head), "| length:", ll_length(head))

    head = ll_prepend(head, 0)
    print("prepend 0:", ll_repr(head))
    head = ll_append(head, 4)
    print("append 4:", ll_repr(head))
    head = ll_insert(head, 2, 99)
    print("insert(2, 99):", ll_repr(head))
    head = ll_remove(head, 99)
    print("remove 99:", ll_repr(head))

    print("ll_reverse")
    print("до:   ", ll_repr(head))
    head = ll_reverse(head)
    print("после:", ll_repr(head))

    print("Ошибки")
    try:
        ll_insert(head, 10, 5)
    except IndexError as e:
        print("insert вне диапазона -> IndexError:", e)
    try:
        ll_remove(head, 1000)
    except ValueError as e:
        print("remove отсутствующего -> ValueError:", e)
    print("пустой список:", ll_repr(None), "| from_list([]) is None:", ll_from_list([]) is None)