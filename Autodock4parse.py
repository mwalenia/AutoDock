from tkinter import *
from tkinter import filedialog
import time
import subprocess
import database as db
import ADTparser as fp

window=Tk()
window.wm_title("Add to database")

def browse():
    global filename
    filename=filedialog.askopenfilename(filetypes=[("Docking reports","*.dlg")])
    print(filename)
    fileprint = Label(window, text=filename).grid(row=0, column=0)
    time.sleep(1)
    window.update()
    return filename
def run():
    #filename=browse()
    db.df2sqlite(fp.parse(filename),'ATD_database.db','data')
    try:
        fileadded = Label(window, text="Database successfully updated").grid(row=1, column=0)
    except Exception:
        filenotadded = Label(window, text="Error! Check file content").grid(row=2, column=0)

def open_sqlitebrowser():
    dbbrowser=subprocess.run(["sqlitebrowser"])

button1=Button(window, text="Browse", command=browse).grid(row=0, column=2)
#fileprint=Label(window, text=filename).grid(row=0,column=1)
button2=Button(window, text="Add to database", command=run).grid(row=1, column=2)
button3=Button(window, text="Open database browser", command=open_sqlitebrowser).grid(row=2, column=2)

window.mainloop()

