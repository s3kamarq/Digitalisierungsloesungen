from tkinter import filedialog
from tkinter import messagebox
import pandas as pd

inputfile= filedialog.askopenfilename()
type(inputfile)
print(inputfile)
def openpreviousdata():
    m= messagebox.askyesno(message=r'Möchten Sie das Zwischnergebnis einlesen?')
    if m==True:
        inputfile= filedialog.askopenfilename()
        eingelesenesDataframe= pd.read_pickle(inputfile)
    else:
        eingelesenesDataframe=pd.DataFrame()
    return eingelesenesDataframe

print(eingelesenesDataframe)

k=0
for i in webelem_links['links']:
    
    for j in intermediate_result['Link']:
        if i==j:
            print(i)
    

for i in intermediate_result['Link']:
    k+=1
    print(k)
    if i in webelem_links['links']:
        print(i)
    else:
        print('not found')

    
intermediate_result['Link'][0]==webelem_links['links'][1]
t=webelem_links['webelements']
type(t)
item=webelem_links['webelements'][0]
type(item) # webelement

for item in webelem_links['webelements']:
    print(item)