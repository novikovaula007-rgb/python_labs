def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Возвращает кортеж (минимум, максимум) для списка чисел."""
    if not nums:
        raise ValueError("Список чисел не должен быть пустым")
    return min(nums), max(nums)


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Возвращает отсортированный по возрастанию список уникальных значений."""
    return sorted(set(nums))


def flatten(mat: list[list | tuple]) -> list:
    """Расплющивает список списков/кортежей в один список по строкам (row-major)."""
    result = []
    for row in mat:
        if not isinstance(row, (list, tuple)):
            raise TypeError("Элемент матрицы должен быть списком или кортежем")
        result.extend(row)
    return result