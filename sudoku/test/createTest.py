'''
    Created on Oct 17, 2019
    
    @author: Byron He    
'''
from unittest import TestCase
import sudoku.create as sudoku
from sudoku.create import _create
import sudoku.resource as resource

class CreateTest(TestCase):
        def test100_010ShouldReturnDictionary(self):
            result = False
            level = {"level" : "1"};
            if isinstance(_create(level), dict):
                result = True
            self.assertTrue(result)
            
        def test100_020ShouldReturnDictionaryWithLevel1(self):
            level = {"level" : "1"}
            result = _create(level)
            self.assertEqual(result['grid'], [-8, -1, -5, -7, -6, -9, -3, -2, 0, -4, -9, \
                0, 0, 0, -5, -8, -7, 0, 0, 0, -6, 0, -4, -8, 0, -9, -5, 0, -8, \
                -1, 0, 0, -3, 0, 0, -2, 0, -5, 0, -1, -8, 0, -9, 0, -7, -7, -3,\
                -9, -5, -2, -4, -6, -8, -1, -9, -4, 0, 0, 0, -7, 0, -1, -8, -5,\
                -2, 0, -8, -9, 0, -4, -6, -3, -1, -6, 0, -4, -3, -2, -7, 0, 0])
            self.assertEqual(result['status'], 'ok')
            self.assertEqual(result['integrity'], '634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5')
            
        def test100_030ShouldReturnDictionaryWithLevel2(self):
            level = {"level" : "2"}
            result = _create(level)
            self.assertEqual(result['grid'], [0, -3, 0, 0, 0, -2, 0, -6, -5, -5, -8, 0, \
                -1, -3, -4, 0, -2, -9, 0, -2, -7, 0, -5, 0, 0, 0, -1, 0, 0, -2, 0, 0, -9, 0, \
                -1, -3, -8, -5, -9, 0, -7, -1, 0, -4, -2, -1, 0, 0, -6, -2, 0, 0, 0, -7, 0, \
                0, 0, 0, -4, -7, -2, -5, 0, -6, -7, -5, 0, 0, -8, 0, -9, 0, 0, -9, -4, -5, \
                -6, 0, 0, -7, -8])
            self.assertEqual(result['status'], 'ok')
            self.assertEqual(result['integrity'], '39a4fbe2283d82b8dff98f36e6fcb09e6071653a77795e9527b26f90b4ad0d26')
            
        def test100_040ShouldReturnDictionaryWithLevel3(self):
            level = {"level" : "3"}
            result = _create(level)
            self.assertEqual(result['grid'], [0, 0, -3, 0, 0, -7, 0, -2, 0, -4, 0, -7, 0, 0, \
                -5, -3, 0, 0, 0, 0, -8, -9, 0, -6, -7, 0, -1, -8, 0, -2, -5, 0, 0, -6, 0, \
                -4, 0, -7, 0, 0, -8, 0, -1, -5, 0, -5, 0, 0, -7, -6, 0, 0, 0, -9, 0, 0, \
                -5, 0, 0, -9, 0, 0, -6, 0, -1, 0, -6, 0, 0, -2, -8, 0, 0, -2, -4, -1, -7, \
                0, -5, 0, 0])
            self.assertEqual(result['status'], 'ok')
            self.assertEqual(result['integrity'], 'b594924588d873f60df054a64a7bfaa1d4196ab1d2000f1788a453c1765b05b8')
            
        def test100_050ShouldReturnDictionaryWithLevel4(self):
            level = {"level" : "4"}
            result = _create(level)
            self.assertEqual(result['grid'], [0, -6, -7, 0, -2, 0, 0, 0, -3, 0, -8, 0, \
                -7, 0, -3, 0, 0, -6, -1, 0, 0, 0, 0, 0, 0, -7, 0, 0, -5, 0, 0, -3, 0, 0, 0, \
                -8, -8, 0, 0, 0, -4, 0, 0, 0, -1, -4, 0, 0, 0, -6, 0, 0, -5, 0, -3, 0, 0, 0, \
                0, 0, 0, 0, -2, -6, 0, 0, -2, 0, -4, 0, -3, 0, -5, 0, 0, 0, -9, 0, -8, -4, 0])
            self.assertEqual(result['status'], 'ok')
            self.assertEqual(result['integrity'], '0ea83ad27c27241477102e2377f1bb14cc2f8c6125fbc85fab972c9ab0661319')
            
        def test100_060ShouldReturnDictionaryWithLevel5(self):
            level = {"level" : "5"}
            result = _create(level)
            self.assertEqual(result['grid'], [-2, 0, 0, 0, -5, 0, -9, -1, 0, -6, 0, 0, 0, 0, \
                -8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 0, 0, -2, -4, 0, 0, 0, 0, 0, 0, 0, 0, \
                0, -4, 0, 0, 0, 0, -7, 0, -9, -3, 0, -1, 0, -5, 0, 0, 0, 0, 0, 0, 0, -7, 0, \
                0, -2, 0, -1, 0, 0, -3, 0, 0, -5, 0, -4, 0, 0, -6, 0, 0, 0, 0, 0])
            self.assertEqual(result['status'], 'ok')
            self.assertEqual(result['integrity'], '110a79143bc7c2b66faff5e8fe895320d402e4f91dbbe6b969931228abb84242')
            
        def test100_070ShouldReturnDictionaryWithLevelEmpty(self):
            level = {"level" : ""}
            result = _create(level)
            self.assertEqual(result['grid'], [0, 0, -3, 0, 0, -7, 0, -2, 0, -4, 0, -7, 0, 0, \
                -5, -3, 0, 0, 0, 0, -8, -9, 0, -6, -7, 0, -1, -8, 0, -2, -5, 0, 0, -6, 0, \
                -4, 0, -7, 0, 0, -8, 0, -1, -5, 0, -5, 0, 0, -7, -6, 0, 0, 0, -9, 0, 0, \
                -5, 0, 0, -9, 0, 0, -6, 0, -1, 0, -6, 0, 0, -2, -8, 0, 0, -2, -4, -1, -7, \
                0, -5, 0, 0])
            self.assertEqual(result['status'], 'ok')
            self.assertEqual(result['integrity'], 'b594924588d873f60df054a64a7bfaa1d4196ab1d2000f1788a453c1765b05b8')
            
