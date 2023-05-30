"""
Coded by: RONGERE Julien
This file creates the prediction window which allows the user to predict the classes of the images in a directory once the model has been trained

"""

#------------Imports begin------------

#GUI imports
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from tkinter import messagebox

import numpy as np


import Tools.Data_From_Dir_manager as Data_From_Dir_manager

from tensorflow import keras
from PIL import ImageTk, Image,ImageOps

#------------Imports end------------
class Prediction_win(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.name ="Predictions"

        self.Widgets_Dict = {}

        self.y_pred_label = tk.Label(self,text = "Predicted Class : \n",font=("Helvetica", 10))
        self.y_pred_label.place(x=310,y=80)
        self.y_class_label = tk.Label(self,text = "Predicted Class : \n",font=("Helvetica", 10))
        self.y_class_label.place(x=310,y=120)

        self.image = None 
        self.create_image_reader()
        self.Create_Buttons()
        
#widgets creations
    def Create_Buttons(self):
        #this function creates the buttons that allow the user to open an image and predict its class

        Predict_Button = tk.Button(self,text = "Predict",command = self.Predict,font=("Helvetica", 10))
        Predict_Button.place(x=310,y=40)
        self.Widgets_Dict["Predict_Button"] = Predict_Button


        Open_Image_Button = tk.Button(self,text = "Open Image",command = self.open_image)
        Open_Image_Button.place(x=180,y=15)
        self.Widgets_Dict["Open_Image_Button"] = Open_Image_Button
        

        sort_filder_button = tk.Button(self,text = "Sort Folder",command = self.sort_folder)
        sort_filder_button.place(x=310,y=180)
        self.Widgets_Dict["sort_filder_button"] = sort_filder_button


    def create_image_reader(self):
        #this function creates the frame where the image will be displayed

        image_reader = tk.Frame(self,bg="white",width=250,height=250)
        image_reader.place(x=50,y=60)
        self.Widgets_Dict["image_reader"] = image_reader


#widgets creations end


#functions
    def open_image(self):
        #this function opens the image that the user wants to predict

        image_path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.image = Image.open(image_path)
        self.image = ImageOps.grayscale(self.image) #convert the image to grayscale
        resized_image = self.image.resize((250,250),  Image.ANTIALIAS)
        self.image_object = ImageTk.PhotoImage(resized_image)
        self.image_label = tk.Label(self.image_reader,image = self.image_object)
        self.image_label.place(x=0,y=0)

        self.y_class_label.config(text = "Predicted Class : \n")
        self.y_pred_label.config(text = "Probability : \n")
        

    def Predict(self):
        #this function predicts the class of the image and displays the result 

        model = self.controller.shared_data["Current_Model"]

        if self.image == None:
            return

        self.image = self.image.resize((model.input_shape[1],model.input_shape[2]),  Image.ANTIALIAS) #resize the image to the input shape of the model
    
        modified_image = np.array(self.image)
        modified_image = np.expand_dims(modified_image, axis=0) #add a dimension to the image to make it a batch of 1 image


        y_pred = model.predict(modified_image).round(2)
        y_class = np.argmax(y_pred,axis=1)

        self.y_pred_label.config(text = "Probability : \n" + str(y_pred))
        self.y_class_label.config(text = "Predicted Class : \n" + str(y_class))

    def sort_folder(self):
        #this function sorts the images in a folder according to their predicted class

        folder_path = filedialog.askdirectory(initialdir = "/",title = "Select folder")
        model = self.controller.shared_data["Current_Model"]

        Data_From_Dir_manager.sort_folder(folder_path,model)