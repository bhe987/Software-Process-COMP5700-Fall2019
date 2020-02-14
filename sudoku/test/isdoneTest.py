'''
        Created on October 31, 2019
        
        The purpose of this is to test the _isdone() function.
        
        @author: Byron He
'''
from unittest import TestCase
import sudoku.isdone as sudoku 
from sudoku.isdone import _isdone

class IsdoneTest(TestCase):
    
    def test_Sad1_ShouldReturnErrorFromMissingGrid(self):
        parms = {'integrity': 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6',
            'op': 'isdone'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'error: missing grid')
    
    def test_Sad2_ShouldReturnErrorFromMissingIntegrity(self):
        parms = {'grid': "[4,-5,-8,-9,3,-1,-6,7,2,-2,3,7,-5,-8,6,9,-4,-1,-9,6,1,7,4,2,3,-5,"+\
                            "8,-3,9,-6,-1,-5,7,8,-2,4,-1,-4,5,3,-2,8,-7,6,-9,7,8,2,4,-6,9,-5,1,"+\
                            "3,6,-1,-3,-2,9,5,-4,-8,-7,8,2,-4,6,7,-3,1,9,5,-5,7,9,-8,-1,4,-2,3,6]",
            'op': 'isdone'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'error: missing integrity')
        
    def test_Sad3_ShouldReturnErrorGridIntegrityMismatch(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,"+\
                            "-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,"+\
                            "-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
            'integrity': "0000000000000000000000000000000000000000000000000000000000000000",
            'op': 'isdone'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'error: integrity mismatch')
        
    def test_Sad4_ShouldReturnErrorFromInvalidCellInGrid(self):
        parms = {'grid': "['a',-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,"+\
                            "-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,"+\
                            "-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                'integrity': '794c0035da1689b6562cbdd76ad37f1a32537ab716d0632ca0967de038079756',
                'op': 'isdone'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'error: invalid grid')
    
    def test_Sad5_ShouldReturnErrorFromInvalidCellInGrid2(self):
        parms = {'grid': "[-10,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,"+\
                            "-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,"+\
                            "-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
            'integrity': '93574c2d0c472770fcb8e91405ab39baf1e42ff8a238d182fbed0ca70d77bca5'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'error: invalid grid')
        
    def test_Sad6_ShouldErrOnEmptyGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = ''
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test_Sad7_ShouldErrOnBlankGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = '     '
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test_Sad8_ShouldErrOnInvalidGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[, ]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad9_ShouldErrOnStrGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = '-8-4000-7-9-5-1-1-90-8-5-3-4-2-6-50-6-10-9000-7000-1-50-8-4-60-40-8-20-9-3-9-5-8-30-4-70-2-3-800-9-60-4-7-2-7-900-8-1-6000-5-2-7-1-8-30'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad10_ShouldErrOnIntegerGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = '23'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad11_ShouldErrOnGridWithEmptyList(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 

    def test_Sad12_ShouldErrOnGridHasGT81Elements(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[-8,-1,-5,-7,-6,-9,-3,-2,0,' +\
                        '-4,-9,0,0,0,-5,-8,-7,0,' +\
                        '0,0,-6,0,-4,-8,0,-9,-5,' +\
                        '0,-8,-1,0,0,-3,0,0,-2,' +\
                        '0,-5,0,-1,-8,3,0,-9,0,-7,' +\
                        '-7,-3,-9,-5,-2,-4,-6,-8,-1,' +\
                        '-9,-4,0,0,0,-7,0,-1,-8,' +\
                        '-5,-2,0,-8,-9,0,-4,-6,-3,' +\
                        '-1,-6,0,-4,-3,-2,-7,0,0,-2]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad13_ShouldErrOnGridHasLT81Elements(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[-8,-1,-5,-7,-6,-9,-3,-2,0,' +\
                        '-4,-9,0,0,0,-5,-8,-7,0,' +\
                        '0,0,-6,0,-4,-8,0,-9,-5,' +\
                        '0,-8,-1,0,0,-3,0,0,-2,' +\
                        '0,-5,0,-1,-8,3,0,-9,0,' +\
                        '-7,-3,-9,-5,-2,-4,-6,-8,-1,' +\
                        '-9,-4,0,0,0,-7,0,-1,-8,' +\
                        '-5,-2,0,-8,-9,0,-4,-6,-3,' +\
                        '-1,-6,0,-4,-3,-2,-7,0]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 

    def test_Sad14_ShouldErrOnGridHasElementsGT9(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[-8,-1,-5,-7,-6,10,-3,-2,0,' +\
                        '-4,-9,0,0,0,-5,-8,-7,0,' +\
                        '0,0,-6,0,-4,-8,0,-9,-5,' +\
                        '0,-8,-1,0,0,-3,0,0,-2,' +\
                        '0,-5,0,-1,-8,0,-9,0,-7,' +\
                        '-7,-3,-9,-5,-2,-4,-6,-8,-1,' +\
                        '-9,-4,0,0,0,-7,0,-1,-8,' +\
                        '-5,-2,0,-8,-9,0,-4,-6,-3,' +\
                        '-1,-6,0,-4,-3,-2,-7,0,0]' 
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad15_ShouldErrOnGridHasElementsLTMinus9(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[-8,-1,-5,-7,-6,-10,-3,-2,0,' +\
                        '-4,-9,0,0,0,-5,-8,-7,0,' +\
                        '0,0,-6,0,-4,-8,0,-9,-5,' +\
                        '0,-8,-1,0,0,-3,0,0,-2,' +\
                        '0,-5,0,-1,-8,0,-9,0,-7,' +\
                        '-7,-3,-9,-5,-2,-4,-6,-8,-1,' +\
                        '-9,-4,0,0,0,-7,0,-1,-8,' +\
                        '-5,-2,0,-8,-9,0,-4,-6,-3,' +\
                        '-1,-6,0,-4,-3,-2,-7,0,0]' 
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad16_ShouldErrOnGridHasBlankElements(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[-8,-1,-5,-7,-6, ,-3,-2,0,' +\
                        '-4,-9,0,0,0,-5,-8,-7,0,' +\
                        '0,0,-6,0,-4,-8,0,-9,-5,' +\
                        '0,-8,-1,0,0,-3,0,0,-2,' +\
                        '0,-5,0,-1,-8,0,-9,0,-7,' +\
                        '-7,-3,-9,-5,-2,-4,-6,-8,-1,' +\
                        '-9,-4,0,0,0,-7,0,-1,-8,' +\
                        '-5,-2,0,-8,-9,0,-4,-6,-3,' +\
                        '-1,-6,0,-4,-3,-2,-7,0,0]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad17_ShouldErrOnGridHasFloatingPointElements(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[-8,-1,-5,-7,-6,3.14,-3,-2,0,' +\
                        '-4,-9,0,0,0,-5,-8,-7,0,' +\
                        '0,0,-6,0,-4,-8,0,-9,-5,' +\
                        '0,-8,-1,0,0,-3,0,0,-2,' +\
                        '0,-5,0,-1,-8,0,-9,0,-7,' +\
                        '-7,-3,-9,-5,-2,-4,-6,-8,-1,' +\
                        '-9,-4,0,0,0,-7,0,-1,-8,' +\
                        '-5,-2,0,-8,-9,0,-4,-6,-3,' +\
                        '-1,-6,0,-4,-3,-2,-7,0,0]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test_Happy1_ShouldReturnSolvedWithCompletedGrid(self):
        parms = {'grid': "[4,-5,-8,-9, 3, -1, -6, 7, 2,-2, 3, 7, -5, -8, 6, 9, -4, -1, -9, 6, 1, 7, 4, 2, 3, -5, " +\
                            "8, -3, 9, -6, -1, -5, 7, 8, -2, 4, -1, -4, 5, 3, -2, 8, -7, 6, -9, 7, 8, 2, 4, -6, 9, -5, 1, 3, " +\
                            "6, -1, -3, -2, 9, 5, -4, -8, -7, 8, 2, -4, 6, 7, -3, 1, 9, 5, -5, 7, 9, -8, -1, 4, -2, 3, 6]",
            'integrity': "e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6",
            'op': 'isdone'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'solved')
        
    def test_Happy2_ShouldReturnIncompleteForIncompGridFollowRules(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,"+\
                            "-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,"+\
                            "-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                'integrity': "634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5",
                'op': 'isdone'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:10], 'incomplete')
        
    def test_Happy3_ShouldReturnWarningForIncompGridBreakRules(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,8,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,"+\
                            "-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,"+\
                            "-1,-6,0,-4,-3,-2,-7,0,0]",
                'integrity': "fb50f09c24b3af3d2633b4b6648ea412785c9d2a9ef117e7fecb3d2993456d0e",
                'op': 'isdone'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:7], 'warning')
        
    def test_Happy4_ShouldReturnWarningForRowViolatingRule(self):
        # Changed first cell to 5 from the perfect grid.
        # so now there are two 5s in the first row, which will give warning
        grid = "[5,2,3,4,5,6,7,8,9," +\
                "7,8,9,1,2,3,4,5,6," +\
                "4,5,6,7,8,9,1,2,3," +\
                "3,1,2,6,4,5,9,7,8," +\
                "9,7,8,3,1,2,6,4,5," +\
                "6,4,5,9,7,8,3,1,2," +\
                "2,3,1,5,6,4,8,9,7," +\
                "8,9,7,2,3,1,5,6,4," +\
                "5,6,4,8,9,7,2,3,1]"
        parms = {'grid': grid,
                 'integrity': 'd675c71cac8dd61f8ee3076f17aaaea564d8ee4978a8dae397ba021b8a5b62e4'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'warning')
    
    def test_Happy5_ShouldReturnWarningForColumnViolatingRule(self):
        grid = "[1,2,3,4,5,6,7,8,9," +\
                "1,2,3,4,5,6,7,8,9," +\
                "4,5,6,7,8,9,1,2,3," +\
                "3,1,2,6,4,5,9,7,8," +\
                "9,7,8,3,1,2,6,4,5," +\
                "6,4,5,9,7,8,3,1,2," +\
                "2,3,1,5,6,4,8,9,7," +\
                "8,9,7,2,3,1,5,6,4," +\
                "5,6,4,8,9,7,2,3,1]"
        parms = {'grid': grid,
                 'integrity': "ce82814b351938310fdc070da61ee84933b43f239b3c217d829410c9f7c557ff"}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'warning')
    
    def test_Happy6_ShouldReturnWarningForSubgridViolatingRule(self):
        grid = '[1,2,4,3,5,6,7,8,9,' +\
                '7,8,1,9,2,3,4,5,6,' +\
                '4,5,7,6,8,9,1,2,3,' +\
                '3,1,6,2,4,5,9,7,8,' +\
                '9,7,3,8,1,2,6,4,5,' +\
                '6,4,9,5,7,8,3,1,2,' +\
                '2,3,5,1,6,4,8,9,7,' +\
                '8,9,2,7,3,1,5,6,4,' +\
                '5,6,8,4,9,7,2,3,1]'
        parms = {'grid': grid,
                 'integrity': '34e4943cadbe4c468cc0b980e344de3d07905cc5ef2c57e70cd30b9e2d637b20'}
        result = _isdone(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'warning')