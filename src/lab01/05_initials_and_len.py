raw_input = input("ФИО: ")
words = raw_input.split()
initials = "".join(word[0].upper() for word in words)
clean_text = " ".join(words)

print(f"Инициалы: {initials}.")
print(f"Длина (символов): {len(clean_text)}")