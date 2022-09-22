import sys
sys.path.insert(1, 'D:/Projets_info/Class_Auto/Tools')

import tkinter as tk
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

from tensorflow import keras
import pandas
import os



class Application(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)

        self.Project_Dir = ""
        self.Current_Csv = pandas.DataFrame({'A' : []})

        self.create_menu_bar()
        self.Create_Csv_reader()
        self.Create_Reader_Buttons()
        self.Create_Import_Button()
        self.Create_Separators()
        self.Create_Model_Viewer()
        self.Create_Model_Buttons()


#Widgets creations
    def create_menu_bar(self):
        menu_bar = tk.Menu(self)

        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="New", command=self.Setup_Project)
        menu_file.add_command(label="Open", command=self.Load_Project)
        menu_file.add_command(label="Save")
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About")
        menu_bar.add_cascade(label="Help",menu=menu_help)

        self.config(menu=menu_bar) 

    def Create_Reader_Buttons(self):

        self.add_button_image = tk.PhotoImage(file=File_Manager_Tool.get_active_dir() + r"\\images\\add_button.png")
        rounded_add_button = tk.Button(self, image=self.add_button_image,command=self.Add_Class)
        rounded_add_button.place(x=355,y=25)

        self.del_button_image = tk.PhotoImage(file=File_Manager_Tool.get_active_dir() + r"\\images\\del.png")
        rounded_del_button = tk.Button(self, image=self.del_button_image,command=self.Del_Class)
        rounded_del_button.place(x=400,y=25)

    def Create_Csv_reader(self):

        csv_frame = tk.Frame(self,bg="white",width=350,height=400)  
        csv_frame.place(x=25,y=25)

        columns = ('Id', 'Class_Name', 'Images_Ctn','Val_Split')

        self.tree_csv = ttk.Treeview(csv_frame, columns=columns, show='headings')

        self.tree_csv.heading('Id', text='Id')
        self.tree_csv.column("Id", minwidth=0, width=50, stretch=NO)

        self.tree_csv.heading('Class_Name', text='Class Name')
        self.tree_csv.column("Class_Name", minwidth=0, width=100, stretch=NO)

        self.tree_csv.heading('Images_Ctn', text='Image total Count')
        self.tree_csv.column("Images_Ctn", minwidth=0, width=100, stretch=NO)

        self.tree_csv.heading('Val_Split', text='Val Split')
        self.tree_csv.column("Val_Split", minwidth=0, width=50, stretch=NO)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree_csv.yview)
        scrollbar.place(x=327,y=25,height=225)

        self.tree_csv.configure(yscroll=scrollbar.set)
        self.tree_csv.grid(sticky='nsew')

    def Create_Import_Button(self):
        Import_Button = tk.Button(self,text="Import Images",width = 16,command = lambda : Data_From_Dir_manager.Import_Classes_Images(self.Current_Csv, self.Project_Dir + "/Data"))
        Import_Button.place(x=25,y=255)

    def Create_Separators(self):
        bar_label = lambda : ttk.Label(self,text="|")
        for i in range(15):
            bar_label().place(x=440,y=25 + 15*i)

    def Create_Model_Viewer(self):
        Model_frame = tk.Frame(self,bg="white",width=250,height=400)  
        Model_frame.place(x=460,y=25)

        columns = ('Id', 'Layer_Name', 'Parameters')

        self.tree_model = ttk.Treeview(Model_frame, columns=columns, show='headings')

        self.tree_model.heading('Id', text='Id')
        self.tree_model.column("Id", minwidth=0, width=50, stretch=NO)

        self.tree_model.heading('Layer_Name', text='Layer Name')
        self.tree_model.column("Layer_Name", minwidth=0, width=100, stretch=NO)

        self.tree_model.heading('Parameters', text='Parameters')
        self.tree_model.column("Parameters", minwidth=0, width=100, stretch=NO)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree_model.yview)
        scrollbar.place(x=715,y=25,height=225)

        self.tree_model.configure(yscroll=scrollbar.set)
        self.tree_model.grid(sticky='nsew')


    def Create_Model_Buttons(self):
        Load_Model_Button = tk.Button(self,text="Import a model",command=self.Load_Model)
        Load_Model_Button.place(x=735,y=25)

        Fit_Model_Button = tk.Button(self,text="Fit the model",fg="red",command=self.Fit_Model)
        Fit_Model_Button.place(x=735,y=70)


