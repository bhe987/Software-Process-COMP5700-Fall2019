'''
    Created on Oct 25, 2019
    
    The purpose of this file is to allow insertion of values into the sudoku grid.
    Error checking is included with error messages.
    
    @author: Byron He    
'''
import hashlib
import ast
#from builtins import False
ERRORMESSAGE = 'error: '

VALIDINPUTS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
VALIDCELLNUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
VALIDGRIDNUMBERS = ['-9','-8','-7','-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7','8','9']
VALIDGRIDNUMBERSINT = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def _insert(parms):
    result = {'status': 'insert stub'}
    
#    parms['grid'] = ast.literal_eval(parms['grid'])
    
    if ('cell' not in parms):
        result['status'] = 'error: missing cell reference'
        return result
    if ('grid' not in parms):
        result['status'] = 'error: missing grid'
        return result
    if ('integrity' not in parms):
        result['status'] = 'error: missing integrity'
        return result
    if (not CheckValidInputCell(parms['cell'])):
        result['status'] = 'error: invalid cell reference'
        return result
    if (not CheckInputValueIsValid(parms)):
        result['status'] = 'error: invalid value. Value must be integers 0-9'
        return result
    if (not CheckGridIsValid(parms)):
        result['status'] = 'error: invalid grid'
        return result
    if (not CheckGridAndIntegrityMatch(parms)):
        result ['status'] = 'error: integrity mismatch with grid'
        return result
    if (not CheckTargetCellIsAvailable(parms)):
        result['status'] = 'error: attempt to change fixed hint'
        return result
    if ('value' not in parms):
        parms['value'] = 0
    
    ValidRow = CheckRowForWarningsIsItValid(parms)
    ValidColumn = CheckColumnForWarningsIsItValid(parms)
    ValidSubgrid = CheckSubgridForWarningsIsItValid(parms)
    
    newValue = int(parms['value'])
    if (newValue > 0 and ValidRow and ValidColumn and ValidSubgrid):
        newGrid = ast.literal_eval(parms['grid']).copy()
        indexToAddValue = FindIndexToAddValue(parms)
        newGrid[indexToAddValue] = newValue
        result['grid'] = newGrid
        result['status'] = 'ok'
        result['integrity'] = CalculateIntegrity(newGrid)
    elif (newValue > 0 and not ValidRow):
        newGrid = ast.literal_eval(parms['grid']).copy()
        indexToAddValue = FindIndexToAddValue(parms)
        newGrid[indexToAddValue] = newValue
        result['grid'] = newGrid
        result['status'] = 'warning'
        result['integrity'] = CalculateIntegrity(newGrid)
    elif (newValue > 0 and not ValidColumn):
        newGrid = ast.literal_eval(parms['grid']).copy()
        indexToAddValue = FindIndexToAddValue(parms)
        newGrid[indexToAddValue] = newValue
        result['grid'] = newGrid
        result['status'] = 'warning'
        result['integrity'] = CalculateIntegrity(newGrid)
    elif (newValue > 0 and not ValidSubgrid):
        newGrid = ast.literal_eval(parms['grid']).copy()
        indexToAddValue = FindIndexToAddValue(parms)
        newGrid[indexToAddValue] = newValue
        result['grid'] = newGrid
        result['status'] = 'warning'
        result['integrity'] = CalculateIntegrity(newGrid)
    else:
        newGrid = ast.literal_eval(parms['grid']).copy()
        indexToRemoveValue = FindIndexToAddValue(parms)
        newGrid[indexToRemoveValue] = 0
        result['grid'] = newGrid
        result['status'] = 'ok'
        result['integrity'] = CalculateIntegrity(newGrid)
    
#    result['grid'] = str(result['grid'])
    return result

def CheckValidInputCell(targetCell):
    if (len(targetCell) != 4):
        return False
    targetCell = targetCell.lower()
    if (targetCell[0:1] != 'r'):
        return False
    if (targetCell[1:2] not in VALIDCELLNUMBERS):
        return False
    if (targetCell[2:3] != 'c'):
        return False
    if (targetCell[3] not in VALIDCELLNUMBERS):
        return False
    
    return True

