from collections import defaultdict
from glob import glob
from os.path import *
from src.tokenizer import tokenize


class URLFreqs:
    def __init__(self):
        self.all_url_freqs = defaultdict(int)
        self.save_dir = dirname(realpath(__file__))

    def go_through_files(self, custom_dir: str = None) -> None:
        # check if using a valid custom directory
        if custom_dir is not None and isdir(custom_dir):
            self.save_dir = str(custom_dir)

        # iterate through all the text files in the directory to be processed
        for url_hash in glob(pathname=f'{self.save_dir}/**/*.txt', recursive=True):
            if "_freqs" not in url_hash:
                self.process_file_words(url_hash)

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
                self.all_url_freqs[word] += 1
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

    def process_all_freqs(self) -> None:
        # open a file for writing the global frequencies
        try:
            write_obj = open(f"{self.save_dir}/all_file_freqs.txt", "w")
        except OSError:
            print("Error opening current file: all_file_freqs.txt")
            return

        # write the number of words found at the beginning of the file
        write_obj.write(f"Total words found: {len(self.all_url_freqs.keys())}\n")

        # sort the global frequencies
        sorted_items = sorted(sorted(self.all_url_freqs.items(), key=lambda x: x[0]), key=lambda x: x[1], reverse=True)

        # write each word frequency to the file
        for word, freq in sorted_items:
            write_obj.write(f'{word} -> {freq}\n')

        # close the file for writing
        write_obj.close()


def record_url_freqs(custom_dir: str) -> None:
    url_freqs = URLFreqs()
    url_freqs.go_through_files(custom_dir)
    url_freqs.process_all_freqs()
