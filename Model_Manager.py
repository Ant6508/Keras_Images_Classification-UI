import os

def get_active_dir():
    path = os.getcwd()
    path = path.replace("\\","/")
    return path

import sys
sys.path.insert(1, get_active_dir() + '/Tools')

import tkinter as tk
import tkinter as ttk
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
import Results_Viewer
import Classes_Importer

from tensorflow import keras
import pandas
import time
import keras
from keras import layers
import inspect



class M_M_win(tk.Frame):

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.Create_Model_Viewer()
        self.Create_Model_Buttons()
        self.test= "test"


    def Create_Model_Viewer(self):



        self.Model_frame = tk.Frame(self,bg="white",width=250,height=400)  
        self.Model_frame.place(x=25,y=50)

        columns = ('Id', 'Layer_Name', 'Parameters')

        self.tree_model = ttk.Treeview(self.Model_frame, columns=columns, show='headings')

        self.tree_model.heading('Id', text='Id')
        self.tree_model.column("Id", minwidth=0, width=20, stretch=NO)

        self.tree_model.heading('Layer_Name', text='Layer Name')
        self.tree_model.column("Layer_Name", minwidth=0, width=100, stretch=NO)

        self.tree_model.heading('Parameters', text='Parameters')
        self.tree_model.column("Parameters", minwidth=0, width=130, stretch=NO)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree_model.yview)
        scrollbar.place(x=275,y=50,height=225)

        self.tree_model.configure(yscroll=scrollbar.set)
        self.tree_model.grid(sticky='nsew')


    def Create_Model_Buttons(self):
        Load_Model_Button = tk.Button(self,text="Import a model",command=self.Load_Model)
        Load_Model_Button.place(x=320,y=50)

        Add_Layer_Button = tk.Button(self,text="Add a layer",command =self.Add_Layer_win)
        Add_Layer_Button.place(x=320,y=80)

#model functions
    def Load_Model(self):

        self.Model_Path = filedialog.askdirectory(title="Select the model")

        self.controller.shared_data["Current_Model"] = keras.models.load_model(self.Model_Path)

        for i in range(len(self.controller.shared_data["Current_Model"].layers)):
            layer = self.controller.shared_data["Current_Model"].layers[i]
            line =  [i,layer.name,"parametres non dispo"]

            self.tree_model.insert('', tk.END, values=line)


    def Add_Layer_win(self):


        self.child_win = Toplevel(self)
        self.child_win.title("Add a layer to the current model")
        self.child_win.geometry("290x180")

        
        self.Add_Layer_Label= ttk.Label(self.child_win,text="Select the layer to add")
        self.Add_Layer_Label.place(x=90,y=25)

        self.Layer_Combobox = ttk.Combobox(self.child_win,values=["Conv2D","MaxPooling2D","Dense","Flatten"] , state="readonly")
        self.Layer_Combobox.place(x=90,y=45)
        self.Layer_Combobox.bind("<<ComboboxSelected>>", self.Move_Widgets)

        self.Add_Button = tk.Button(self.child_win,text="Add this layer",command= lambda : self.Add_Layer())
        self.Add_Button.place(x=90,y=70)

        self.New_Arg_Button = tk.Button(self.child_win,text="Add a parameter",command= lambda : self.New_Param() , state ="disabled")
        self.New_Arg_Button.place(x=25,y=125)

        self.Arg_Combobox = ttk.Combobox(self.child_win,values=[""] , state="disabled")
        self.Arg_Combobox.place(x=135,y=125)


        self.child_win.mainloop()



    def Inc_height(self,n): # incrase the windows size by n
        h = int(self.child_win.geometry().split("+")[0].split("x")[1]) + n
        h = str(h)

        self.child_win.geometry(f"290x{h}")
        self.child_win.update()


    def New_Param(self):
        param = self.Arg_Combobox.get() #current selected param
        print(param)

        n =len(self.arg_list)
        y_curr = 150 + 30 * (n+1)

        exec(f"self.{param}_label = tk.Label(self.child_win, text='{param}:', fg='blue')") # #create and place label of text "param"
        exec(f"self.{param}_label.place(x=25,y={y_curr})")

        x_txt = str(25 + len(param) * 8)

        exec(f"self.{param}_textbox = tk.Text(self.child_win, height = 1, width = 15)")
        exec(f"self.{param}_textbox.place(x={x_txt},y={y_curr})")
                    
        self.arg_list.append(param)

        print(self.arg_list)
        self.Inc_height(30)
        self.Arg_Combobox["values"] = tuple(item for item in self.Arg_Combobox["values"] if item != param) # deletes the added param from the combobox
        self.Arg_Combobox.set(self.Arg_Combobox["values"][0])


        #button that deletes the widgets associated to the param (including himself)
        exec(f"self.{param}_button = tk.Button(self.child_win,text='Del',command=print('test'))")
        exec(f"self.{param}_button.place(x=250,y={y_curr})")
        
    def Delete_param_widgets(self,param):
        print("tesetzzf")
        exec(f"self.{param}_textbox.detroy()")
        exec(f"self.{param}_label.destroy()")
        exec(f"self.{param}_button.detroy()")
        self.Arg_Combobox["values"] += (param,)
        self.arg_list.remove(param)
        self.Inc_height(-30)
        self.child_win.update()


    def Move_Widgets(self,*args):

  
        self.New_Arg_Button["state"] = "normal"
        self.Arg_Combobox["state"]= "readonly"
        self.Arg_Combobox["values"] = []


        self.arg_list = []
        y_curr = 150
 
        l = eval(f"layers.{self.Layer_Combobox.get()}")
  
        for arg in list(inspect.signature(l).parameters.keys()) : # iterates throught all the keras layer arguments

                if self.Arg_Combobox["values"] == "":
                    
                    self.Arg_Combobox["values"] = ("init") #we must initiate 

                t = str(inspect.signature(l).parameters[arg])

                if t.count("=") > 0: # if the argument is not mandatory : break
                    
                    self.Arg_Combobox["values"] += (arg,)

                elif arg == "kwargs": continue


                else : 
                    y_curr +=30
                    self.Inc_height(30) # increase the window's height by 50

                    exec(f"self.{arg}_label = tk.Label(self.child_win, text='{arg}:', fg='red')") # #create and place label of text "arg"
                    exec(f"self.{arg}_label.place(x=25,y={y_curr})")

                    x_txt = str(25 + len(arg) * 8)

                    exec(f"self.{arg}_textbox = tk.Text(self.child_win, height = 1, width = 15)")
                    exec(f"self.{arg}_textbox.place(x={x_txt},y={y_curr})")
                    
                    self.arg_list.append(arg)

        self.Arg_Combobox["values"] = self.Arg_Combobox["values"][1:]


    def Add_Layer(self,activation_func="relu",im_size=400,*args):

        layer = self.Layer_Combobox.get() #current selected layer 

        if self.controller.shared_data["Current_Model"] == None:

            self.controller.shared_data["Current_Model"] = keras.Sequential([layers.Rescaling(1.255,input_shape = (im_size,im_size,1))])

            self.Add_Layer(self,activation_func,im_size)

        else :

            l = f"layers.{layer}("
            for arg in self.arg_list:

                ans = eval(f"self.{arg}_textbox.get(1.0, 'end-1c')") # ans = textbox input related to the arg

                l += f"{arg} = {ans},"
                
                if self.arg_list.index(arg) == len(self.arg_list) -1: # if its the last arg
                    l = l.rstrip(l[-1]) #removes last ","


            l += ")"

            self.controller.shared_data["Current_Model"].add(eval(l))
            print(self.controller.shared_data["Current_Model"].layers)
