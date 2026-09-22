import re


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    """
    Нормализует строку text.

    Если casefold = True - приводит к casefold.
    Если yo2e = True - заменяет все ё/Ё на е/Е.
    Убирает невидимые управляющие символы (например, \t, \r) -> 
    заменяет на пробелы, схлопывает повторяющиеся пробелы в один.
    """
    result = text

    if casefold:
        result = result.casefold()

    if yo2e:
        result = result.replace("ё", "е")
        result = result.replace("Ё", "Е")

    result = result.replace("\t", " ")
    result = result.replace("\r", " ")
    result = result.replace("\n", " ")

    result = re.sub(r" +", " ", result)

    result = result.strip()

    return result


def tokenize(text: str) -> list[str]:
    """
    Разбивает текст на список слов (токенов).

    Словом считается последовательность символов \\w (буквы, цифры,
    подчёркивание), внутри которой может встречаться дефис,
    соединяющий две части слова (например, "по-настоящему").

    Всё остальное (знаки препинания, пробелы, эмодзи и т.д.)
    считается разделителем и в результат не попадает.
    """
    pattern = r"\w+(?:-\w+)*"
    tokens = re.findall(pattern, text)
    return tokens


def count_freq(tokens: list[str]) -> dict[str, int]:
    """
    Считает, сколько раз каждое слово встречается в списке токенов.
    Возвращает словарь вида {слово: количество}.
    """
    freq: dict[str, int] = {}

    for token in tokens:
        if token in freq:
            freq[token] = freq[token] + 1
        else:
            freq[token] = 1

    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """
    Возвращает n самых частых слов из словаря частот freq.

    Пары (слово, частота) сортируются по убыванию частоты,
    а при равной частоте - по алфавиту (по возрастанию).

    Пример:
    >>> freq = {"a": 3, "b": 2, "c": 1}
    >>> top_n(freq, 2)
    [('a', 3), ('b', 2)]
    """
    pairs = list(freq.items())

    pairs.sort(key=lambda pair: (-pair[1], pair[0]))

    return pairs[:n]


if __name__ == "__main__":
    # небольшие проверки, запускаются командой: python text.py
    
    # normalize
    assert normalize("ПрИвЕт\nМИр\t") == "привет мир"
    assert normalize("ёжик, Ёлка") == "ежик, елка"
    assert normalize("Hello\r\nWorld") == "hello world"
    assert normalize("  двойные   пробелы  ") == "двойные пробелы"

    # tokenize
    assert tokenize("привет мир") == ["привет", "мир"]
    assert tokenize("по-настоящему круто") == ["по-настоящему", "круто"]
    assert tokenize("2025 год") == ["2025", "год"]

    # count_freq + top_n
    freq = count_freq(["a", "b", "a", "c", "b", "a"])
    assert freq == {"a": 3, "b": 2, "c": 1}
    assert top_n(freq, 2) == [("a", 3), ("b", 2)]

    # тай-брейк по слову при равной частоте
    freq2 = count_freq(["bb", "aa", "bb", "aa", "cc"])
    assert freq2 == {"aa": 2, "bb": 2, "cc": 1}
    assert top_n(freq2, 2) == [("aa", 2), ("bb", 2)]