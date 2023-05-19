import os

def get_active_dir():
    path = os.getcwd()
    path = path.replace("\\","/")
    return path

import sys
sys.path.insert(1, get_active_dir() + '/Tools')

import tkinter as tk
import tkinter as ttk
import tkinter.font as tkfont
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from tkinter import messagebox
import numpy as np

import Tools.Keras_Model_Manager as Keras_Model_Manager
import Tools.File_Manager_Tool as File_Manager_Tool
import Tools.Project_Manager as Project_Manager
import Tools.Req_Manager as Req_Manager

from tensorflow import keras
import pandas
import time
import keras
from keras import layers
from keras.layers import *
import inspect

class M_M_win(tk.Frame):

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        self.controller = controller #referes to the main app

        self.name = "Model Manager"

        self.Create_Model_Viewer()
        self.Create_Model_Buttons()
        self.keras_layers_list = sorted([layer for layer in keras.layers.__dict__.keys() if inspect.isclass(eval(f"layers.{layer}"))]) # keras layers functions

        self.tree_model.bind("<Up>",lambda event:self.swap_layers(event))
        self.tree_model.bind("<Down>",lambda event:self.swap_layers(event))

#widgets creation
    def Create_Model_Viewer(self):
        #function which initializes the model viewer

        self.Model_frame = tk.Frame(self,bg="white",width=250,height=400)  
        self.Model_frame.place(x=25,y=50)

        columns = ('Id', 'Layer_Name', 'Parameters')

        self.tree_model = ttk.Treeview(self.Model_frame, columns=columns, show='headings')

        self.tree_model.heading('Id', text='Id')
        self.tree_model.column("Id", minwidth=0, width=20, stretch=tk.NO)

        self.tree_model.heading('Layer_Name', text='Layer Name')
        self.tree_model.column("Layer_Name", minwidth=0, width=100, stretch=tk.NO)

        self.tree_model.heading('Parameters', text='Parameters')
        self.tree_model.column("Parameters", minwidth=0, width=130, stretch=tk.NO)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree_model.yview)
        scrollbar.place(x=275,y=50,height=225)

        self.tree_model.bind("<Double-1>", self.Modify_layer_win) # double click on a layer leads to the modify layer window

        self.tree_model.configure(yscroll=scrollbar.set)   #set the scrollbar to the treeview
        self.tree_model.grid(sticky='nsew')

    def Create_Model_Buttons(self):
        #function which initializes the model buttons

        Save_Model_Button = tk.Button(self,text="Save the model",command=self.save_model)
        Save_Model_Button.place(x=320,y=20)

        Load_Model_Button = tk.Button(self,text="Import a model",command=self.Load_Model)
        Load_Model_Button.place(x=320,y=50)

        Add_Layer_Button = tk.Button(self,text="Add a layer",command =self.Add_Layer_win)
        Add_Layer_Button.place(x=320,y=80)

        Remove_Layer_Button = tk.Button(self,text="Remove a layer",command =self.Remove_Layer)
        Remove_Layer_Button.place(x=320,y=110)
#widgets creation end

#model functions
    def save_model(self):
        #function which saves the current model in a folder

        if self.controller.shared_data["Current_Model"] == None:
            messagebox.showerror("Error","No model to save")
            return
        
        self.Model_Path = filedialog.askdirectory(title="Select the folder where you want to save the model")

        if self.Model_Path == "":
            return

        model_name = simpledialog.askstring("Model name","Enter the model name")
        if model_name == None:
            model_name = "model"

        self.Model_Path = self.Model_Path + "/" + model_name
        os.mkdir(self.Model_Path)
        self.controller.shared_data["Current_Model"].save(self.Model_Path)

    def Load_Model(self):
        #function which loads a keras model from a file and disolays it in the model viewer

        self.Model_Path = filedialog.askdirectory(title="Select the model")
        if self.Model_Path == "":
            return

        try:
            self.controller.shared_data["Current_Model"] = keras.models.load_model(self.Model_Path)

        except OSError :
            messagebox.showerror("Error","This is not a valid model")
            return
 

        for i in range(len(self.controller.shared_data["Current_Model"].layers)):
            layer = self.controller.shared_data["Current_Model"].layers[i]
            line =  [i,layer.__class__.__name__,"parametres non dispo"]

            self.tree_model.insert('', tk.END, values=line)

        messagebox.showinfo("Success","Model loaded successfully")

