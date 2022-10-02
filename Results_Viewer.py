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

from tensorflow import keras
import threading
from threading import Thread
import pandas
import time

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
        print(parent,self.controller)

        self.Create_Text_Box()
        self.Create_Buttons()


#Widgets creations

  
    def Create_Text_Box(self):

        self.Txt_Box = tk.Text(self, height=14, width=47)

        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.Txt_Box.yview)
        self.Txt_Box.configure(yscrollcommand=self.vsb.set)

        self.Txt_Box.place(x=25 , y=50 )
        self.vsb.place(x=407,y=50 , height = 227)


    def Create_Buttons(self):


        Fit_Model_Button = tk.Button(self,text="Fit the model",fg="red",command= self.Start_Fitting)
        Fit_Model_Button.place(x=25,y=280)


#aux fonctions creations

    def Fit_Model(self):


            Train_Data,Val_Data =  Data_From_Dir_manager.Create_Classes_Data(self.controller.shared_data["Project_Dir"],size=400,batch_size=3,Seed=None)
            Keras_Model_Manager.Compile_Model(self.controller.shared_data["Current_Model"])


            acc = Keras_Model_Manager.Fit_Model(self.controller.shared_data["Current_Model"],Train_Data,Val_Data,CustomCallback())


            messagebox.showinfo("Information",f"Your model was successfully trained\nwith the data you provided\nwith an accuracy of { round(acc[-1],3)*100  } %")

            Model_Name = simpledialog.askstring("Save trained model","Enter the model Name")

            if Project_Name != None:
                self.controller.shared_data["Current_Model"].save(self.controller.shared_data["Project_Dir"] + '/Ia_Models/' + Model_Name)


    def Start_Fitting(self):

        t1=Thread(target=self.Display_Results)
        t1.start()

        t2=Thread(target=self.Fit_Model)
        t2.start()

    def Display_Results(self):

        boo = True
        while boo:
            self.Txt_Box.delete(1.0,END)
            with open("temp_log.txt",'r') as txt : 

                for line in txt.readlines():
                    self.Txt_Box.insert("end",line)

            self.Txt_Box.see(END)
            time.sleep(1)




class CustomCallback(keras.callbacks.Callback):


    def on_train_begin(self, logs=None):

        self.Add_2_Log("Training has begun...\n\n\n")

    def on_train_end(self, logs=None):

        self.Add_2_Log("Training has ended")

    def on_epoch_begin(self, epoch, logs=None):

        self.Add_2_Log(f"Epoch {epoch} has begun\n\n")

    def on_epoch_end(self, epoch, logs=None):
        pass

    def on_train_batch_begin(self, batch, logs=None):
        pass

    def on_train_batch_end(self, batch, logs=None):

        acc = round(logs["accuracy"],3)
        loss =round(logs["loss"],3)

        self.Add_2_Log(f"After batch {batch} , accuracy: {acc}, loss: {loss}\n")

    def Add_2_Log(self,text):

        with open("temp_log.txt","a") as txt:

            txt.write(text)
