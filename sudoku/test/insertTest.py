'''
    Created on Oct 25, 2019
    
    The purpose of this file is to test the insert.py file and _insert() function
        as they are being developed.
    
    @author: Byron He    
'''
from unittest import TestCase
import sudoku.insert as sudoku
import sudoku.resource as resource 
from sudoku.insert import _insert
import ast

class InsertTest(TestCase):
    
    def testSad1ShouldErrOnInsertInvalidColumn(self):
        parms = {"cell": 'r3c0'}
        parms['value'] = '3'
        parms['grid'] = resource.gridLevel1String
        parms['integrity'] = resource.integrityLevel1
        parms['op'] = 'insert'
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def testSad2ShouldErrOnInsertNoLocation(self):
        parms = {'value': '3',
            'grid': resource.gridLevel1String,
            'integrity': resource.integrityLevel1,
            'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def testSad3ShouldErrOnInsertInvalidRow(self):
        parms = {'cell': 'r0c3',
            'value': '3',
            'grid': resource.gridLevel1String,
            'integrity': resource.integrityLevel1,
            'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def testSad4ShouldErrOnInsertToFixedCell(self):
        parms = {'cell': 'r1c1',
            'value': '3',
            'grid': resource.gridLevel1String,
            'integrity': resource.integrityLevel1,
            'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def testSad5ShouldErrOnInsertGridWIthInvalidCell(self):
        parms = {'cell': 'r1c3',
            'value': '3',
            'grid': "[-10,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6, "+\
                "0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,-9,0,-7, "+\
                "-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,"+\
                "-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
            'integrity': '634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5',
            'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def testSad5ShouldErrOnInsertGridWIthInvalidCell2(self):
        parms = {'cell': 'r1c3',
            'value': '3',
            'grid': "['a',-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6, "+\
                "0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,-9,0,-7, "+\
                "-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,"+\
                "-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
            'integrity': '634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5',
            'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def testSad6ShouldErrOnInsertGridMismatchIntegrity(self):
        parms = {'cell': 'r1c1',
            'value': '3',
            'grid': resource.gridLevel1String,
            'integrity': '0000000000000000000000000000000000000000000000000000000000000000',
            'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def testSad7ShouldErrOnInsertInvalidLowValue(self):
        parms = {'cell': 'r2c3',
            'value': '0',
            'grid': resource.gridLevel1String,
            'integrity': resource.integrityLevel1,
            'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def testSad8ShouldErrOnInsertInvalidHighValue(self):
        parms = {'cell': 'r2c3',
            'value': '10',
            'grid': resource.gridLevel1String,
            'integrity': resource.integrityLevel1,
            'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def testSad9ShouldErrOnInsertInvalidValue(self):
        parms = {'cell': 'r2c3',
            'value': 'a',
            'grid': resource.gridLevel1String,
            'integrity': resource.integrityLevel1,
            'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def testHappy1ShouldReturnValidOnCorrectInsert(self):
        parms = {'cell': 'r3c1'}
        parms['value'] = '3'
        parms['grid'] = resource.gridLevel1String#.copy()
        parms['integrity'] = resource.integrityLevel1
        parms['op'] = 'insert'
        result = _insert(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('grid', result)
        expectedGrid = "[-8, -1, -5, -7, -6, -9, -3, -2, 0, -4, -9, 0, 0, 0, -5, -8, -7, 0, 3, 0, "+\
            "-6, 0, -4, -8, 0, -9, -5, 0, -8, -1, 0, 0, -3, 0, 0, -2, 0, -5, 0, -1, -8, 0, -9, 0, -7, -7, -3, -9, "+\
            "-5, -2, -4, -6, -8, -1, -9, -4, 0, 0, 0, -7, 0, -1, -8, -5, -2, 0, -8, -9, 0, -4, -6, -3, -1, -6, 0, "+\
            "-4, -3, -2, -7, 0, 0]"
        self.assertEqual(result['grid'], expectedGrid)
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '96484cb0a36217f3a7500c50b5b7d3b6012b336be9a1cae83abab27e48c7a627')
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
    
    def testHappy2ShouldReturnValidOnRemove(self):
        parms = {'cell': 'r3c1'}
#        parms['input'] = '3'
        parms['grid'] = "[-8, -1, -5, -7, -6, -9, -3, -2, 0, -4, -9, 0, 0, 0, -5, -8, -7, 0, 3, 0, "+\
            "-6, 0, -4, -8, 0, -9, -5, 0, -8, -1, 0, 0, -3, 0, 0, -2, 0, -5, 0, -1, -8, 0, -9, 0, -7, -7, -3, -9, "+\
            "-5, -2, -4, -6, -8, -1, -9, -4, 0, 0, 0, -7, 0, -1, -8, -5, -2, 0, -8, -9, 0, -4, -6, -3, -1, -6, 0, "+\
            "-4, -3, -2, -7, 0, 0]"
        parms['integrity'] = '96484cb0a36217f3a7500c50b5b7d3b6012b336be9a1cae83abab27e48c7a627'
        parms['op'] = 'insert'
        result = _insert(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [-8, -1, -5, -7, -6, -9, -3, -2, 0, -4, -9, 0, 0, 0, -5, -8, -7, 0, 0, 0, \
            -6, 0, -4, -8, 0, -9, -5, 0, -8, -1, 0, 0, -3, 0, 0, -2, 0, -5, 0, -1, -8, 0, -9, 0, -7, -7, -3, -9, \
            -5, -2, -4, -6, -8, -1, -9, -4, 0, 0, 0, -7, 0, -1, -8, -5, -2, 0, -8, -9, 0, -4, -6, -3, -1, -6, 0, \
            -4, -3, -2, -7, 0, 0])
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], resource.integrityLevel1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        
    def testHappy3ShouldReturnWarningRow(self):
        parms = {'cell': 'r3c1',
              'value': '4',
              'grid': resource.gridLevel1String,
              'integrity': resource.integrityLevel1,
              'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], "[-8, -1, -5, -7, -6, -9, -3, -2, 0, -4, -9, 0, 0, 0, -5, -8, -7, 0, 4, 0, "+\
            "-6, 0, -4, -8, 0, -9, -5, 0, -8, -1, 0, 0, -3, 0, 0, -2, 0, -5, 0, -1, -8, 0, -9, 0, -7, -7, -3, -9, "+\
            "-5, -2, -4, -6, -8, -1, -9, -4, 0, 0, 0, -7, 0, -1, -8, -5, -2, 0, -8, -9, 0, -4, -6, -3, -1, -6, 0, "+\
            "-4, -3, -2, -7, 0, 0]")
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], resource.CalculateIntegrity([-8, -1, -5, -7, -6, -9, -3, -2, 0, -4, 
            -9, 0, 0, 0, -5, -8, -7, 0, 4, 0, -6, 0, -4, -8, 0, -9, -5, 0, -8, -1, 0, 0, -3, 0, 0, -2, 0, -5, 0, 
            -1, -8, 0, -9, 0, -7, -7, -3, -9, -5, -2, -4, -6, -8, -1, -9, -4, 0, 0, 0, -7, 0, -1, -8, -5, -2, 0, 
            -8, -9, 0, -4, -6, -3, -1, -6, 0, -4, -3, -2, -7, 0, 0]))
        self.assertIn('status', result)
        self.assertIn(result['status'][0:7], 'warning:')
        
    def testHappy4ShouldReturnWarningColumn(self):
        parms = {'cell': 'r3c1',
              'value': '4',
              'grid': resource.gridLevel1String,
              'integrity': resource.integrityLevel1,
              'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], "[-8, -1, -5, -7, -6, -9, -3, -2, 0, -4, -9, 0, 0, 0, -5, -8, -7, 0, 4, 0, "+\
            "-6, 0, -4, -8, 0, -9, -5, 0, -8, -1, 0, 0, -3, 0, 0, -2, 0, -5, 0, -1, -8, 0, -9, 0, -7, -7, -3, -9, "+\
            "-5, -2, -4, -6, -8, -1, -9, -4, 0, 0, 0, -7, 0, -1, -8, -5, -2, 0, -8, -9, 0, -4, -6, -3, -1, -6, 0, "+\
            "-4, -3, -2, -7, 0, 0]")
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], resource.CalculateIntegrity([-8, -1, -5, -7, -6, -9, -3, -2, 0, -4, 
            -9, 0, 0, 0, -5, -8, -7, 0, 4, 0, -6, 0, -4, -8, 0, -9, -5, 0, -8, -1, 0, 0, -3, 0, 0, -2, 0, -5, 0, 
            -1, -8, 0, -9, 0, -7, -7, -3, -9, -5, -2, -4, -6, -8, -1, -9, -4, 0, 0, 0, -7, 0, -1, -8, -5, -2, 0, 
            -8, -9, 0, -4, -6, -3, -1, -6, 0, -4, -3, -2, -7, 0, 0]))
        self.assertIn('status', result)
        self.assertIn(result['status'][0:7], 'warning:')
    
    def testHappy5ShouldReturnWarningSubgrid(self):
        parms = {'cell': 'r1c3',
                 'value': '8',
                 'grid': resource.gridLevel2String,
                 'integrity': resource.integrityLevel2,
                 'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], "[0, -3, 8, 0, 0, -2, 0, -6, -5, -5, -8, 0, -1, -3, -4, 0, -2, -9, "+\
            "0, -2, -7, 0, -5, 0, 0, 0, -1, 0, 0, -2, 0, 0, -9, 0, -1, -3, -8, -5, -9, 0, -7, -1, 0, -4, "+\
            "-2, -1, 0, 0, -6, -2, 0, 0, 0, -7, 0, 0, 0, 0, -4, -7, -2, -5, 0, -6, -7, -5, 0, 0, -8, 0, -9, "+\
            "0, 0, -9, -4, -5, -6, 0, 0, -7, -8]")
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '01e950501f8c9a79008b2de39dd8a34379a61364a4b6f49c5a4979e0661ea20b')
        self.assertIn('status', result)
        self.assertIn(result['status'][0:7], 'warning:')
    
    def testHappy5ShouldReturnWarningSubgrid2(self):
        parms = {'cell': 'r2c3',
              'value': '6',
              'grid': resource.gridLevel1String,
              'integrity': resource.integrityLevel1,
              'op': 'insert'}
        result = _insert(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], "[-8, -1, -5, -7, -6, -9, -3, -2, 0, -4, -9, 6, 0, 0, -5, -8, -7, 0, 0, 0, "+\
            "-6, 0, -4, -8, 0, -9, -5, 0, -8, -1, 0, 0, -3, 0, 0, -2, 0, -5, 0, -1, -8, 0, -9, 0, -7, -7, -3, -9, "+\
            "-5, -2, -4, -6, -8, -1, -9, -4, 0, 0, 0, -7, 0, -1, -8, -5, -2, 0, -8, -9, 0, -4, -6, -3, -1, -6, 0, "+\
            "-4, -3, -2, -7, 0, 0]")
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '3ef1f63a9f87c0b8268b3bd59b648d3b475a3e05bba5d0a60d1aadc92ec6155a')
        self.assertIn('status', result)
        self.assertIn(result['status'][0:6], 'warning')
    
    def test300_120ShouldInsertValueOnLowerCaseRowCapitalCol(self):   
        parms = {'op':'insert'}
        parms['cell'] = "r6C3"
        parms['integrity'] = "2984cb01c6e28fbe5493d97d747a9e567c60854aa0e5a7f358c2b6e035e8ece5"
        
        parms['value'] = '7'
        parms['grid'] ='[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,0,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,0,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1 ]'
                      
        expectedGrid=[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,0,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1 ]
        result = _insert(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], 'ok')
#        self.assertListEqual(result['grid'], expectedGrid)
    
        self.assertEquals(result['integrity'],'0602732c075d6e079b5b698f2796db734c29ea5b34625d384486f08399f0dfbb')

    def test300_100ShouldInsertValueOnLowerCaseRowAndCol(self):   
        parms = {'op':'insert'}
        parms['cell'] = "r1c6"
        parms['integrity'] = "660d5e909d20d90d590adaf19ac3d211f67b7df40c078e6fbda9a6c5dc6e7088"
        parms['value'] = '8'
        parms['grid'] ='[-7,0,0,0,-6,0,0,-4,0,\
              -4,0,0,-1,0,0,0,-8,-5,\
              0,0,-8,0,-9,-4,0,0,-3,\
              0,-8,-4,0,0,-6,0,0,0,\
              0,0,0,-7,-3,-2,0,0,0,\
              0,0,0,-8,0,0,-3,-1,0,\
              -5,0,0,-3,-8,0,-2,0,0,\
              -8,-4,0,0,0,-1,0,0,-7,\
              0,-7,0,0,-5,0,0,0,-1 ]'
        expectedGrid=[-7,0,0,0,-6,8,0,-4,0,\
                      -4,0,0,-1,0,0,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,0,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,0,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1 ]
        result = _insert(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], 'ok')
        self.assertListEqual(result['grid'], expectedGrid)
        self.assertEquals(result['integrity'],"8f33014a3edf131ca46fe1ebc5354dd7d82a5d4f13a0584851c9fbab6b4e2013")