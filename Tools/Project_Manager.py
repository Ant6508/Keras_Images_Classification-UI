#imports

import pandas
import os
import shutil
import glob
import File_Manager_Tool


def Create_Project(Project_Name,Project_Dir):

	os.mkdir(Project_Dir+"/"+Project_Name)
	Project_Dir = Project_Dir+"/"+Project_Name

	Folder_List = ["Data", "Code_Render","Ia_Models"]
	for Folder in Folder_List:
		os.mkdir(Project_Dir+"/"+Folder)
	os.mkdir(Project_Dir+"/Data/Training")
	os.mkdir(Project_Dir+"/Data/Validation")

	shutil.copy2(File_Manager_Tool.get_active_dir() + '/Tools/Classes_Setup.csv', Project_Dir+"/Project_Classes.csv")
	

	Load_Project(Project_Dir)


def Load_Project(Project_Dir):
	
	pass