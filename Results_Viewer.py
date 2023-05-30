import os
import queue


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

import Model_Manager

class R_win(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.name = "Fit"

        self.Create_Text_Box()
        self.Create_Buttons()

        # Bind the custom event to a function
        self.bind('<<UpdateText>>', self.update_text)

#Widgets creations

  
    def Create_Text_Box(self):

        self.Txt_Box = tk.Text(self, height=14, width=47,state="disabled") #read-only entry

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

        #create the log file on the project directory
        with open(self.controller.shared_data["Project_Dir"] +  "/temp_log.txt","w") as txt:
            txt.write("This file contains the log of the training of the model\n\n")


        acc = Keras_Model_Manager.Fit_Model(self.controller.shared_data["Current_Model"],Train_Data,Val_Data,CustomCallback(self)) #fit the model , the callback will be used to display the accuracy
        
        self.done_training = True

        messagebox.showinfo("Information",f"Your model was successfully trained\nwith the data you provided\nwith an accuracy of { round(acc[-1],3)*100  } %")

        if self.done_training != True:

            self.Stop_Training()
        return
    
    def save_model(self):
        #saves the model in the project directory
        Model_Name = simpledialog.askstring("Model Name","Enter the name of the model")

        if Model_Name == None:
            Model_Name = "My_Model"

        Model_Name.replace(" ","_")
        self.controller.shared_data["Current_Model"].save(self.controller.shared_data["Project_Dir"] + '/Ia_Models/' + Model_Name)
        shutil.move(self.controller.shared_data["Project_Dir"] + "/temp_log.txt",self.controller.shared_data["Project_Dir"] + '/Ia_Models/' + Model_Name + "/log.txt")
        shutil.move(self.controller.shared_data["Project_Dir"] + "/acc_array.txt",self.controller.shared_data["Project_Dir"] + '/Ia_Models/' + Model_Name + "/data_array.txt")


    def Start_Fitting(self):
        #starts the fitting of the model along with the thread that will display the accuracy

        #ask for the batch size 
        self.batch_size = simpledialog.askinteger("Batch Size","Enter the batch size",minvalue=1,maxvalue=1000)
        if self.batch_size == None:
            self.batch_size = 10

        self.q = queue.Queue()


        self.t2=Thread(target=self.Fit_Model)
        self.t2.start()

        self.update_text()

    def Show_Plot(self):
        #shows the plot of the accuracy and loss of the model

        path = self.controller.shared_data["Project_Dir"] + "/acc_array.txt"

        with open(path,"r") as data_file:
            data = data_file.readlines()
            X,Y = [],[]
            for line in data:
                (x,y) = eval(line)
                X.append(x)
                Y.append(y)

        plt.plot(X,Y,label="Accuracy of the model in function of the epochs")
        plt.show()
        

    def Stop_Training(self):
        #stops the training of the model

        self.done_training = True

        self.controller.shared_data["Current_Model"].stop_training = True
        messagebox.showinfo("Information","Training stopped")

        Thread(target = self.Show_Plot).start()

        self.controller.after(0,self.save_model)

        
        return
      
    def update_text(self,event=None):
        #updates the text box with the accuracy of the model

        try:
            Text = self.q.get_nowait()
        except queue.Empty:
            pass
        else:
            self.Txt_Box.configure(state="normal")
            self.Txt_Box.insert(tk.END,Text)
            self.Txt_Box.see(tk.END)
            self.Txt_Box.update()
            self.Txt_Box.configure(state="disabled")


class CustomCallback(keras.callbacks.Callback):
    #custom callback to display the results of the training
    #also saves the results in a log file

    def __init__(self, parent, *args, **kwargs):
        super(CustomCallback, self).__init__(*args, **kwargs)
        self.parent = parent
        self.queue = parent.q

    def on_train_begin(self, logs=None):

        self.Add_2_Log("Training has begun...\n\n\n")

        self.X = [] # batch abscissas
        self.Y = [] # accuracy ordinates

        self.current_batch = 0

    def on_train_end(self, logs=None):

        self.Add_2_Log("\n\n\nTraining has ended")


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

        with open(self.parent.controller.shared_data["Project_Dir"] +  "/temp_log.txt","a") as txt:
            txt.write(text)


        self.queue.put(text)

        # Generate a custom event to tell the GUI to update which is triggered by the callback.
        self.parent.event_generate('<<UpdateText>>', when='tail')



    def Add_2_Array_File(self,acc):
        #add the accuracy to the array
     
        with open(self.parent.controller.shared_data["Project_Dir"] + "/acc_array.txt","a") as txt:
            
            txt.write(f"{(self.current_batch,acc)}\n") 