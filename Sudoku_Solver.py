# import the tools we need
import CSP_With_Heuristic,SA, CSP_With_No_Heuristic,Sudoku_Variable, CSP_Usage
import math, random,time,copy
import matplotlib.pyplot as plt
import numpy as np

#function to print the results after solving
def printResults(sudokuBoard,numberOfBoxes,widthOfSmallBoxes,completness,executionTime,numberOfConstrainsViolated,numOfBacktracks):
    if not completness:
        print("Failed to solve the Sudoku puzzle.")
        CSP_Usage.printSudoku(sudokuBoard, numberOfBoxes, widthOfSmallBoxes)
        print("Number of violated constrains in the final board:", numberOfConstrainsViolated)
        print("Time taken to attempt to solve the puzzle: %.3f ms." % (executionTime*1000))
    else:
        print("The solved Sudoku puzzle solution is:")
        CSP_Usage.printSudoku(sudokuBoard, numberOfBoxes, widthOfSmallBoxes)
        print("Time taken to solve the puzzle: %.3f ms." % (executionTime*1000))
    print("Number of backtracks/itterations performed:", numOfBacktracks)
    
    #main function to run the Sudoku solver
def runSodukuSolver():
    print("Welcome to the Sudoku Solver and Generator!")
    numberOfRunTimes=3
    while(True):
        print("What is the size of the Sudoku board you want to solve?(for 9*9 enter 9, for 16*16 enter 16...):") 
        numberOfBoxes=int(input())
        widthOfSmallBoxes=math.isqrt(numberOfBoxes)
        if widthOfSmallBoxes**2!=numberOfBoxes:
            print("Please enter a perfect square number")
        else:
            break
         # create an empty board
    sudokuBoard=[]
    for i in range (numberOfBoxes):
            row=[]
            for j in range (numberOfBoxes):
                row.append(Sudoku_Variable.SudokuVariable(numberOfBoxes))
            sudokuBoard.append(row)
            #generate a full solved board
    solved, numberOfBacktracks=CSP_With_Heuristic.backTrackSudoku(sudokuBoard,numberOfBoxes,widthOfSmallBoxes)      
    if not solved:
            print("Failed to generate a valid Question.")
