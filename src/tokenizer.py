from nltk.tokenize import word_tokenize


def tokenize(input_str: str) -> list:
    nltkTokenize = word_tokenize(input_str)
    
    
    
    result = []
    
    #removes punctuation.
    for i in nltkTokenize:
        if any([char in ",.!@©/?[]{}#$^&*()\\|;:<>=+" for char in i]):
            continue
        result.append(i)
    return result

if __name__ == "__main__":
    print(tokenize("My name is Hitoki, however ? !@#, This is not a thing! What."))