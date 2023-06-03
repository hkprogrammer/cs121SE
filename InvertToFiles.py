from time import time
from tqdm import tqdm
import os
from pathlib import Path
def set_word_index(all_inverted_index_directory):
    #opens new word_index file to store word_index
    try:
        print(f"{all_inverted_index_directory}/word_index.txt")
        # word_index = open(f"{all_inverted_index_directory}\\word_index.txt","w","utf-8")
        
        f = Path(f"{all_inverted_index_directory}/word_index.txt")
        if not f.exists():
            f.touch()
        word_index = open(f,"w",encoding="utf-8")
    except OSError as ex:
        print(f"Error opening current file: word_index.txt")
        return
    #opens all_inverted_index file as f and loops through each line with enumerate
    
    
    isExist = os.path.exists(Path(all_inverted_index_directory + "/word_index_holder"))
    if not isExist:

        # Create a new directory because it does not exist
        os.makedirs(Path(all_inverted_index_directory + "/word_index_holder"))
    
    with open(Path(f"{all_inverted_index_directory}/all_inverted_index.txt"), "r",encoding="utf-8") as f:
        for index,line in tqdm(enumerate(f)):
            try:
                wordFile = Path(f"{all_inverted_index_directory}/word_index_holder/file{index}.txt")
                if not wordFile.exists():
                    wordFile.touch()
                word_value = open(wordFile,"w",encoding="utf-8")
            except OSError as ex:
                raise ex
                print(f"Error opening current file: file{index}.txt")
                continue
            #gets word from file
            word = line.split(" -> ")[0]
            #writes writes word and index in word_index file
            word_index.write(f"{word} -> {index}\n")
            #writes line in file{index} file
            word_value.write(line)
            
def read_word_index(word) -> int:
    #opens word_index
    with open(Path("developer/DEV/word_index.txt"), "r", encoding="utf-8") as f:
        for line in f:
            line_list = line.split(" -> ")
            if(line_list[0] == word):
                
                with open(Path(f"developer/DEV/word_index_holder/file{line_list[1].strip()}.txt"),"r",encoding="utf-8") as file:
                    return file.readlines()[0].strip()
                
               
    #returns -1 if nothing is found
    return -1


if __name__ == "__main__":
    # s = time()
    set_word_index("developer/DEV")
    # v = time()
    
    # print(v-s)
    
    
    # print(read_word_index("Christina"))