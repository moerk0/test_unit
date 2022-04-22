import code
from dataclasses import dataclass
import logging as log
from tkinter.tix import CheckList

log.basicConfig(level=log.DEBUG, format="%(levelname)s:%(message)s")





@dataclass
class TestData:
    """
    Each one object holds one Row of ExcelTable and it holds the Color coding of the result file
    Initially TestData requires 4 Inputs: 
    The Bin Num to send, The expected Char, The name of the key and The modifier Key.

    Recieved and Passed are Values that the Test_unit Program fills. They are not mandatory for the Encoder,
    but it is nice to keep them, so a future fusion is possible.

    The Color variables indicate where Data has to be rechecked. They are handled by the validate() Function
    Green means that there was a mistake, that the programm corrected.
    OR
    The Test is passed

    Yellow means there was a mistake that influences the Output of the .h -File 
    OR
    for the received Column it means that no data arrieved( receivied = None) during runtime of the test

    Red means Either the Char column or the Int column are Faulty
    OR
    For the passed Column it means that the expected char and the recieved Char are not equal.

    """
    
    row : int

    num: int
    brai: str
    cha: str
    
    key: str
    mod: str

    dead: str
    dmod : str

    received: str = None
    passed: bool =  False
    
    #Color Codes: 0 = No Color, 1 = Green, 2 = Yellow, 3 = Red
    color_num: int = 0
    color_cha: int = 0
    color_key: int = 0
    color_mod: int = 0
    color_ded: int = 0
    color_dmo: int = 0

    color_rec: int = 0
    color_pas: int = 3

    def validate_num(self):
        
        if self.num == 0:
            
            log.error(f'\tRow: {self.row} - Num >> {self.num} << is Null.')
            self.color_num = 3
            
        else:
            pass

    def validate_cha(self):
        if self.cha is None:
            log.warning(f"Row: {self.row} - Cha is None")
            self.color_cha = 2

        elif str(self.cha).isspace() == True:                        # if it is escaped char
            pass

        else:
            self.cha = str(self.cha)
            len_cha = len(self.cha)
            
            if len_cha > 1:
                self.cha = self.cha.strip()
                    
                try:
                    ord(self.cha)
                    log.info(f"\tRow: {self.row} - Cha >> {self.cha} << had a space character. Removed")
                    self.color_cha = 1
                    self.cha = self.cha.strip()
                except:
                    log.error(f"\tRow: {self.row} - Cha >> {self.cha} << is not a single character!")
                    self.color_cha = 3
            else:
                pass
                
                

    def checkList(self, arg, l) -> int:
        if arg in l:
            return 0
        else:
            log.warning(f'Row: {self.row} - Mod >> {arg} << is not in Key list')
            return  2            
               
    def validate_key(self):
        key_names = ['SPACE','TAB','ENTER','PLUS', 'MINUS','QUOTE','PERIOD', 'SEMICOLON', 
                    'LEFT_BRACE', 'RIGHT_BRACE','GRAVE', 'NON_US_BS','BACKSLASH','COMMA'] 
        
        if self.key is None:
            log.warning(f"Row: {self.row} - Key is None")
            self.color_key = 2
        

                                                                # Key is not a int Number
        else:
            self.key = str(self.key).strip()
            ret = self.checkCase(self.key)
            self.key = ret[0]
            self.color_key = ret[1]



            if self.key.isalpha() and len(self.key)<=1:
                ret = self.checkASCII(self.key)
                if self.color_key < ret:
                    self.color_key = ret

            elif self.key.isdigit():
                pass    

            elif self.checkList(self.key, key_names) == 2:
                self.color_key = 2    
            

            
    def checkASCII(self, arg) -> tuple:
        if str(arg).isascii():
            code = 0
        else:
            log.warning(f'\tRow: {self.row} - Mod >> {arg} << is not ASCII')
            code = 2
        return code

    def checkCase(self,arg)->tuple:
        if str(arg).isupper() == False:
            arg = arg.upper()
            log.info(f'\tRow: {self.row} -  >> {arg} << is not upper. Corrected')
            code = 1
        else:
            code = 0
        return arg, code

    def checkSpace(self, arg):
        if " " in arg:
            arg = arg.strip()
            log.info(f'\tRow: {self.row} - >> {arg} << unexpected Space character. Corrected')
            code = 1
        else:
            code = 0
        return arg, code
            


    def validate_mod(self):
        modifier = ['SHIFT', 'RIGHT_ALT', 'LEFT_ALT', 'CTRL']
            
        if self.mod is not None:
            ret =  self.checkCase(self.mod)
            self.mod =       ret[0]
            self.color_mod = ret[1]
            
            ret = self.checkSpace(self.mod)
            self.mod =       ret[0]
            if ret[1] >= self.color_mod:
                self.color_mod = ret[1]

            if self.mod not in modifier:    
                self.mod = self.mod.replace(" ", "_")
                
                if self.mod in modifier:
                    log.info(f"\tRow: {self.row} - Mod >> {self.mod} << had no underscore. Corrected")
                    self.color_mod = 1
                else:
                    log.warning(f"Row: {self.row} - Mod >> {self.mod} << is unkonwn modifier")
                    self.color_mod = 2
    
    def validate_dmod(self):
        modifier = ['SHIFT', 'RIGHT_ALT', 'LEFT_ALT', 'CTRL']
            
        if self.dmod is not None:
            ret =  self.checkCase(self.dmod)
            self.dmod =       ret[0]
            self.color_dmo = ret[1]
            
            ret = self.checkSpace(self.dmod)
            self.dmod =       ret[0]
            if ret[1] >= self.color_dmo:
                self.color_dmo = ret[1]

            if self.dmod not in modifier:    
                self.dmod = self.dmod.replace(" ", "_")
                
                if self.dmod in modifier:
                    log.info(f"\tRow: {self.row} - Mod >> {self.dmod} << had no underscore. Corrected")
                    self.color_dmod = 1
                else:
                    log.warning(f"Row: {self.row} - Mod >> {self.dmod} << is unkonwn modifier")
                    self.color_dmo = 2
                        
                   
       
    #    ret =  self.checkCase(self.dmod)
    #         self.mod =       ret[0]
    #         self.color_mod = ret[1]

    def validate_all(self):
        l = [self.validate_num, self.validate_cha, self.validate_key, self.validate_mod, self.validate_dmod]
        for call_func in l:
            call_func()
        

    def content(self, level="initial"):
        levels = ["initial", "color", "test", "full"]
        ouput = [

            self.row, self.color_num, self.cha, self.key, self.mod,
            self.received, self.passed, 
            self.color_num,self.color_cha,self.color_key,self.color_mod,self.color_rec, self.color_pas
            
            ]

        if level not in levels:
            log.error(f'{level} not vaild. Possible args: {levels}')
        
        else:
            if level == "initial":
                return *ouput[1:4],
            if level == "color":
                return *ouput[-6:-1],
            if level == "test":
                return *ouput[1,2,5,6],
            if level == "full":
                return *ouput,
    

# d = TestData(1,1,1,'\r ','A','SHIFT',None,None)
# d.validate_all()
# print(len('\x20'))
# if '\x20' == ' ':
#     print('jo')