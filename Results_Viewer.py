import os

def get_active_dir():
    path = os.getcwd()
    path = path.replace("\\","/")
    return path

import sys
sys.path.insert(1, get_active_dir() + '/Tools')

import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

from tensorflow import keras
from threading import Thread
import time
import shutil
import matplotlib.pyplot as plt

import Tools.Data_From_Dir_manager as Data_From_Dir_manager
import Tools.Keras_Model_Manager as Keras_Model_Manager
import Tools.File_Manager_Tool as File_Manager_Tool
import Tools.Project_Manager  as Project_Manager
import Tools.Req_Manager  as Req_Manager

import Model_Manager

class R_win(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.name = "Fit"

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
        #creates the buttons that will be used in the form


        Fit_Model_Button = tk.Button(self,text="Fit the model",fg="red",command=self.Start_Fitting)
        Fit_Model_Button.place(x=25,y=280)

        Stop_training_Button = tk.Button(self,text="Stop training",fg="red",command=self.Stop_Training)
        Stop_training_Button.place(x=200,y=280)


#aux fonctions creations

    def Fit_Model(self):
        # Fits the model while displaying the accuracy to the user
        #also saves the model in the project directory as well as the log file
  
        self.done_training = False

        if self.controller.shared_data["Current_Model"] == None or self.controller.shared_data["Current_Model"].built == False:
            messagebox.showerror("Error","You need to create and train a model first")
            return
        
        #check if the data folder contains images
        if len(os.listdir(self.controller.shared_data["Project_Dir"] + "/Data/Training")) == 0  :
            messagebox.showerror("Error","You need to add images to the training folder")
            return
        elif len(os.listdir(self.controller.shared_data["Project_Dir"] + "/Data/Validation")) == 0  :
            messagebox.showerror("Error","You need to add images to the validation folder")
            return
        



        Train_Data,Val_Data =  Data_From_Dir_manager.Create_Classes_Data(self.controller.shared_data["Project_Dir"],batch_size=self.batch_size,Seed=None)
        Keras_Model_Manager.Compile_Model(self.controller.shared_data["Current_Model"])


        acc = Keras_Model_Manager.Fit_Model(self.controller.shared_data["Current_Model"],Train_Data,Val_Data,CustomCallback()) #fit the model
        
        self.done_training = True

        messagebox.showinfo("Information",f"Your model was successfully trained\nwith the data you provided\nwith an accuracy of { round(acc[-1],3)*100  } %")

        self.controller.after(0,self.save_model)

        Thread(target = self.Show_Plot).start()

        return
    
    def save_model(self):
        #saves the model in the project directory
        Model_Name = simpledialog.askstring("Model Name","Enter the name of the model")

        if Model_Name == None:
            Model_Name = "My_Model"

        Model_Name.replace(" ","_")
        self.controller.shared_data["Current_Model"].save(self.controller.shared_data["Project_Dir"] + '/Ia_Models/' + Model_Name)
        shutil.move("temp_log.txt",self.controller.shared_data["Project_Dir"] + '/Ia_Models/' + Model_Name + "/log.txt")
        shutil.move("acc_array.txt",self.controller.shared_data["Project_Dir"] + '/Ia_Models/' + Model_Name + "/data_array.txt")


    def Start_Fitting(self):

        with open("temp_log.txt","w") as txt: #clear the log file
            txt.write("")

        #ask for the batch size 
        self.batch_size = simpledialog.askinteger("Batch Size","Enter the batch size",minvalue=1,maxvalue=1000)

        self.t2=Thread(target=self.Fit_Model)
        self.t2.start()

        self.t1=Thread(target=self.Display_Results)
        self.t1.start()

    def Display_Results(self):
        #displays the results of the training in the text box

        while not self.done_training:
            self.Txt_Box.delete(1.0,END)
            with open("temp_log.txt",'r') as txt : 

                for line in txt.readlines():
                    self.Txt_Box.insert("end",line)    

            self.Txt_Box.see(END)
            time.sleep(1)
        return

    def Show_Plot(self):
        #shows the plot of the accuracy and loss of the model

        data_file = open("acc_array.txt","r")
        data = data_file.readlines()
        X,Y = [],[]
        for line in data:
            (x,y) = eval(line)
            X.append(x)
            Y.append(y)
        plt.plot(X,Y)
        plt.show()

    def Stop_Training(self):
        #stops the training of the model

        self.done_training = True

        self.controller.shared_data["Current_Model"].stop_training = True
        messagebox.showinfo("Information","Training stopped")

        self.controller.after(0,self.save_model)

        Thread(target = self.Show_Plot).start()

        return
        

class CustomCallback(keras.callbacks.Callback):
    #custom callback to display the results of the training
    #also saves the results in a log file


    def on_train_begin(self, logs=None):

        self.Add_2_Log("Training has begun...\n\n\n")

        self.X = [] # batch abscissas
        self.Y = [] # accuracy ordinates

        self.current_batch = 0

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

        self.current_batch +=1
        self.Add_2_Array_File(acc)

        self.X.append(self.current_batch)
        self.Y.append(acc)

    def Add_2_Log(self,text):
        #add the text to log file

        with open("temp_log.txt","a") as txt:

            txt.write(text)

    def Add_2_Array_File(self,acc):
        #add the accuracy to the array
     
        with open("acc_array.txt","a") as txt:
            
            txt.write(f"{(self.current_batch,acc)}\n") 