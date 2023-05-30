"""
Created by : Rongere Julien
Date : Sepctember 2022
Goal : this file creates the classes importer window which deals with the user data importation
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
import Tools.File_Manager_Tool as File_Manager_Tool

import pandas
import shutil


#------------Imports end------------

class C_I_win(tk.Frame):

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        self.controller = controller  #referes to the main window

        self.name = "Classes_Importer" #name of the window

        self.Current_Csv = pandas.DataFrame({'A' : []}) # csv where the different classes are stored
        self.progress_bar = None
  

        self.Widgets_Dict = {} #dictionary that will contain the different pairs (widget name , widget object)

        self.Create_Csv_reader()
        self.Create_Reader_Buttons()
        self.Create_Import_Button()


#Widgets creations

    def Create_Reader_Buttons(self):
        #this function initializes the buttons that allow the user to add or delete classes
        #it is a must to store the images to avoid garbage collection

        #buttons that adds a class to the csv
        self.add_button_image = tk.PhotoImage(file=File_Manager_Tool.get_active_dir() + r"/images/add_button.png")
        rounded_add_button = tk.Button(self, image=self.add_button_image,command=self.Add_Class)
        rounded_add_button.place(x=355,y=50)
        self.Widgets_Dict["add_button"] = rounded_add_button

        #buttons that removes a class from the csv
        self.del_button_image = tk.PhotoImage(file=File_Manager_Tool.get_active_dir() + r"/images/del.png")
        rounded_del_button = tk.Button(self, image=self.del_button_image,command=lambda: self.after(100,self.Del_Class))
        rounded_del_button.place(x=400,y=50)
        self.Widgets_Dict["del_button"] = rounded_del_button

    def Create_Csv_reader(self):
        #this function creates the csv reader which displays the classes

        csv_frame = tk.Frame(self,bg="white",width=350,height=400)  
        csv_frame.place(x=25,y=50)

        columns = ('Id', 'Class_Name', 'Images_Ctn','Val_Split')

        self.Widgets_Dict["Classes_Viewer"] = ttk.Treeview(csv_frame, columns=columns, show='headings')

        self.Widgets_Dict["Classes_Viewer"].heading('Id', text='Id')
        self.Widgets_Dict["Classes_Viewer"].column("Id", minwidth=0, width=50, stretch=tk.NO)

        self.Widgets_Dict["Classes_Viewer"].heading('Class_Name', text='Class Name')
        self.Widgets_Dict["Classes_Viewer"].column("Class_Name", minwidth=0, width=100, stretch=tk.NO)

        self.Widgets_Dict["Classes_Viewer"].heading('Images_Ctn', text='Image total Count')
        self.Widgets_Dict["Classes_Viewer"].column("Images_Ctn", minwidth=0, width=100, stretch=tk.NO)

        self.Widgets_Dict["Classes_Viewer"].heading('Val_Split', text='Val Split')
        self.Widgets_Dict["Classes_Viewer"].column("Val_Split", minwidth=0, width=50, stretch=tk.NO)

        #scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.Widgets_Dict["Classes_Viewer"].yview)
        scrollbar.place(x=327,y=50,height=225)

        self.Widgets_Dict["Classes_Viewer"].configure(yscroll=scrollbar.set)
        self.Widgets_Dict["Classes_Viewer"].grid(sticky='nsew')

    def Create_Import_Button(self):
        #this function creates the import button which allows the user to import the classes to his project directory

        Import_Button = tk.Button(self,text="Import Images",width = 16,
                                    command = lambda : File_Manager_Tool.create_thread
                                            ( lambda : Data_From_Dir_manager.Import_Classes_Images #creates and run a thread that imports the classes
                                            (self,self.Current_Csv, self.controller.shared_data["Project_Dir"] + "/Data")))
        Import_Button.place(x=25,y=280)

        self.Widgets_Dict["Import_Button"] = Import_Button

    def Create_Progress_Bar(self,maximum):
        #this function creates the progress bar which shows the user the progress of the current importation
        #the progress bar steps each time one image is copied to the project directory

        if self.progress_bar != None:
            self.progress_bar.destroy()

        self.progress_bar = ttk.Progressbar(self, orient="horizontal",length=150, mode="determinate")
        self.progress_bar.place(x=150,y=280)

        self.progress_bar["maximum"] = maximum
        self.progress_bar["value"] = 0

    def Create_Open_Data_Button(self):
        #this function creates the button that allows the user to open the project data directory

        Open_Data_Button = tk.Button(self,text="Open Data Directory",width = 16,
                                    command = self.Open_Data_Directory)
        Open_Data_Button.place(x=100,y=280)

        self.Widgets_Dict["Open_Data_Button"] = Open_Data_Button

#auxiliary fonctions
#project functions

    def Load_Csv_File(self,File_Path):
        #this function loads the csv file that contains the classes
        #and displays it in the csv reader

        self.Current_Csv = pandas.read_csv(File_Path)
        self.Widgets_Dict["Classes_Viewer"].delete(*self.Widgets_Dict["Classes_Viewer"].get_children())

        Lines = []
        for i in range(len(self.Current_Csv)):
            l = self.Current_Csv.loc[i, :].values.tolist()
            Lines.append(l)

        for line in Lines :
            self.Widgets_Dict["Classes_Viewer"].insert('', tk.END, values=line)

    def Open_Data_Directory(self):
    #this function opens the project data directory

        if self.controller.shared_data["Project_Dir"] == None:
            messagebox.showinfo("Error", "You must create a project first")
            return

        File_Manager_Tool.Open_Directory(self.controller.shared_data["Project_Dir"])


#classes actions
    def Add_Class(self,Val_Split = 0.2):
        #this function adds a class to the project csv

        if self.controller.shared_data["Project_Dir"] == None:
            messagebox.showinfo("Error", "You must create a project first")
            return

        class_path = filedialog.askdirectory(title="Where is your class directory?")
        if class_path == "":
            return
        class_name= class_path.split("/")[-1] #the class name corresponds to the folder's name

        img_ctn = File_Manager_Tool.count_files_in_dir(class_path)

        self.Current_Csv.loc[len(self.Current_Csv.index)] = [ len(self.Current_Csv.index),class_name, str(img_ctn), Val_Split, class_path]
        self.Current_Csv.to_csv(self.controller.shared_data["Project_Dir"] + "/Project_Classes.csv",index=False)
        self.Load_Csv_File(File_Path= self.controller.shared_data["Project_Dir"] + "/Project_Classes.csv")

        self.controller.shared_data["Classes_num"] +=1

    def Del_Class(self):
        #this function removes the selected class from the csv and removes from the project directory

        Selected_Class_Id = self.Widgets_Dict["Classes_Viewer"].focus() #get the selected row
        if Selected_Class_Id == "":
            messagebox.showinfo("Error", "You must select a class first")
            return
        Selected_Class_Id = int(self.Widgets_Dict["Classes_Viewer"].item(Selected_Class_Id)["values"][0])  #get the id of the selected row
 
        for i in range(Selected_Class_Id+1,len(self.Current_Csv)):
            self.Current_Csv.loc[i] =np.concatenate( ([i-1] , (self.Current_Csv.loc[i])[1:]) ) 

        self.Current_Csv.drop (self.Current_Csv.index[Selected_Class_Id], inplace=True)

        self.Current_Csv.to_csv(self.controller.shared_data["Project_Dir"] + "/Project_Classes.csv",index=False)
        self.Load_Csv_File(File_Path= self.controller.shared_data["Project_Dir"] + "/Project_Classes.csv")

        self.controller.shared_data["Classes_num"] -=1

        #remove the class from the project directory
        try:

            shutil.rmtree(self.controller.shared_data["Project_Dir"] + "/Data/" + self.Current_Csv.loc[Selected_Class_Id,"Class_Name"])
        except:
            pass