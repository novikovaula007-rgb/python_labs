def validate_rectangular(mat: list[list[float | int]]) -> None:
    """Проверяет, является ли матрица прямоугольной (одинаковая длина строк)."""
    if not mat:
        return
    first_len = len(mat[0])
    if any(len(row) != first_len for row in mat):
        raise ValueError("Матрица должна быть прямоугольной.")


def transpose(mat: list[list[float | int]]) -> list[list]:
    """Меняет строки и столбцы матрицы местами."""
    if not mat:
        return []

    validate_rectangular(mat)
    transposed = [[mat[row][col] for row in range(len(mat))] for col in range(len(mat[0]))]

    return transposed


def row_sums(mat: list[list[float | int]]) -> list[float]:
    """Вычисляет сумму элементов по каждой строке матрицы."""
    if not mat:
        return []

    validate_rectangular(mat)

    return [sum(row) for row in mat]


def col_sums(mat: list[list[float | int]]) -> list[float]:
    """Вычисляет сумму элементов по каждому столбцу матрицы."""
    if not mat:
        return []

    validate_rectangular(mat)
    column_sums = [sum(mat[row][col] for row in range(len(mat))) for col in range(len(mat[0]))]
    
    return column_sums