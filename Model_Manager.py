"""
This module contains the Model Manager window Widgets and methods to manage the user model
Supports layer creation, layer modification, layer deletion, model saving and loading

To do : Fix swap layers function
        Implemente before/after model differences display via another top level window

"""


import os


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

        self.widgets_dict = {} #dictionary which contains all the widgets of the window

        self.Create_Model_Viewer()
        self.Create_Model_Buttons()
        self.keras_layers_list = sorted([layer for layer in keras.layers.__dict__.keys() if inspect.isclass(eval(f"layers.{layer}"))]) # keras layers functions

        self.widgets_dict["Model_Treeview"].bind("<Up>",lambda event:self.swap_layers(event))
        self.widgets_dict["Model_Treeview"].bind("<Down>",lambda event:self.swap_layers(event))

#widgets creation
    def Create_Model_Viewer(self):
        #function which initializes the model viewer and adds it the widgets dictionary

        Model_frame = tk.Frame(self,bg="white",width=250,height=400)  
        self.widgets_dict["Model_frame"] = Model_frame
        self.widgets_dict["Model_frame"].place(x=25,y=50)

        columns = ('Id', 'Layer_Name', 'Parameters')

        self.widgets_dict["Model_Treeview"] = ttk.Treeview(self.widgets_dict["Model_frame"], columns=columns, show='headings')

        self.widgets_dict["Model_Treeview"].heading('Id', text='Id')
        self.widgets_dict["Model_Treeview"].column("Id", minwidth=0, width=20, stretch=tk.NO)

        self.widgets_dict["Model_Treeview"].heading('Layer_Name', text='Layer Name')
        self.widgets_dict["Model_Treeview"].column("Layer_Name", minwidth=0, width=100, stretch=tk.NO)

        self.widgets_dict["Model_Treeview"].heading('Parameters', text='Parameters')
        self.widgets_dict["Model_Treeview"].column("Parameters", minwidth=0, width=130, stretch=tk.NO)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.widgets_dict["Model_Treeview"].yview)
        scrollbar.place(x=275,y=50,height=225)

        self.widgets_dict["Model_Treeview"].bind("<Double-1>", self.Modify_layer_win) # double click on a layer leads to the modify layer window

        self.widgets_dict["Model_Treeview"].configure(yscroll=scrollbar.set)   #set the scrollbar to the treeview
        self.widgets_dict["Model_Treeview"].grid(sticky='nsew')

    def Create_Model_Buttons(self):
        #function which initializes the model buttons and adds them to the widgets dictionary

        Save_Model_Button = tk.Button(self,text="Save the model",command=self.save_model)
        self.widgets_dict["Save_Model_Button"] = Save_Model_Button
        self.widgets_dict["Save_Model_Button"].place(x=320,y=20)

        Load_Model_Button = tk.Button(self,text="Import a model",command=self.Load_Model)
        self.widgets_dict["Load_Model_Button"] = Load_Model_Button
        self.widgets_dict["Load_Model_Button"].place(x=320,y=50)

        Add_Layer_Button = tk.Button(self,text="Add a layer",command =self.Add_Layer_win)
        self.widgets_dict["Add_Layer_Button"] = Add_Layer_Button
        self.widgets_dict["Add_Layer_Button"].place(x=320,y=80)

        Remove_Layer_Button = tk.Button(self,text="Remove a layer",command =self.Remove_Layer)
        self.widgets_dict["Remove_Layer_Button"] = Remove_Layer_Button
        self.widgets_dict["Remove_Layer_Button"].place(x=320,y=110)

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

        try:
            self.controller.shared_data["Current_Model"].save(self.Model_Path)

        except :
            messagebox.showerror("Error","An error occured while saving the model")
            return

    def Load_Model(self):
        #function which loads a keras model from a file and displays it in the model viewer

        self.Model_Path = filedialog.askdirectory(title="Select the model")

        if self.Model_Path == "": #if the user cancels the file selection
            return

        try:
            self.controller.shared_data["Current_Model"] = keras.models.load_model(self.Model_Path)

        except OSError :
            messagebox.showerror("Error","This is not a valid model")
            return
        except:
            messagebox.showerror("Error","An error occured while loading the model")
            return
 
        self.widgets_dict["Model_Treeview"].delete(*self.widgets_dict["Model_Treeview"].get_children()) #clear the model viewer

        for i in range(len(self.controller.shared_data["Current_Model"].layers)):
            layer = self.controller.shared_data["Current_Model"].layers[i]
            line =  [i,layer.__class__.__name__,"not available yet"]

            self.widgets_dict["Model_Treeview"].insert('', tk.END, values=line)

        messagebox.showinfo("Success","Model loaded successfully")

        return

