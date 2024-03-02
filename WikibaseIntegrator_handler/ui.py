import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import manager
import os

class Window(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.show_widgets()

    def show_widgets(self):
        self.master.title("WikibaseIntegratorDataHandler_v2.0.0")
        self.master.geometry("500x500")
        button2 = tk.Button(self, text="Insert new data", command=self.insertion_handler)
        button2.pack(padx=20, pady=30)
        b_quit = tk.Button(self, text="EXIT", command=self.close_window)
        b_quit.pack(padx=5, pady=100)

    def insertion_handler(self):
        self.dirname = filedialog.askdirectory()
        if self.dirname == "" or self.dirname == " ":
            messagebox.showerror("Error", "Invalid directory name")
        else:
            manager.work_with_folder(self.dirname)

    def close_window(self):
        self.master.destroy()



def main():
    print (os.getcwd())
    root = tk.Tk()
    Window(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
