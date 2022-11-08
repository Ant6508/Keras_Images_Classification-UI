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
import tkinter.font as tkfont
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
        self.child_win.geometry("350x180")

    
        self.Add_Layer_Label= ttk.Label(self.child_win,text="Select the layer to add")
        self.Add_Layer_Label.place(x=120,y=25)


        layers_list = [layer for layer in keras.layers.__dict__.keys() if inspect.isclass(eval(f"keras.layers.{layer}"))]

        self.Layer_Combobox = ttk.Combobox(self.child_win,values=sorted(layers_list) , state="readonly",width=30)
        self.Layer_Combobox.place(x=80,y=45)
        self.Layer_Combobox.bind("<<ComboboxSelected>>", self.Move_Widgets)

        self.Add_Button = tk.Button(self.child_win,text="Add this layer",command= lambda : self.Add_Layer())
        self.Add_Button.place(x=140,y=75)

        self.New_Arg_Button = tk.Button(self.child_win,text="Add this parameter",command= lambda : self.New_Param() , state ="disabled")
        self.New_Arg_Button.place(x=25,y=125)

        self.Arg_Combobox = ttk.Combobox(self.child_win,values=[""] , state="disabled",width=25)
        self.Arg_Combobox.place(x=150,y=125)


        self.child_win.mainloop()



    def Inc_height(self,n): # incrase the windows size by n
        h = int(self.child_win.geometry().split("+")[0].split("x")[1]) + n
        h = str(h)

        self.child_win.geometry(f"350x{h}")
        self.child_win.update()


    def New_Param(self):
        param = self.Arg_Combobox.get() #current selected param
        if param =="":
            return
        n =len(self.arg_list)
        y_curr = 150 + 30 * (n+1)


        self.Wid_Dict[param] = [Label(self.child_win, text=param+" : ", fg='blue')]
        self.Wid_Dict[param][0].place(x=25,y=y_curr)

        x_txt = 25 + len(param) * 7

        self.Wid_Dict[param].append(tk.Text(self.child_win, height=1, width=15))
        self.Wid_Dict[param][1].place(x=x_txt,y=y_curr)                    

        self.arg_list.append(param)


        self.Inc_height(30)
        self.Arg_Combobox["values"] = tuple(item for item in self.Arg_Combobox["values"] if item != param) # deletes the added param from the combobox
        self.Arg_Combobox.set("")


        #button that deletes the widgets associated to the param (including himself)
  
        self.Wid_Dict[param].append(tk.Button(self.child_win,text="Del", command= lambda :self.Delete_param_widgets(param)))
        self.Wid_Dict[param][2].place(x=250,y=y_curr)                    

    def Delete_param_widgets(self,param):

        if self.Arg_Combobox["values"] =="":
            self.Arg_Combobox["values"] = (param,)
        else:
            self.Arg_Combobox["values"] += (param,) #put back the parameters in the combobox
        

        for param_widgets in self.Wid_Dict:
            if self.Wid_Dict[param_widgets][0].winfo_rooty() > self.Wid_Dict[param][0].winfo_rooty()  :
                for wid in self.Wid_Dict[param_widgets]:
                    x,y =  self.get_pos(wid)
                    wid.place(x=x,y=y -30)



        for wid in self.Wid_Dict[param]:
            wid.destroy() #deletes all the widgets associated with the parameter

        self.arg_list.remove(param) #deletes the parameters from the used ones list
        del self.Wid_Dict[param] #same but for widgets dictionnary

        self.Inc_height(-30) #resizes the window
        self.child_win.update()


    def Move_Widgets(self,*args):

  
        self.New_Arg_Button["state"] = "normal"
        self.Arg_Combobox["state"]= "normal"
        self.Arg_Combobox["values"] = []

        try:
            for arg in self.Wid_Dict.values():
                for wid in arg:
                    wid.destroy()
                self.Inc_height(-30)
                self.Arg_Combobox.set('')
        except AttributeError:
            print("vide")

        self.arg_list = []
        y_curr = 150
 
        l = eval(f"layers.{self.Layer_Combobox.get()}")

        self.Wid_Dict = {}
  
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

                    self.Wid_Dict[arg]= [tk.Label(self.child_win,text=arg, fg="red")]
                    self.Wid_Dict[arg][0].place(x=25,y=y_curr)  

                    x_txt = 25 + len(arg) * 8

                    self.Wid_Dict[arg].append(tk.Text(self.child_win, height = 1, width = 15))
                    self.Wid_Dict[arg][1].place(x=x_txt,y=y_curr) 
                    
                    self.arg_list.append(arg)

        self.Arg_Combobox["values"] = self.Arg_Combobox["values"][1:]


    def Add_Layer(self,im_size=400,*args):

        layer = self.Layer_Combobox.get() #current selected layer
        print(layer)

        if self.controller.shared_data["Current_Model"] == None:

            self.controller.shared_data["Current_Model"] = keras.Sequential([layers.Rescaling(1./255,input_shape = (im_size,im_size,1))])

            self.Add_Layer(self,im_size)

        else :

            l = f"layers.{layer}("
            for arg in self.arg_list:
                ans = self.Wid_Dict[arg][1].get(1.0, 'end-1c')

                l += f"{arg} = {ans},"
                
                if self.arg_list.index(arg) == len(self.arg_list) -1: # if its the last arg
                    l = l.rstrip(l[-1]) #removes last ","
            l += ")"

            self.controller.shared_data["Current_Model"].add(eval(l))
            print(self.controller.shared_data["Current_Model"].layers)

            layer = eval(l)
            line =  [len(self.controller.shared_data["Current_Model"].layers),layer.name,"parametres non dispo"]

            self.tree_model.insert('', tk.END, values=line)

            self.child_win.destroy()

    def get_pos(self,widget):
        return widget.winfo_rootx()-self.child_win.winfo_rootx(),widget.winfo_rooty()-self.child_win.winfo_rooty()