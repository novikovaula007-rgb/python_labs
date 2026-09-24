def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Возвращает кортеж (минимум, максимум) для списка чисел."""
    if not nums:
        raise ValueError("Список чисел не должен быть пустым")

    minimum = nums[0]
    maximum = nums[0]

    for num in nums[1:]:
        if num < minimum:
            minimum = num
        if num > maximum:
            maximum = num

    return minimum, maximum


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Возвращает отсортированный по возрастанию список уникальных значений."""
    unique_nums = []

    for x in nums:
        if not any(x == existing for existing in unique_nums):
            unique_nums.append(x)

    for i in range(1, len(unique_nums)):
        key = unique_nums[i]
        j = i - 1
        while j >= 0 and unique_nums[j] > key:
            unique_nums[j + 1] = unique_nums[j]
            j -= 1
        unique_nums[j + 1] = key

    return unique_nums


def flatten(mat: list[list | tuple]) -> list:
    """Расплющивает список списков/кортежей в один список по строкам (row-major)."""
    result = []

    for row in mat:
        if not isinstance(row, (list, tuple)):
            raise TypeError("Элемент матрицы должен быть списком или кортежем")
        result.extend(row)
        
    return result