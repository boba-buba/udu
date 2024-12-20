import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import manager
import os
from csv_parser import parse_csv_with_images

class Window(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.show_widgets()

    def show_widgets(self):
        self.master.title("WBIntegrator")
        self.master.geometry("500x500")
        button_download_imgs = tk.Button(self, text="Download Images", command=self.images_downloader_handler)
        button_download_imgs.pack(padx=20, pady=30)

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

    def images_downloader_handler(self, directory_path: str):
        self.filename = filedialog.askopenfile(defaultextension="csv")
        if self.filename == "" or self.filename == " ":
            messagebox.showerror("Error", "Invalid file name")
        else:
            parse_csv_with_images(self.filename)

    def close_window(self):
        self.master.destroy()



def main():
    print (os.getcwd())
    root = tk.Tk()
    Window(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
