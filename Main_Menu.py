"""
Created by : Rongere Julien
Date : Sepctember 2022

Goal : this file initialize the app itself , declares the different forms and creates the menu bar
    It behaves as the main of this while project for the moment
    
"""


#------------Imports begin------------

#GUI imports
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from tkinter import messagebox

import Tools.Data_From_Dir_manager as Data_From_Dir_manager
import Tools.Keras_Model_Manager as Keras_Model_Manager
import Tools.File_Manager_Tool as File_Manager_Tool
import Tools.Project_Manager as Project_Manager
import Model_Manager
import Classes_Importer
import Results_Viewer
import Prediction

from tensorflow import keras
import pandas

#------------Imports end------------

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = self.frames_notebook = ttk.Notebook(self) #creates the notebook that will contain the different forms the user can switch between

        self.shared_data = {"Project_Dir" : "" ,  "Current_Model" : None , "Classes_num" : 0 ,"paramters":{"size":400}}   #shared project data other forms can access

        self.frames = {} #dictionary that will contain the different pairs (form name , form object)

        for F in (  Classes_Importer.C_I_win , Model_Manager.M_M_win , Results_Viewer.R_win,Prediction.Prediction_win):  # forms declaration

            page_name = F.__name__
            frame = F(parent=container, controller=self) #parent : the form container , controller : the app itself
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("C_I_win")
        self.create_menu_bar()
        self.Create_Nav_Bar()

    def show_frame(self, page_name:str):
        #shows the form that is passed as a parameter

        frame = self.frames[page_name]
        frame.tkraise()

#Navigation widgets creation
    def Create_Nav_Bar(self):
        #creates the navigation bar which allows to switch between the different forms

        
        self.frames_notebook.pack(side="top", fill="both", expand=True)

        for frame in self.frames.values():
            name = frame.name

            self.frames_notebook.add(frame, text=name)

    def create_menu_bar(self): #creates the menu bar
        menu_bar = tk.Menu(self)

        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="New", command=self.Setup_Project)
        menu_file.add_command(label="Open", command=self.Load_Project)
        menu_file.add_command(label="Save")
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_options = tk.Menu(menu_bar, tearoff=0)
        menu_options.add_command(label="Data Options")
        menu_bar.add_cascade(label="Datas", menu=menu_options)

 
        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About")
        menu_bar.add_cascade(label="Help",menu=menu_help)

        self.config(menu=menu_bar)


#Project menu bar functions
    def Setup_Project(self):
        #function that creates the project

        Project_Dir = filedialog.askdirectory(title="Where should the project be created ?")

        if Project_Dir == "": #if the user cancels the operation
            return

        Project_Name = simpledialog.askstring("Enter The Project Name","Enter The Project Name")
        if Project_Name == None:
            Project_Name = "My_Project"

        self.shared_data["Project_Dir"] = f"{Project_Dir}/{Project_Name}"

        Project_Manager.Create_Project(Project_Name,Project_Dir)

        Classes_Importer.C_I_win.Load_Csv_File(self.frames["C_I_win"], File_Path = self.shared_data["Project_Dir"] + "/Project_Classes.csv")

        messagebox.showinfo("Project Created","The project has been created")

    def Load_Project(self):
        #function that loads a project
        #the project is loaded by selecting the project directory which contains the project classes file

        ans = self.shared_data["Project_Dir"] = filedialog.askdirectory(title="Where is your project directory?")

        if ans == "": #if the user cancels the operation
            return
        
        try:
            File_Path = self.shared_data["Project_Dir"] + "/Project_Classes.csv"
            Classes_Importer.C_I_win.Load_Csv_File(self.frames["C_I_win"] ,File_Path = File_Path)
            self.shared_data["Classes_num"] = len(pandas.read_csv(File_Path).index)

        except FileNotFoundError:
            messagebox.showerror("Error","The project is not valid")
            return

        messagebox.showinfo("Project Loaded","The project has been loaded")
    

if __name__ == "__main__":
    app = Application()
    app.title("Py_Auto_Class")
    app.geometry("440x350")
    app.resizable(width=False, height=False)
    app.iconbitmap("Images/Icon.ico")
    app.mainloop()