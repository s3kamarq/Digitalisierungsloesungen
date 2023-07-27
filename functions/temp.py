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

