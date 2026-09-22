import sys
from src.lib.text import normalize, tokenize, count_freq, top_n

def main() -> None:
    raw_text = sys.stdin.read()
 
    normalized = normalize(raw_text)
    tokens = tokenize(normalized)
 
    freq = count_freq(tokens)
    total_words = len(tokens)
    unique_words = len(freq)
 
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5:")
 
    for word, count in top_n(freq, 5):
        print(f"{word}: {count}")
 
 
if __name__ == "__main__":
    main()
