import os
import configparser





def WorkingDir()->str:
   return(os.getcwd() + os.path.sep)






#  Text File handlers API
def TextRead(file_name:str)->str:
   f = open(file_name, 'r')
   return(f.read())


def TextReadLines(file_name:str)->str:
   f=open('WordsDomain.txt','r')
   words = f.read()
   return(words.split('\n'));

def TextWrite(file_name:str,txt:str)->bool:
   result :bool = True
   try:
      f = open(file_name)
      f.write(txt)
   except:
      result = False
   return(result)





def IniRed(file_name:str)->list:
   result :bool = True
   try:
      config = configparser.ConfigParser()
      config.read('config.ini')
   except:
      result = False
   return(result)
