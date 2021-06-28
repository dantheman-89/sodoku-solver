import numpy as np
import itertools

# import problem
problem = np.loadtxt("problem.txt", dtype=int)
print("problem to solve: \n",  problem)

# find empty slots to fill in the numbers

# backtrack functions
def check_safe(problem, i, j, num):
    # index for the sqaure
    square_i = i // 3 * 3
    square_j = j // 3 * 3
    
    # check if row is okay
    if any(problem[i,:] == num):
        return False
    
    # check if column is okay
    elif any(problem[:,j] == num):
        return False

    # check if square is okay    
    elif (problem[square_i:square_i+3, square_j:square_j+3] == num).any():
        return False

    # return true if passing all checks
    else:
        return True
    

def solve(problem, blanks, location):
    # problem is the numpy 2D array holding the sudoku to solve
    # blanks is a list of (row, column) tuple with blank cells to fill
    # location is the current starting point to solve the problem. The starting location should be 0  
    p = problem.copy()
    
    # try each of the 9 numbers
    for num in range(1,10):
        
        # if the number doesn't work, either try the next one or dead end the branch
        if check_safe(p, blanks[location][0], blanks[location][1], num) == False:
            if num == 9:
                return "dead end", p
            else:
                continue

        # if the number works, go to the next slot to evaluate
        else:
            # fill in the number if it works
            pp = p.copy()
            pp[blanks[location]] = num

            # if the number works and we are at the end, we have solved it!
            if location == len(blanks)-1:
                return "solved", pp 
                break
            # if the number works and we are not at the end, recursively work one level deeper 
            else:
                status, solution = solve(pp, blanks, location+1)
                # if the level below solved it, pass the results back
                if status == "solved":
                    return "solved", solution
                    break
                # if the level below is an dead end, skip to the next number
                elif status == "dead end":
                    if num == 9:
                        # if everything failed, return not solvable
                        if location == 0:
                            return "not solvable", p
                        # if this level failed, send dead end on the level up    
                        else:
                            return "dead end", p
                    else:
                        # move onto the next number if the current number leads to failure
                        continue


def solve_sudoku(problem):
    # create a list of slots to fill in numbers
    blanks = list()
    for i, j in itertools.product(range(9), range(9)):
        if problem[i,j] == 0:
            blanks.append((i, j))

    # run solver
    status, solution = solve(problem, blanks, 0)
    
    # print answer
    print(status)
    if status == "solved":
        print(solution)

# solution
solve_sudoku(problem)