#layers management windows creation
    def Add_Layer_win(self):
        #function which opens the add layer window where the user can choose the layer he wants to add along with its parameters


        self.add_child_win = tk.Toplevel(self)
        self.add_child_win.title("Add a layer to the current model")
        self.add_child_win.geometry("350x180")

        #disabling the main window
        self.add_child_win.grab_set()

        #widgets creation

        self.Add_Layer_Label= ttk.Label(self.add_child_win,text="Select the layer to add")
        self.Add_Layer_Label.place(x=120,y=25)

        self.Layer_Combobox = ttk.Combobox(self.add_child_win,values=sorted(self.keras_layers_list) , state="readonly",width=30) #combobox which contains the keras layers
        self.Layer_Combobox.place(x=80,y=45)
        self.Layer_Combobox.bind("<<ComboboxSelected>>", self.Move_Widgets) # on layer selection, the parametre widgets are re-initialized

        self.Add_Button = tk.Button(self.add_child_win,text="Add this layer",command= lambda : self.Add_Layer())
        self.Add_Button.place(x=140,y=75)

        self.New_Arg_Button = tk.Button(self.add_child_win,text="Add this parameter",command= lambda : self.New_Param(self.add_child_win) , state ="disabled")
        self.New_Arg_Button.place(x=25,y=125)

        self.Arg_Combobox = ttk.Combobox(self.add_child_win,values=[""] , state="disabled",width=25)
        self.Arg_Combobox.place(x=150,y=125)
        #widgets creation end 


        self.arg_list = [] #list which contains the parameters of the layer to add
        self.wid_dict = {} #dictionary which contains the widgets of the add layer window

        self.add_child_win.mainloop()

    def Modify_layer_win(self,event):
        
        #function which opens the modify layer window where the user can modify the parameters of a layer
        #the layer is selected by double clicking on it in the model viewer
        # if one of the keras layer's parameters value is not the default one, it is displayed in the modify layer window

        self.Wid_Dict = {} #dictionary which contains the widgets of the modify layer window
        self.arg_list = [] #list which contains the parameters of the selected layer
        

        if self.tree_model.selection() == (): #if no layer is selected
            messagebox.showerror("Error","No layer selected")
            return
        
        selected = self.tree_model.item(self.tree_model.selection()[0],"values")
        layer_id = int(selected[0])
        self.layer_name = selected[1]
        layer = self.controller.shared_data["Current_Model"].layers[layer_id] #get the layer object of the current model
        
        self.mod_child_win = tk.Toplevel(self)
        self.mod_child_win.title("Modify this layer")
        self.mod_child_win.geometry("350x170")

        #disabling the main window
        self.mod_child_win.grab_set()

        self.Current_layer_label = tk.Label(self.mod_child_win,text=f"Current layer:\n{self.layer_name}")
        self.Current_layer_label.place(x=140,y=25)

        self.Add_Button = tk.Button(self.mod_child_win,text="Apply changes",command= self.Modify_Layer)

        self.Add_Button.place(x=140,y=75)

        self.New_Arg_Button = tk.Button(self.mod_child_win,text="Add this parameter",command= lambda : self.New_Param(self.mod_child_win) )
        self.New_Arg_Button.place(x=25,y=125)

        self.Arg_Combobox = ttk.Combobox(self.mod_child_win,values=[""] ,width=25)
        self.Arg_Combobox.place(x=150,y=125)

        modified_params = File_Manager_Tool.get_non_default_args(layer) #get the non default parameters of the selected layer except the inializer (dict)

        y_courant = 170

        for arg in File_Manager_Tool.get_positional_arguments(layer):
            #places all the widgets related to the positional arguments of the layer

            label = tk.Label(self.mod_child_win, text=arg+" : ", fg='red')
            label.place(x=25,y=y_courant)

            value = File_Manager_Tool.to_string(layer.get_config()[arg])
            entry = tk.Entry(self.mod_child_win, width=20)
            entry.place(x=150,y=y_courant)
            entry.insert(0,value)

            self.Wid_Dict[arg] = [label,entry]
            y_courant += 30

            self.arg_list.append(arg)
    

        for arg,value in modified_params.items():
            #places all the widgets related to the non default parameters of the layer

            label = tk.Label(self.mod_child_win, text=arg+" : ", fg='blue')
            label.place(x=25,y=y_courant)
            
            value = File_Manager_Tool.to_string(value)
            entry = tk.Entry(self.mod_child_win, width=20)
            entry.place(x=150,y=y_courant)
            entry.insert(0,value)

            button = tk.Button(self.mod_child_win, text="Delete", command= lambda arg=arg : self.Delete_param_widgets(arg,self.mod_child_win))
            button.place(x=300,y=y_courant)
            
            self.Wid_Dict[arg] = [label,entry,button]
            y_courant += 30

            self.arg_list.append(arg)
    

        self.mod_child_win.mainloop()

#layers management windows creation end

