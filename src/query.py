from src.tokenizer import tokenize
import json
import os
# from tokenizer to


#complete this class for query
class Query:
    def __init__(self,query:str)->None:
        self.query = query
    
    
    def makeQuery(self)->list[tuple["url",int]]:
        wordMapping,docMapping = self.readFile(self.query) # wordMapping: {word: [[docID,freq],...]}, docMapping: {docID: url}
        pureDocIDs = dict() # pureDocIDs: {word: [docID,docID,docID,...]}
        for i in wordMapping:
            pureDocIDs[i] = [j[0] for j in wordMapping[i]]
        
        # print(pureDocIDs)
        # print(wordMapping[:10],docMapping[:10],pureDocIDs[:10])
        queries = self.stringToBooleans(self.query)
        listOfDocID = self.recursiveCheck(queries,pureDocIDs)
        docList = []
        for i in listOfDocID:      
            
            result = self.checkQueryInFile(self.query,docMapping[i])
            if result[0] == True:
                docList.append((docMapping[i],result[1]))
        
        
        
        urlList = [] 
        for i in docList:
            tup = (self.pathToUrl(i[0]),i[1])       
            if tup[0] == "":
                continue
            urlList.append(tup)
        
        return urlList
            
    
    
    def stringToBooleans(self,query:str) -> list[list]:
        #TODO
        return [[]]
    
    def recursiveCheck(self,booleanQuery:list[str],docIDs:list[int]) -> list[int]:
        #TODO
        return list(docIDs.values())[0]
    
    def findIntersection(self,list1:list[int],list2:list[int]) -> list[int]:
        #TODO
        return [1]
    
    def checkQueryInFile(self,query,targetJson) -> tuple[bool,int]:
        """
        check if a query exist inside a target JSON html. Return (True,tf-idf) score of the query in the targetJSON. If false return (False,-1)
        """
        #TODO
        return (True,-1)
    
    def tfidf(self,tf,idf)->int:
        #TODO
        return -1
    
    def pathToUrl(self,path) -> str:
        try:
            
            with open(os.getcwd() + "/developer/DEV/" + path) as f:
                file = json.load(f)
                
                return file["url"]
        except Exception as ex:
            print(ex)
            return ""

    def readFile(self,query:str)-> dict:
        d = {}
        neededIDs = set()
        queryWords = query.split(" ")
        with open("developer/DEV/all_inverted_index.txt","r",encoding="utf-8") as f:
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
                    docID,freq = int(tup[0]),int(tup[1])
                    docs.append([docID,freq])
                    neededIDs.add(docID)
                
                d[word] = docs
        mappings = {}
        with open("developer/DEV/id_map.txt","r",encoding="utf-8") as f:
            for i in f:
                line = i.rstrip("\n").split(" -> ")
                docID = int(line[0])
                if docID not in neededIDs:
                    continue
                # url = line[1].replace("_",".")
                mappings[docID] = line[1]
        
        return d,mappings
                
                
    
if __name__ == "__main__":
    Query("Test Query")
            
            
        
        
                