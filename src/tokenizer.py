from nltk.tokenize import word_tokenize


def tokenize(input_str: str) -> list:
    
    input_str = input_str.rstrip("\n")
    nltkTokenize = word_tokenize(input_str)
    

    result = []
    
    #removes punctuation.
    for i in nltkTokenize:
        if len(i) == 0 or i == " ":
            continue
        
        if any([char in ",.!@©/?[]{}#$^&*()\\|;:<>=+" for char in i]):
            continue
        
        
        if len(i) > 0 and (i[0] == "\'" or i[0] == "\""):
            i = i[1:]
        
        if len(i) >0 and (i[-1] == "\'" or i[-1] == "\""):
            i = i[:-1]
        if len(i) == 0 or i == " ":
            continue
        result.append(i)
        
    return result


    # token_list = []
    
    # for word in input_str.split():
    #     if not word.encode().isalnum():
    #         for i in range(len(word)):
    #             if not word[i].encode().isalnum():
    #                 word = word.replace(word[i], " ")
    #         token_list.extend(word.split())
    #     else:
    #         token_list.append(word)
    
    # return token_list


if __name__ == "__main__":
    print(tokenize("'something''"))