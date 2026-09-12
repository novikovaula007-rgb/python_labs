m = int(input("Минуты: "))

hours = m // 60
minutes = m % 60

print(f"{hours}:{minutes:02d}")