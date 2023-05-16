from collections import defaultdict
from glob import glob
from os.path import *
from src.tokenizer import tokenize


class ProcessJson:
    def __init__(self):
        self.all_json_freqs = defaultdict(int)
        self.all_json_inverts = defaultdict(list)
        self.save_dir = dirname(realpath(__file__))

    def go_through_files(self, custom_dir: str = None) -> None:
        # check if using a valid custom directory
        if custom_dir is not None and isdir(custom_dir):
            self.save_dir = str(custom_dir)

        # iterate through all the text files in the directory to be processed
        for json_hash in glob(pathname=f'{self.save_dir}/**/*.txt', recursive=True):
            if "_freqs" not in json_hash:
                self.process_file_words(json_hash)
                self.invert_index(json_hash)

    def process_file_words(self, url_filename: str) -> None:
        # verify that the filename is a valid text file
        if not isfile(url_filename) or '.txt' not in url_filename:
            print(f"Not valid file name: {url_filename}")
            return

        # open the file for reading
        try:
            read_obj = open(url_filename, "r")
        except OSError:
            print(f"Error opening current file: {url_filename}")
            return

        # create a dicitonary to keep track of local word frequencies
        read_dict = defaultdict(int)

        # go through each line in the file and tokenize it
        for line in read_obj:
            tokenized_words = tokenize(line)
            for word in tokenized_words:
                # add the counts to the global and local frequencies
                self.all_json_freqs[word] += 1
                read_dict[word] += 1

        # close the file for reading
        read_obj.close()

        # create a file for writing
        freq_filename = f"{url_filename.rsplit('.txt', 1)[0]}_freqs.txt"
        try:
            write_obj = open(freq_filename, "w")
        except OSError:
            print(f"Error opening current file: {freq_filename}")
            return

        # sort the local frequencies
        sorted_items = sorted(sorted(read_dict.items(), key=lambda x: x[0]), key=lambda x: x[1], reverse=True)

        # write each word frequency to the file
        for word, freq in sorted_items:
            write_obj.write(f'{word} -> {freq}\n')

        # close the file for writing
        write_obj.close()
        
        
        
    def invert_index(self, json_filename):
        # Checks if file is a .txt file
        if not isfile(json_filename) or '.txt' not in json_filename:
            print(f"Not valid file name: {json_filename}")
            return
        # Opens and read json_filename
        try:
            read_obj = open(json_filename, "r")
        except OSError:
            print(f"Error opening current file: {json_filename}")
            return
        # Removes .txt from json_filename
        json_name = json_filename[:-4].split("\\")[-1]
        #gets json name from file path
        
        # Appends tokens into all_json_inverts
        for line in read_obj:
            tokenized_words = tokenize(line)
            for word in tokenized_words:
                if(json_name not in self.all_json_inverts[word]):
                    self.all_json_inverts[word].append(json_name)    
        read_obj.close()
        
        

    def process_all_inverts(self) -> None:
        # opens a write all_inverted_index.txt
        try:
            write_obj = open(f"{self.save_dir}/all_inverted_index.txt", "w")
        except OSError:
            print("Error opening current file: all_inverted_index.txt")
            return

        # sort the global frequencies
        sorted_items = sorted(sorted(self.all_json_inverts.items()), key=lambda x: len(x[1]), reverse=True)

        # write each word json_names to the file
        for word, json_names in sorted_items:
            json_name_str = str()
            for json_name in json_names:
                json_name_str += json_name + ","
            write_obj.write(f'{word} -> {json_name_str}\n')

        # close the file for writing
        write_obj.close()
    def process_all_freqs(self) -> None:
        # open a file for writing the global frequencies
        try:
            write_obj = open(f"{self.save_dir}/all_file_freqs.txt", "w")
        except OSError:
            print("Error opening current file: all_file_freqs.txt")
            return

        # write the number of words found at the beginning of the file
        write_obj.write(f"Total words found: {len(self.all_json_freqs.keys())}\n")

        # sort the global frequencies
        sorted_items = sorted(sorted(self.all_json_freqs.items(), key=lambda x: x[0]), key=lambda x: x[1], reverse=True)

        # write each word frequency to the file
        for word, freq in sorted_items:
            write_obj.write(f'{word} -> {freq}\n')

        # close the file for writing
        write_obj.close()



def record_json_freq_invert(custom_dir: str) -> None:
    pj = ProcessJson()
    pj.go_through_files(custom_dir)
    pj.process_all_freqs()
    pj.process_all_inverts()


