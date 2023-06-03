from src.query import Query
import time
class Interface:
    
    def __init__(self):
        self.run = True
        self.showingNumber = 15
        self.quer = Query()
        

    def runProgram(self):
        
        while self.run:
            self.showInterface()
            user_input = self.userInput()
            
            if user_input == "q":
                self.run = False
                continue
            
            self.query(user_input)

    def showInterface(self):
        print("=====================================")
        print("type [q] to quit")
    
    def userInput(self) -> str:
        return input("Enter phrase to query: ")
    
    def query(self,query):
        
        start = time.time()
        result,docfound,queryMethod = self.quer.makeQuery(query,self.showingNumber)
        end = time.time()
        
        result = sorted(result,key=lambda x:x[1],reverse=True)        
        
        for i in result[:self.showingNumber]:
            q = queryMethod
            if len(i) == 3:
                q = "Exact Search"
            print("Page: ", i[0], f", {q}:",i[1])
            # print(i[0])
        print(f"found on a total of {docfound} pages, showing {min(self.showingNumber,len(result))} in {end-start} time")
        
    def GUIquery(self,query):
        returnString = ""
        returnRank = ""
        start = time.time()
        result,docfound,queryMethod = self.quer.makeQuery(query,self.showingNumber)
        end = time.time()
        
        result = sorted(result,key=lambda x:x[1],reverse=True)        
        
        
      
        
        for i in result[:self.showingNumber]:
            q = queryMethod
            if len(i) == 3:
                q = "Exact Search"
            returnString += f"Page: {i[0]}\n"
            returnRank +=  f"{q}: {i[1]}\n"
            # print(i[0])
        returnString += f"found on a total of {docfound} pages, showing {min(self.showingNumber,len(result))} in {(end-start) * 1000} ms\n"
        
        return returnString,returnRank