#layers management windows creation
    def Add_Layer_win(self):
        #function which opens the add layer window where the user can choose the layer he wants to add along with its parameters

        self.arg_list = [] #list which contains the parameters of the layer to include during the layer instantiation

        self.Top_Level_Wid_Dic = {} #dictionary which contains the widgets of the top level window 
                                    

        #initializing the window
        self.add_child_win = tk.Toplevel(self)
        self.add_child_win.title("Add a layer to the current model")
        self.add_child_win.geometry("350x180")

        #disabling the main window
        self.add_child_win.grab_set()

        #widgets creation
        Add_Layer_Label= ttk.Label(self.add_child_win,text="Select the layer to add")
        self.Top_Level_Wid_Dic["Add_Layer_Label"] = Add_Layer_Label
        self.Top_Level_Wid_Dic["Add_Layer_Label"].place(x=120,y=25)


        Layer_Combobox = ttk.Combobox(self.add_child_win,values=sorted(self.keras_layers_list) , state="readonly",width=30) #combobox which contains the keras layers
        self.Top_Level_Wid_Dic["Layer_Combobox"] = Layer_Combobox
        self.Top_Level_Wid_Dic["Layer_Combobox"].place(x=80,y=45)
        self.Top_Level_Wid_Dic["Layer_Combobox"].bind("<<ComboboxSelected>>", self.New_Layer_Selected) # on layer selection, the parametre widgets are re-initialized


        Add_Button = tk.Button(self.add_child_win,text="Add this layer",command= self.Add_Layer , state ="disabled")
        self.Top_Level_Wid_Dic["Add_Button"] = Add_Button
        self.Top_Level_Wid_Dic["Add_Button"].place(x=140,y=75)

        New_Arg_Button = tk.Button(self.add_child_win,text="Add this parameter",command= lambda : self.New_Param(self.add_child_win) , state ="disabled")
        self.Top_Level_Wid_Dic["New_Arg_Button"] = New_Arg_Button
        self.Top_Level_Wid_Dic["New_Arg_Button"].place(x=25,y=125)

        Arg_Combobox = ttk.Combobox(self.add_child_win,values=[""] , state="disabled",width=25)
        self.Top_Level_Wid_Dic["Arg_Combobox"] = Arg_Combobox
        self.Top_Level_Wid_Dic["Arg_Combobox"].place(x=150,y=125)
        #widgets creation end 


        self.add_child_win.mainloop()

    def Modify_layer_win(self,event):
        
        #function which opens the modify layer window where the user can modify the parameters of a layer
        #the layer is selected by double clicking on it in the model viewer
        # if one of the keras layer's parameters value is not the default one, it is displayed in the modify layer window

        self.Top_Level_Wid_Dic = {} #dictionary which contains the widgets of the modify layer window
        self.arg_list = [] #list which contains the parameters of the selected layer
        
        self.Param_Wid_Dic = {} #dictionary which contains the widgets related to one parameter (parameter  : [label,text entry]) and a delete button if the parameter is not the default one

        if self.widgets_dict["Model_Treeview"].selection() == (): #if no layer is selected
            messagebox.showerror("Error","No layer selected")
            return
        
        selected = self.widgets_dict["Model_Treeview"].item(self.widgets_dict["Model_Treeview"].selection()[0],"values")
        [layer_id,self.layer_name,_] = selected #getting the layer id, name and parameters from the model viewer as strings
        layer = self.controller.shared_data["Current_Model"].layers[int(layer_id)] #get the layer object of the current model
        
        #initializing the window
        self.mod_child_win = tk.Toplevel(self)
        self.mod_child_win.title("Modify this layer")
        self.mod_child_win.geometry("350x170")

        #disabling the main window
        self.mod_child_win.grab_set()

        #widgets creation
        Current_layer_label = tk.Label(self.mod_child_win,text=f"Current layer:\n{self.layer_name}")
        self.Top_Level_Wid_Dic["Current_layer_label"] = Current_layer_label
        self.Top_Level_Wid_Dic["Current_layer_label"].place(x=140,y=25)

        Add_Button = tk.Button(self.mod_child_win,text="Apply changes",command= self.Modify_Layer)
        self.Top_Level_Wid_Dic["Add_Button"] = Add_Button
        self.Top_Level_Wid_Dic["Add_Button"].place(x=140,y=75)

        New_Arg_Button = tk.Button(self.mod_child_win,text="Add this parameter",command= lambda : self.New_Param(self.mod_child_win))
        self.Top_Level_Wid_Dic["New_Arg_Button"] = New_Arg_Button
        self.Top_Level_Wid_Dic["New_Arg_Button"].place(x=25,y=125)

        Arg_Combobox = ttk.Combobox(self.mod_child_win,values=[""] ,width=25)
        self.Top_Level_Wid_Dic["Arg_Combobox"] = Arg_Combobox
        self.Top_Level_Wid_Dic["Arg_Combobox"].place(x=150,y=125)
        #widgets creation end

        modified_params = File_Manager_Tool.get_non_default_args(layer) #get the non default parameters of the selected layer except the inializer (dict)

        y_offset = 170

        for arg in File_Manager_Tool.get_positional_arguments(layer):
            #places all the widgets related to the positional arguments of the layer

            label = tk.Label(self.mod_child_win, text=arg+" : ", fg='red')
            label.place(x=25,y=y_offset)

            value = File_Manager_Tool.to_string(layer.get_config()[arg])
            entry = tk.Text(self.mod_child_win, width=20,height=1)
            entry.place(x=150,y=y_offset)
            entry.insert("1.0",value)

            self.Param_Wid_Dic[arg] = [label,entry]
            y_offset += 30

            self.arg_list.append(arg)
    

        for arg,value in modified_params.items():
            #places all the widgets related to the non default parameters of the layer

            label = tk.Label(self.mod_child_win, text=arg+" : ", fg='blue')
            label.place(x=25,y=y_offset)
            
            value = File_Manager_Tool.to_string(value)
            entry = tk.Text(self.mod_child_win, width=20,height=1)
            entry.place(x=150,y=y_offset)
            entry.insert("1.0",value)

            button = tk.Button(self.mod_child_win, text="Delete", command= lambda arg=arg : self.Delete_Param_Widgets(arg,self.mod_child_win))
            button.place(x=300,y=y_offset)
            
            self.Param_Wid_Dic[arg] = [label,entry,button]
            y_offset += 30

            self.arg_list.append(arg)
    

        #increases the height of the window according to the number of parameters that will be displayed

        for _ in range(0,len(self.arg_list)):
            self.Inc_height(30, self.mod_child_win)

        self.mod_child_win.mainloop()