#aux fonctions creations

    def Setup_Project(self):

        Project_Dir = filedialog.askdirectory(title="Where should the project be created ?")

        Project_Name = simpledialog.askstring("Enter The Project Name","Enter The Project Name")

        Project_Manager.Create_Project(Project_Name,Project_Dir)

        self.Project_Dir = Project_Dir +"/"+Project_Name
        self.Load_Csv_File(File_Path = self.Project_Dir + "/Project_Classes.csv")

    def Load_Csv_File(self,File_Path):

        self.Current_Csv = pandas.read_csv(File_Path)
        self.tree_csv.delete(*self.tree_csv.get_children())

        Lines = []
        for i in range(len(self.Current_Csv)):
            l = self.Current_Csv.loc[i, :].values.tolist()
            Lines.append(l)

        for line in Lines :
            self.tree_csv.insert('', tk.END, values=line)

    def Load_Project(self):

        self.Project_Dir = filedialog.askdirectory(title="Where is your project directory?")
        self.Load_Csv_File(File_Path = self.Project_Dir + "/Project_Classes.csv")

    def Add_Class(self,Val_Split = 0.2):
        class_path = filedialog.askdirectory(title="Where is your class directory?")

        class_name= class_path.split("/")[-1]

        img_ctn = 0
        for root, dirs, files in os.walk(class_path):
            img_ctn += len(files)

        self.Current_Csv.loc[len(self.Current_Csv.index)] = [ len(self.Current_Csv.index),class_name, img_ctn, Val_Split, class_path]
        self.Current_Csv.to_csv(self.Project_Dir + "/Project_Classes.csv",index=False)
        self.Load_Csv_File(File_Path= self.Project_Dir + "/Project_Classes.csv")

    def Del_Class(self):
        Selected_Class_Id = self.tree_csv.focus()
        Selected_Class_Id = int(self.tree_csv.item(Selected_Class_Id)["values"][0])
        print(Selected_Class_Id)

        for i in range(Selected_Class_Id+1,len(self.Current_Csv)):
            self.Current_Csv.loc[i] =np.concatenate( ([i-1] , (self.Current_Csv.loc[i])[1:]) ) 

        self.Current_Csv.drop (self.Current_Csv.index[Selected_Class_Id], inplace=True)

        self.Current_Csv.to_csv(self.Project_Dir + "/Project_Classes.csv",index=False)
        self.Load_Csv_File(File_Path= self.Project_Dir + "/Project_Classes.csv")

    def Load_Model(self):

        self.Current_Model_Path = filedialog.askdirectory(title="Select the model"


            )
        self.Current_Model = keras.models.load_model(self.Current_Model_Path)

        for i in range(len(self.Current_Model.layers)):
            layer = self.Current_Model.layers[i]
            line =  [i,layer.name,"parametres non dispo"]

            self.tree_model.insert('', tk.END, values=line)

    def Fit_Model(self):


        Train_Data,Val_Data =  Data_From_Dir_manager.Create_Classes_Data(self.Project_Dir,size=400,batch_size=5,Seed=None)
        self.Current_Model = Keras_Model_Manager.Load_Premade(400,2)
        Keras_Model_Manager.Compile_Model(self.Current_Model)

        acc = Keras_Model_Manager.Fit_Model(self.Current_Model,Train_Data,Val_Data)
        messagebox.showinfo("Information","Your model was successfully trained\nwith the data you provided\nwith an accuracy of {a}".format(a=acc))

        Project_Name = simpledialog.askstring("Save trained model","Enter the model Name")

        self.Current_Model.save(self.Project_Dir + '/Ia_Models')


if __name__ == "__main__":
    app = Application()
    app.title("Py_Auto_Class")
    app.geometry("900x325")
    app.resizable(width=False, height=False)
    app.mainloop()