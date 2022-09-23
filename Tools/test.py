import os

def get_active_dir():
    path = os.getcwd()
    path = path.replace("\\","/")
    return path

import sys
sys.path.insert(1, get_active_dir() + '/Tools')

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from tkinter import messagebox
import numpy as np

import Data_From_Dir_manager
import Keras_Model_Manager
import File_Manager_Tool
import Project_Manager
import Req_Manager

import Classes_Importer

from tensorflow import keras
import pandas


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Classes_Importer.win , Classes_Importer.win):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("win")

        self.create_menu_bar()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)

        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="New", command=self.Setup_Project)
        menu_file.add_command(label="Open", command=self.Load_Project)
        menu_file.add_command(label="Save")
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About")
        menu_bar.add_cascade(label="Help",menu=menu_help)

        self.config(menu=menu_bar)

#Project menu bar functions
    def Setup_Project(self):

        Project_Dir = filedialog.askdirectory(title="Where should the project be created ?")

        Project_Name = simpledialog.askstring("Enter The Project Name","Enter The Project Name")

        Project_Manager.Create_Project(Project_Name,Project_Dir)

        self.Project_Dir = Project_Dir +"/"+Project_Name
        self.Load_Csv_File(File_Path = self.Project_Dir + "/Project_Classes.csv")


    def Load_Project(self):

        self.Project_Dir = filedialog.askdirectory(title="Where is your project directory?")
        self.Load_Csv_File(File_Path = self.Project_Dir + "/Project_Classes.csv")






       

if __name__ == "__main__":
    app = Application()
    app.title("Py_Auto_Class")
    app.geometry("900x325")
    app.resizable(width=False, height=False)
    app.mainloop()