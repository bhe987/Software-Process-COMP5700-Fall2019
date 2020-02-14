'''
        Created on October 31, 2019
        
        The purpose of this is to automatically solve a given sudoku grid
        or to return an error message if the given grid cannot be solved.
        
        @author: Byron He
'''
import ast
import hashlib
from sudoku.isdone import _isdone
import sys
VALIDGRIDNUMBERS = ['-9','-8','-7','-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7','8','9']
PERFECTGRIDNUMBERS = [1,2,3,4,5,6,7,8,9]
GRID = []
sys.setrecursionlimit(10**6)
def _solve(parms):
    result = {'status': 'solve stub'}
    
    if 'grid' not in parms:
        result['status'] = 'error: missing grid'
        return result
    if 'integrity' not in parms:
        result['status'] = 'error: missing integrity'
        return result
    if not isGridValid(parms):
        result['status'] = 'error: invalid grid'
        return result
    if not isGridIntegrityMatch(parms):
        result['status'] = 'error: integrity mismatch'
        return result
     
    grid = parms['grid']
    grid = ast.literal_eval(grid)
 
    
    #if the sudoku grid is already solved, return the resulting grid with ok status 
    statusDict = _isdone(parms)
    status = statusDict['status']
    if (status == 'solved'):
        result['grid'] = ast.literal_eval(parms['grid'])
        result['integrity'] = parms['integrity']
        result['status'] = 'ok'
        return result 
    elif(status == 'warning'):
        result['status'] = 'error: grid not solvable'
        return result
    elif (status != 'incomplete'):
        result['status'] = status
        return result
    
    solve_puzzle = solvePuzzle(parms)

    if (solve_puzzle == True):
        #modify the global grid variable
        global GRID
        grid = GRID
        result['grid'] = grid
        result['integrity'] = calculateIntegrity(grid)
        result['status'] = 'ok'
        return result
    else:
        #if solve_puzzle returns false, that means the initial grid is not solveable
        result['status'] = 'error: grid not solvable'
        return result

def solvePuzzle(parms): 

    if (0 not in ast.literal_eval(parms['grid'])):
        return True  
    counter = findNextZero(parms)
    
    for number in range(1,10):
        #check if location is safe to insert
        if (isSubgridFollowsRules(parms, counter, number) \
            and isColumnFollowRules(parms, counter, number) \
            and isRowFollowRules(parms, counter, number)):
            
            #turn the grid from parms into a list and then put into global variable
            global GRID
            GRID = parms['grid']
            GRID = ast.literal_eval(GRID)
            #insert number into grid
            GRID[counter] = number
            #update parms to be a string-casted list
            parms['grid'] = str(GRID)
            #start recursive check for success
            if (solvePuzzle(parms)):
                return True
            # if failure
            GRID[counter] = 0
            #update parms
            parms['grid'] = str(GRID)
    return False

def calculateIntegrity(grid):
    columnMajor = ""
    for row in range(9):
        for col in range(9):
            columnMajor += str( grid[9 * col + row] )
    return ( hashlib.sha256(columnMajor.encode()).hexdigest() )

def findNextZero(parms):
    grid = parms['grid']
    grid = ast.literal_eval(grid)
    for index in range(0,81):
        if (grid[index] == 0):
            return index

def isGridIntegrityMatch(parms):
    gridToCheck = parms['grid']
    gridToCheck = gridToCheck = ast.literal_eval(gridToCheck)
    IntegrityFromParms = parms['integrity']
    IntegrityCalculatedFromGrid = calculateIntegrity(gridToCheck)
    if IntegrityFromParms == IntegrityCalculatedFromGrid:
        return True
    else:
        return False

def isGridValid(parms):
    gridToCheck = parms['grid']
    if gridToCheck == '':
        return False
#if '  ' in gridToCheck:
    #    return False
    if ',,' in gridToCheck or ', ,' in gridToCheck:
        return False
    #if len(gridToCheck) < 150:
    #    return False
    # this next block checks that there is a number between all commas 
    # and that there is a single comma between numbers,
    #  and that there are only two brackets with a number between them.
    #  
    commaCount = 0
    bracketCount = 0
    integerCount = 0
    for i in range(len(gridToCheck)):
        if gridToCheck[i] == ',':
            commaCount += 1
            integerCount = 0
        if gridToCheck[i] == '[' or gridToCheck[i] == ']':
            bracketCount += 1
        if gridToCheck[i] in VALIDGRIDNUMBERS:
            commaCount = 0
            bracketCount = 0
            integerCount += 1
        if commaCount > 1 or bracketCount > 1 or integerCount > 1:
            return False
    try:
        gridToCheck = ast.literal_eval(gridToCheck)
    except:
        return False
    if len(gridToCheck) != 81:
        return False
    for i in range(0, 81):
        if (str(gridToCheck[i]) not in VALIDGRIDNUMBERS):
            return False
    return True

def isRowFollowRules(parms, counter, number):
    grid = parms['grid']
    grid = ast.literal_eval(grid)
    # find which row the current counter is in
    row = int(counter / 9)
    # get indices of row to set range of iteration
    a = row * 9
    b = a + 9
    # check row and see if our current number we are considering 
    # adding, whether it already exists in the row
    for index in range(a,b):
        if (abs(grid[index]) == number):
            return False
    return True

def isColumnFollowRules(parms, counter, number):
    grid = parms['grid']
    grid = ast.literal_eval(grid)
    # find which column the current counter is in
    column = counter % 9
    # check column and see if our current number we are considering
    # adding, whether is already exists in the row
    for row in range (0,9):
        index = column + (row * 9)
        if (abs(grid[index]) == number):
            return False
    return True

def isSubgridFollowsRules(parms, counter, number):
    grid = parms['grid']
    grid = ast.literal_eval(grid)
    ##### find which subgrid our counter is in ######
    # find which row our counter is in
    row = int(counter / 9)
    # find which column our counter is in
    column = counter % 9
    # find which subgrid the counter is in, based on the row and column it's in
    subgrid = 0
    if (column < 3):
        if (row < 3):
            subgrid = 0
        elif (row < 6):
            subgrid = 3
        else:
            subgrid = 6
    elif (column < 6):
        if (row < 3):
            subgrid = 1
        elif (row < 6):
            subgrid = 4
        else:
            subgrid = 7
    else:
        if (row < 3):
            subgrid = 2
        elif (row < 6):
            subgrid = 5
        else:
            subgrid = 8
    #get right column indices to know the ranges of iteration for each subgrid
    if((subgrid % 3) == 0):
        a = 0
        b = 3
    elif((subgrid % 3) == 1):
        a = 3
        b = 6
    else:
        a = 6
        b = 9  
    #iterate through the subgrid   
    for col in range(a, b):   
        for row in range(3):
            if (subgrid < 3):
                Index = (col + (row * 9))  
            elif (subgrid < 6):
                Index = (col + (row * 9) + 27)
            else:
                Index = (col + (row * 9) + 54)   
            if (abs(grid[Index]) == number):
                return False
    return True