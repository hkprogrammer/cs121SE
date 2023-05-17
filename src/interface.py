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
        print("type [q] to quit")
    
    def userInput(self) -> str:
        return input("Enter phrase to query: ")
    
    def query(self,query):
        quer = Query(query)
        result = quer.makeQuery()
        
        
        for i in result[:self.showingNumber]:
            print("Page: ", i[0], ", freq:",i[1])
        print(f"found on a total of {len(result)} pages, showing {min(self.showingNumber,len(result))}")