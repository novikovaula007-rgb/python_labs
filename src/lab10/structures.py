from collections import deque


def stack_push(st: list, item) -> None:
    """Добавляет элемент item на вершину стека."""
    st.append(item)


def stack_pop(st: list):
    """Снимает верхний элемент стека и возвращает его."""
    if not st:
        raise IndexError("Нельзя снять элемент: стек пуст")
    return st.pop()


def stack_peek(st: list):
    """
    Возвращает верхний элемент стека без удаления.
    Если стек пуст - возвращает None.
    """
    if not st:
        return None
    return st[-1]


def stack_is_empty(st: list) -> bool:
    """True, если стек пуст."""
    return len(st) == 0


def queue_enqueue(q: deque, item) -> None:
    """Добавляет элемент item в конец очереди."""
    q.append(item)


def queue_dequeue(q: deque):
    """Берёт элемент из начала очереди и возвращает его."""
    if not q:
        raise IndexError("Нельзя взять элемент: очередь пуста")
    return q.popleft()


def queue_peek(q: deque):
    """
    Возвращает первый элемент очереди без удаления.
    """
    if not q:
        return None
    return q[0]


def queue_is_empty(q: deque) -> bool:
    """True, если очередь пуста."""
    return len(q) == 0


def is_balanced(s: str) -> bool:
    """
    Проверяет скобочную последовательность для скобок (), [], {}.
    Все остальные символы игнорируются. Решение - один проход со стеком.

    is_balanced("([]{})") -> True
    is_balanced("([)]")   -> False
    is_balanced("((")     -> False
    is_balanced("")       -> True
    """
    # закрывающая скобка -> какая открывающая должна быть на вершине стека
    pairs = {")": "(", "]": "[", "}": "{"}
    st = []

    for ch in s:
        if ch in "([{":
            stack_push(st, ch)
        elif ch in pairs:
            # закрывающая скобка: стек не должен быть пуст, а на вершине - её пара
            if stack_is_empty(st) or stack_pop(st) != pairs[ch]:
                return False

    # если в конце в стеке что-то осталось - есть незакрытые скобки
    return stack_is_empty(st)


if __name__ == "__main__":
    print("Стек")
    st = []
    stack_push(st, 1)
    stack_push(st, 2)
    stack_push(st, 3)
    print("после push 1, 2, 3:", st)
    print("peek:", stack_peek(st))
    print("pop:", stack_pop(st), "->", st)
    print("is_empty:", stack_is_empty(st))
    print("peek пустого стека:", stack_peek([]))
    try:
        stack_pop([])
    except IndexError as e:
        print("pop пустого стека -> IndexError:", e)

    print("Очередь")
    q = deque()
    queue_enqueue(q, "a")
    queue_enqueue(q, "b")
    queue_enqueue(q, "c")
    print("после enqueue a, b, c:", list(q))
    print("peek:", queue_peek(q))
    print("dequeue:", queue_dequeue(q), "->", list(q))
    print("is_empty:", queue_is_empty(q))
    try:
        queue_dequeue(deque())
    except IndexError as e:
        print("dequeue пустой очереди -> IndexError:", e)

    print("Скобочная последовательность")
    for text in ["([]{})", "([)]", "((", "", "a(b)c", ")("]:
        print(f"{text} -> {is_balanced(text)}")

        