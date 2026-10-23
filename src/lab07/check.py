import random
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort


def check_sorting(fn, trials: int = 100) -> int:
    """
    Проверяет функцию сортировки на случайных данных против эталонного sorted().
    Принимает функцию сортировки для проверки и количество испытаний (по умолчанию 100).
    Возвращает количество успешно пройденных тестов.
    """
    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        original = list(nums)
        result = fn(nums)
        assert result == sorted(nums), f"{fn.__name__} ошиблась на {nums}: получено {result}, ожидалось {sorted(nums)}"
        assert nums == original, f"{fn.__name__} изменила исходный список"
    return trials


def check_search() -> int:
    """
    Проверяет функции linear_search и binary_search на случайных данных.
    Возвращает количество успешно пройденных испытаний.
    """
    trials = 100
    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-50, 50) for _ in range(n)]
        x = random.randint(-60, 60)
        
        # Линейный поиск против list.index
        try:
            expected_lin = nums.index(x)
        except ValueError:
            expected_lin = -1
        actual_lin = linear_search(nums, x)
        assert actual_lin == expected_lin, f"linear_search ошиблась для поиска {x} в {nums}: получено {actual_lin}, ожидалось {expected_lin}"

        # Бинарный поиск
        sorted_nums = sorted(nums)
        try:
            expected_bin = sorted_nums.index(x)
        except ValueError:
            expected_bin = -1
        actual_bin = binary_search(sorted_nums, x)
        if expected_bin == -1:
            assert actual_bin == -1, f"binary_search не нашла элемент, которого нет: {x} в {sorted_nums}"
        else:
            assert actual_bin != -1 and sorted_nums[actual_bin] == x, f"binary_search вернула некорректный индекс {actual_bin} для {x} в {sorted_nums}"
    return trials


def check_two_sum(trials: int = 100) -> int:
    """
    Проверяет эквивалентность результатов two_sum_brute и two_sum_fast.
    Принимает количество испытаний (по умолчанию 100).
    Возвращает количество успешно пройденных тестов.
    """
    for _ in range(trials):
        n = random.randint(2, 30)
        nums = [random.randint(-50, 50) for _ in range(n)]
        if random.random() > 0.3 and n >= 2:
            i, j = random.sample(range(n), 2)
            target = nums[i] + nums[j]
        else:
            target = random.randint(-200, 200)

        res_brute = two_sum_brute(nums, target)
        res_fast = two_sum_fast(nums, target)

        if res_brute is None:
            assert res_fast is None, f"two_sum_brute нашла None, а fast нашла {res_fast} для nums={nums}, target={target}"
        else:
            bi, bj = res_brute
            assert nums[bi] + nums[bj] == target, f"two_sum_brute вернула неверные индексы {res_brute}"
            assert res_fast is not None, f"two_sum_brute нашла пару, а fast вернула None"
            fi, fj = res_fast
            assert nums[fi] + nums[fj] == target, f"two_sum_fast вернула неверные индексы {res_fast}"
    return trials


if __name__ == "__main__":
    random.seed(42)
    total = 0
    for fn in (bubble_sort, insertion_sort, selection_sort):
        total += check_sorting(fn)
    total += check_search()
    total += check_two_sum()
    print(f"OK: {total} проверок")