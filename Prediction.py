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

import Main_Menu
import Tools.Data_From_Dir_manager as Data_From_Dir_manager
import Tools.Keras_Model_Manager as Keras_Model_Manager
import Tools.File_Manager_Tool as File_Manager_Tool
import Tools.Project_Manager as Project_Manager
import Tools.Req_Manager as Req_Manager
import Model_Manager

from tensorflow import keras
from PIL import ImageTk, Image

#------------Imports end------------
class Prediction_win(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.name ="Predictions"

        self.y_pred_label = tk.Label(self,text = "Predicted Class : \n",font=("Helvetica", 10))
        self.y_pred_label.place(x=310,y=80)
        self.y_class_label = tk.Label(self,text = "Predicted Class : \n",font=("Helvetica", 10))
        self.y_class_label.place(x=310,y=120)

        self.create_image_reader()
        self.Create_Buttons()
        
#widgets creations
    def Create_Buttons(self):
        #this function creates the buttons that allow the user to open an image and predict its class

        self.Predict_Button = tk.Button(self,text = "Predict",command = self.Predict,font=("Helvetica", 10))
        self.Predict_Button.place(x=310,y=40)

        self.Open_Image_Button = tk.Button(self,text = "Open Image",command = self.open_image)
        self.Open_Image_Button.place(x=180,y=15)

        self.sort_filder_button = tk.Button(self,text = "Sort Folder",command = self.sort_folder)
        self.sort_filder_button.place(x=310,y=180)

    def create_image_reader(self):
        #this function creates the frame where the image will be displayed

        self.image_reader = tk.Frame(self,bg="white",width=250,height=250)
        self.image_reader.place(x=50,y=60)

    def open_image(self):
        #this function opens the image that the user wants to predict

        image_path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.image = Image.open(image_path)
        resized_image = self.image.resize((250,250),  Image.ANTIALIAS)
        self.image_object = ImageTk.PhotoImage(resized_image)
        self.image_label = tk.Label(self.image_reader,image = self.image_object)
        self.image_label.place(x=0,y=0)

    def Predict(self):
        #this function predicts the class of the image and displays the result 

        model = self.controller.shared_data["Current_Model"]

        self.image = self.image.resize(model.input_shape[1:3],  Image.ANTIALIAS)
        photoimage = ImageTk.PhotoImage(self.image)

        y_pred = model.predict(self.image)
        y_class = np.argmax(y_pred,axis=1)

        self.y_pred_label.config(text = "Probability : \n" + str(y_pred))
        self.y_class_label.config(text = "Predicted Class : \n" + str(y_class))

    def sort_folder(self):
        #this function sorts the images in a folder according to their predicted class

        folder_path = filedialog.askdirectory(initialdir = "/",title = "Select folder")
        model = self.controller.shared_data["Current_Model"]

        Data_From_Dir_manager.sort_folder(folder_path,model)