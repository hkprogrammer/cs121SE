from src.tokenizer import tokenize
import json
import os
from bs4 import BeautifulSoup
import math
from tqdm import tqdm
from time import time
from collections import defaultdict
from pathlib import Path


#complete this class for query
class Query:
    def __init__(self)->None:
        
        # self.threshold = 5
        self.doc_count = 0
        self.inner_lists = []

        # s = time()
        # self.allWordMapping,self.wordMapping,self.docMapping = self.readFile() # wordMapping: {word: [[docID,freq],...]}, docMapping: {docID: url}
        # v = time()
        # print(v-s)
        
        self.loadWordList = self.readWordList()
        
        
    
    def makeQuery(self,query,threshold=5)->list[tuple["url",int]]:
        """the makeQuery function makes a query using self.query and returns the search result along with it

        Returns:
            list of urls: a list containing the url and the tf-idf score of that word in that particular url.  
        """
        
        
        
        
        #initialize 
        self.query = query
        self.tokenizedQuery = tokenize(self.query)
        self.tokenLen = len(self.tokenizedQuery)
        self.threshold = threshold
        
        
        self.wordMapping, self.docMapping = self.readFile(self.tokenizedQuery)
        
        wordMapping,docMapping = self.wordMapping,self.docMapping
        
        
        
    
        #create just the docIDs needed
        pureDocIDs = dict() # pureDocIDs: {word: [docID,docID,docID,...]}
        for i in wordMapping:
            pureDocIDs[i] = [j[0] for j in wordMapping[i]]



        
        #create docsDict like a 2-d list but in a dictionary format.
        wordList = list(wordMapping.keys())
        docsDict = {}
        for i in tqdm(wordList):
            for j in wordMapping[i]:
                if j[0] not in docsDict:
                    docsDict[j[0]] = [0 for _ in range(len(wordList))]  
                docsDict[j[0]][wordList.index(i)] = j[1]       
        
        queryWords = [0 for _ in range(len(wordList))]
        
        
        
        
        # if any word is not in corpus, then use tf-idf to calculate. Or else the cosine similarity method might cause error
        tfidfFlag = False
        for i in self.tokenizedQuery:
            if i not in wordList:
                tfidfFlag = True
                break
            locator = wordList.index(i)
            queryWords[locator] = self.tfidf((self.tokenizedQuery.count(i)/self.tokenLen), (2))
        # queryWords = [self.tfidf((tokenize(self.query).count(i)/len(tokenize(self.query))), (2)) for i in tokenize(self.query)]
        
        
        
        if tfidfFlag or len(docsDict) == 0 or self.tokenLen == 1 or len(queryWords) != len(list(docsDict.values())[0]):
            tfidf_cosine = "tf-idf"
            # use 1-gram search
            
            
            # listOfDocID get just the IDS.
            

            if len(list(pureDocIDs.values())) == 0:
                # if there are no docs matching with any word (meaning that the entire query does not exist in corpus), return empty.
                return [],0,""
            listOfDocID = list(pureDocIDs.values())[0]

            # filters through the doc only if the checkquery is true, else then skip that doc.
            docList = {}
            pureDocs = {}
            
           
            
            print("===============1-gram Seaching=================")
            c = 0
            for i in tqdm(listOfDocID):      
                
                if c == self.threshold:
                    break
                
                # this iterate through to see the highest tf-idf value for each word given the docs. 
                for j in self.tokenizedQuery:
                    if j not in wordMapping:
                        continue
                    result = self.checkQueryInFile(j,i,docMapping[i],wordMapping,docMapping)
                    if i in pureDocs and pureDocs[i] <= result[1]:
                        continue
                    if result[0] == True:
                        docList[docMapping[i]] = result[1]
                        pureDocs[i] = result[0]
                c+=1

            
            
                
                    
                
            
            #conversion
            docList = list(docList.items())
            docfound = len(listOfDocID)
            docList = sorted(docList,key=lambda x:x[1],reverse=True)[:self.threshold]
        
        
        
        else:
            tfidf_cosine = "cosine"
            #cosine similarity
            print("===============Cosine Similarity Seaching=================")
            
            
            
            for i in docsDict:
                
                
                # cosine similairty computation for vector i against self.query
                cosSim = sum([queryWords[j] * docsDict[i][j] for j in range(len(queryWords))]) / (math.sqrt(sum([j**2 for j in docsDict[i]])) * math.sqrt(sum([j**2 for j in queryWords])) )
                docsDict[i] = cosSim
            
            
            
            
            # convert docsDict to URL list
            docsDict = list(sorted(docsDict.items(),key=lambda x:x[1],reverse = True))
            docfound = len(docsDict)
            docList = [list(i) for i in docsDict]
            for i in range(len(docList)):
                docList[i][0] = docMapping[docList[i][0]]
        
        
        
        
        # this is an implmentation of exact search, though it decreases the runtime by around 100ms, so we left the code here and decide not to do.
        # try:
        
        #     # twoGramBool = self.stringToBooleans(self.tokenizedQuery,self.tokenLen)
        #     # twoGramResult = self.recursiveCheck(twoGramBool,pureDocIDs)
            
        #     if self.tokenLen > 5:
        #         print("===============Exact Seaching=================")

        #         currentIntersection = set(pureDocIDs[self.tokenizedQuery[0]])
        #         for i in self.tokenizedQuery[1:]:
        #             currentIntersection = currentIntersection.intersection(set(pureDocIDs[i]))
                    
        #         # print(currentIntersection)
        #         if len(currentIntersection) > 0:
        #             exactList = []
        #             for i in currentIntersection:
        #                 exactList.append([docMapping[i],1,"Exact"])

        #             docList = exactList + docList

                              
        # except Exception as ex:
        #     print("cannot do exact search: ", ex)
        
        
        
    
        urlList = docList
        
   

        return urlList,docfound,tfidf_cosine

    def stringToBooleans(self,query:str, n:int=2) -> list:
        """stringToBoolean function takes in the string query splits it to a (n)-gram finder.

        Args:
            query (str): input string to tokenize
            n (int): number of words to include in each inner list

        Returns:
            list[list]: a list of lists each containing n words
        """
        assert n > 0, "No point in splitting string into lists with 0 words"
        split_words = query # give nthat query is the tokenized list
        return_list = []
        for start_index in range(len(split_words) - n + 1):
            return_list.append([split_words[x] for x in range(start_index, start_index + n)])
        return return_list
    
    def recursiveCheck(self,booleanQuery:list,docIDs:dict) -> list:
        """The recursiveCheck should take in the booleanQuery and compute the 1-gram, 2-gram, 3-gram and n-gram search and return a list of docIDs

        Args:
            booleanQuery (list[str]): the 2-gram boolean query
            docIDs (list[int]): mapping of {word: [docId, docId,...],...}

        Returns:
            list[int]: list of docIDs from search.
            
        """
        if len(booleanQuery) == 0:
            returnList = []
            if len(self.inner_lists) >= 1:
                sortedBySize = sorted(self.inner_lists, key=lambda x: len(x))
                returnList = sortedBySize[0]
                sortedBySize = sortedBySize[1:]
                while len(sortedBySize) > 0:
                    if len(returnList) == 0:
                        break
                    returnList = self.findIntersection(returnList, sortedBySize[0])
                    sortedBySize = sortedBySize[1:]
            self.inner_lists = []
            return returnList
        else:
            check_lists = [docIDs[curr_word] for curr_word in booleanQuery[0]]
            sortedBySize = sorted(check_lists, key=lambda x: len(x))
            append_list = []
            if len(sortedBySize) >= 1:
                append_list = sortedBySize[0]
                sortedBySize = sortedBySize[1:]
                while len(sortedBySize) > 0:
                    if len(append_list) == 0:
                        break
                    append_list = self.findIntersection(append_list, sortedBySize[0])
                    sortedBySize = sortedBySize[1:]
            self.inner_lists.append(append_list)
            return self.recursiveCheck(booleanQuery[1:], docIDs)
    
    def findIntersection(self,list1:list,list2:list) -> list:
        """finds the intersection between list1 and list2. Try to implement a more efficeint way than just using set.intersection()
        Perferably using pointers that locates at the front of both lists and can fast forward if needed. 

        Args:
            list1 (list[int]): list of docIDs 
            list2 (list[int]): list of docIDs

        Returns:
            list[int]: common list of docIDs
        """
        sortedIDs1 = sorted(list1)
        sortedIDs2 = sorted(list2)
        commonIDs = []
        while len(sortedIDs1) > 0 and len(sortedIDs2) > 0:
            elem1 = sortedIDs1[0]
            elem2 = sortedIDs2[0]
            if elem1 < elem2:
                sortedIDs1 = sortedIDs1[1:]
            elif elem2 < elem1:
                sortedIDs2 = sortedIDs2[1:]
            else:
                commonIDs.append(elem1)
                sortedIDs1 = sortedIDs1[1:]
                sortedIDs2 = sortedIDs2[1:]
        return commonIDs
    
    def checkQueryInFile(self,query:str,docID:int,targetJson,wordMapping,docMapping) -> tuple[bool,float]:
        """check if a query exist inside a target JSON html. Return (True,tf-idf) score of the query in the targetJSON. If false return (False,-1)

        Args:
            query (str): query in string
            targetJson (_type_): target JSON file.
        
        Returns:
            tuple[bool,int]: _description_
        """
        is_in_file = True
        
        tfidf = 0
        for k,v in wordMapping[query]:
            if k == docID:
                tfidf = v
                break
        else:
            is_in_file = False
        
        return (is_in_file,tfidf)
    
    def tfidf(self,tf,idf)->float:
        return tf*math.log(idf)
    
    def pathToUrl(self,url) -> str:
        # try:
            
        #     with open(os.getcwd() + "\\developer\\DEV\\" + path) as f:
        #         file = json.load(f)
                
        #         return file["url"]
        # except Exception as ex:
        #     print(ex)
        #     return ""
        return url # we modified the code such that the item stored in the mapping for docID is url instead of path to increase the speed

    def readFile(self,query:list)-> dict:
        """
        reads through inverted index and id_map and returns a tuple of two elements
            -> mapping of {word: [[docID,freq],...]}
            -> mapping of {docID: jsonFile}
        
        This function also filters through the inverted index and only return back mapping that the word is part of the search.
        Like let's say if searching "UC Irvine" then this will only return the tokens and its docID if the words are "UC" or "Irvine"
        
        input: 
            - query (str): the query sentence/word. 

        
        """
        
        # find the docs to read by reading the master doc.
        docsToRead = []
        for i in query:
            if i in self.loadWordList:
                docsToRead.append(self.loadWordList[i])
                
        
        
        # open each individual index file on disk.    
        d = {}
        neededIDs = set()
        for i in tqdm(docsToRead):
            with open(Path(f"developer/DEV/word_index_holder/file{i}.txt"),"r",encoding="utf-8") as file:
                # return file.readlines()[0].strip()
                line = file.readlines()[0].strip()
                line = line.split(" -> ")
                
                if line[0] not in d:
                    
                    docs = []
                    if "),(" in line[1]:
                        
                        
                        #parsing if more than 1 posting
                        for i in line[1].split("),("):
                            numbers = i[1:-1] if i.startswith("(") and i.endswith(")") else i[1:] if i.startswith("(") else i[:-1] if i.endswith(")") else i 
                            tup = numbers.split(", ")
                            docID,freq = int(tup[0]),float(tup[1])
                            docs.append([docID,freq])
                            neededIDs.add(docID)
                    else:
                        #parsing if only 1 posting
                        numbers = line[1][1:-1]
                        tup = numbers.split(", ")
                        docID,freq = int(tup[0]),float(tup[1])
                        docs.append([docID,freq])
                        neededIDs.add(docID)
                        
                        
                    
                    d[line[0]] = docs
        
        
        # read the mappings.
        mappings = {}
        with open(Path("developer/DEV/id_map.txt"),"r",encoding="utf-8") as f:
            for i in f:
                line = i.rstrip("\n").split(" -> ")
                docID = int(line[0])
                if docID not in neededIDs:
                    continue
                # url = line[1].replace("_",".")
                mappings[docID] = line[1]
        
        
        with open(Path("developer/DEV/inverted_index_count.txt"),"r",encoding="utf-8") as f:
            
            for i in f:
                self.doc_count = int(i.rstrip("\n"))
                break
        
        return d,mappings
    
    
    def readWordList(self):
        
        
        wordlists = {}
        with open(Path("developer/DEV/word_index.txt"),"r",encoding="utf-8") as f:
            for i in tqdm(f):
                line = i.strip().split(" -> ")
                
                if line[0] in wordlists:
                    print("This should not happen")
                    continue
                if len(line) > 0:
                    wordlists[line[0]] = int(line[1])
        return wordlists
    
if __name__ == "__main__":
    Query("Test Query")
            
            
        
        
                