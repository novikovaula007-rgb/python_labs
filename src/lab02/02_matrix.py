from src.lib.matrix import col_sums, row_sums, transpose

print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))

try:
    transpose([[1, 2], [3]])
except ValueError as e:
    print(f"ValueError: {e}")

print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))

try:
    row_sums([[1, 2], [3]])
except ValueError as e:
    print(f"ValueError: {e}")

print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))

try:
    col_sums([[1, 2], [3]])
except ValueError as e:
    print(f"ValueError: {e}")