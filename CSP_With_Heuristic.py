import random, heapq, math, time, CSP_Usage,Sudoku_Variable #import the tools we need
# function to find the variable that restricts the search the most
def findMostConstrainingVariable(board,n,variables, widthOfSmallBoxes):#determines which variable (cell) in the list of variables will restrict the search the most
    maxConstraints=-1
    mostConstrainingVariable=variables[0]
    for row,col in variables:
        box_row_start = (row // widthOfSmallBoxes) * widthOfSmallBoxes
        box_col_start = (col // widthOfSmallBoxes) * widthOfSmallBoxes
        constraints=0
        for j in range(n):
            if not j==col and not board[row][j].isAssigned():
                constraints+=1
        for i in range(n):
            if not i==row and not board[i][col].isAssigned():
                constraints+=1
        for i in range(box_row_start, box_row_start + widthOfSmallBoxes):
            for j in range(box_col_start, box_col_start + widthOfSmallBoxes):
                    if not (i==row or j==col) and not board[i][j].isAssigned():
                        constraints+=1
        if maxConstraints<constraints:
            maxConstraints=constraints
            mostConstrainingVariable=(row,col)
    return mostConstrainingVariable
# function to find the variable with the smallest domain
def findMostConstrainedVariable(board,n,widthOfSmallBoxes):
    existSomeUnassignedValues=False
    minDomain=n+1
    minValueVariables=[]
    for i in range(n):
        for j in range(n):
            if not board[i][j].isAssigned():
                existSomeUnassignedValues=True
                if minDomain > len(board[i][j].domain):
                    minDomain=len(board[i][j].domain)
                    minValueVariables=[(i,j)]
                elif  minDomain == len(board[i][j].domain):
                    minValueVariables.append((i,j))
    if not existSomeUnassignedValues:
        return None,None
    return findMostConstrainingVariable(board,n,minValueVariables,widthOfSmallBoxes)
# function to order values by least constraining
def findLeastConstraningValuesInOrder(board, n,row,col,widthOfSmallBoxes):
    heap=[]
    ordered_values = []
    box_row_start = (row // widthOfSmallBoxes) * widthOfSmallBoxes
    box_col_start = (col // widthOfSmallBoxes) * widthOfSmallBoxes
    for num in board[row][col].domain:
        conflicts=0
        for i in range(n):
            if not i==row and not board[i][col].isAssigned() and num in board[i][col].domain:
                conflicts+=1
        for j in range(n):
            if not j==col and not board[row][j].isAssigned() and num in board[row][j].domain:
                conflicts+=1
        for i in range(box_row_start, box_row_start + widthOfSmallBoxes):
            for j in range(box_col_start, box_col_start + widthOfSmallBoxes):
                    if not (i == row and j == col) and not board[i][j].isAssigned() and num in board[i][j].domain:
                        conflicts += 1
        heapq.heappush(heap, (conflicts,random.random(), num))
    while heap:
        _,_,value = heapq.heappop(heap)
        ordered_values.append(value)
    return ordered_values
 # function to remove values from domains using forward checking       
def deleteChosenNum(board, n,row,col,widthOfSmallBoxes):#delete by forward checking and record removed values in a list
    num=board[row][col].value
    removed=[]
    box_row_start = (row // widthOfSmallBoxes) * widthOfSmallBoxes
    box_col_start = (col // widthOfSmallBoxes) * widthOfSmallBoxes
    for i in range(n):
        if not i==row and not board[i][col].isAssigned() and  num in board[i][col].domain:
            board[i][col].domain.remove(num)
            removed.append((i,col,num))
            if len(board[i][col].domain)==0:
                return removed, True
    for j in range(n):
        if not j==col and not board[row][j].isAssigned() and  num in board[row][j].domain:
            board[row][j].domain.remove(num)
            removed.append((row,j,num))
            if len(board[row][j].domain)==0:
                return removed, True
    for i in range(box_row_start, box_row_start + widthOfSmallBoxes):
        for j in range(box_col_start, box_col_start + widthOfSmallBoxes):
                if not (i == row and j == col) and not board[i][j].isAssigned() and num in board[i][j].domain:
                    board[i][j].domain.remove(num)
                    removed.append((i, j, num))
                    if len(board[i][j].domain) == 0:
                        return removed, True
    return removed,False
# function to restore domains after backtracking
def restoreDomains(board,restore):# restore domain bedore the value was assigned because a backtrack happened
    for i,j,val in restore:
        if val not in board[i][j].domain:
            board[i][j].domain.append(val)
# main backtracking function with heuristics
def backTrackSudoku(board,n,widthOfSmallBoxes,numOfBacktracks=0):# i should use LCV here
    row, col=findMostConstrainedVariable(board,n,widthOfSmallBoxes)
    if row is None:
        return True, numOfBacktracks
    numsInOrder=findLeastConstraningValuesInOrder(board, n, row, col,widthOfSmallBoxes)
    for num in numsInOrder:
        if CSP_Usage.isConsistent(board,row,col,num,n,widthOfSmallBoxes):
            board[row][col].value=num
            removed, failureDetected = deleteChosenNum(board, n, row, col,widthOfSmallBoxes)
            if not failureDetected:
                solved, numOfBacktracks=backTrackSudoku(board, n,widthOfSmallBoxes,numOfBacktracks)
                if solved:
                    return True, numOfBacktracks
            board[row][col].value="."#backtracking needed to makesure that the sodoku will always have a solution
            restoreDomains(board, removed)
            numOfBacktracks+=1
            if numOfBacktracks> 300000:
                return False, numOfBacktracks
    return False, numOfBacktracks
    
    # function to run the CSP solver.
def runCSP(sodukoBoard, numberOfBoxes, widthOfSmallBoxes):
    return backTrackSudoku(sodukoBoard, numberOfBoxes,widthOfSmallBoxes)#time limit of 5 minutes
# main part to run the program
if __name__ == "__main__":
    difficulity=""
    print("Welcome to the sodoku puzzle game, we wil try to solve using CSP with heuristic!")
    while(True):
        try:
            numberOfBoxes = int(input("What is the size of the Sudoku board you want to solve?(for 9*9 enter 9, for 16*16 enter 16...): "))
            widthOfSmallBoxes = math.isqrt(numberOfBoxes)
            if widthOfSmallBoxes**2 != numberOfBoxes:
                print("Size must be a perfect square (e.g., 4, 9, 16, 25).")
            else: break
        except ValueError:
            print("Invalid input. Please enter a number.")
    while(True):
        print("Please choose which difficulity you want to play on:\n1-Easy.\n2-Medium.\n3-Hard.")
        difficulity=input()
        if difficulity in ("1","2","3"):
            break
        else:
            print("Please enter the numebr representing a correct difficulity.")
#Hard-> 30%->40% Filled
#Meduim-> 40%->50% Filled
#Easy-> 50%->60% Filled
    percentageOfFilledValues=((30+(abs(int(difficulity)-3))*10+random.uniform(0.0,1.0)*10)/100)
    skoduBoard=[]
    for i in range (numberOfBoxes):
        row=[]
        for j in range (numberOfBoxes):
            row.append(Sudoku_Variable.SudokuVariable(numberOfBoxes))
        skoduBoard.append(row)
    solved, numberOfBacktracks=backTrackSudoku(skoduBoard,numberOfBoxes,widthOfSmallBoxes)
    if not solved:
        print("Failed to generate a valid Question.")
    else:
        listOfBoxes=[]
        for i in range(numberOfBoxes):
            for j in range(numberOfBoxes):
                listOfBoxes.append((i,j))
        random.shuffle(listOfBoxes)
        for (i,j) in listOfBoxes[round(percentageOfFilledValues*numberOfBoxes*numberOfBoxes):]:
            skoduBoard[i][j].value="."
        print("The Sudoku puzzle is: ")
        CSP_Usage.printSudoku(skoduBoard,numberOfBoxes,widthOfSmallBoxes)
        CSP_Usage.recomputeAllDomains(skoduBoard, numberOfBoxes,widthOfSmallBoxes)
        startTimer=time.perf_counter()
        solved, numberOfBacktracks=backTrackSudoku(skoduBoard, numberOfBoxes,widthOfSmallBoxes)
        executionTime=time.perf_counter()-startTimer
        numberOfConstrainsViolated=0
        if not solved:
            numberOfConstrainsViolated=CSP_Usage.calculateNumberOfViolatedConstrains(skoduBoard,numberOfBoxes,widthOfSmallBoxes)
        CSP_Usage.printResultsForCSP(skoduBoard,numberOfBoxes,widthOfSmallBoxes,solved,executionTime,numberOfConstrainsViolated,numberOfBacktracks)
        