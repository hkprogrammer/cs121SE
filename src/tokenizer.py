from nltk.tokenize import word_tokenize


def tokenize(input_str: str) -> list:
    return word_tokenize(input_str)