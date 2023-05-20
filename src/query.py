from src.tokenizer import tokenize
import json
import os
from bs4 import BeautifulSoup
import math
from tqdm import tqdm


#complete this class for query
class Query:
    def __init__(self,query:str,threshold:int)->None:
        self.query = query
        self.threshold = 5
        self.doc_count = 0
        self.inner_lists = []
    
    def makeQuery(self)->list[tuple["url",int]]:
        """the makeQuery function makes a query using self.query and returns the search result along with it

        Returns:
            list of urls: a list containing the url and the tf-idf score of that word in that particular url.  
        """
        
        
        wordMapping,docMapping = self.readFile(self.query) # wordMapping: {word: [[docID,freq],...]}, docMapping: {docID: url}
        pureDocIDs = dict() # pureDocIDs: {word: [docID,docID,docID,...]}
        for i in wordMapping:
            pureDocIDs[i] = [j[0] for j in wordMapping[i]]


        queries = self.stringToBooleans(self.query,2)
        listOfDocID = self.recursiveCheck(queries,pureDocIDs)
        
        
        # filters through the doc only if the checkquery is true, else then skip that doc.
        docList = {}
        pureDocs = {}
        print("===============1-gram Seaching=================")
        
        for i in tqdm(listOfDocID):      
            
            for j in tokenize(self.query):
                if j not in wordMapping:
                    continue
                result = self.checkQueryInFile(j,i,docMapping[i],wordMapping,docMapping)
                if i in pureDocs and pureDocs[i] <= result[1]:
                    continue
                if result[0] == True:
                    docList[docMapping[i]] = result[1]
                    pureDocs[i] = result[0]
            
            
                
            
        
        docList = list(docList.items())
        docfound = len(docList)
        docList = sorted(docList,key=lambda x:x[1],reverse=True)[:self.threshold]
        
        #go through each path and finds its corresponding url. If the function throws an error, then it will skip that particular url.
        urlList = [] 
        print("===============URLing=================")
        
        for i in tqdm(docList):
            tup = (self.pathToUrl(i[0]),i[1])       
            if tup[0] == "":
                continue
            urlList.append(tup)

        return urlList

    def stringToBooleans(self,query:str, n:int=2) -> list:
        """stringToBoolean function takes in the string query splits it to a (n)-gram finder.

        Args:
            query (str): input string to tokenize
            n (int): number of words to include in each inner list

        Returns:
            list[list]: a list of lists each containing n words
        """
        assert n > 0, "No point in splitting string into lists with 0 words"
        split_words = tokenize(query)
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
        doc_count = 0
        doc_with_word_count = 0
        tf_idf = 0
        json_docid = 0
        
        # json_name = targetJson[:-4].split("\\")[-1]
        word_frequency = 0
        # wordMapping,docMapping = self.readFile(self.query)
        #beautifulsoup to open json file
        # with open(os.getcwd() + "\\developer\\DEV\\" + targetJson) as f:
        #     data = json.load(f)

        #     html_content = data['content']
        #     soup = BeautifulSoup(html_content, 'html.parser')
        #     text = soup.get_text()
        #     # text = []
        #     # for i in f:
        #     #     text.extend(tokenize(i.rstrip("\n")))

        #     #checks to see if query is in text
        #     if(query in text):
        #         is_in_file = True
        #     else:
        #         return (False, -1)
        #     #calcualte tf and idf
        #     # docs_with_word_count = len(wordMapping[query])
        #     # docs_count = self.doc_count
            
            
        #     # for key, value in docMapping.items():
        #     #     if(value == json_name):
        #     #         json_docid = key
        #     # for docid, frequency in wordMapping[query]:
        #     #     if(json_docid == docid):
        #     #         word_frequency = frequency
        #     #         break
            
            
            
            
        #     # tf_idf = self.tfidf((word_frequency/len(text)),(docs_count/(1+docs_with_word_count)))
        
        tfidf = 0
        for k,v in wordMapping[query]:
            if k == docID:
                tfidf = v
                break
        return (is_in_file,tfidf) or (False, -1)
    
    def tfidf(self,tf,idf)->float:
        return tf*math.log(idf)
    
    def pathToUrl(self,path) -> str:
        try:
            
            with open(os.getcwd() + "\\developer\\DEV\\" + path) as f:
                file = json.load(f)
                
                return file["url"]
        except Exception as ex:
            print(ex)
            return ""

    def readFile(self,query:str)-> dict:
        """
        reads through inverted index and id_map and returns a tuple of two elements
            -> mapping of {word: [[docID,freq],...]}
            -> mapping of {docID: jsonFile}
        
        This function also filters through the inverted index and only return back mapping that the word is part of the search.
        Like let's say if searching "UC Irvine" then this will only return the tokens and its docID if the words are "UC" or "Irvine"
        
        input: 
            - query (str): the query sentence/word. 

        
        """
        d = {}
        neededIDs = set()
        queryWords = tokenize(query)
        with open("developer\\DEV\\all_inverted_index.txt","r",encoding="utf-8") as f:
            for i in f:
                line = i.rstrip("\n").split(" -> ")
                word = line[0]
                if word not in queryWords:
                    continue
                docIDs = line[1]
                docs = []
                for i in docIDs.split("),("):
                    numbers = i[1:] if i.startswith("(") else i[:-1] if i.endswith(")") else i 
                    tup = numbers.split(", ")
                    docID,freq = int(tup[0]),float(tup[1])
                    docs.append([docID,freq])
                    neededIDs.add(docID)
                
                d[word] = docs
        mappings = {}
        with open("developer\\DEV\\id_map.txt","r",encoding="utf-8") as f:
            for i in f:
                line = i.rstrip("\n").split(" -> ")
                docID = int(line[0])
                if docID not in neededIDs:
                    continue
                # url = line[1].replace("_",".")
                mappings[docID] = line[1]
        
        
        with open("developer\\DEV\\inverted_index_count.txt","r",encoding="utf-8") as f:
            
            for i in f:
                self.doc_count = int(i.rstrip("\n"))
                break
        
        return d,mappings
                
                
    
if __name__ == "__main__":
    Query("Test Query")
            
            
        
        
                