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
import Model_Manager
import Results_Viewer

from tensorflow import keras
import pandas


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)  #stacked frames containers
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.shared_data = {"Project_Dir" : "" ,  "Current_Model" : None}   #shared project data other forms can access

        self.frames = {}

        for F in (  Classes_Importer.C_I_win , Model_Manager.M_M_win , Results_Viewer.R_win):  # forms declaration

            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("C_I_win")
        self.create_menu_bar()
        self.Create_Nav_Bar()

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

        self.shared_data["Project_Dir"] = f"{Project_Dir}/{Project_Name}"

        Project_Manager.Create_Project(Project_Name,Project_Dir)

        Classes_Importer.C_I_win.Load_Csv_File(self.frames["C_I_win"], File_Path = self.shared_data["Project_Dir"] + "/Project_Classes.csv")

    def Load_Project(self):

        self.shared_data["Project_Dir"] = filedialog.askdirectory(title="Where is your project directory?")
        Classes_Importer.C_I_win.Load_Csv_File(self.frames["C_I_win"] ,File_Path = self.shared_data["Project_Dir"] + "/Project_Classes.csv")

    def Create_Nav_Bar(self):

        button1 = ttk.Button(self,text="Import Classes",width = 22,command = lambda : self.show_frame(page_name="C_I_win") )
        button1.place(x=0,y=0)

        button2 = ttk.Button(self,text="Manage Model",width = 22,command = lambda : self.show_frame(page_name="M_M_win") )
        button2.place(x=146,y=0)

        button3 = ttk.Button(self,text="See Results",width = 22,command = lambda : self.show_frame(page_name="R_win") )
        button3.place(x=293,y=0)

if __name__ == "__main__":
    app = Application()
    app.title("Py_Auto_Class")
    app.geometry("440x325")
    app.resizable(width=False, height=False)
    app.mainloop()