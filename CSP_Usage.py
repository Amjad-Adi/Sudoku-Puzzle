#This class is not for running the CSP but to provide utility functions that can be used by CSP implementations
import random
#function to update the domain for one cell
def recomputeDomainForCell(board, n, row, col,widthOfSmallBoxes):
    if board[row][col].isAssigned():
        board[row][col].domain = []
    else:
        board[row][col].domain.clear()
        for v in range(1, n+1):
            if isConsistent(board, row, col, v, n, widthOfSmallBoxes):
                board[row][col].domain.append(v)
        random.shuffle(board[row][col].domain)
# function to update domains for all cells
def recomputeAllDomains(board, n,widthOfSmallBoxes):
    for i in range(n):
        for j in range(n):
            recomputeDomainForCell(board, n, i, j,widthOfSmallBoxes)
    # function to check if a value is okay for a cell        
def isConsistent(skoduBoard,row,col,choice,numberOfBoxes, widthOfSmallBoxes):
    for i in range(numberOfBoxes):
        if skoduBoard[i][col].value==choice:
            return False
    for j in range(numberOfBoxes):
        if skoduBoard[row][j].value==choice:
            return False
    start_row= (row//widthOfSmallBoxes)*widthOfSmallBoxes
    start_col= (col//widthOfSmallBoxes)*widthOfSmallBoxes
    for i in range(start_row, start_row+widthOfSmallBoxes):
        for j in range(start_col, start_col+widthOfSmallBoxes):
            if skoduBoard[i][j].value == choice:
                return False
    return True
# function to count how many rules are broken
def calculateNumberOfViolatedConstrains(board,n,widthOfSmallBoxes):
    countViolatedConstrains=0
    for i in range(widthOfSmallBoxes):
        start_row= widthOfSmallBoxes*i
        for j in range(widthOfSmallBoxes):
            start_col=widthOfSmallBoxes*j
            setOfNumbersInBoxes=set()
            for k in range(start_row, start_row+widthOfSmallBoxes):
                for l in range(start_col, start_col+widthOfSmallBoxes):
                    if board[k][l].value not in range(1,n+1):
                        countViolatedConstrains+=1
                    setOfNumbersInBoxes.add(board[k][l].value)
            if n!=len(setOfNumbersInBoxes):
                countViolatedConstrains+=1
    for i in range(n):
        setOfNumbersInBoxes.clear() # pyright: ignore[reportPossiblyUnboundVariable]
        for j in range(n):
            setOfNumbersInBoxes.add(board[i][j].value)# pyright: ignore[reportPossiblyUnboundVariable]
        if n!=len(setOfNumbersInBoxes):# pyright: ignore[reportPossiblyUnboundVariable]
            countViolatedConstrains+=1
    for j in range(n):
        setOfNumbersInBoxes.clear()# pyright: ignore[reportPossiblyUnboundVariable]
        for i in range(n):
            setOfNumbersInBoxes.add(board[i][j].value)# pyright: ignore[reportPossiblyUnboundVariable]
        if n!=len(setOfNumbersInBoxes):# pyright: ignore[reportPossiblyUnboundVariable]
            countViolatedConstrains+=1
    return countViolatedConstrains
# function to print the Sudoku board 
def printSudoku(skoduBoard, n,widthOfSmallBoxes):
    width=len(str(n))
    segment_len = 1 + widthOfSmallBoxes * (width + 1)
    border = "+" + "+".join(["-" * segment_len] * widthOfSmallBoxes) + "+"
    for i in range(n):
        if i % widthOfSmallBoxes== 0:
            print(border)
        print("|", end=" ")
        for j in range(n):
            print("%*s" %(width, skoduBoard[i][j].value) , end=" ")
            if (j + 1) % widthOfSmallBoxes == 0:
                print("|", end=" ")
        print()
    print(border)
    # function to print results after solving
def printResultsForCSP(sudokuBoard,numberOfBoxes,widthOfSmallBoxes,completness,executionTime,numberOfConstrainsViolated,numOfBacktracks):
    if not completness:
        print("Failed to solve the Sudoku puzzle.")
        print("Number of violated constrains in the final board:", numberOfConstrainsViolated)
        print("Time taken to attempt to solve the puzzle: %.3f ms." % (executionTime*1000))
    else:
        print("The solved Sudoku puzzle solution is:")
        printSudoku(sudokuBoard, numberOfBoxes, widthOfSmallBoxes)
        print("Time taken to solve the puzzle: %.3f ms." % (executionTime*1000))
    print("Number of backtracks performed:", numOfBacktracks)