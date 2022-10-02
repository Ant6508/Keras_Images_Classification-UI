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

import Main_Menu
import Data_From_Dir_manager
import Keras_Model_Manager
import File_Manager_Tool
import Project_Manager
import Req_Manager

import Model_Manager

from tensorflow import keras
import pandas



class C_I_win(tk.Frame):

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.Current_Csv = pandas.DataFrame({'A' : []})
  

        self.Create_Csv_reader()
        self.Create_Reader_Buttons()
        self.Create_Import_Button()


#Widgets creations

    def Create_Reader_Buttons(self):

        self.add_button_image = tk.PhotoImage(file=File_Manager_Tool.get_active_dir() + r"/images/add_button.png")
        rounded_add_button = tk.Button(self, image=self.add_button_image,command=self.Add_Class)
        rounded_add_button.place(x=355,y=50)

        self.del_button_image = tk.PhotoImage(file=File_Manager_Tool.get_active_dir() + r"/images/del.png")
        rounded_del_button = tk.Button(self, image=self.del_button_image,command=self.Del_Class)
        rounded_del_button.place(x=400,y=50)

    def Create_Csv_reader(self):

        csv_frame = tk.Frame(self,bg="white",width=350,height=400)  
        csv_frame.place(x=25,y=50)

        columns = ('Id', 'Class_Name', 'Images_Ctn','Val_Split')

        self.tree_csv = ttk.Treeview(csv_frame, columns=columns, show='headings')

        self.tree_csv.heading('Id', text='Id')
        self.tree_csv.column("Id", minwidth=0, width=50, stretch=NO)

        self.tree_csv.heading('Class_Name', text='Class Name')
        self.tree_csv.column("Class_Name", minwidth=0, width=100, stretch=NO)

        self.tree_csv.heading('Images_Ctn', text='Image total Count')
        self.tree_csv.column("Images_Ctn", minwidth=0, width=100, stretch=NO)

        self.tree_csv.heading('Val_Split', text='Val Split')
        self.tree_csv.column("Val_Split", minwidth=0, width=50, stretch=NO)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree_csv.yview)
        scrollbar.place(x=327,y=50,height=225)

        self.tree_csv.configure(yscroll=scrollbar.set)
        self.tree_csv.grid(sticky='nsew')

    def Create_Import_Button(self):
        Import_Button = tk.Button(self,text="Import Images",width = 16,command = lambda : Data_From_Dir_manager.Import_Classes_Images(self.Current_Csv, self.controller.shared_data["Project_Dir"] + "/Data"))
        Import_Button.place(x=25,y=280)


#aux fonctions creations

#project functions


    def Load_Csv_File(self,File_Path):

        self.Current_Csv = pandas.read_csv(File_Path)
        self.tree_csv.delete(*self.tree_csv.get_children())

        Lines = []
        for i in range(len(self.Current_Csv)):
            l = self.Current_Csv.loc[i, :].values.tolist()
            Lines.append(l)

        for line in Lines :
            self.tree_csv.insert('', tk.END, values=line)

#classes actions
    def Add_Class(self,Val_Split = 0.2):
        class_path = filedialog.askdirectory(title="Where is your class directory?")

        class_name= class_path.split("/")[-1]

        img_ctn = 0
        for root, dirs, files in os.walk(class_path):
            img_ctn += len(files)
            
        self.Current_Csv.loc[len(self.Current_Csv.index)] = [ len(self.Current_Csv.index),class_name, img_ctn, Val_Split, class_path]
        self.Current_Csv.to_csv(self.controller.shared_data["Project_Dir"] + "/Project_Classes.csv",index=False)
        self.Load_Csv_File(File_Path= self.controller.shared_data["Project_Dir"] + "/Project_Classes.csv")


    def Del_Class(self):
        Selected_Class_Id = self.tree_csv.focus()
        Selected_Class_Id = int(self.tree_csv.item(Selected_Class_Id)["values"][0])
 
        for i in range(Selected_Class_Id+1,len(self.Current_Csv)):
            self.Current_Csv.loc[i] =np.concatenate( ([i-1] , (self.Current_Csv.loc[i])[1:]) ) 

        self.Current_Csv.drop (self.Current_Csv.index[Selected_Class_Id], inplace=True)

        self.Current_Csv.to_csv(self.controller.shared_data["Project_Dir"] + "/Project_Classes.csv",index=False)
        self.Load_Csv_File(File_Path= self.controller.shared_data["Project_Dir"] + "/Project_Classes.csv")