#   Sad Path Tests
#
        def test100_901ReturnsErrorFromLowerBound(self):
            parms = {"level" : "0"}
            result = _create(parms)
            self.assertEqual(result['status'], "error: level is below Lower Bound limit")
            
        def test100_902ReturnsErrorFromUpperBound(self):
            parms = {"level" : '6'}
            result = _create(parms)
            self.assertEqual(result['status'], "error: level is above Upper Bound limit")
            
        def test100_903ReturnsErrorFromInvalidType(self):
            parms = {"level" : "abc"}
            result = _create(parms)
            self.assertEqual(result['status'], "error: level is of Invalid type")
            
        def test100_904ReturnsErrorFromFloatType(self):
            parms = {"level" : "2.5"}
            result = _create(parms)
            self.assertEqual(result['status'], "error: level is of Float type")
            
            
            
        def testShouldReturn(self):
            parms = {}
            parms['op'] = 'create'
            result =_create(parms)
            self.assertEqual(len(result), 3)
            self.assertEquals(result['status'], 'ok')
            self.assertIn('grid', result)
            grid = result['grid']
            self.assertTrue(resource.gridLevel3, grid)
        def testErrOnLevelBeingNotInteger(self):
            parms = {'level':"2.0"}
            parms['op'] = 'create'
            result = _create(parms)
            self.assertEqual(len(result), 1)
            self.assertIn('status', result)
            self.assertIn(result['status'][0:5], 'error:')