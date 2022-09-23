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

from subprocess import run
import numpy as np
from tensorflow import keras
import pandas

import Data_From_Dir_manager
import Keras_Model_Manager
import File_Manager_Tool
import Project_Manager
import Req_Manager

import Model_Manager







class R_win(tk.Frame):

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.Create_Text_Box()



    def Create_Text_Box(self):

        self.Txt_Box = tk.Text(self, height=14, width=48)

        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.Txt_Box.yview)
        self.Txt_Box.configure(yscrollcommand=self.vsb.set)

        self.Txt_Box.place(x=25 , y=50 )
        self.vsb.place(x=400,y=50 , height = 225)
#Widgets creations

  

#aux fonctions creations

#project functions
