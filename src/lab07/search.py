def linear_search(nums: list[int], x: int) -> int:
    """
    Ищет первое вхождение элемента x в списке nums.
    Принимает список чисел для поиска nums и искомое значение x.
    Возвращает индекс первого вхождения элемента или -1, если элемент не найден.

    linear_search([4, 2, 7, 2], 2) -> 1
    linear_search([4, 2, 7, 2], 9) -> -1
    linear_search([], 1) -> -1
    """
    for i, value in enumerate(nums):
        if value == x:
            return i
 
    return -1


def binary_search(sorted_nums: list[int], x: int) -> int:
    """
    Ищет элемент x в отсортированном списке с помощью бинарного поиска.
    На неотсортированном списке результат не определён.
    Принимает отсортированный по возрастанию список чисел и искомое значение x.
    Возвращает индекс найденного элемента или -1, если элемент отсутствует.

    binary_search([1, 3, 5, 7], 5) -> 2
    binary_search([1, 3, 5, 7], 4) -> -1
    binary_search([5], 5) -> 0
    binary_search([], 5) -> -1
    """
    lo, hi = 0, len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == x:
            return mid
        elif sorted_nums[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def two_sum_brute(nums: list[int], target: int) -> tuple[int, int] | None:
    """
    Находит пару индексов (i, j) с i < j таких, что сумма nums[i] + nums[j] == target.
    Принимает список чисел и целевую сумму target.
    Возвращает кортеж с индексами (i, j) или None, если пара не найдена.
    Использует метод полного перебора (O(n^2)).

    two_sum_brute([2, 7, 11, 15], 9) -> (0, 1)
    two_sum_brute([1, 2], 10) -> None
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_fast(nums: list[int], target: int) -> tuple[int, int] | None:
    """Находит пару индексов (i, j) с i < j таких, что сумма nums[i] + nums[j] == target.
    Принимает список чисел и целевую сумму target.
    Возвращает кортеж с индексами (i, j) или None, если пара не найдена.
    Использует эффективный подход со словарём за один проход (O(n)).
    """
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return (seen[diff], i)
        seen[num] = i
    return None