#Layers management windows functions start
    def New_Param(self,top_level):
        #function which displays the required arguments for the selected layer to work ( red label ) and stores in a combo box the non-mandatory arguments ( blue label )
        #the user can then choose the argument he wants to add to the layer

        param = self.Arg_Combobox.get() #current selected paramater
        if param =="":
            return 
        n =len(self.arg_list)
        y_curr = 150 + 30 * (n+1) # y position of the current argument

        self.Wid_Dict[param] = [tk.Label(top_level, text=param+" : ", fg='blue')] # for each parameter, 3 widgets are created : a label, an entry and a button and stored as a list in a dictionary
        self.Wid_Dict[param][0].place(x=25,y=y_curr)

        x_txt = 25 + len(param) * 7

        self.Wid_Dict[param].append(tk.Text(top_level, height=1, width=15))
        self.Wid_Dict[param][1].place(x=x_txt,y=y_curr)                    

        self.arg_list.append(param)

        self.Inc_height(30,top_level)
        self.Arg_Combobox["values"] = tuple(item for item in self.Arg_Combobox["values"] if item != param) # deletes the added param from the combobox
        self.Arg_Combobox.set("") #reset the combobox

        #button that deletes the widgets associated to the param (including himself)

        self.Wid_Dict[param].append(tk.Button(top_level,text="Del", command= lambda :self.Delete_param_widgets(param,top_level)))
        self.Wid_Dict[param][2].place(x=250,y=y_curr)                    

    def Delete_param_widgets(self,param,window):
        #function which deletes the widgets associated to a parameter

        if self.Arg_Combobox["values"] =="": # if the combobox is empty, the param is added to it
            self.Arg_Combobox["values"] = (param,)
        else:
            self.Arg_Combobox["values"] += (param,) #put back the parameters in the combobox


            
        print(self.Wid_Dict)
        for param_widgets in self.Wid_Dict:
            if self.Wid_Dict[param_widgets][0].winfo_rooty() > self.Wid_Dict[param][0].winfo_rooty()  : # if the widget is below the deleted one, it is moved up
                for wid in self.Wid_Dict[param_widgets]:
                    x,y =  self.get_pos(wid,window)
                    wid.place(x=x,y=y-30)

        for wid in self.Wid_Dict[param]:
            wid.destroy() #deletes all the widgets associated with the parameter

        self.arg_list.remove(param) #deletes the parameters from the used ones list
        del self.Wid_Dict[param] #same but for widgets dictionnary
        print(self.Wid_Dict)

        self.Inc_height(-30,window) #resizes the window
        window.update()

    def Move_Widgets(self,*args):
        #function which re-inintializes the widgets when a layer is selected along with the parameters combo box
        #it also deletes the widgets associated to the previous layer

        self.layer_name = self.Layer_Combobox.get()
  
        self.New_Arg_Button["state"] = "normal"
        self.Arg_Combobox["state"]= "normal"
        self.Arg_Combobox["values"] = []

        try:
            for arg in self.Wid_Dict.values():
                for wid in arg:
                    wid.destroy()
                self.Inc_height(-30,self.add_child_win)
                self.Arg_Combobox.set('')
        except AttributeError:
            print("vide")

        self.arg_list = []
        y_curr = 150
 
        l = eval(f"layers.{self.Layer_Combobox.get()}") #gets the layer class

        self.Wid_Dict = {} #dictionnary which stores the widgets associated to each parameter
  
        for arg in list(inspect.signature(l).parameters.keys()) : # iterates throught all the keras layer arguments

                if self.Arg_Combobox["values"] == "":
                    
                    self.Arg_Combobox["values"] = ("init") #we must initiate the Combobox with a value

                t = str(inspect.signature(l).parameters[arg]) 

                if t.count("=") > 0: # if the argument is not mandatory : break
                    
                    self.Arg_Combobox["values"] += (arg,)

                elif arg == "kwargs": continue

                else : 
                    y_curr +=30
                    self.Inc_height(30,self.add_child_win) # increase the window's height by 30 pixels

                    self.Wid_Dict[arg]= [tk.Label(self.add_child_win,text=arg, fg="red")]
                    self.Wid_Dict[arg][0].place(x=25,y=y_curr)  

                    x_txt = 25 + len(arg) * 8

                    self.Wid_Dict[arg].append(tk.Text(self.add_child_win, height = 1, width = 15))
                    self.Wid_Dict[arg][1].place(x=x_txt,y=y_curr) 
                    
                    self.arg_list.append(arg)

        self.Arg_Combobox["values"] = self.Arg_Combobox["values"][1:]
#Layers management windows functions end
    
