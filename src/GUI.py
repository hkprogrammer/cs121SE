import tkinter
from src.interface import Interface


class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("CS121 Search Engine")
        self.root.geometry("1400x500")
    
        
        self.frame = tkinter.Frame(self.root)
        self.frame.pack()
        
        
        self.searchInput = tkinter.Entry(self.frame,width=100)
        self.searchInput.grid(row=0,column=0)
        
        self.searchButton = tkinter.Button(self.frame,text="Search",command=self.query)
        self.searchButton.grid(row=0,column=1)
        
        self.displayContent = tkinter.StringVar(value="Nothing.")
        self.displayArea = tkinter.Label(self.frame,textvariable=self.displayContent,justify="left")
        self.displayArea.grid(row=1,column=0)
        
        
        self.rankContent = tkinter.StringVar(value="")
        self.displayRank = tkinter.Label(self.frame,textvariable=self.rankContent,anchor="w")
        self.displayRank.grid(row=1,column=1)
        
        self.queryInterface = Interface()
        
    def query(self):
        result,rank = self.queryInterface.GUIquery(self.searchInput.get())
        self.displayContent.set(result)
        self.rankContent.set(rank)
        
    
    def start(self):
        self.root.mainloop()
    
    
    
