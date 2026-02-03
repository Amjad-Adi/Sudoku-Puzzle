import random
class SudokuVariable: # to represents a cell in the Sudoku grid
    def __init__(self, numberOfBoxes,value="."):
        self.value = value #s the value assigned to the cell "."means unassigned
        self.domain = list(range(1, numberOfBoxes + 1)) #list of possible values for the cell initialized with numbers 1 to numberOfBoxes
        random.shuffle(self.domain)#shuffled to introduce randomness

    def isAssigned(self): #checks if the cell has a value assigned or not
        return self.value != "."