#layers management windows creation end

#Layers management windows functions start
    def New_Param(self,top_level):
        #function which displays the required arguments for the selected layer to work ( red label ) and stores in a combo box the non-mandatory arguments ( blue label )
        #the user can then choose the argument he wants to add to the layer

        param = self.Top_Level_Wid_Dic["Arg_Combobox"].get() #current selected paramater

        if param =="":
            return 
        
        n =len(self.arg_list)
        y_curr = 150 + 30 * (n+1) # y position of the current argument

        self.Param_Wid_Dic[param] = [tk.Label(top_level, text=param+" : ", fg='blue')] # for each parameter, 3 widgets are created : a label, an entry and a button and stored as a list in a dictionary
        self.Param_Wid_Dic[param][0].place(x=25,y=y_curr)

        x_txt = 25 + len(param) * 7 # quick way to calculate the x position of the entry widget

        self.Param_Wid_Dic[param].append(tk.Text(top_level, width=15,height=1))
        self.Param_Wid_Dic[param][1].place(x=x_txt,y=y_curr)                    
        self.arg_list.append(param)

        #button that deletes the widgets associated to the param (including Itself)

        self.Param_Wid_Dic[param].append(tk.Button(top_level,text="Del", command= lambda :self.Delete_Param_Widgets(param,top_level)))
        self.Param_Wid_Dic[param][2].place(x=250,y=y_curr)                    

        self.Inc_height(30,top_level)

        self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] = tuple(item for item in self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] if item != param) # deletes the added param from the combobox
        self.Top_Level_Wid_Dic["Arg_Combobox"].set("") #reset the current value of the combobox

    def Delete_Param_Widgets(self,param,window):
        #function which deletes the widgets associated to a parameter

        if self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] =="": # if the combobox is empty, the param is added to it
            self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] = (param,)
        else:
            self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] += (param,) #put back the parameters in the combobox


        for param_widgets in self.Param_Wid_Dic:
            if self.Param_Wid_Dic[param_widgets][0].winfo_rooty() > self.Param_Wid_Dic[param][0].winfo_rooty()  : # if the widget is below the deleted one, it is moved up
                for wid in self.Param_Wid_Dic[param_widgets]:
                    x,y =  self.get_pos(wid,window)
                    wid.place(x=x,y=y-30)

        for wid in self.Param_Wid_Dic[param]:
            wid.destroy() #deletes all the widgets associated with the parameter

        self.arg_list.remove(param) #deletes the parameters from the used ones list
        del self.Param_Wid_Dic[param] #same but for widgets dictionnary

        self.Inc_height(-30,window) #resizes the window
        window.update()

    def New_Layer_Selected(self,*args):
        #function which re-inintializes the widgets when a layer is selected along with the parameters combo box
        #it also deletes the widgets associated to the previous layer

        self.layer_name = self.Top_Level_Wid_Dic["Layer_Combobox"].get()
        
  
        #since a new layer is selected, we can re-enable these widgets
        self.Top_Level_Wid_Dic["New_Arg_Button"].config(state="normal")
        self.Top_Level_Wid_Dic["Add_Button"].config(state="normal")
        self.Top_Level_Wid_Dic["Arg_Combobox"].config(state="normal")
    

        self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] = []

        #deletes the widgets associated to the previous layer
        try:
            for arg in self.Param_Wid_Dic.values():
                for wid in arg:
                    wid.destroy()
                    self.Inc_height(-30,self.add_child_win)
                self.Top_Level_Wid_Dic["Arg_Combobox"].set('')
        except AttributeError:
            pass

        self.arg_list = []
        self.Param_Wid_Dic = {} #dictionnary which stores the widgets associated to each parameter
        y_curr = 150
 
        l = eval(f"layers.{self.layer_name}") #gets the layer class
  
  
        #we iterate through all the arguments of the layer class and build the widgets associated to them

        for arg in list(inspect.signature(l).parameters.keys()) : # iterates throught all the keras layer arguments

                if self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] == "":
                    
                    self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] = ("init") #we must initiate the Combobox with a value

                t = str(inspect.signature(l).parameters[arg]) 

                if t.count("=") > 0: # if the argument is not mandatory : we add it to the combobox
                    
                    self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] += (arg,)

                elif arg == "kwargs": continue

                else : 
                    y_curr +=30
                    self.Inc_height(30,self.add_child_win) # increase the window's height by 30 pixels

                    self.Param_Wid_Dic[arg]= [tk.Label(self.add_child_win,text=arg, fg="red")]
                    self.Param_Wid_Dic[arg][0].place(x=25,y=y_curr)  

                    x_txt = 25 + len(arg) * 8

                    self.Param_Wid_Dic[arg].append(tk.Text(self.add_child_win, width = 15,height=1))
                    self.Param_Wid_Dic[arg][1].place(x=x_txt,y=y_curr) 
                    
                    self.arg_list.append(arg)

        self.Top_Level_Wid_Dic["Arg_Combobox"]["values"] = self.Top_Level_Wid_Dic["Arg_Combobox"]["values"][1:] #we remove the init value from the combobox



