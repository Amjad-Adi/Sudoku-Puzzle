# import the tools we need
import random, math, time, copy, Sudoku_Variable, CSP_With_Heuristic,CSP_Usage
#class for each cell in Sudoku
class SudokuVariable:
    def __init__(self, numberOfBoxes, value="."): 
        self.value = value
        self.domain = list(range(1, numberOfBoxes + 1))

    def isAssigned(self):
        return self.value != "."
# function to find possible values for a cell
def get_possible_values(board, row, col, n):
    used = set()
    box_size = int(math.sqrt(n))
    
    for j in range(n):
        if board[row][j].value != '.':
            used.add(board[row][j].value)
    
    for i in range(n):
        if board[i][col].value != '.':
            used.add(board[i][col].value)
    
    box_row = (row // box_size) * box_size
    box_col = (col // box_size) * box_size
    for i in range(box_row, box_row + box_size):
        for j in range(box_col, box_col + box_size):
            if board[i][j].value != '.':
                used.add(board[i][j].value)
    
    possible = []
    for v in range(1, n + 1):
        if v not in used:
            possible.append(v)
    return possible
#function to calculate how many rules are broken
def calculate_cost(board, n):
    violations = 0
    box_size = int(math.sqrt(n))
    
    for i in range(n):
        row_values = []
        for j in range(n):
            if board[i][j].value != '.':
                row_values.append(board[i][j].value)
        violations += len(row_values) - len(set(row_values))
    
    for j in range(n):
        col_values = []
        for i in range(n):
            if board[i][j].value != '.':
                col_values.append(board[i][j].value)
        violations += len(col_values) - len(set(col_values))
    
    for i in range(0, n, box_size):
        for j in range(0, n, box_size):
            box_values = []
            for di in range(box_size):
                for dj in range(box_size):
                    value = board[i + di][j + dj].value
                    if value != '.':
                        box_values.append(value)
            violations += len(box_values) - len(set(box_values))
    
    empty_count = 0
    for i in range(n):
        for j in range(n):
            if not board[i][j].isAssigned():
                empty_count += 1
    violations += empty_count
    
    return violations
#function to count violations
def count_violations(board, n):
    violations = 0
    box_size = int(math.sqrt(n))
    
    for i in range(n):
        row_values = []
        for j in range(n):
            if board[i][j].value != '.':
                row_values.append(board[i][j].value)
        violations += len(row_values) - len(set(row_values))
    
    for j in range(n):
        col_values = []
        for i in range(n):
            if board[i][j].value != '.':
                col_values.append(board[i][j].value)
        violations += len(col_values) - len(set(col_values))
    
    for i in range(0, n, box_size):
        for j in range(0, n, box_size):
            box_values = []
            for di in range(box_size):
                for dj in range(box_size):
                    value = board[i + di][j + dj].value
                    if value != '.':
                        box_values.append(value)
            violations += len(box_values) - len(set(box_values))
    
    return violations
#function to check if the board is fully solved
def is_valid_solution(board, n):
    for i in range(n):
        for j in range(n):
            if board[i][j].value == '.':
                return False
    return count_violations(board, n) == 0
#function to make a small change to the board
def generate_neighbor(board, n):
    empty_cells = []
    for i in range(n):
        for j in range(n):
            if not board[i][j].isAssigned():
                empty_cells.append((i, j))
    
    if empty_cells:
        random.shuffle(empty_cells)
        for row, col in empty_cells:
            possible = get_possible_values(board, row, col, n)
            new_board = copy.deepcopy(board)
            if possible:
                new_value = random.choice(possible)
            else:
                new_value = random.randint(1, n)  
            new_board[row][col].value = new_value
            return new_board
    else:
        new_board = copy.deepcopy(board)
        attempts = 0
        max_attempts = 10  
        while attempts < max_attempts:
            if random.random() < 0.5: 
                row = random.randint(0, n - 1)
                non_fixed_cols = []
                for j in range(n):
                    if not board[row][j].isAssigned():
                        non_fixed_cols.append(j)
                if len(non_fixed_cols) >= 2:
                    col1, col2 = random.sample(non_fixed_cols, 2)
                    new_board[row][col1].value, new_board[row][col2].value = new_board[row][col2].value, new_board[row][col1].value
                    return new_board
            else: 
                col = random.randint(0, n - 1)
                non_fixed_rows = []
                for i in range(n):
                    if not board[i][col].isAssigned():
                        non_fixed_rows.append(i)
                if len(non_fixed_rows) >= 2:
                    row1, row2 = random.sample(non_fixed_rows, 2)
                    new_board[row1][col].value, new_board[row2][col].value = new_board[row2][col].value, new_board[row1][col].value
                    return new_board
            attempts += 1
        return new_board
# main simulated annealing function
def simulated_annealing(board, n, initial_temperature, cooling_rate, max_iterations):
    temperature = initial_temperature
    current_board = copy.deepcopy(board) 
    current_cost = calculate_cost(current_board, n)
    iteration = 0  
    
    for iteration in range(max_iterations):
        iteration += 1
        neighbor_board = generate_neighbor(current_board, n)
        neighbor_cost = calculate_cost(neighbor_board, n)
        
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / temperature):
            current_board = neighbor_board
            current_cost = neighbor_cost
        
        temperature *= cooling_rate
        if temperature < 1e-6: 
            break
        
        if current_cost == 0:  
            break
    
    return current_board, current_cost, iteration
# function to print the sudoku board
def printSudoku(board, n):
    widthOfSmallBoxes = int(math.sqrt(n))
    width = len(str(n))
    segment_len = 1 + widthOfSmallBoxes * (width + 1)
    border = "+" + "+".join(["-" * segment_len] * widthOfSmallBoxes) + "+"
    
    for i in range(n):
        if i % widthOfSmallBoxes == 0:
            print(border)
        print("|", end=" ")
        for j in range(n):
            print("%*s" % (width, board[i][j].value), end=" ")
            if (j + 1) % widthOfSmallBoxes == 0:
                print("|", end=" ")
        print()
    print(border)
# main function to run the SA solver
def runSA():
    print("Welcome to the sodoku puzzle game, we wil try to solve using SA!")
    n = 0
    while True: 
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
    sudokuBoard=[]
    for i in range (numberOfBoxes):
        row=[]
        for j in range (numberOfBoxes):
            row.append(Sudoku_Variable.SudokuVariable(numberOfBoxes))
        sudokuBoard.append(row)
    solved, _ =CSP_With_Heuristic.backTrackSudoku(sudokuBoard,numberOfBoxes,widthOfSmallBoxes)
    if not solved:
        print("Failed to generate a valid Question.")
    else:
        listOfBoxes=[]
        for i in range(numberOfBoxes):
            for j in range(numberOfBoxes):
                listOfBoxes.append((i,j))
        random.shuffle(listOfBoxes)
        for (i,j) in listOfBoxes[round(percentageOfFilledValues*numberOfBoxes*numberOfBoxes):]:
            sudokuBoard[i][j].value="."
        print("The Sudoku puzzle is: ")
        CSP_Usage.printSudoku(sudokuBoard,numberOfBoxes,widthOfSmallBoxes)
    if difficulity == "1":
        initial_temperature = 300
        cooling_rate = 0.95
    elif difficulity == "2":
        initial_temperature = 500
        cooling_rate = 0.9
    else:
        initial_temperature = 700
        cooling_rate = 0.85
    max_iterations = 20000
    start_time = time.perf_counter()
    solution,cost, iterations = simulated_annealing(sudokuBoard, n, initial_temperature, cooling_rate, max_iterations)
    end_time = time.perf_counter()
    print("The solved Sudoku puzzle solution is:")
    printSudoku(solution, n)

    runtime_ms = (end_time - start_time) 
    print(f"Time taken to solve the puzzle: {runtime_ms:.3f} s.")
    print(f"Number of itterations performed: {iterations}")
# run the main function if this is the main file
if __name__ == "__main__":
    runSA()
