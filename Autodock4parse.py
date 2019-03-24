from tkinter import Label
from tkinter import Button
from tkinter import filedialog
from tkinter import Tk
import time
import subprocess
import database as db
import ADTparser as file_parser

window=Tk()
window.wm_title("Add to database")

def browse():
    global filename
    filename=filedialog.askopenfilename(filetypes=[("Docking reports","*.dlg")])
    Label(window, text=filename).grid(row=0, column=4)
    time.sleep(1)
    window.update()
    return filename

def run():
    db.df2sqlite(file_parser.parse(filename),'ATD_database.db','data')
    try:
        Label(window, text="Database successfully updated").grid(row=1, column=0)
    except Exception:
        Label(window, text="Error! Check file content").grid(row=2, column=0)

def open_sqlitebrowser():
    dbbrowser=subprocess.run(["sqlitebrowser"])

Button(window, text="Browse", command=browse).grid(row=0, column=2)
Button(window, text="Add to database", command=run).grid(row=1, column=2)
Button(window, text="Open database browser", command=open_sqlitebrowser).grid(row=2, column=2)

window.mainloop()

