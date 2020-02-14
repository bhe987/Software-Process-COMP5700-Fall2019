from unittest import TestCase
import http.client
from urllib.parse import urlencode
import json
import sudoku.dispatch as sudoku 
import sudoku.resource as resource


class MicroserviceTest(TestCase):
    def setUp(self):
        self.PATH = '/sudoku?'
        self.PORT = 5000
        self.URL = 'localhost'
        self.status = "ok"
        self.validity = "Valid"
        self.validGridValue='[-8,-1,-5,-7,-6,-9,-3,-2,0,\
                          -4,-9,0,0,0,-5,-8,-7,0,\
                          0,0,-6,0,-4,-8,0,-9,-5,\
                          0,-8,-1,0,0,-3,0,0,-2,\
                          0,-5,0,-1,-8,0,-9,0,-7,\
                          -7,-3,-9,-5,-2,-4,-6,-8,-1,\
                          -9,-4,0,0,0,-7,0,-1,-8,\
                          -5,-2,0,-8,-9,0,-4,-6,-3,\
                          -1,-6,0,-4,-3,-2,-7,0,0]'
        self.validIntegrityValue= '634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5'

        
    def microservice(self, parm = ""):
        '''Issue HTTP Get and return result, which will be JSON string'''
        try:
            theParm = urlencode(parm)
            theConnection = http.client.HTTPConnection(self.URL, self.PORT)
            theConnection.request("GET", self.PATH + theParm)
            theStringResponse = str(theConnection.getresponse().read(), "utf-8")
        except Exception as e:
            theStringResponse = "{'diagnostic': '" + str(e) + "'}"
            
        '''Convert JSON string to dictionary'''
        result = {}
        try:
            jsonString = theStringResponse.replace("'", "\"")
            unicodeDictionary = json.loads(jsonString)
            for element in unicodeDictionary:
                if(isinstance(unicodeDictionary[element], str)):
                    result[str(element)] = str(unicodeDictionary[element])
                else:
                    result[str(element)] = unicodeDictionary[element]
        except Exception as e:
            result['diagnostic'] = str(e)
        return result
        
# Happy path
#    Test that each dispatched operation returns a status element
#     def test100_010ShouldVerifyInstallOfCreate(self):
#         parms = {}
#         parms['op'] = 'create'
#         result = self.microservice(parms)
#         self.assertIn('status', result)
#         self.assertIn('create', result['status'])
#  
#     def test100_020ShouldVerifyInstallOfInsert(self):
#         parms = {}
#         parms['op'] = 'insert'
#         result = self.microservice(parms)
#         self.assertIn('status', result)
#         self.assertIn('insert', result['status'])
#         
#    def test100_030ShouldVerifyInstallOfIsdone(self):
#        parms = {}
#        parms['op'] = 'isdone'
#        result = self.microservice(parms)
#        self.assertIn('status', result)
#        self.assertIn('isdone', result['status'])
        
#    def test100_040ShouldVerifyInstallOfSolve(self):
#        parms = {}
#        parms['op'] = 'solve'
#        result = self.microservice(parms)
#        self.assertIn('status', result)
#        self.assertIn('solve', result['status'])
        
