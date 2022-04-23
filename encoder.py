import logging as log
from test_data import TestData, ReturnCode
from excelHandler import Excel

class Encoder:
    def __init__(self,d:'list[TestData]', lang) -> None:
        self.d = d
        self.lang = str(lang)
        self.filename = f'./data/braille_{self.lang[0:3].lower().replace("-","")}.h'


    def sort_data(self) -> None:
        self.d.sort(key= lambda x: getattr(x, 'num'))

    def header(self) -> str:
        s = "\n"
        special_char_map = {ord('Ä'):'A', ord('Ü'):'U', ord('Ö'):'O'}
        guardname = self.filename[-13:-2].upper().replace('-','').translate(special_char_map).replace('/','')
       
        

        ifguard =(
                f"#ifndef __{guardname}_H__",
                f"#define __{guardname}_H__",
                2*'\n'
        )

        include = ('#include "keylayouts.h"', 2*'\n')
        
        declaration = ( "// Erich Schmids 8 Keys Braille",
            "const static uint16_t chord_id_keycode[256][4] = {",
            "//            {char, char_modifier, deadkey, deadkey_modifier}"
        )
        head = ifguard + include + declaration
        return s.join(head)
    
    def array(self,key,mod,dead,dmod) -> str:
        if key == None:
            key = 0

        elif key == "GRAVE" or key == "SCANCODE_GRAVE":
            key ='SCANCODE_GRAVE'
        
        

        else:
            key = 'KEY_' + key

        if mod == None:
            mod = 0
        else: 
            mod = 'MODIFIERKEY_' + mod

        if dead == None:
            dead = 0
        elif dead == "GRAVE" or dead == "SCANCODE_GRAVE":
            dead = 'SCANCODE_GRAVE'
        else: 
            dead = 'DEADKEY_' + dead

        if dmod == None:
            dmod = 0
        else: 
            dmod = 'MODIFIERKEY_' + dmod


        s = f"{key}, {mod}, {dead}, {dmod}"
        return '{' + s + '},'

    def num(self, num)-> str:
        s = f"/* {num}  */"
        return s

    def braille_cha(self, brai, cha) -> str:
        s = f"/* '{cha}' dots-{brai} */"
        return s
    
    def null_line(self, num)-> str:
        s = f"/* {num}  */\t"+"{0, 0, 0, 0},"+ 59*' ' +"// 0"
        return s

    def end_of_file(self)->str:
        s = "};" + 2*'\n' + '#endif'
        return s

    def tab_handler(self,len)-> str:
        max_space = 72
        space = max_space - len
        return space*' '

    def run(self):
        self.sort_data()

        with open(self.filename, 'w') as file:                # a = append, w = (over)write
            print(self.header(), file=file)
            idx = 0
            cnt = 0
            prev_num = -1
            while idx < len(self.d):
                data = self.d[idx]    
                if prev_num == data.num or cnt > data.num:
                    log.error(f"{prev_num} exists twice !!!! Not good. You almost buffer overflowed")
                    break
                
                # if data is shitty
                elif data.color_key >= ReturnCode.YELLOW or data.color_mod >= ReturnCode.YELLOW or data.color_dmo >= ReturnCode.YELLOW:
                    print(self.null_line(cnt), file=file)
                    idx += 1

                elif cnt == data.num:
                    print(self.num(data.num), file=file, end='\t')
                    arr = self.array(data.key, data.mod, data.dead, data.dmod)
                    print(arr, file=file, end=self.tab_handler(len(arr)))
                    print(self.braille_cha(data.brai, data.cha), file=file)
                    prev_num = data.num
                    idx +=1
                else:
                    print(self.null_line(cnt), file=file)

                cnt+=1
                
            log.info(f"{cnt} Rows encoded")
            print(self.end_of_file(), file=file)



#numbers= [1,3,5,7,9,10,11,12,13,15,17,19,20]



# dat= [TestData(0,n,randint(100,200000),'a','A',' ',' ',' ') for n in numbers]
# encoder = Encoder(dat,'türkisch')
# encoder.sort_data()
# encoder.encode()



