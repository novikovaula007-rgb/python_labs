from src.lib.tuples import format_record

print(format_record(("Иванов Иван Иванович", "BIVT-25", 4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))

try:
    format_record(("", "BIVT-25", 4.5))
except ValueError as e:
    print(f"ValueError: {e}")

try:
    format_record(("Иванов Иван Иванович", "", 4.5))
except ValueError as e:
    print(f"ValueError: {e}")

try:
    format_record(("Иванов Иван Иванович", "BIVT-25", "4.5"))
except TypeError as e:
    print(f"TypeError: {e}")