#Layers management windows functions end
    
#Model's layers management functions start

    def Build_layer(self):
        #function which builds the layer with the parameters the user entered
        # returns a keras layer object or None if the an error occured 
        

        layer = self.layer_name

        if self.controller.shared_data["Current_Model"] == None:

            self.controller.shared_data["Current_Model"] = keras.Sequential() #initates the model

            return self.Build_layer() #calls itself to build the layer
            

        else : #we iterates throught the parameters the user entered and creates the layer with them

            l ="layers." + layer + "("

            for arg in self.arg_list:

                #gets the paramaters the user entered as string
                print(type(self.Param_Wid_Dic[arg][1]))
                ans = self.Param_Wid_Dic[arg][1].get("1.0", "end-1c")
  
                l+= arg + "=" + ans + ","

            if len(self.arg_list) > 0: #if the user entered parameters, we remove the last comma
                l = l[:-1]
            l += ")"

        try:
            layer = eval(l) #creates the layer

        except Exception as e:

            print("the following error occured during layer creation : \n",e)
            return None
        
        layer = Keras_Model_Manager.set_unique_name(self.controller.shared_data["Current_Model"],layer)
        return layer

    def Add_Layer(self,im_size=400,position=None):

        layer = self.Build_layer() #gets the layer
        if layer == None:
            print("error")
            return

        self.controller.shared_data["Current_Model"].add(layer) #adds the layer to the model

        layer_name = layer.__class__.__name__ #gets the layer's name

        line =  [len(self.controller.shared_data["Current_Model"].layers)-1,layer_name,"parametres non dispo"]

        self.widgets_dict["Model_Treeview"].insert('', tk.END, values=line)

        self.add_child_win.destroy()


    def Modify_Layer(self,*args):
        #function which modifies a layer in the model

        index_to_modify = self.widgets_dict["Model_Treeview"].item(self.widgets_dict["Model_Treeview"].selection())["values"][0] # not a good line of code : we must have this info stored  before runnnig the function
        
        layer = self.Build_layer() #gets the layer
        if layer == None: return

        self.replace_layer(layer,index_to_modify) #replaces the layer in the model

        self.mod_child_win.destroy()


    def Remove_Layer(self):
        #function which removes a layer from the model
        #we recreate a model and then add the layers one by one except for the one the user is removing
        #we must change the input_shape of all the layers after the ones placed after the removed one

        model = self.controller.shared_data["Current_Model"]

        try:
            index_to_remove =self.widgets_dict["Model_Treeview"].item(self.widgets_dict["Model_Treeview"].selection())["values"][0]
        except IndexError:
            messagebox.showerror("Error","Please select a layer to remove")
            return
        
        print(index_to_remove)
        
        new_model = keras.Sequential(model.layers[:index_to_remove]) #we create a new model with the first layers to add
        for layer in model.layers[index_to_remove+1:]:
            input_shape = (None, new_model.output_shape[-1]) #we change its shape to the output_shape of the last layer
            layer.build(input_shape=input_shape)
            new_model.add(layer)

        self.controller.shared_data["Current_Model"] = new_model

        self.widgets_dict["Model_Treeview"].delete(self.Model_Treeview.selection()) #deletes the deleted layer from the treeview
        for i in range(index_to_remove,len(model.layers)):
           self.widgets_dict["Model_Treeview"].set(0,i,i-1) #decrease the index of the layers after the removed one to keep the right order

    def swap_layers(self,event):
        #function which swaps two layers in the model
        #still has to be tested properly

        model = self.controller.shared_data["Current_Model"]
        if event.keysym == "Up":
            dx=-1 #represents the direction of the swap
        elif event.keysym == "Down":
            dx=1

        i,j =self.widgets_dict["Model_Treeview"].item(self.Model_Treeview.selection())["values"][0] +dx,self.widgets_dict["Model_Treeview"].item(self.Model_Treeview.selection())["values"][0]

        if i < 0 or i >= len(model.layers):
            return #if the swap is impossible, we return
        
        layer_i, layer_j = model.layers[i], model.layers[j]

        new_model = keras.Sequential(model.layers[:i]) #we create a new model with the first layers to add

        for layer in [layer_j,layer_i] + model.layers[j+1:]: #the swap operates here by adding the layers in the wrong order and adding the right ones after
            input_shape = (None, new_model.output_shape[-1]) #we change its input shape to the output_shape of the last layer
            layer.build(input_shape=input_shape) #we build the layer with the new input shape
            new_model.add(layer)     

        self.controller.shared_data["Current_Model"] = new_model

        self.widgets_dict["Model_Treeview"].delete(self.Model_Treeview.selection())
        self.widgets_dict["Model_Treeview"].insert('', i, values=[i,layer_j.name,"parametres non dispo"])
        self.widgets_dict["Model_Treeview"].insert('', j, values=[j,layer_i.name,"parametres non dispo"])
        

        print([layer.name for layer in self.controller.shared_data["Current_Model"].layers])
        
    def replace_layer(self,new_layer,layer_index):
        #function which replaces a layer in the model by another one
        #we recreate a model and then add the layers one by one except for the one the user is modyfing
        #in case the shape of the layer changes, we must change the layer's input shape

        #we must as well rename the layer inner names to avoid conflicts with keras


        if len(self.controller.shared_data["Current_Model"].layers) == 1:
            model = keras.Sequential()
            model.add(new_layer)
            self.controller.shared_data["Current_Model"] = model
            return

        current_model = self.controller.shared_data["Current_Model"]
        new_model = keras.Sequential()
        for layer in current_model.layers:

            if layer_index == current_model.layers.index(layer):

                if layer_index == 0: #if the layer is the first one, we can't change its input shape
                    simpledialog.showerror("Error","You can't modify the input layer")
                    return

                input_shape = (None, new_model.output_shape[-1]) #we change its input shape to the output_shape of the last layer

                new_layer._name = layer.name #we change the layer's name to avoid conflicts with keras
                new_layer.build(input_shape=input_shape) #we build the layer with the new input shape
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

        previous_geometry = top.geometry()

        current_height = self.get_current_height(top)
    
        new_height = current_height + n

        try :
            top.geometry("{}x{}".format(top.winfo_width(), new_height))

        except :
            top.geometry(previous_geometry)
        top.update()
        print("previous height : {} new height : {}".format(current_height,new_height))        


    def get_current_height(self,top):

        #returns the current height of the window

        current_geometry = top.geometry()
        h_string = current_geometry.split("+")[0].split("x")[1]

        return int(h_string)