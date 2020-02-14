'''
        Created on October 31, 2019
        
        The purpose of this is to determine if a given sudoku grid is 
        solved and completed, and to detect if the rules of sudoku are broken.
        
        @author: Byron He
'''
VALIDGRIDNUMBERS = ['-9','-8','-7','-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7','8','9']
import hashlib
import ast
def _isdone(parms):
    result = {'status': 'isdone stub'}
    
    if (not isGridExists(parms)):
        result['status'] = 'error: missing grid'
        return result
    if (not isIntegrityExists(parms)):
        result['status'] = 'error: missing integrity'
        return result
    if (not isGridValid(parms)):
        result['status'] = 'error: invalid grid'
        return result
    if (not isGridIntegrityMatches(parms)):
        result['status'] = 'error: integrity mismatch'
        return result
    
    rowsFollowRules = isRowFollowRules(parms)
    columnsFollowRules = isColumnsFollowRules(parms)
    subgridsFollowRules = isSubgridsFollowRules(parms)
    gridIsComplete = isGridCompleted(parms)
    
    if not rowsFollowRules:
        result['status'] = 'warning'
        return result
    if not columnsFollowRules:
        result['status'] = 'warning'
        return result
    if not subgridsFollowRules:
        result['status'] = 'warning'
        return result
    if not gridIsComplete:
        result['status'] = 'incomplete'
        return result
    
    result['status'] = 'solved'
    return result

def calculateIntegrity(grid):
    columnMajor = ""
    for row in range(9):
        for col in range(9):
            columnMajor += str( grid[9 * col + row] )
    return ( hashlib.sha256(columnMajor.encode()).hexdigest() )

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
    #check that there is a number between all commas and that there 
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

def isGridExists(parms):
    if ('grid' not in parms):
        return False
    else:
        return True
    
def isIntegrityExists(parms):
    if ('integrity' not in parms):
        return False
    else:
        return True
    
def isGridIntegrityMatches(parms):
    gridToCheck = parms['grid']
    gridToCheck = gridToCheck = ast.literal_eval(gridToCheck)
    IntegrityFromParms = parms['integrity']
    IntegrityCalculatedFromGrid = calculateIntegrity(gridToCheck)
    if IntegrityFromParms == IntegrityCalculatedFromGrid:
        return True
    else:
        return False
    
def isRowFollowRules(parms):
    grid = parms['grid']
    grid = ast.literal_eval(grid)
   
    for row in range (0,9):
        # a represents starting index of the row and
        # b represents ending index of the row we want to check
        a = row * 9
        b = a + 9
        values = []
        for index in range (a,b):
            if (grid[index] == 0):
                continue
            if (abs(grid[index]) not in values): 
                values.append(abs(grid[index]))
            else:
                return False      
    return True

def isColumnsFollowRules(parms):
    grid = parms['grid']
    grid = ast.literal_eval(grid)
    
    for colIndex in range (0,9):
        values = []
        for rowIndex in range (0,9):
            index = colIndex + (9 * rowIndex)
            if (grid[index] == 0):
                continue
            if (abs(grid[index]) not in values): 
                values.append(abs(grid[index]))
            else:
                return False
    return True

def isSubgridsFollowRules(parms):
    grid = parms['grid']
    grid = ast.literal_eval(grid)
    
    for subGrid in range(0,9):
        
        values = []
        # this block selects a 3x3 subgrid to check. 
        if((subGrid % 3) == 0):
            a = 0
            b = 3
        elif((subGrid % 3) == 1):
            a = 3
            b = 6
        else:
            a = 6
            b = 9
            
        for colIndex in range(a, b):
            for rowIndex in range(3):
                index = (colIndex + (rowIndex * 9))
                if (grid[index] == 0):
                    continue
                if (abs(grid[index]) not in values): 
                    values.append(abs(grid[index]))
                else:
                    return False
    return True

def isGridCompleted(parms):
    gridToCheck = parms['grid']
    gridToCheck = ast.literal_eval(gridToCheck)
    for index in range(0,81):
        if (gridToCheck[index] == 0):
            return False
    return True