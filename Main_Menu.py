import sys
sys.path.insert(1, 'D:/Projets_info/Class_Auto/Tools')

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk

import Data_From_Dir_manager
import Keras_Model_Manager
import File_Manager_Tool
import Project_Manager
import Req_Manager
import pandas
import os


class Application(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.create_menu_bar()
        self.Create_Csv_reader()
        self.Create_Reader_Buttons()


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
        rounded_del_button = tk.Button(self, image=self.del_button_image)
        rounded_del_button.place(x=400,y=25)

  
    def Create_Csv_reader(self):

        csv_frame = tk.Frame(self,bg="white",width=350,height=400)  
        csv_frame.place(x=25,y=25)

        columns = ('Id', 'Class_Name', 'Images_Ctn','Val_Split')

        self.tree = ttk.Treeview(csv_frame, columns=columns, show='headings')

        self.tree.heading('Id', text='Id')
        self.tree.column("Id", minwidth=0, width=50, stretch=NO)

        self.tree.heading('Class_Name', text='Class Name')
        self.tree.column("Class_Name", minwidth=0, width=100, stretch=NO)

        self.tree.heading('Images_Ctn', text='Image total Count')
        self.tree.column("Images_Ctn", minwidth=0, width=100, stretch=NO)

        self.tree.heading('Val_Split', text='Val Split')
        self.tree.column("Val_Split", minwidth=0, width=50, stretch=NO)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.place(x=327,y=25,height=225)

        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(sticky='nsew')

#aux fonctions creations

    def Setup_Project(self):

        Project_Dir = filedialog.askdirectory(title="Where should the project be created ?")

        Project_Name = simpledialog.askstring("Enter The Project Name","Enter The Project Name")

        Project_Manager.Create_Project(Project_Name,Project_Dir)

        self.Project_Dir = Project_Dir +"/"+Project_Name
        self.Load_Csv_File(File_Path = self.Project_Dir + "/Project_Classes.csv")

    def Load_Csv_File(self,File_Path):

        self.Current_Csv = pandas.read_csv(File_Path)
        self.tree.delete(*self.tree.get_children())

        Lines = []
        for i in range(len(self.Current_Csv)):
            l = self.Current_Csv.loc[i, :].values.tolist()
            Lines.append(l)

        for line in Lines :
            self.tree.insert('', tk.END, values=line)

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
        print(self.Current_Csv,class_path,class_name,img_ctn)
        self.Load_Csv_File(File_Path= self.Project_Dir + "/Project_Classes.csv")

if __name__ == "__main__":
    app = Application()
    app.title("Py_Auto_Class")
    app.geometry("450x800")
    app.resizable(width=False, height=False)
    app.mainloop()