#Model's layers management functions start

    def Build_layer(self):
        #function which builds the layer with the parameters the user entered
        # returns a keras layer object

        layer = self.layer_name

        if self.controller.shared_data["Current_Model"] == None:

            self.controller.shared_data["Current_Model"] = keras.Sequential() #initates the model

            return self.Build_layer() #calls itself to build the layer
            

        else : #we iterates throught the parameters the user entered and creates the layer with them

            l ="layers." + layer + "("

            for arg in self.arg_list:
                ans = self.Wid_Dict[arg][1].get() #gets the paramaters the user entered as string
               
                l+= arg + "=" + ans + ","

            if len(self.arg_list) > 0: #if the user entered parameters, we remove the last comma
                l = l[:-1]
            l += ")"

        return eval(l)

    def Add_Layer(self,im_size=400,position=None):

        layer = self.Build_layer() #gets the layer
        self.controller.shared_data["Current_Model"].add(layer) #adds the layer to the model

        layer_name = layer.__class__.__name__ #gets the layer's name

        line =  [len(self.controller.shared_data["Current_Model"].layers)-1,layer_name,"parametres non dispo"]

        self.tree_model.insert('', tk.END, values=line)

        self.add_child_win.destroy()


    def Modify_Layer(self,*args):

        model = self.controller.shared_data["Current_Model"]
        index_to_modify = self.tree_model.item(self.tree_model.selection())["values"][0]
        print(index_to_modify)
        
        layer = self.Build_layer() #gets the layer
        self.replace_layer(layer,index_to_modify) #replaces the layer in the model

        self.mod_child_win.destroy()


    def Remove_Layer(self):
        #function which removes a layer from the model
        #we recreate a model and then add the layers one by one except for the one the user is removing
        #we must change the input_shape of all the layers after the ones placed after the removed one

        model = self.controller.shared_data["Current_Model"]

        try:
            index_to_remove = self.tree_model.item(self.tree_model.selection())["values"][0]
        except IndexError:
            messagebox.showerror("Error","Please select a layer to remove")

            return
        print(index_to_remove)
        
        new_model = keras.Sequential(model.layers[:index_to_remove]) #we create a new model with the first layers to add
        for layer in model.layers[index_to_remove+1:]:
            input_shape = (None, new_model.output_shape[-1]) #we change its inpself.tree_model.item(self.tree_model.selection())["values"][0]ut shape to the output_shape of the last layer
            layer.build(input_shape=input_shape)
            new_model.add(layer)


        self.controller.shared_data["Current_Model"] = new_model

        self.tree_model.delete(self.tree_model.selection())
        for i in range(index_to_remove,len(model.layers)):
            self.tree_model.set(0,i,i-1)

    def swap_layers(self,event):
        model = self.controller.shared_data["Current_Model"]
        if event.keysym == "Up":
            dx=-1 #represents the direction of the swap
        elif event.keysym == "Down":
            dx=1
        i,j = self.tree_model.item(self.tree_model.selection())["values"][0] +dx, self.tree_model.item(self.tree_model.selection())["values"][0]
        layer_i, layer_j = model.layers[i], model.layers[j]

        new_model = keras.Sequential(model.layers[:i]) #we create a new model with the first layers to add

        for layer in [layer_j,layer_i] + model.layers[j+1:]: #the swap operates here by adding the layers in the wrong order and adding the right ones after
            input_shape = (None, new_model.output_shape[-1]) #we change its input shape to the output_shape of the last layer
            layer.build(input_shape=input_shape) #we build the layer with the new input shape
            new_model.add(layer)     

        self.controller.shared_data["Current_Model"] = new_model

        self.tree_model.delete(self.tree_model.selection())
        self.tree_model.insert('', i, values=[i,layer_j.name,"parametres non dispo"])
        self.tree_model.insert('', j, values=[j,layer_i.name,"parametres non dispo"])
    

        print([layer.name for layer in self.controller.shared_data["Current_Model"].layers])
        
    def replace_layer(self,new_layer,layer_index):
        #function which replaces a layer in the model by another one
        #we recreate a model and then add the layers one by one except for the one the user is modyfing
        #in case the shape of the layer changes, we must change the layer's input shape

        current_model = self.controller.shared_data["Current_Model"]
        new_model = keras.Sequential()
        for layer in current_model.layers:
            if layer_index == current_model.layers.index(layer):
                
                input_shape = (None, new_model.output_shape[-1]) #we change its input shape to the output_shape of the last layer
                new_model.add(new_layer)
                   
            else:
                new_model.add(layer)

        self.controller.shared_data["Current_Model"] = new_model

        self.mod_child_win.destroy()
#Model's layers management functions end 

#other functions related to windows management

    def get_pos(self,widget,window ):
        #function which returns the position of a widget relative to the window

        return widget.winfo_rootx() - window.winfo_rootx(), widget.winfo_rooty() - window.winfo_rooty()

    def Inc_height(self,n,top):
        # incrase the windows heiht by n pixels

        current_geometry = top.geometry()
        current_height = int(current_geometry.split("x")[1].split("+")[0])
        new_height = current_height + n
        top.geometry("{}x{}".format(top.winfo_width(), new_height))
        top.update()
        print(current_height,top.winfo_height())