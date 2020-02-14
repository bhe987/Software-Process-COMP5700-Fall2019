from unittest import TestCase
import sudoku.dispatch as sudoku 

class DispatchTest(TestCase):
        
# Happy path
#    Test that each dispatched operation returns a status element
    def test100_010ShouldVerifyInstallOfCreate(self):
        parms = {}
        parms['op'] = 'create'
        result = sudoku._dispatch(parms)
        self.assertIn('status', result)
 
    def test100_020ShouldVerifyInstallOfInsert(self):
        parms = {}
        parms['op'] = 'insert'
        result = sudoku._dispatch(parms)
        self.assertIn('status', result)
        
    def test100_030ShouldVerifyInstallOfIsdone(self):
        parms = {}
        parms['op'] = 'isdone'
        result = sudoku._dispatch(parms)
        self.assertIn('status', result)
        
    def test100_040ShouldVerifyInstallOfSolve(self):
        parms = {}
        parms['op'] = 'solve'
        result = sudoku._dispatch(parms)
        self.assertIn('status', result)
        
# Sad path
#    Verify status of 
#        1) missing parm
#        2) non-dict parm
#        3) missing "op" keyword
#        4) empty "op" keyword
#        5) invalid op name

    def test100_910ShouldErrOnMissingParm(self):
        result = sudoku._dispatch()
        self.assertIn('status', result)
        self.assertEquals(result['status'], sudoku.ERROR01)
        
    def test100_920ShouldErrOnNoOp(self):
        parms = {}
        parms['level'] = 3
        result = sudoku._dispatch(parms)
        self.assertIn('status', result)
        self.assertEquals(result['status'], sudoku.ERROR01)
                
    def test100_930ShouldErrOnEmptyOp(self):
        parms = {}
        parms['op'] = ''
        result = sudoku._dispatch(parms)
        self.assertIn('status', result)
        self.assertEquals(result['status'], sudoku.ERROR03)
        
    def test100_940ShouldErrOnUnknownOp(self):
        parms = {}
        parms['op'] = 'nop'
        result = sudoku._dispatch(parms)
        self.assertIn('status', result)
        self.assertEquals(result['status'], sudoku.ERROR03)
        
