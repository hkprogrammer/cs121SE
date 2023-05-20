from collections import defaultdict
from glob import glob
from os.path import *
from src.tokenizer import tokenize
from tqdm import tqdm
from src.extractText import extract_text_from_json_files
import math

class ProcessJson:
    def __init__(self):
        self.all_json_freqs = defaultdict(int)
        self.all_json_inverts = defaultdict(list)
        self.save_dir = dirname(realpath(__file__))
        self.doc_id = {}
        self.doc_id_num = 1
        self.doc_freqs = {}
        self.saveThreshold = 8000 # threshold in lecture slides
        self.counterFileName = 1
        self.savedTokens = 0
        self.savedDocs = 0
        self.docLength = {}
        


    def go_through_files(self, custom_dir: str = None) -> None:
        # check if using a valid custom directory
        if custom_dir is not None and isdir(custom_dir):
            self.save_dir = str(custom_dir)

        # iterate through all the text files in the directory to be processed
        print("===============Extract/Parsing File=================")
        print(f"===============LEG {self.counterFileName}=================")
        
        counter = 1
        for json_hash in tqdm(glob(pathname=f'{self.save_dir}/**/*.json', recursive=True)):
            # print(json_hash)

            try:
                if counter % self.saveThreshold == 0:
                    self.saveData()

                text = extract_text_from_json_files(json_hash)
                if text == "":
                    continue
                self.process_file_words(text,json_hash)
                self.invert_index(text,json_hash)
                counter += 1
                
            except Exception as ex:
                print("exception hapepened during parsing: ", ex)
                print("file: ",json_hash)
        return counter

    def process_file_words(self, fileText: str,url_filename:str) -> None:
        # verify that the filename is a valid text file
        read_dict = defaultdict(int)
        # go through each line in the file and tokenize it

        tokenized_words = tokenize(fileText)
        for word in tokenized_words:
            # add the counts to the global and local frequencies
            self.all_json_freqs[word] += 1
            read_dict[word] += 1

        # sort the local frequencies
        sorted_items = sorted(sorted(read_dict.items(), key=lambda x: x[0]), key=lambda x: x[1], reverse=True)
        
        word_freq = {}
        # write each word frequency to the file
        for word, freq in sorted_items:
            # write_obj.write(f'{word} -> {freq}\n')
            word_freq[word] = freq
        
        self.doc_freqs[url_filename.rsplit('.json', 1)[0]] = word_freq

        # close the file for writing
        # write_obj.close()
        
        
        
    def invert_index(self, file_text:str,json_name):
        
        
        
        tokenized_words = tokenize(file_text)
        for word in tokenized_words:
            if(json_name not in self.all_json_inverts[word]):
                full_extention_name = json_name[json_name.index("DEV")+4:]
                if full_extention_name in self.doc_id:
                    docId = self.doc_id[full_extention_name]
                else:
                    
                    docId = self.doc_id_num
                    self.docLength[docId] = len(file_text)
                    self.doc_id[full_extention_name] = docId
                    self.doc_id_num +=1
                # if docId in self.all_json_inverts[word]:
                #     continue
                freq = self.doc_freqs[json_name[:-5]][word]
                if (docId,freq) in self.all_json_inverts[word]:
                    continue
                
                self.all_json_inverts[word].append((docId,freq))    
        
    def process_all_inverts(self) -> None:
        # opens a write all_inverted_index.txt
        
        
        
        try:
            
            write_obj = open(f"{self.save_dir}/{self.counterFileName}_inverted_index.txt", "w",encoding="utf-8")
        except OSError:
            print("Error opening current file: {self.counterFileName}_inverted_index.txt")
            return

        # sort the global frequencies
        for k,v in self.all_json_inverts.items():
            v = sorted(v,key=lambda x:x[1],reverse=True)
            self.all_json_inverts[k] = v
        sorted_items = sorted(self.all_json_inverts.items(), key=lambda x: len(x[1]), reverse=True)

        # write each word json_names to the file
        print(f"===============Writing {self.counterFileName} Inverted Index File=================")
        for word, id in tqdm(sorted_items):
            
            
            # json_name_str = str()
            # for json_name in json_names:
            #     json_name_str += json_name + ","
            
            
            # freq = self.doc_freqs[self.doc]
            # print(f'{word} -> {",".join([f"({i[0]}, {i[1]})" for i in id])}\n')
            
            write_obj.write(f'{word} -> {",".join([f"({i[0]}, {i[1]})" for i in id])}\n')

        # close the file for writing
        write_obj.close()
        
    def process_all_freqs(self) -> None:
        # open a file for writing the global frequencies
        try:
            write_obj = open(f"{self.save_dir}/all_file_freqs.txt", "w",encoding="utf-8")
        except OSError:
            print("Error opening current file: all_file_freqs.txt")
            return

        # write the number of words found at the beginning of the file
        write_obj.write(f"Total words found: {len(self.all_json_inverts)}\n")

        # sort the global frequencies
        # sorted_items = sorted(sorted(self.all_json_freqs.items(), key=lambda x: x[0]), key=lambda x: x[1], reverse=True)

        sorted_items = defaultdict(int)
       
        for i in self.all_json_inverts:
            for doc,freq in self.all_json_inverts[i]:
                sorted_items[i] += freq


        # write each word frequency to the file
        
        for word, freq in sorted_items.items():
            write_obj.write(f'{word} -> {freq}\n')

        # close the file for writing
        write_obj.close()
    def writeDocID(self):
        
        #reverse DocIDs:
        
        f = open(f"{self.save_dir}/{self.counterFileName}_id_map.txt","w",encoding="utf-8")
        appearedID = set()
        # print(self.doc_id)
        print(f"===============Writing {self.counterFileName} DocID Map File=================")
        
        for path, id in tqdm(self.doc_id.items()):
            if id in appearedID:
                print("ERRORS: ",path,id)
                continue
            appearedID.add(id)
            f.write(f"{id} -> {path}\n")
        f.close()
    
    def writeNumDocs(self):
        print(f"===============Writing final Inverted Index Count File=================")
        f = open(f"{self.save_dir}/inverted_index_count.txt","w",encoding="utf-8")
        f.write(str(len(self.all_json_inverts)))
        f.close()
            
    def saveData(self):
        
        
        print(f"\n\n\n{len(self.all_json_inverts)} numer of words have been parsed. {len(self.doc_id)} docs has been parsed.")
        print(f"Saved {self.savedTokens} non-duplicative tokens so far. Saved {self.savedDocs} so far")
        print(f"===============LEG {self.counterFileName}=================")
        self.savedTokens += len(self.all_json_inverts)
        self.savedDocs += len(self.doc_id)
        self.process_all_inverts()
        self.writeDocID()
        self.all_json_inverts = {}
        
        self.counterFileName+=1
        self.all_json_freqs = defaultdict(int)
        self.all_json_inverts = defaultdict(list)
        self.doc_id = {}
        self.doc_freqs = {}
    
    def mergeFiles(self):
        self.all_json_freqs = defaultdict(int)
        self.all_json_inverts = defaultdict(list)
        self.doc_id = {}
        self.doc_freqs = {}
        print("===============Merging files=================")

        for fileNum in tqdm(range(1,self.counterFileName+1)):
            #merge inverted index of all files
            
            with open(f"{self.save_dir}/{fileNum}_inverted_index.txt","r",encoding="utf-8") as f:
                for i in f:
                    line = i.rstrip("\n").split(" -> ")
                    word = line[0]
                    
                    docIDs = line[1]
                    docs = []
                    for j in docIDs.split("),("):
                        j = j.rstrip("\n")
                        numbers = j[1:-1] if j.startswith("(") and j.endswith(")") else j[1:] if j.startswith("(") else j[:-1] if j.endswith(")") else j 
                        
                        tup = numbers.split(", ")
                        docID,freq = int(tup[0]),int(tup[1])
                        docs.append((docID,freq))
                       
                    if word in self.all_json_inverts:
                        self.all_json_inverts[word].extend(docs)
                    else:
                        self.all_json_inverts[word] = docs
                        
            with open(f"{self.save_dir}/{fileNum}_id_map.txt","r",encoding="utf-8") as f:
                for i in f:
                    line = i.rstrip("\n").split(" -> ")
                    docID = int(line[0])
                    
                    if docID in self.doc_id:
                        print(f"some how {docID} appeared in self.doc_id during {fileNum}_id_map.txt")
                        continue
                    self.doc_id[docID] = line[1]            
                
    def writeFinal(self):
        try:
            
            write_obj = open(f"{self.save_dir}/all_inverted_index.txt", "w",encoding="utf-8")
        except OSError:
            print("Error opening current file: all_inverted_index.txt")
            return

        # sort the global frequencies
        allDocLength = len(self.all_json_inverts)
        for k,v in self.all_json_inverts.items():
            
            
            
            
            for i in range(len(v)):
                v[i] = list(v[i])    
                v[i][1] = self.tfidf((v[i][1]/self.docLength[v[i][0]]),(allDocLength/(1+len(v))))
                v[i] = tuple(v[i])
            v = sorted(v,key=lambda x:x[1],reverse=True)
            self.all_json_inverts[k] = v
            
            
    
        sorted_items = sorted(self.all_json_inverts.items(), key=lambda x: len(x[1]), reverse=True)

        # write each word json_names to the file
        print("===============Writing Final Inverted Index File=================")
        for word, id in tqdm(sorted_items):
            
            
            # json_name_str = str()
            # for json_name in json_names:
            #     json_name_str += json_name + ","
            
            
            # freq = self.doc_freqs[self.doc]
            # print(f'{word} -> {",".join([f"({i[0]}, {i[1]})" for i in id])}\n')
            
            write_obj.write(f'{word} -> {",".join([f"({i[0]}, {i[1]})" for i in id])}\n')

        # close the file for writing
        write_obj.close()
        
        f = open(f"{self.save_dir}/id_map.txt","w",encoding="utf-8")
        appearedID = set()
        # print(self.doc_id)
        print("===============Writing Final DocID Map File=================")
        
        for path, id in tqdm(self.doc_id.items()):
            if id in appearedID:
                print("ERRORS: ",path,id)
                continue
            appearedID.add(id)
            f.write(f"{path} -> {id}\n")
        f.close()
        
        
    def tfidf(self,tf,idf)->float:
        return tf*math.log(idf)
        
            
def record_json_freq_invert(custom_dir: str) -> None:
    
    pj = ProcessJson()
    pj.go_through_files(custom_dir)

    pj.process_all_inverts()
    pj.writeDocID()
    
    pj.mergeFiles()
    pj.process_all_freqs()
    pj.writeFinal()
    pj.writeNumDocs()


