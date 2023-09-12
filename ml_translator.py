from googletrans import Translator
import pandas as pd
import time


def ml_translator(text):
    #print(text)
    
    lang = translator.detect(text)
    print (lang.lang)


    if lang.lang == 'en':
      output = translator.translate(text, dest='de')
      return output.text
    else:
      return text

File_name = 'Inputdatei.xlsx'    #Enter file name here! 
Name_of_relevant_col = 'Jobbeschreibung' #Enter column name in file here! Custom value='Jobbeschreibung'    

#Load the data from excel file
df=pd.read_excel(File_name)

#df = df.head(10)
output_liste = []
zaehler=0
for i in df[Name_of_relevant_col]:
   #print(i)
   translator = Translator()
   output_liste.append(ml_translator(i))
   zaehler= zaehler+1
   #time.sleep(2)
   del translator
   print(zaehler)

zwischenergebnis = pd.Series(output_liste)
zwischenergebnis.to_excel('translated.xlsx', encoding='utf-16')