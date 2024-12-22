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
        self.pack(fill=tk.BOTH, expand=True)
        self.show_widgets()
    
    def show_widgets(self):
        self.master.title("WBIntegrator")
        self.master.geometry("500x500")

        # Label for the Entry widget
        lbl_directory = tk.Label(self, text="Directory name:")
        lbl_directory.pack(pady=(20, 5))  # Top padding for spacing

        # Entry widget for input
        self.evar = tk.StringVar()  # Use instance variable to access later if needed
        self.entry_directory = tk.Entry(self, textvariable=self.evar, width=50)
        self.entry_directory.pack(pady=(0, 20))  # Padding for spacing

        # Button to download images
        button_download_imgs = tk.Button(self, text="Download Images", command=self.images_downloader_handler)
        button_download_imgs.pack(padx=20, pady=10)

        # Button to insert new data
        button_insert_data = tk.Button(self, text="Insert new data", command=self.insertion_handler)
        button_insert_data.pack(padx=20, pady=10)

        # Button to exit the application
        b_quit = tk.Button(self, text="EXIT", command=self.close_window)
        b_quit.pack(padx=20, pady=(10, 50))

    # def show_widgets(self):
    #     self.master.title("WBIntegrator")
    #     self.master.geometry("500x500")

    #     evar = tk.StringVar()
    #     note = tk.Entry(self, width=150, 
    #                 textvariable=evar)

    #     button_download_imgs = tk.Button(self, text="Download Images", command=self.images_downloader_handler)
    #     button_download_imgs.pack(padx=20, pady=30)

    #     button2 = tk.Button(self, text="Insert new data", command=self.insertion_handler)
    #     button2.pack(padx=20, pady=30)

    #     b_quit = tk.Button(self, text="EXIT", command=self.close_window)
    #     b_quit.pack(padx=5, pady=100)

    def insertion_handler(self):
        self.dirname = filedialog.askdirectory()
        if self.dirname == "" or self.dirname == " ":
            messagebox.showerror("Error", "Invalid directory name")
        else:
            manager.work_with_folder(self.dirname)

    def images_downloader_handler(self):
        self.filename = filedialog.askopenfilename(defaultextension="csv")

        self.dirname = self.evar.get()

        if self.dirname == "" or self.dirname == " ":
            messagebox.showerror("Error", "Inavlid directory path")
        else:
            if self.filename == "" or self.filename == " " or not self.filename.endswith(".csv"):
                messagebox.showerror("Error", "Invalid file name")
            else:
                parse_csv_with_images(self.filename, self.dirname)

    def close_window(self):
        self.master.destroy()

def main():
    print (os.getcwd())
    root = tk.Tk()
    Window(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
