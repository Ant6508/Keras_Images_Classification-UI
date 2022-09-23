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





class M_M_win(tk.Frame):

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.Create_Model_Viewer()
        self.Create_Model_Buttons()


    def Create_Model_Viewer(self):



        self.Model_frame = tk.Frame(self,bg="white",width=250,height=400)  
        self.Model_frame.place(x=25,y=50)

        columns = ('Id', 'Layer_Name', 'Parameters')

        self.tree_model = ttk.Treeview(self.Model_frame, columns=columns, show='headings')

        self.tree_model.heading('Id', text='Id')
        self.tree_model.column("Id", minwidth=0, width=50, stretch=NO)

        self.tree_model.heading('Layer_Name', text='Layer Name')
        self.tree_model.column("Layer_Name", minwidth=0, width=100, stretch=NO)

        self.tree_model.heading('Parameters', text='Parameters')
        self.tree_model.column("Parameters", minwidth=0, width=100, stretch=NO)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree_model.yview)
        scrollbar.place(x=275,y=50,height=225)

        self.tree_model.configure(yscroll=scrollbar.set)
        self.tree_model.grid(sticky='nsew')


    def Create_Model_Buttons(self):
        Load_Model_Button = tk.Button(self,text="Import a model",command=self.Load_Model)
        Load_Model_Button.place(x=300,y=50)

        Fit_Model_Button = tk.Button(self,text="Fit the model",fg="red",command=self.Fit_Model)
        Fit_Model_Button.place(x=300,y=95)


#model functions
    def Load_Model(self):

        self.Current_Model_Path = filedialog.askdirectory(title="Select the model")

        self.Current_Model = keras.models.load_model(self.Current_Model_Path)

        for i in range(len(self.Current_Model.layers)):
            layer = self.Current_Model.layers[i]
            line =  [i,layer.name,"parametres non dispo"]

            self.tree_model.insert('', tk.END, values=line)

    def Fit_Model(self):


        Train_Data,Val_Data =  Data_From_Dir_manager.Create_Classes_Data(self.Project_Dir,size=400,batch_size=5,Seed=None)
        Keras_Model_Manager.Compile_Model(self.Current_Model)

        acc = Keras_Model_Manager.Fit_Model(self.Current_Model,Train_Data,Val_Data)
        messagebox.showinfo("Information","Your model was successfully trained\nwith the data you provided\nwith an accuracy of {a} %".format(a=round(acc[-1],3)*100 ))

        Project_Name = simpledialog.askstring("Save trained model","Enter the model Name")

        if Project_Name != None:
            self.Current_Model.save(self.Project_Dir + '/Ia_Models/' + Project_Name)