# Sad path
#    Verify status of 
#        1) missing parm
#        2) non-dict parm
#        3) missing "op" keyword
#        4) empty "op" keyword
#        5) invalid op name

    def test100_910ShouldErrOnMissingParm(self):
        result = self.microservice()
        self.assertIn('status', result)
        self.assertEquals(result['status'], sudoku.ERROR01)
        
    def test100_920ShouldErrOnNoOp(self):
        parms = {}
        parms['level'] = 3
        result = self.microservice(parms)
        self.assertIn('status', result)
        self.assertEquals(result['status'], sudoku.ERROR01)
                
    def test100_930ShouldErrOnEmptyOp(self):
        parms = {}
        parms['op'] = ''
        result = self.microservice(parms)
        self.assertIn('status', result)
        self.assertEquals(result['status'], sudoku.ERROR03)
        
    def test100_940ShouldErrOnUnknownOp(self):
        parms = {}
        parms['op'] = 'nop'
        result = self.microservice(parms)
        self.assertIn('status', result)
        self.assertEquals(result['status'], sudoku.ERROR03)
        

        
    

    
    # Analysis
    # test200 - create
    #    Sad path
    #        test 200_910:    sting; level="two" 
    #        test 200_920:    level = None
    #        test 200_930:    level = ""; empty string
    #        test 200_940:    level ="  " blank string
    #        test 200_950:    level = -2  out of boundary where level is less than 1  
    #        test 200_960:    level = 6   out of boundary where greater than 5
    #        test 200_970:    level = 1.5 floating point
    #        test 200_980:    level = 2.0 floating point
    
    def test200_910ShouldErrOnLevelBeingString(self):
        parms = {'level':'two'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test200_920ShouldErrOnLevelBeingNone(self):
        parms = {'level': None}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test200_930ShouldErrOnLevelBeingEmptyStr(self):
        parms = {'level':""}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test200_940ShouldErrOnLevelBeingBlankStr(self):
        parms = {'level':"    "}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test200_950ShouldErrOnLevelLT1(self):
        parms = {'level':"0"}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test200_960ShouldErrOnLevelGT5(self):
        parms = {'level':"10"}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test200_970ShouldErrOnLevelBeingNotInteger(self):
        parms = {'level':"1.5"}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test200_980ShouldErrOnLevelBeingNotInteger(self):
        parms = {'level':"2.0"}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
        
# Sad Path Test        
    def test300_910ShouldReturnErrOnMissingCell(self):
        parms = {'op':'insert'}
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300_920ShouldReturnErrOnMissingGrid(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3c1"
        parms['integrity'] = self.validIntegrityValue
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    
    def test300_930ShouldReturnErrOnMissingIntegrity(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3c1"
        parms['grid'] = self.validGridValue
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300_940ShouldReturnErrOnStrValue(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "two"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300_950ShouldReturnErrOnFloatingPointValue(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2.5"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
                
    def test300_960ShouldReturnErrOnValueGT9(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "11"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300_970ShouldReturnErrOnValueLT1(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "0"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300_980ShouldReturnErrOnNegativeValue(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "-2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300_990ShouldReturnErrOnInvalidRowKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "x3c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1000ShouldReturnErrOnExtraLettersInRowKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "Rx3c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1010ShouldReturnErrOnMissingRowKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "3c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1020ShouldReturnErrOnBlankRowKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = " 3c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1030ShouldReturnErrOnIntegerRowKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "33c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1040ShouldReturnErrOnfFloatingPointRowKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "3.03c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1050ShouldReturnErrOnMissingRowNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "rc1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1060ShouldReturnErrOnBlankRowNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1070ShouldReturnErrOnStrRowNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "rcc1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1080ShouldReturnErrOnRowNumLT1InCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r0c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1090ShouldReturnErrOnRowNumGT9InCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r10c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1100ShouldReturnErrOnFloatingPointRowNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r9.2c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1110ShouldReturnErrOnFloatingPointRowNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2.0c1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
        
    def test300__1120ShouldReturnErrOnInvalidColKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3x1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1130ShouldReturnErrOnExtraLettersInColKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "R3cx1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
     
    def test300__1140ShouldReturnErrOnMissingColKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r31"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
     
    def test300__1150ShouldReturnErrOnBlankColKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3 1"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
     
    def test300__1160ShouldReturnErrOnIntegerColKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r331"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
     
    def test300__1170ShouldReturnErrOnfFloatingPointColKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3c1.0"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1180ShouldReturnErrOnfFloatingPointColKeyInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r3c1.7"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1190ShouldReturnErrOnMissingColNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1200ShouldReturnErrOnBlankColNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r1c "
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
     
    def test300__1210ShouldReturnErrOnStrColNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2cc"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
     
    def test300__1220ShouldReturnErrOnColNumLT1InCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r1c0"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
   
    def test300__1230ShouldReturnErrOnColNumGT9InCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r1c14"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
     
    def test300__1240ShouldReturnErrOnFloatingPointColNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r8c9.2"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
     
    def test300__1250ShouldReturnErrOnFloatingPointColNumInCell(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2.0"
        parms['grid'] = self.validGridValue
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1260ShouldReturnErrOnEmptyGrid(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = ''
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1270ShouldReturnErrOnBlankGrid(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = '     '
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300__1280ShouldReturnErrOnInvalidGrid(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = '[, ]'
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1290ShouldReturnErrOnStrGrid(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = "-8-4000-7-9-5-1-1-90-8-5-3-4-2-6-50-6-10-9000-7000-1-50-8-4-60-40-8-20-9-3-9-5-8-30-4-70-2-3-800-9-60-4-7-2-7-900-8-1-6000-5-2-7-1-8-30"
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1300ShouldReturnErrOnIntegerGrid(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = '23'
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1310ShouldReturnErrOnGridWithEmptyList(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = '[]'
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300__1320ShouldReturnErrOnGridHasGT81Elements(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = "[-8,-1,-5,-7,-6,-9,-3,-2,0,\
                         -4,-9,0,0,0,-5,-8,-7,0,\
                         0,0,-6,0,-4,-8,0,-9,-5,\
                         0,-8,-1,0,0,-3,0,0,-2,\
                         0,-5,0,-1,-8,3,0,-9,0,-7,\
                         -7,-3,-9,-5,-2,-4,-6,-8,-1,\
                         -9,-4,0,0,0,-7,0,-1,-8,\
                         -5,-2,0,-8,-9,0,-4,-6,-3,\
                         -1,-6,0,-4,-3,-2,-7,0,0, -2]"
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300__1330ShouldReturnErrOnGriHasLT81Elements(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = "[-8,-1,-5,-7,-6,-9,-3,-2,0,\
                         -4,-9,0,0,0,-5,-8,-7,0,\
                         0,0,-6,0,-4,-8,0,-9,-5,\
                         0,-8,-1,0,0,-3,0,0,-2,\
                         0,-5,0,-1,-8,3,0,-9,0,-7,\
                         -7,-3,-9,-5,-2,-4,-6,-8,-1,\
                         -9,-4,0,0,0,-7,0,-1,-8,\
                         -5,-2,0,-8,-9,0,-4,-6,-3,\
                         -1,-6,0,-4,-3,-2,-7,0,0, -2]"
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1340ShouldReturnErrOnGriHasLT81Elements(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        gridList = [1]*78
        gridList.append(3)
        gridList.append(4)
        gridList.append(2)
        gridListStr = ''.join(str(e) for e in gridList)
        parms['grid'] = gridListStr
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300__1350ShouldReturnErrOnGriHasElementsGT9(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = '[-8,-1,-5,-7,-6,19,-3,-2,0,\
                          -4,-9,0,0,0,-5,-8,-7,0,\
                          0,0,-6,0,-4,-8,0,-9,-5,\
                          0,-8,-1,0,0,-3,0,0,-2,\
                          0,-5,0,-1,-8,0,-9,0,-7,\
                          -7,-3,-9,-5,-2,-4,-6,-8,-1,\
                          -9,-4,0,0,0,-7,0,-1,-8,\
                          -5,-2,0,-8,-9,0,-4,-6,-3,\
                          -1,-6,0,-4,-3,-2,-7,0,0]'
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1360ShouldReturnErrOnGriHasElementsLTMinus9(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = '[-8,-1,-5,-7,-6,-19,-3,-2,0,\
                          -4,-9,0,0,0,-5,-8,-7,0,\
                          0,0,-6,0,-4,-8,0,-9,-5,\
                          0,-8,-1,0,0,-3,0,0,-2,\
                          0,-5,0,-1,-8,0,-9,0,-7,\
                          -7,-3,-9,-5,-2,-4,-6,-8,-1,\
                          -9,-4,0,0,0,-7,0,-1,-8,\
                          -5,-2,0,-8,-9,0,-4,-6,-3,\
                          -1,-6,0,-4,-3,-2,-7,0,0]'
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1370ShouldReturnErrOnGriHasBlankElements(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = '[-8,-1,-5,-7,-6, ,-3,-2,0,\
                          -4,-9,0,0,0,-5,-8,-7,0,\
                          0,0,-6,0,-4,-8,0,-9,-5,\
                          0,-8,-1,0,0,-3,0,0,-2,\
                          0,-5,0,-1,-8,0,-9,0,-7,\
                          -7,-3,-9,-5,-2,-4,-6,-8,-1,\
                          -9,-4,0,0,0,-7,0,-1,-8,\
                          -5,-2,0,-8,-9,0,-4,-6,-3,\
                          -1,-6,0,-4,-3,-2,-7,0,0]'
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1380ShouldReturnErrOnGriHasStrElements(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = '[-8,-1,-5,-7,-6,two,-3,-2,0,\
                          -4,-9,0,0,0,-5,-8,-7,0,\
                          0,0,-6,0,-4,-8,0,-9,-5,\
                          0,-8,-1,0,0,-3,0,0,-2,\
                          0,-5,0,-1,-8,0,-9,0,-7,\
                          -7,-3,-9,-5,-2,-4,-6,-8,-1,\
                          -9,-4,0,0,0,-7,0,-1,-8,\
                          -5,-2,0,-8,-9,0,-4,-6,-3,\
                          -1,-6,0,-4,-3,-2,-7,0,0]'
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1390ShouldReturnErrOnGriHasFloatingPointElements(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = '[-8,-1,-5,-7,-6,2.4,-3,-2,0,\
                          -4,-9,0,0,0,-5,-8,-7,0,\
                          0,0,-6,0,-4,-8,0,-9,-5,\
                          0,-8,-1,0,0,-3,0,0,-2,\
                          0,-5,0,-1,-8,0,5.2,0,-7,\
                          -7,-3,-9,-5,-2,-4,-6,-8,-1,\
                          -9,-4,0,0,0,-7,0,-1,-8,\
                          -5,-2,0,-8,-9,0,-4,-6,-3,\
                          -1,-6,0,-4,-3,-2,-7,0,0]'
        parms['integrity'] = self.validIntegrityValue
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300__1400ShouldReturnErrOnEmptyIntegrityValue(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = self.validGridValue
        parms['integrity'] = ''
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1410ShouldReturnErrOnIntegerIntegrityValue(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = self.validGridValue
        parms['integrity'] = '3'
        parms['value'] = "2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1420ShouldReturnErrOnBlankIntegrityValue(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = self.validGridValue
        parms['integrity'] = '    '
        parms['value'] = "3"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1430ShouldReturnErrOnInvalidIntegrityValue(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = self.validGridValue
        parms['integrity'] = '634dd6769e9b9a53e   e4416edb9790684ac18dcbde5b879260610ff27794b66f5'
        parms['value'] = '3'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300__1440ShouldReturnErrOnInvalidIntegrityValue(self):
        parms = {'op':'insert'}
        parms['cell'] = "r2c2"
        parms['grid'] = self.validGridValue
        parms['integrity'] = (self.validIntegrityValue+"abc")
        parms['value'] = '3'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1450ShouldReturnErrWhenAttemptedToChangeFixedHint(self):
        parms = {'op':'insert'}
        parms['cell'] = "r6c3"
        parms['grid'] = self.validGridValue
        parms['integrity'] = (self.validIntegrityValue)
        parms['value'] = '3'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300__1460ShouldReturnErrWhenColNotGiven(self):
        parms = {'op':'insert'}
        parms['cell'] = "r6"
        parms['grid'] = self.validGridValue
        parms['integrity'] = (self.validIntegrityValue)
        parms['value'] = '3'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test300__1470ShouldReturnErrWhenRowNotGiven(self):
        parms = {'op':'insert'}
        parms['cell'] = "c6"
        parms['grid'] = self.validGridValue
        parms['integrity'] = (self.validIntegrityValue)
        parms['value'] = '3'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test300__1480ShouldReturnWhenAttemptedToChangeFixedHint(self):   
        parms = {'op':'insert'}
        parms['cell'] = "R7C1"
        parms['integrity'] = "c1a503b42fd08e20e49dc0fca9031d4aa21ed4afbab3d43e9ce98f38858d6edd"
        
        parms['grid'] ='[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,-7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1]'
                      
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
        
    # Happy Path Test
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], self.status)
        self.assertListEqual(result['grid'], expectedGrid)
        self.assertEquals(result['integrity'],"8f33014a3edf131ca46fe1ebc5354dd7d82a5d4f13a0584851c9fbab6b4e2013")
        
        
    
    def test300_110ShouldInsertValueOnCapitalRowLowerCaseCol(self):   
        parms = {'op':'insert'}
        parms['cell'] = "R2c6"
        parms['integrity'] = "3419ea2ff6ecca9ed69c9ac9976abdf9d3bad3034249356038ea9d1d52c59814"
        
        parms['value'] = '3'
        parms['grid'] ='[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,0,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,0,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,0,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1 ]'
        expectedGrid=[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,0,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,0,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1 ]
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], self.status)
        self.assertListEqual(result['grid'], expectedGrid)
    
        self.assertEquals(result['integrity'],'208b5e451cfa05fe9066e59178521a3fefb705ae21e617e68445c3c17e7a79c5')
        
        
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], self.status)
        self.assertListEqual(result['grid'], expectedGrid)
    
        self.assertEquals(result['integrity'],'0602732c075d6e079b5b698f2796db734c29ea5b34625d384486f08399f0dfbb')
        
    def test300_130ShouldInsertValueOnCapitalRowAndCol(self):   
        parms = {'op':'insert'}
        parms['cell'] = "R7C6"
        parms['integrity'] = "e667ed7782a71cae93d89f7a5a93aaeacc0484b0b95ae2518b1aa82b33a6c836"
        
        parms['value'] = '7'
        parms['grid'] ='[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,0,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1 ]'
                      
        expectedGrid=[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1]
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], self.status)
        self.assertListEqual(result['grid'], expectedGrid)
    
        self.assertEquals(result['integrity'],'938ee8d77f0ddb7920348da08490a7118a14525676a2d369094dde65c1a419c3')   
        
    def test300_140ShouldReturnWarningOnColumnConflict(self):   
        parms = {'op':'insert'}
        parms['cell'] = "R9C6"
        parms['integrity'] = "c1a503b42fd08e20e49dc0fca9031d4aa21ed4afbab3d43e9ce98f38858d6edd"
        
        parms['value'] = '8'
        parms['grid'] ='[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,-7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1]'
                      
        expectedGrid=[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,-7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,8,0,0,-1]
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], "warning")
        self.assertListEqual(result['grid'], expectedGrid)
    
        self.assertEquals(result['integrity'],'5b44b1b8fad8648388e82f91f500c748786d35ede2ba246ff95ba9e799871628')   

    def test300_150ShouldReturnWarningOnRowConflict(self):   
        parms = {'op':'insert'}
        parms['cell'] = "r9c6"
        parms['integrity'] = "c1a503b42fd08e20e49dc0fca9031d4aa21ed4afbab3d43e9ce98f38858d6edd"
        
        parms['value'] = '1'
        parms['grid'] ='[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,-7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1]'
                      
        expectedGrid=[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,-7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,1,0,0,-1]
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], "warning")
        self.assertListEqual(result['grid'], expectedGrid)
    
        self.assertEquals(result['integrity'],'da81eaf11882d515c83c2e43017d48b0ac1173939d3675468888f8d1417827af')   
    
    
    def test300_160ShouldReturnWarningOnBoxConflict(self):   
        parms = {'op':'insert'}
        parms['cell'] = "r9c6"
        parms['integrity'] = "c1a503b42fd08e20e49dc0fca9031d4aa21ed4afbab3d43e9ce98f38858d6edd"
        
        parms['value'] = '3'
        parms['grid'] ='[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,-7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1]'
                      
        expectedGrid=[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,-7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,3,0,0,-1]
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], "warning")
        self.assertListEqual(result['grid'], expectedGrid)
    
        self.assertEquals(result['integrity'],'e96321274f97dcec471716e6103f05b10010c6f6d39fba78a4f7ffcd4afc1efb')   

    def test300_160ShouldRemoveContentWhenValueNotGivenWithSmallCaseRAndC(self):   
        parms = {'op':'insert'}
        parms['cell'] = "r8c2"
        parms['integrity'] = "1e860669d27712015911b2901a637ebafe24771280895847e9d1024a28a0741f"
        
        parms['grid'] ='[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,-7,-2,0,0,\
                      -8,4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1]'
                      
        expectedGrid=[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      -5,0,0,-3,-8,-7,-2,0,0,\
                      -8,0,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1]
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], self.status)
        self.assertListEqual(result['grid'], expectedGrid)
    
        self.assertEquals(result['integrity'],'580b1cf59720a77a6210113c95a1ed1a32b9d5ade0599851be82147ce3203838')   

    def test300_170ShouldRemoveContentWhenValueNotGivenWithSCapitalRAndC(self):   
        parms = {'op':'insert'}
        parms['cell'] = "R7C1"
        parms['integrity'] = "42d45f94a55ee84d7fea682e3f5e56601edee6e95c55f4f1c84d8a02f38cb31a"
        
        parms['grid'] ='[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      5,0,0,-3,-8,-7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1]'
                      
        expectedGrid=[-7,0,0,0,-6,-8,0,-4,0,\
                      -4,0,0,-1,0,-3,0,-8,-5,\
                      0,0,-8,0,-9,-4,0,0,-3,\
                      0,-8,-4,0,0,-6,0,0,0,\
                      0,0,0,-7,-3,-2,0,0,0,\
                      0,0,-7,-8,0,0,-3,-1,0,\
                      0,0,0,-3,-8,-7,-2,0,0,\
                      -8,-4,0,0,0,-1,0,0,-7,\
                      0,-7,0,0,-5,0,0,0,-1]
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertEquals(result['status'], self.status)
        self.assertListEqual(result['grid'], expectedGrid)
    
        self.assertEquals(result['integrity'],'f61c9cb407a4c5287289f4ae8bbc1fb43b189874061d63d61bb06b2541654395')
        
#        ----- isdone Tests -----

#        ----- isdone happy path Tests -----

    def test400_101ShouldReturnSolvedWithCompletedGrid(self):
        parms = {'grid': "[4,-5,-8,-9, 3, -1, -6, 7, 2,-2, 3, 7, -5, -8, 6, 9, -4, -1, -9, 6, 1, 7, 4, 2, 3, -5, " +\
                            "8, -3, 9, -6, -1, -5, 7, 8, -2, 4, -1, -4, 5, 3, -2, 8, -7, 6, -9, 7, 8, 2, 4, -6, 9, -5, 1, 3, " +\
                            "6, -1, -3, -2, 9, 5, -4, -8, -7, 8, 2, -4, 6, 7, -3, 1, 9, 5, -5, 7, 9, -8, -1, 4, -2, 3, 6]",
            'integrity': "e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6",
            'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:6], 'solved')
        
    def test400_102ShouldReturnIncompleteForIncompGridFollowRules(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,"+\
                            "-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,"+\
                            "-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                'integrity': "634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5",
                'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:10], 'incomplete')
        
    def test400_103ShouldReturnWarningForIncompGridBreakRules(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,8,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,"+\
                            "-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,"+\
                            "-1,-6,0,-4,-3,-2,-7,0,0]",
                'integrity': "fb50f09c24b3af3d2633b4b6648ea412785c9d2a9ef117e7fecb3d2993456d0e",
                'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:7], 'warning')
        
    def test400_104ShouldReturnWarningForRowViolatingRule(self):
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
                 'integrity': 'd675c71cac8dd61f8ee3076f17aaaea564d8ee4978a8dae397ba021b8a5b62e4',
                 'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'warning')
    
    def test400_105_ShouldReturnWarningForColumnViolatingRule(self):
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
                 'integrity': "ce82814b351938310fdc070da61ee84933b43f239b3c217d829410c9f7c557ff",
                 'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'warning')
    
    def test400_106_ShouldReturnWarningForSubgridViolatingRule(self):
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
                 'integrity': '34e4943cadbe4c468cc0b980e344de3d07905cc5ef2c57e70cd30b9e2d637b20',
                 'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'warning')

#        ------ isdone Sad Path Tests ------
        
    def test400_901ShouldReturnErrorInvalidCellInGrid(self):
        parms = {'grid': "['a',-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,"+\
                            "-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,"+\
                            "-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                'integrity': "634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5",
                'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error: invalid grid')
    
    def test400_902ShouldReturnErrorGridIntegrityMismatch(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,"+\
                            "-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,"+\
                            "-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
            'integrity': "0000000000000000000000000000000000000000000000000000000000000000",
            'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error: integrity mismatch')
        
    def test400_903ShouldReturnErrorFromMissingGrid(self):
        parms = {'integrity': 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6',
            'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'error: missing grid')
    
    def test400_904ShouldReturnErrorFromMissingIntegrity(self):
        parms = {'grid': "[4,-5,-8,-9,3,-1,-6,7,2,-2,3,7,-5,-8,6,9,-4,-1,-9,6,1,7,4,2,3,-5,"+\
                            "8,-3,9,-6,-1,-5,7,8,-2,4,-1,-4,5,3,-2,8,-7,6,-9,7,8,2,4,-6,9,-5,1,"+\
                            "3,6,-1,-3,-2,9,5,-4,-8,-7,8,2,-4,6,7,-3,1,9,5,-5,7,9,-8,-1,4,-2,3,6]",
            'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'error: missing integrity')
        
    def test400_905ShouldReturnErrorFromInvalidCellInGrid(self):
        parms = {'grid': "[-10,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,"+\
                            "-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,"+\
                            "-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
            'integrity': '634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5',
            'op': 'isdone'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'], 'error: invalid grid')
        
    def test_400_906_ShouldErrOnEmptyGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = ''
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test_400_907_ShouldErrOnBlankGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = '     '
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test_400_908_ShouldErrOnInvalidGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[, ]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_400_909_ShouldErrOnStrGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = '-8-4000-7-9-5-1-1-90-8-5-3-4-2-6-50-6-10-9000-7000-1-50-8-4-60-40-8-20-9-3-9-5-8-30-4-70-2-3-800-9-60-4-7-2-7-900-8-1-6000-5-2-7-1-8-30'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_400_910_ShouldErrOnIntegerGrid(self):
        parms = {'op':'isdone'}
        parms['grid'] = '23'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_400_911_ShouldErrOnGridWithEmptyList(self):
        parms = {'op':'isdone'}
        parms['grid'] = '[]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 

    def test_400_912_ShouldErrOnGridHasGT81Elements(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_400_913_ShouldErrOnGridHasLT81Elements(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 

    def test_400_914_ShouldErrOnGridHasElementsGT9(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_400_915_ShouldErrOnGridHasElementsLTMinus9(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_400_916_ShouldErrOnGridHasBlankElements(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_400_917_ShouldErrOnGridHasFloatingPointElements(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
##################################
#    Solve Happy Paths
    
    def test500_101_ShouldSolveASolvableGrid(self):
        parms = {'grid': '[0,-5,-8,-9,0,-1,-6,0,0,-2,0,0,-5,-8,0,0,-4,-1,-9,0,0,0,0,0,0,-5,0,-3,0,-6,-1,' +\
                        '-5,0,0,-2,0,-1,-4,0,0,-2,0,-7,0,-9,0,0,0,0,-6,0,-5,0,0,0,-1,-3,-2,0,0,-4,-8,-7,' +\
                        '0,0,-4,0,0,-3,0,0,0,-5,0,0,-8,-1,0,-2,0,0]',
                 'integrity': '6594d6506dc349fdbd9e5dda58acfa8d563657b0ef8bfc3a24ea53df9c988f9b'
                }
        parms['op'] = 'solve'
        result = self.microservice(parms)
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
        
    def test500_102_ShouldSolveAlreadySolvedGrid(self):
        parms = {'grid': '[4, -5, -8, -9, 3, -1, -6, 7, 2, -2, 3, 7, -5, -8, 6, 9, -4, -1,' +\
                        ' -9, 6, 1, 7, 4, 2, 3, -5, 8, -3, 9, -6, -1, -5, 7, 8, -2, 4, -1, -4, 5, 3, -2,' +\
                        ' 8, -7, 6, -9, 7, 8, 2, 4, -6, 9, -5, 1, 3, 6, -1, -3, -2, 9, 5, -4, -8, -7, 8,' +\
                        ' 2, -4, 6, 7, -3, 1, 9, 5, -5, 7, 9, -8, -1, 4, -2, 3, 6]',
                 'integrity': 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
                }
        parms['op'] = 'solve'
        result = self.microservice(parms)
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
    
    def test500_103_ShouldSolveLevel5Grid(self):
        parms = {'grid': '[-2,0,0,0,-5,0,-9,-1,0,-6,0,0,0,0,-8,0,0,0,0,0,0,0,0,0,0,-3,0,0,-2,-4,0,0,0,0,0,' +\
                           '0,0,0,0,-4,0,0,0,0,-7,0,-9,-3,0,-1,0,-5,0,0,0,0,0,0,0,-7,0,0,-2,0,-1,0,0,-3,0,0,' +\
                           '-5,0,-4,0,0,-6,0,0,0,0,0]', 
                 'integrity': '110a79143bc7c2b66faff5e8fe895320d402e4f91dbbe6b969931228abb84242',
                 'op': 'solve'
                }
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '21bc00d8038232acc79ff372bd3047617d6e4bafb47e2f77896c08b56ca26503') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [-2, 4, 8, 7, -5, 3, -9, -1, 6, -6, 3, 1, 9, 4, -8, 2, 7, 5, 9, 7, 5, 1, 6, 2, 4, \
                         -3, 8, 5, -2, -4, 3, 7, 9, 8, 6, 1, 1, 8, 6, -4, 2, 5, 3, 9, -7, 7, -9, -3, 8, -1, \
                         6, -5, 2, 4, 3, 6, 9, 5, 8, -7, 1, 4, -2, 8, -1, 7, 2, -3, 4, 6, -5, 9, -4, 5, 2, -6, 9, 1, 7, 8, 3])
        
    def test500_104_ShouldSolveLevel4Grid(self):
        parms = {'grid': '[0,-6,-7,0,-2,0,0,0,-3,0,-8,0,-7,0,-3,0,0,-6,-1,0,0,0,0,0,0,-7,0,'+\
                            '0,-5,0,0,-3,0,0,0,-8,-8,0,0,0,-4,0,0,0,-1,-4,0,0,0,-6,0,0,-5,'+\
                            '0,-3,0,0,0,0,0,0,0,-2,-6,0,0,-2,0,-4,0,-3,0,-5,0,0,0,-9,0,-8,-4,0]',
                'integrity': '0ea83ad27c27241477102e2377f1bb14cc2f8c6125fbc85fab972c9ab0661319',
                'op': 'solve'}
        result = self.microservice(parms)
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
        
    def test500_105_ShouldSolveLevel3Grid(self):
        parms = {'grid': '[0,0,-3,0,0,-7,0,-2,0,-4,0,-7,0,0,-5,-3,0,0,0,0,-8,-9,0,-6,-7,0,-1,-8,0,-2,-5,0,0,' +\
                        '-6,0,-4,0,-7,0,0,-8,0,-1,-5,0,-5,0,0,-7,-6,0,0,0,-9,0,0,-5,0,0,-9,0,0,-6,0,-1,0,-6,' +\
                        '0,0,-2,-8,0,0,-2,-4,-1,-7,0,-5,0,0]', 
                 'integrity': 'b594924588d873f60df054a64a7bfaa1d4196ab1d2000f1788a453c1765b05b8'
                }
        parms['op'] = 'solve'
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], 'ec6c0462503c83794dab7b293bda2f35fdfa1a858f975a5d293fa8f3d70015ca') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [1, 6, -3, 8, 4, -7, 9, -2, 5, -4, 9, -7, 2, 1, -5, -3, 6, 8, 2, 5, -8, -9, 3, -6, \
                        -7, 4, -1, -8, 3, -2, -5, 9, 1, -6, 7, -4, 9, -7, 6, 4, -8, 3, -1, -5, 2, -5, 4, 1, -7, -6, 2, 8, 3, \
                         -9, 7, 8, -5, 3, 2, -9, 4, 1, -6, 3, -1, 9, -6, 5, 4, -2, -8, 7, 6, -2, -4, -1, -7, 8, -5, 9, 3])
        
    def test500_106_ShouldSolveLevel2Grid(self):
        parms = {'grid': '[0,-3,0,0,0,-2,0,-6,-5,-5,-8,0,-1,-3,-4,0,-2,-9,0,-2,-7,0,-5,0,0,0,-1,0,0,-2,0,0,-9,0,-1,-3,-8,' +\
                        '-5,-9,0,-7,-1,0,-4,-2,-1,0,0,-6,-2,0,0,0,-7,0,0,0,0,-4,-7,-2,-5,0,-6,-7,-5,0,0,-8,0,-9,0,0,-9,' +\
                        '-4,-5,-6,0,0,-7,-8]', 
                 'integrity': '39a4fbe2283d82b8dff98f36e6fcb09e6071653a77795e9527b26f90b4ad0d26'
                }
        parms['op'] = 'solve'
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '36a7cfdc8c6ddbcaf32d004aa6051850b2f2151df043371383221bc022be194b') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [4, -3, 1, 7, 9, -2, 8, -6, -5, -5, -8, 6, -1, -3, -4, 7, -2, -9, 9, -2, -7, 8, -5, \
                         6, 4, 3, -1, 7, 6, -2, 4, 8, -9, 5, -1, -3, -8, -5, -9, 3, -7, -1, 6, -4, -2, -1, 4, 3, -6, -2, 5, 9, \
                         8, -7, 3, 1, 8, 9, -4, -7, -2, -5, 6, -6, -7, -5, 2, 1, -8, 3, -9, 4, 2, -9, -4, -5, -6, 3, 1, -7, -8])
        
    def test500_107_ShouldSolveLevel1Grid(self):
        parms = {'grid': '[-8,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,' +\
                        '-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,' +\
                        '-3,-2,-7,0,0]', 
                 'integrity': '634dd6769e9b9a53ee4416edb9790684ac18dcbde5b879260610ff27794b66f5'
                }
        parms['op'] = 'solve'
        result = self.microservice(parms)
        self.assertEqual(len(result), 3)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('integrity', result)
        self.assertEqual(result['integrity'], '5d3bfc4209683f988d09888d0ef6e0d1e9cfe541fbc8c82bf0590889ee462dcf') 
        self.assertIn('grid', result)
        self.assertEqual(result['grid'], [-8, -1, -5, -7, -6, -9, -3, -2, 4, -4, -9, 2, 3, 1, -5, -8, -7, 6, 3, 7, -6, 2, -4, \
                         -8, 1, -9, -5, 6, -8, -1, 9, 7, -3, 5, 4, -2, 2, -5, 4, -1, -8, 6, -9, 3, -7, -7, -3, -9, -5, -2, -4, \
                         -6, -8, -1, -9, -4, 3, 6, 5, -7, 2, -1, -8, -5, -2, 7, -8, -9, 1, -4, -6, -3, -1, -6, 8, -4, -3, -2, -7, 5, 9])
        
##################################
#    Solve Sad Paths
        
    def test_500_903_AttemptToSolveGridWithUnsolvableValues(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,8,-4,-9,0,0,0,-5,-8,-7,"+\
                            "0,0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,"+\
                            "-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,"+\
                            "-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                 'integrity': "fb50f09c24b3af3d2633b4b6648ea412785c9d2a9ef117e7fecb3d2993456d0e",
                 'op': 'solve'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:6], 'error: grid not solvable')
    def test_500_904_ShouldErrOnGridWithInvalidCell(self):
        parms = {'grid': "[a,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,"+\
                            "0,0,-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,"+\
                            "0,-1,-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,"+\
                            "0,0,0,-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,"+\
                            "-3,-2,-7,0,0]",
                'integrity': 'bb6a5a53f35b567013fba3dcdfe5718ca2b794ae4bfcdb043f657cc4bfde1e48',
                'op': 'solve'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: invalid grid')
    def test_500_905_ShouldErrOnIntegrityMismatch(self):
        parms = {'grid': "[-8,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,"+\
                            "-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,"+\
                            "-8,0,-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,"+\
                            "-7,0,-1,-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                 'integrity': '0000000000000000000000000000000000000000000000000000000000000000',
                 'op': 'solve'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: integrity mismatch')
        
    def test_500_906_ShouldErrOnGridWithInvalidCell(self):
        parms = {'grid': "[-10,-1,-5,-7,-6,-9,-3,-2,0,-4,-9,0,0,0,-5,-8,-7,0,0,0,"+\
                            "-6,0,-4,-8,0,-9,-5,0,-8,-1,0,0,-3,0,0,-2,0,-5,0,-1,-8,0,"+\
                            "-9,0,-7,-7,-3,-9,-5,-2,-4,-6,-8,-1,-9,-4,0,0,0,-7,0,-1,"+\
                            "-8,-5,-2,0,-8,-9,0,-4,-6,-3,-1,-6,0,-4,-3,-2,-7,0,0]",
                 'integrity': '93574c2d0c472770fcb8e91405ab39baf1e42ff8a238d182fbed0ca70d77bca5',
                 'op': 'solve'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: invalid grid')
        
    def test_500_907_ShouldErrOnMissingIntegrity(self):
        parms = {'grid': "[4,-5,-8,-9,3,-1,-6,7,2,-2,3,7,-5,-8,6,9,-4,-1,-9,6,1,7,"+\
                            "4,2,3,-5,8,-3,9,-6,-1,-5,7,8,-2,4,-1,-4,5,3,-2,8,-7,6,"+\
                            "-9,7,8,2,4,-6,9,-5,1,3,6,-1,-3,-2,9,5,-4,-8,-7,8,2,-4,"+\
                            "6,7,-3,1,9,5,-5,7,9,-8,-1,4,-2,3,6]",
                'op': 'solve'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: missing integrity')
        
    def test_500_908_ShouldErrOnMissingGrid(self):
        parms = {'integrity': "e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6",
                 'op': 'solve'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'error: missing grid')
        
    def test_500_909_ShouldErrOnEmptyGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = ''
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test_500_910_ShouldErrOnBlankGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = '     '
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test_500_911_ShouldErrOnInvalidGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = '[, ]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_500_912_ShouldErrOnStrGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = '-8-4000-7-9-5-1-1-90-8-5-3-4-2-6-50-6-10-9000-7000-1-50-8-4-60-40-8-20-9-3-9-5-8-30-4-70-2-3-800-9-60-4-7-2-7-900-8-1-6000-5-2-7-1-8-30'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_500_913_ShouldErrOnIntegerGrid(self):
        parms = {'op':'solve'}
        parms['grid'] = '23'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_500_914_ShouldErrOnGridWithEmptyList(self):
        parms = {'op':'solve'}
        parms['grid'] = '[]'
        parms['integrity'] = 'e33e2de2fdbb25aacf25b299e101cccfdd2e1be4284acc257bcdc76737272af6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 

    def test_500_915_ShouldErrOnGridHasGT81Elements(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_500_916_ShouldErrOnGridHasLT81Elements(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 

    def test_500_917_ShouldErrOnGridHasElementsGT9(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_500_918_ShouldErrOnGridHasElementsLTMinus9(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_500_919_ShouldErrOnGridHasBlankElements(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test_500_920_ShouldErrOnGridHasFloatingPointElements(self):
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
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')