#list of algorithms to test
    algorithms = ['CSP with Heuristics', 'CSP without Heuristics', 'SA Parameters A', 'SA Parameters B']
    time_data = {alg: [] for alg in algorithms}
    completeness_data = {alg: [] for alg in algorithms}
    violations_data = {alg: [] for alg in algorithms}
    backtracks_data = {alg: [] for alg in algorithms}
    difficulties = [1, 2, 3]        
    while numberOfRunTimes>0:
        if numberOfRunTimes==3:
            print("Generating an easy Sudoku puzzle...")
        elif numberOfRunTimes==2:
            print("Generating a medium Sudoku puzzle...")
        elif numberOfRunTimes==1:
            print("Generating a hard Sudoku puzzle...")
        sudokuBoardForThisItteration=copy.deepcopy(sudokuBoard)
        percentageOfFilledValues=((30+(numberOfRunTimes-1)*10+random.uniform(0.0,1.0)*10)/100)
        listOfBoxes=[]
        for i in range(numberOfBoxes):
            for j in range(numberOfBoxes):
                 listOfBoxes.append((i,j))
        random.shuffle(listOfBoxes)
        for (i,j) in listOfBoxes[round(percentageOfFilledValues*numberOfBoxes*numberOfBoxes):]:
            sudokuBoardForThisItteration[i][j].value="."
        print("The Sudoku puzzle is:")
        CSP_Usage.printSudoku(sudokuBoardForThisItteration,numberOfBoxes,widthOfSmallBoxes)
        #make copies for each method
        sudokuBoardForCSPWithHeuristics=copy.deepcopy(sudokuBoardForThisItteration)
        sudokuBoardForCSPWithOutHeuristics=copy.deepcopy(sudokuBoardForThisItteration)
        sudokuBoardForSAWithParametersA=copy.deepcopy(sudokuBoardForThisItteration)
        sudokuBoardForSAWithParametersB=copy.deepcopy(sudokuBoardForThisItteration)
        # solve with CSP with heuristics
        print("Solving using CSP with Heuristics...")
        startTimer=time.perf_counter()
        solved, numberOfBacktracks= CSP_With_Heuristic.runCSP(sudokuBoardForCSPWithHeuristics, numberOfBoxes,widthOfSmallBoxes)
        executionTime=time.perf_counter()-startTimer
        numberOfConstrainsViolated=0
        if not solved:
            numberOfConstrainsViolated=CSP_Usage.calculateNumberOfViolatedConstrains(sudokuBoardForCSPWithHeuristics,numberOfBoxes,widthOfSmallBoxes)
        printResults(sudokuBoardForCSPWithHeuristics,numberOfBoxes,widthOfSmallBoxes,solved,executionTime,numberOfConstrainsViolated,numberOfBacktracks)
        time_data['CSP with Heuristics'].append(executionTime)
        completeness_data['CSP with Heuristics'].append(1 if solved else 0)
        violations_data['CSP with Heuristics'].append(numberOfConstrainsViolated)
        backtracks_data['CSP with Heuristics'].append(numberOfBacktracks)
        # solve with CSP without heuristics
        print("Solving using CSP without Heuristics...")
        startTimer=time.perf_counter()
        solved, numberOfBacktracks= CSP_With_No_Heuristic.runCSP(sudokuBoardForCSPWithOutHeuristics, numberOfBoxes,widthOfSmallBoxes)
        executionTime=time.perf_counter()-startTimer
        numberOfConstrainsViolated=0
        if not solved:
            numberOfConstrainsViolated=CSP_Usage.calculateNumberOfViolatedConstrains(sudokuBoardForCSPWithOutHeuristics,numberOfBoxes,widthOfSmallBoxes)
        printResults(sudokuBoardForCSPWithOutHeuristics,numberOfBoxes,widthOfSmallBoxes,solved,executionTime,numberOfConstrainsViolated,numberOfBacktracks)
        time_data['CSP without Heuristics'].append(executionTime)
        completeness_data['CSP without Heuristics'].append(1 if solved else 0)
        violations_data['CSP without Heuristics'].append(numberOfConstrainsViolated)
        backtracks_data['CSP without Heuristics'].append(numberOfBacktracks)
        # solve with SA parameters A
        initial_temperature_A = 400
        cooling_rate_A = 0.92
        max_iterations_A = 15000
        startTimer = time.perf_counter()
        solution_A, cost_A, iterations_A = SA.simulated_annealing(sudokuBoardForSAWithParametersA, numberOfBoxes, initial_temperature_A, cooling_rate_A, max_iterations_A)
        executionTime_A = time.perf_counter() - startTimer
        solved_A = (cost_A == 0)
        numberOfConstrainsViolated_A = 0
        if not solved_A:
            numberOfConstrainsViolated_A =CSP_Usage.calculateNumberOfViolatedConstrains(solution_A, numberOfBoxes, widthOfSmallBoxes)
        print("SA with Parameters A (temp=400, rate=0.92, max_iter=15000):")
        printResults(solution_A, numberOfBoxes, widthOfSmallBoxes, solved_A, executionTime_A, numberOfConstrainsViolated_A, iterations_A)
        time_data['SA Parameters A'].append(executionTime_A)
        completeness_data['SA Parameters A'].append(1 if solved_A else 0)
        violations_data['SA Parameters A'].append(numberOfConstrainsViolated_A)
        backtracks_data['SA Parameters A'].append(iterations_A)
        # solve with SA parameters B
        initial_temperature_B = 600
        cooling_rate_B = 0.88
        max_iterations_B = 25000
        startTimer = time.perf_counter()
        solution_B, cost_B, iterations_B = SA.simulated_annealing(sudokuBoardForSAWithParametersB, numberOfBoxes, initial_temperature_B, cooling_rate_B, max_iterations_B)
        executionTime_B = time.perf_counter() - startTimer
        solved_B = (cost_B == 0)
        numberOfConstrainsViolated_B = 0
        if not solved_B:
            numberOfConstrainsViolated_B =CSP_Usage.calculateNumberOfViolatedConstrains(solution_B, numberOfBoxes, widthOfSmallBoxes)
            print("SA with Parameters B (temp=600, rate=0.88, max_iter=25000):")
            printResults(solution_B, numberOfBoxes, widthOfSmallBoxes, solved_B, executionTime_B, numberOfConstrainsViolated_B, iterations_B)
        time_data['SA Parameters B'].append(executionTime_B)
        completeness_data['SA Parameters B'].append(1 if solved_B else 0)
        violations_data['SA Parameters B'].append(numberOfConstrainsViolated_B)
        backtracks_data['SA Parameters B'].append(iterations_B)
        numberOfRunTimes-=1
        # plot the graphs
    plotGraphs(difficulties, time_data, completeness_data, violations_data, backtracks_data, algorithms)
# function to plot comparison graphs
def plotGraphs(problem_sizes, time_data, completeness_data, violations_data, backtracks_data, algorithms):
    colors = ['blue', 'green', 'red', 'orange']
    markers = ['o', 's', '^', 'd']
    
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    for i, alg in enumerate(algorithms):
        ax1.plot(problem_sizes, time_data[alg], color=colors[i], marker=markers[i], label=alg)
    ax1.set_title('Time Comparison')
    ax1.set_xlabel('Difficulty Level (1=Easy, 2=Medium, 3=Hard)')
    ax1.set_ylabel('Time (seconds)')
    ax1.legend()
    ax1.grid(True)
    for i, alg in enumerate(algorithms):
        ax2.plot(problem_sizes, completeness_data[alg], color=colors[i], marker=markers[i], label=alg)
    ax2.set_title('Completeness Comparison')
    ax2.set_xlabel('Difficulty Level (1=Easy, 2=Medium, 3=Hard)')
    ax2.set_ylabel('Completeness (Success Rate)')
    ax2.legend()
    ax2.grid(True)
    for i, alg in enumerate(algorithms):
        ax3.plot(problem_sizes, violations_data[alg], color=colors[i], marker=markers[i], label=alg)
    ax3.set_title('Constraints Violated Comparison')
    ax3.set_xlabel('Difficulty Level (1=Easy, 2=Medium, 3=Hard)')
    ax3.set_ylabel('Number of Constraints Violated')
    ax3.legend()
    ax3.grid(True)
    for i, alg in enumerate(algorithms):
        ax4.plot(problem_sizes, backtracks_data[alg], color=colors[i], marker=markers[i], label=alg)
    ax4.set_title('Iterations/Backtracks Comparison')
    ax4.set_xlabel('Difficulty Level (1=Easy, 2=Medium, 3=Hard)')
    ax4.set_ylabel('Number of Iterations/Backtracks')
    ax4.legend()
    ax4.grid(True)
    
    plt.show()

#run the main function if this is the main file

if __name__ == "__main__":
    runSodukuSolver()