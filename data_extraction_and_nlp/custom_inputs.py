from pathlib import Path

# load custom stopwords
stopwords_path = Path("./data/StopWords")
stopwords_files = list(stopwords_path.glob("*"))

custom_stopwords = set()
for file in stopwords_files:
    with open(file = file, mode = "r", encoding = 'utf-8', errors = 'ignore') as f:
        custom_stopwords.update(f.read().splitlines())

custom_stopwords = set(word.lower() for word in custom_stopwords)
print(f"Custom StopWords: {len(custom_stopwords)}")

positive_words_file = Path("./data/MasterDictionary/positive-words.txt")
negative_words_file = Path("./data/MasterDictionary/negative-words.txt")

def load_positive_negative_words(positive_file:Path, negative_file:Path):
    # load positive and negative words
    positive_words = set()
    negative_words = set()

    # Load positive words
    with open(file = positive_file, mode = "r") as f:
        positive_words.update(f.read().splitlines())

    # Load negative words
    with open(file = negative_file, mode = "r", encoding = 'utf-8', errors = 'ignore') as f:
        negative_words.update(f.read().splitlines())

    positive_words = set(word.lower() for word in positive_words)
    negative_words = set(word.lower() for word in negative_words)

    return positive_words, negative_words

positive_words, negative_words = load_positive_negative_words(
    positive_file = positive_words_file, 
    negative_file = negative_words_file
    )

print(f"Positive Words: {len(positive_words)}")
print(f"Negative Words: {len(negative_words)}")