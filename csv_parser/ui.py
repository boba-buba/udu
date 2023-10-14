import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import manager
import os
import manager

class Window(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.show_widgets()

    def show_widgets(self):
        self.master.title("ImageExtractor")
        self.master.geometry("500x500")
        button1= tk.Button(self, text="Query", command=self.query_handler)
        button1.pack(padx=20, pady=30)
        button2 = tk.Button(self, text="Insert new data", command=self.insertion_handler)
        button2.pack(padx=20, pady=30)
        b_quit = tk.Button(self, text="EXIT", command=self.close_window)
        b_quit.pack(padx=5, pady=100)

    def query_handler():
        query, dump_file = queryScrollBar()
        manager.work_with_quering()

    def insertion_handler(self):
        self.dirname = filedialog.askdirectory()
        if self.dirname == "" or self.dirname == " ":
            messagebox.showerror("Error", "Invalid directory name")
        else:
            manager.work_with_folder()



    '''
    def work_with_dir(self):
        language = Language()
        self.continue_with_dir(language.get())

    def continue_with_dir(self, lang):
        self.dirname = filedialog.askdirectory()
        if self.dirname == "" or self.dirname == " ":
            messagebox.showerror("Error", "Invalid directory name")
        else:
            names, metadata = JournalMetadataScrollBar(self.dirname)
            metadata_parsed = self.read_metadata(metadata)
            manager2.work_with_folder(names, metadata_parsed, lang)
            self.open_save_win()

    def read_metadata(self, metadata):
        metadata_read = []
        for i in range(len(metadata)):
            metadata_read.append(metadata[i].get())
        return metadata_read

    def work_with_link(self):
        language = Language()
        self.continue_with_link(language.get())

    def continue_with_link(self, lang):
        link_entry = Link()
        link = link_entry.get()
        if link == "" or link == " ":
            messagebox.showerror("Error", "Invalid link")
        else:
            manager2.work_with_link(link, lang)
            self.open_save_win()   

    def open_save_win(self):
        save_win = tk.Toplevel(self.master)
        save_win.grab_set()
        SaveWindow(save_win)
    '''
    def close_window(self):
        self.master.destroy()
    

def queryScrollBar():
    queryWindow = tk.Toplevel()
    queryWindow.geometry("500x500")
    queryWindow.grab_set()

    main_frame = tk.Frame(queryWindow)
    main_frame.pack(fill=tk.BOTH, expand=1)
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    my_canvas.configure(yscrollcommand=my_scrollbar)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    second_frame = tk.Frame(my_canvas)
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")


    tk.Label(second_frame, text ="Settings Window").grid(row=0)
    query = ""
    file_name = ""
    l = tk.Label(second_frame, text=entry).grid(row=i, column=0)
    evar = tk.StringVar()
    note = tk.Entry(second_frame, width=30, 
                            textvariable=evar).grid(row=i,column=1,padx=5,pady=5)
    '''for i, entry in enumerate(entries):
        if is_csv(entry):
            l = tk.Label(second_frame, text=entry).grid(row=i, column=0)
            evar = tk.StringVar()
            note = tk.Entry(second_frame, width=30, 
                            textvariable=evar).grid(row=i,column=1,padx=5,pady=5)
            metadata.append(evar)
            names.append(dir_name+"/"+entry)
            count += 1'''

    Button = tk.Button(second_frame, text ="Submit Data", 
                       command = queryWindow.destroy).grid(row=2)


def is_csv(file_name):
    if file_name.endswith('.pdf'):
        return True
    else:
        return False

def main():
    print (os.getcwd())
    root = tk.Tk()
    Window(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
