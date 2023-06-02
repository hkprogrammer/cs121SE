def tokenize(input_str: str) -> list:
    token_list = []
    
    for word in input_str.split():
        if not word.encode().isalnum():
            for i in range(len(word)):
                if not word[i].encode().isalnum():
                    word = word.replace(word[i], " ")
            token_list.extend(word.split())
        else:
            token_list.append(word)
    
    return token_list

if __name__ == "__main__":
    print(tokenize("My name is Hitoki, however ? !@#, This is not a thing! What."))
