'''
        Created on October 31, 2019
        
        The purpose of this is to test the _solve() function.
        
        @author: Byron He
'''
from unittest import TestCase
import sudoku.solve as sudoku 
from sudoku.solve import _solve

class SolveTest(TestCase):
    def test_Sad1_AttemptToSolveGridWithUnsolvableValues(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,8,-4,-9,0,0,0,-5,-8,-7,"+\
                            "0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,"+\
                            "-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,"+\
                            "-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                 'integrity': "fb50f09c24b3af3d2633b4b6648ea412785c9d2a9ef117e7fecb3d2993456d0e"}
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: grid not solvable')
    def test_Sad2_ShouldErrOnGridWithInvalidCell(self):
        parms = {'grid': "[a,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,"+\
                            "0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,"+\
                            "0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,"+\
                            "0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,"+\
                            "-3,-2,-7,0,0]",
                'integrity': 'bb6a5a53f35b567013fba3dcdfe5718ca2b794ae4bfcdb043f657cc4bfde1e48'}
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: invalid grid')
    def test_Sad3_ShouldErrOnIntegrityMismatch(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,"+\
                            "-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,"+\
                            "-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,"+\
                            "-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                 'integrity': '0000000000000000000000000000000000000000000000000000000000000000'}
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: integrity mismatch')
        
    def test_Sad4_ShouldErrOnGridWithInvalidCell(self):
        parms = {'grid': "[-10,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,"+\
                            "-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,"+\
                            "-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,"+\
                            "-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                 'integrity': '93574c2d0c472770fcb8e91405ab39baf1e42ff8a238d182fbed0ca70d77bca5'}
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: invalid grid')
        
    def test_Sad5_ShouldErrOnMissingIntegrity(self):
        parms = {'grid': "[4,-5,-8,-9,3,-1,-6,7,2,-2,3,7,-5,-8,6,9,-4,-1,-9,6,1,7,"+\
                            "4,2,3,-5,8,-3,9,-6,-1,-5,7,8,-2,4,-1,-4,5,3,-2,8,-7,6,"+\
                            "-9,7,8,2,4,-6,9,-5,1,3,6,-1,-3,-2,9,5,-4,-8,-7,8,2,-4,"+\
                            "6,7,-3,1,9,5,-5,7,9,-8,-1,4,-2,3,6]"}
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: missing integrity')
        
    def test_Sad6_ShouldErrOnMissingGrid(self):
        parms = {'integrity': "e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6"}
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: missing grid')
    
    def test_Sad7_ShouldErrOnEmptyGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = ''
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test_Sad8_ShouldErrOnBlankGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = '     '
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test_Sad9_ShouldErrOnInvalidGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = '[, ]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad10_ShouldErrOnStrGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = '-8-4000-7-9-5-1-1-90-8-5-3-4-2-6-50-6-10-9000-7000-1-50-8-4-60-40-8-20-9-3-9-5-8-30-4-70-2-3-800-9-60-4-7-2-7-900-8-1-6000-5-2-7-1-8-30'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad11_ShouldErrOnIntegerGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = '23'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad12_ShouldErrOnGridWithEmptyList(self):
        parms = {'op':'solve'}
        parms['grid'] = '[]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 

    def test_Sad13_ShouldErrOnGridHasGT81Elements(self):
        parms = {'op':'solve'}
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
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad14_ShouldErrOnGridHasLT81Elements(self):
        parms = {'op':'solve'}
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
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 

    def test_Sad15_ShouldErrOnGridHasElementsGT9(self):
        parms = {'op':'solve'}
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
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad16_ShouldErrOnGridHasElementsLTMinus9(self):
        parms = {'op':'solve'}
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
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad17_ShouldErrOnGridHasBlankElements(self):
        parms = {'op':'solve'}
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
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_Sad18_ShouldErrOnGridHasFloatingPointElements(self):
        parms = {'op':'solve'}
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
        result = _solve(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    # ------------------------------------------------------
    # Solve Happy Path tests
    #------------------------------------------------------
    
    def test_Happy1_ShouldSolveASolvableGrid(self):
        parms = {'grid': '[0,-5,-8,-9,0,-1,-6,0,0,-2,0,0,-5,-8,0,0,-4,-1,-9,0,0,0,0,0,0,-5,0,-3,0,-6,-1,' +\
                        '-5,0,0,-2,0,-1,-4,0,0,-2,0,-7,0,-9,0,0,0,0,-6,0,-5,0,0,0,-1,-3,-2,0,0,-4,-8,-7,' +\
                        '0,0,-4,0,0,-3,0,0,0,-5,0,0,-8,-1,0,-2,0,0]',
                 'integrity': '6594d6506dc349fdbd9e5dda58acfa8d563657b0ef8bfc3a24ea53df9c988f9b'
                }
        parms['op'] = 'solve'
        result = _solve(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [4, -5, -8, -9, 3, -1, -6, 7, 2, -2, 3, 7, -5, -8, 6, 9, -4, -1, +
                         -9, 6, 1, 7, 4, 2, 3, -5, 8, -3, 9, -6, -1, -5, 7, 8, -2, 4, -1, -4, 5, 3, -2, +
                         8, -7, 6, -9, 7, 8, 2, 4, -6, 9, -5, 1, 3, 6, -1, -3, -2, 9, 5, -4, -8, -7, 8, +
                         2, -4, 6, 7, -3, 1, 9, 5, -5, 7, 9, -8, -1, 4, -2, 3, 6])
    
    def test_Happy2_ShouldSolveAlreadySolvedGrid(self):
        parms = {'grid': '[4, -5, -8, -9, 3, -1, -6, 7, 2, -2, 3, 7, -5, -8, 6, 9, -4, -1,' +\
                        ' -9, 6, 1, 7, 4, 2, 3, -5, 8, -3, 9, -6, -1, -5, 7, 8, -2, 4, -1, -4, 5, 3, -2,' +\
                        ' 8, -7, 6, -9, 7, 8, 2, 4, -6, 9, -5, 1, 3, 6, -1, -3, -2, 9, 5, -4, -8, -7, 8,' +\
                        ' 2, -4, 6, 7, -3, 1, 9, 5, -5, 7, 9, -8, -1, 4, -2, 3, 6]',
                 'integrity': 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
                }
        parms['op'] = 'solve'
        result = _solve(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [4, -5, -8, -9, 3, -1, -6, 7, 2, -2, 3, 7, -5, -8, 6, 9, -4, -1, +
                         -9, 6, 1, 7, 4, 2, 3, -5, 8, -3, 9, -6, -1, -5, 7, 8, -2, 4, -1, -4, 5, 3, -2, +
                         8, -7, 6, -9, 7, 8, 2, 4, -6, 9, -5, 1, 3, 6, -1, -3, -2, 9, 5, -4, -8, -7, 8, +
                         2, -4, 6, 7, -3, 1, 9, 5, -5, 7, 9, -8, -1, 4, -2, 3, 6])
        
    def test_Happy3_ShouldSolveGridWithoutEnoughHints(self):
        parms = {'grid': '[1,2,3,4,5,6,7,8,9,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0]',       
                 'integrity': 'd00de872fae354bbaec9eb8299bd5baf42d0f2576fe9f795742a1cc56f7ce7f1'
        }
        result = _solve(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], 'f48a9b403e0f5846aea961fda6019c7c817b8d9da6142cf7f01cdfe79c47098e')
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 4, 5, 6, 7, 8, 9, 1, 2, \
                               3, 7, 8, 9, 1, 2, 3, 4, 5, 6, 2, 1, 4, 3, 6, 5, 8, \
                               9, 7, 3, 6, 5, 8, 9, 7, 2, 1, 4, 8, 9, 7, 2, 1, 4, \
                               3, 6, 5, 5, 3, 1, 6, 4, 2, 9, 7, 8, 6, 4, 2, 9, 7, \
                               8, 5, 3, 1, 9, 7, 8, 5, 3, 1, 6, 4, 2])
        
    def test_Happy4_ShouldSolveGridWithoutHints(self):
        parms = {'grid': '[0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0,' +\
                          '0,0,0,0,0,0,0,0,0]',       
                 'integrity': '2b85e16040791cd86bdbe5c80556a2e13fc02dfbc785aff6cc87bd3d70c7f014'
        }
        result = _solve(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], 'f48a9b403e0f5846aea961fda6019c7c817b8d9da6142cf7f01cdfe79c47098e')
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 4, 5, 6, 7, 8, 9, 1, 2, \
                               3, 7, 8, 9, 1, 2, 3, 4, 5, 6, 2, 1, 4, 3, 6, 5, 8, \
                               9, 7, 3, 6, 5, 8, 9, 7, 2, 1, 4, 8, 9, 7, 2, 1, 4, \
                               3, 6, 5, 5, 3, 1, 6, 4, 2, 9, 7, 8, 6, 4, 2, 9, 7, \
                               8, 5, 3, 1, 9, 7, 8, 5, 3, 1, 6, 4, 2])
        
    def test_Happy5_ShouldSolveLevel5Grid(self):
        parms = {'grid': '[-2,0,0,0,-5,0,-9,-1,0,-6,0,0,0,0,-8,0,0,0,0,0,0,0,0,0,0,-3,0,0,-2,-4,0,0,0,0,0,' +\
                           '0,0,0,0,-4,0,0,0,0,-7,0,-9,-3,0,-1,0,-5,0,0,0,0,0,0,0,-7,0,0,-2,0,-1,0,0,-3,0,0,' +\
                           '-5,0,-4,0,0,-6,0,0,0,0,0]', 
                 'integrity': '110a79143bc7c2b66faff5e8fe895320d402e4f91dbbe6b969931228abb84242'
                }
        result = _solve(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '21bc00d8038232acc79ff372bd3047617d6e4bafb47e2f77896c08b56ca26503') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [-2, 4, 8, 7, -5, 3, -9, -1, 6, -6, 3, 1, 9, 4, -8, 2, 7, 5, 9, 7, 5, 1, 6, 2, 4, \
                         -3, 8, 5, -2, -4, 3, 7, 9, 8, 6, 1, 1, 8, 6, -4, 2, 5, 3, 9, -7, 7, -9, -3, 8, -1, \
                         6, -5, 2, 4, 3, 6, 9, 5, 8, -7, 1, 4, -2, 8, -1, 7, 2, -3, 4, 6, -5, 9, -4, 5, 2, -6, 9, 1, 7, 8, 3])
    def test_Happy6_ShouldSolveLevel4Grid(self):
        parms = {'grid': '[0,-6,-7,0,-2,0,0,0,-3,0,-8,0,-7,0,-3,0,0,-6,-1,0,0,0,0,0,0,-7,0,'+\
                            '0,-5,0,0,-3,0,0,0,-8,-8,0,0,0,-4,0,0,0,-1,-4,0,0,0,-6,0,0,-5,'+\
                            '0,-3,0,0,0,0,0,0,0,-2,-6,0,0,-2,0,-4,0,-3,0,-5,0,0,0,-9,0,-8,-4,0]',
                'integrity': '0ea83ad27c27241477102e2377f1bb14cc2f8c6125fbc85fab972c9ab0661319'}
        result = _solve(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '171223b80efd10456311601e8893b0f3eb30544e031cb8314eb7ac5433ce6df8')
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [9, -6, -7, 4, -2, 1, 5, 8, -3, 2, -8, 4, -7, 5, -3, 1, 9, \
                                          -6, -1, 3, 5, 6, 8, 9, 2, -7, 4, 7, -5, 1, 9, -3, 2, 4, 6, \
                                          -8, -8, 9, 6, 5, -4, 7, 3, 2, -1, -4, 2, 3, 1, -6, 8, 7, -5, 9\
                                          , -3, 4, 9, 8, 7, 5, 6, 1, -2, -6, 7, 8, -2, 1, -4, 9, -3, 5, \
                                          -5, 1, 2, 3, -9, 6, -8, -4, 7])
        
    def test_Happy7_ShouldSolveLevel3Grid(self):
        parms = {'grid': '[0,0,-3,0,0,-7,0,-2,0,-4,0,-7,0,0,-5,-3,0,0,0,0,-8,-9,0,-6,-7,0,-1,-8,0,-2,-5,0,0,' +\
                        '-6,0,-4,0,-7,0,0,-8,0,-1,-5,0,-5,0,0,-7,-6,0,0,0,-9,0,0,-5,0,0,-9,0,0,-6,0,-1,0,-6,' +\
                        '0,0,-2,-8,0,0,-2,-4,-1,-7,0,-5,0,0]', 
                 'integrity': 'b594924588d873f60df054a64a7bfaa1d4196ab1d2000f1788a453c1765b05b8'
                }
        #parms['op'] = 'isdone'
        result = sudoku._solve(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], 'ec6c0462503c83794dab7b293bda2f35fdfa1a858f975a5d293fa8f3d70015ca') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [1, 6, -3, 8, 4, -7, 9, -2, 5, -4, 9, -7, 2, 1, -5, -3, 6, 8, 2, 5, -8, -9, 3, -6, \
                        -7, 4, -1, -8, 3, -2, -5, 9, 1, -6, 7, -4, 9, -7, 6, 4, -8, 3, -1, -5, 2, -5, 4, 1, -7, -6, 2, 8, 3, \
                         -9, 7, 8, -5, 3, 2, -9, 4, 1, -6, 3, -1, 9, -6, 5, 4, -2, -8, 7, 6, -2, -4, -1, -7, 8, -5, 9, 3])
        
    def test_Happy8_ShouldSolveLevel2Grid(self):
        parms = {'grid': '[0,-3,0,0,0,-2,0,-6,-5,-5,-8,0,-1,-3,-4,0,-2,-9,0,-2,-7,0,-5,0,0,0,-1,0,0,-2,0,0,-9,0,-1,-3,-8,' +\
                        '-5,-9,0,-7,-1,0,-4,-2,-1,0,0,-6,-2,0,0,0,-7,0,0,0,0,-4,-7,-2,-5,0,-6,-7,-5,0,0,-8,0,-9,0,0,-9,' +\
                        '-4,-5,-6,0,0,-7,-8]', 
                 'integrity': '39a4fbe2283d82b8dff98f36e6fcb09e6071653a77795e9527b26f90b4ad0d26'
                }
        #parms['op'] = 'isdone'
        result = sudoku._solve(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '36a7cfdc8c6ddbcaf32d004aa6051850b2f2151df043371383221bc022be194b') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [4, -3, 1, 7, 9, -2, 8, -6, -5, -5, -8, 6, -1, -3, -4, 7, -2, -9, 9, -2, -7, 8, -5, \
                         6, 4, 3, -1, 7, 6, -2, 4, 8, -9, 5, -1, -3, -8, -5, -9, 3, -7, -1, 6, -4, -2, -1, 4, 3, -6, -2, 5, 9, \
                         8, -7, 3, 1, 8, 9, -4, -7, -2, -5, 6, -6, -7, -5, 2, 1, -8, 3, -9, 4, 2, -9, -4, -5, -6, 3, 1, -7, -8])
    
    def test_Happy9_ShouldSolveLevel1Grid(self):
        parms = {'grid': '[-8,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,' +\
                        '-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,' +\
                        '-3,-2,-7,0,0]', 
                 'integrity': '634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5'
                }
        #parms['op'] = 'isdone'
        result = sudoku._solve(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '5d3bfc4209683f988d09888d0ef6e0d1e9cfe541fbc8c82bf0590889ee462dcf') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [-8, -1, -5, -7, -6, -9, -3, -2, 4, -4, -9, 2, 3, 1, -5, -8, -7, 6, 3, 7, -6, 2, -4, \
                         -8, 1, -9, -5, 6, -8, -1, 9, 7, -3, 5, 4, -2, 2, -5, 4, -1, -8, 6, -9, 3, -7, -7, -3, -9, -5, -2, -4, \
                         -6, -8, -1, -9, -4, 3, 6, 5, -7, 2, -1, -8, -5, -2, 7, -8, -9, 1, -4, -6, -3, -1, -6, 8, -4, -3, -2, -7, 5, 9])