import re
import winsound
zReg = re.compile(r'^[ \-\+]*[zZ]+[ \-\+]*$')
def Zbase(text, sep = ":"):
    try:
        text1 = text.split(sep)
        print(text1)
        
        if(zReg.fullmatch(text1[1])):
            print("ZSTART")
            winsound.PlaySound("base/ZZZ.wav", winsound.SND_FILENAME)
            print("ZEND")
            return True
        else:
            return False
    except:
        return False