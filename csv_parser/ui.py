import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import manager
import os
import sys

class Window(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.show_widgets()

    def show_widgets(self):
        self.master.title("DBhandler")
        self.master.geometry("500x500")
        button1= tk.Button(self, text="Query", command=self.query_handler)
        button1.pack(padx=20, pady=30)
        button2 = tk.Button(self, text="Insert new data", command=self.insertion_handler)
        button2.pack(padx=20, pady=30)
        b_quit = tk.Button(self, text="EXIT", command=self.close_window)
        b_quit.pack(padx=5, pady=100)

    def query_handler(self):
        (query_entry, dump_file_entry) = Query()
        query = query_entry.get()
        dump_file = dump_file_entry.get()
        if query == "" or query == " ":
            messagebox.showerror("Error", "Empty Query")
        if dump_file == "" or dump_file == " ":
            dump_file = os.path.dirname(sys.argv[0]) + "\query.csv"


        manager.work_with_quering(query, dump_file)

    def insertion_handler(self):
        self.dirname = filedialog.askdirectory()
        if self.dirname == "" or self.dirname == " ":
            messagebox.showerror("Error", "Invalid directory name")
        else:
            #print(self.dirname)
            manager.work_with_folder(self.dirname)

    def close_window(self):
        self.master.destroy()

def Query():
    queryWin = tk.Toplevel()
    queryWin.grab_set()
    tk.Label(queryWin, text="Enter Query").grid(row=0)
    evar = tk.StringVar()
    query = tk.Entry(queryWin, width=150, textvariable=evar).grid(row=1)
    tk.Label(queryWin, text="Enter File path").grid(row=2)
    evar_outf = tk.StringVar()
    query_outf = tk.Entry(queryWin, width=150, textvariable=evar_outf).grid(row=3, pady=5, padx=5)
    Button = tk.Button(queryWin, text="OK", command=queryWin.destroy).grid(row=4, pady=10, padx=5)

    queryWin.wait_window()
    return evar, evar_outf


def main():
    print (os.getcwd())
    root = tk.Tk()
    Window(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