def CheckTargetCellIsAvailable(parms):
    targetCell = parms['cell']
    targetRow = int( targetCell[1:2] )
    targetCol = int( targetCell[-1:] )
    gridToCheck = parms['grid']
    gridToCheck = ast.literal_eval(gridToCheck)
    gridIndexToCheck = (targetRow-1) * 9 + (targetCol-1)
    if (  int(gridToCheck[gridIndexToCheck])  >= 0 ):
        return True
    else:
        return False

def CheckGridIsValid(parms):
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

def CheckGridAndIntegrityMatch(parms):
    gridToCheck = parms['grid']
    gridToCheck = ast.literal_eval(gridToCheck)
    integrityToCheck = parms['integrity']
    realIntegrity = CalculateIntegrity(gridToCheck)
    if integrityToCheck == realIntegrity:
        return True
    else:
        return False 

def CheckInputValueIsValid(parms):
    if ('value' not in parms):
        return True
        
    valueToCheck = parms['value']
    if (valueToCheck in VALIDCELLNUMBERS):
        return True
    else:
        return False

def CalculateIntegrity(grid):
    columnMajor = ""
    for row in range(9):
        for col in range(9):
            columnMajor += str( grid[9 * col + row] )
    return ( hashlib.sha256(columnMajor.encode()).hexdigest() )

def FindIndexToAddValue(parms):
    cell = parms['cell']
    row = int(cell[1])
    col = int(cell[3])
    index = 9 * (row-1) + (col-1)
    return index

def CheckRowForWarningsIsItValid(parms):
    value = int(parms['value'])
    gridToCheck = parms['grid']
    gridToCheck = ast.literal_eval(gridToCheck)
    cell = parms['cell']
    row = int(cell[1])
    col = int(cell[3])
    rowToCheck = []
    #if the cell already has the value you're entering in, the loop will skip that cell
    for col_i in range(8):
        indexToAppend = 9 * (row-1) + (col_i)
        valueToAppend = abs(gridToCheck[indexToAppend])
        
        if (col_i == (col-1) and value == valueToAppend):
            continue
        
        rowToCheck.append( valueToAppend )
    if(value not in rowToCheck):
        return True
    else:
        return False
    
def CheckColumnForWarningsIsItValid(parms):
    value = int(parms['value'])
    gridToCheck = parms['grid']
    gridToCheck = ast.literal_eval(gridToCheck)
    cell = parms['cell']
    row = int(cell[1])
    col = int(cell[3])
    colToCheck = []
    for row_i in range(8):
        indexToAppend = 9 * (row_i) + (col-1)
        valueToAppend = abs(gridToCheck[indexToAppend])
        
        if (row_i == (row-1) and value == valueToAppend):
            continue
        
        colToCheck.append( valueToAppend )
    if(value not in colToCheck):
        return True
    else:
        return False
    
def CheckSubgridForWarningsIsItValid(parms):
    cell = parms['cell']
    value = int(parms['value'])
    gridToCheck = parms['grid']
    gridToCheck = ast.literal_eval(gridToCheck)
    row = int(cell[1])
    col = int(cell[3])
    count = 0
    index = (9 * (row - 1)) + col - 1
    if(col <= 3):
        a = 0
        b = 3
    elif(col <= 6):
        a = 3
        b = 6
    else:
        a = 6
        b = 9
    for x in range(a, b):
        for y in range(3):
            if row <= 3:
                Index = (x + (y * 9))
                if Index != index:
                    if abs(gridToCheck[Index]) != value:
                        count = count + 1
            elif row <= 6:
                Index = (x + (y * 9)) + 27
                if Index != index:
                    if abs(gridToCheck[Index]) != value:
                        count = count + 1
            else:
                Index = (x + (y * 9)) + 54
                if Index != index:
                    if abs(gridToCheck[Index]) != value:
                        count = count + 1       
    if count == 8:
        return True
    else:
        return False