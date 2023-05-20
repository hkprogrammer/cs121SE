from src.query import Query
class Interface:
    
    def __init__(self):
        self.run = True
        self.showingNumber = 5
        

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
        quer = Query(query,5)
        result,docfound = quer.makeQuery()

        result = sorted(result,key=lambda x:x[1],reverse=True)        
        
        for i in result[:self.showingNumber]:
            print("Page: ", i[0], ", tf-idf:",i[1])
        print(f"found on a total of {docfound} pages, showing {min(self.showingNumber,len(result))}")