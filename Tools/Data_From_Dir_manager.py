#imports

import tensorflow as tf
import numpy as np
import os
import shutil
import glob
import Tools.File_Manager_Tool as File_Manager_Tool
from tkinter import messagebox
import tkinter as tk
from keras.preprocessing import image


#Aux functions
#Interface independent functions are noticed by the comment #Aux function


def Create_Subsets(Path,Classes_df,i): #Aux function
	#function that creates the training and validation subsets for a given class


	os.mkdir( os.path.join(Path, 'Training'))    # creates the dirs of the new class
	os.mkdir( os.path.join(Path, 'Validation'))

	Images_List = os.listdir(Path)
	Images_List = [ fname for fname in Images_List if fname.endswith(".jpg")]

	Images_count = len(Images_List)

	for j in range(int(Classes_df.loc[i,"Val_Split"]*Images_count)):  # only moves the given ratio of images for validation, the rest will go in the training subset

		os.rename(Path +"/" + Images_List[j]  ,Path+ "/Validation/" + Images_List[j]  )

	Images_List = os.listdir(Path)
	Images_List = [ fname for fname in Images_List if fname.endswith(".jpg")]

	for image in Images_List:
		os.rename(Path +"/" +image  , Path + "/Training/" + image )


def Import_Classes_Images(parent,Classes_df,Data_dir):
	# Imports the images of the classes in the project folder
	# Classes_df is the csv file containing the Classes to import , data_dir the global data folder of the projet where all the other Classes are located

	if parent.controller.shared_data["Project_Dir"] == "" :
		messagebox.showerror("Error","Please create a project first")
		return

	Nbr_Classes = len(Classes_df)
	
	check_label = tk.Label(parent, text="Checking if all the Classes are present")
	check_label.place(x=320,y=270)
	check_subsets(Classes_df)
	check_label.destroy()
	
	for i in range(Nbr_Classes): # for each class

		Path = Classes_df.loc[i,"Path"]
		Class_name = str(Classes_df.loc[i,"Class_Name"])

		
		try :

			os.mkdir(Data_dir + "/Training/" + Class_name)    # creates the dirs of the new class
			os.mkdir( Data_dir + "/Validation/" + Class_name)

		except FileExistsError :  #if it already exists, it means some images were already given for this class
			print("The class " + Class_name + " already exists, some images may be missing")
			pass


		Train_Images_Path = Path + "/Training"
		Val_Images_Path = Path + "/Validation"

		Images_List = os.listdir(Train_Images_Path) # gets the list of images in the training subset
		Train_Images_Count = len(Images_List) 
		parent.Create_Progress_Bar(Train_Images_Count) # creates the progress bar

		label = tk.Label(parent, text="Importing " + Class_name + "\ntraining images")
		label.place(x=320,y=270)


		for image in Images_List:

			try :

				shutil.copy2(Train_Images_Path + "/" + image , Data_dir + r"/Training/"+ Class_name + "/" + image)  #copies each images to prepare it right for the IA
				parent.progress_bar.step(1) # updates the progress bar
			except  shutil.SameFileError:
				#case where the image is already in the folder
				parent.progress_bar.step(1)
				pass


		label.destroy()

		Images_List = os.listdir(Val_Images_Path)
		Val_Images_Count = len(Images_List) 

		parent.Create_Progress_Bar(Val_Images_Count)
		label = tk.Label(parent, text="Importing " + Class_name + "\nvalidation images")
		label.place(x=320,y=270)


		for image in Images_List:
			try:

				shutil.copy2(Val_Images_Path + "/" + image , Data_dir + r"/Validation/"+ Class_name + "/" + image)
				parent.progress_bar.step(1)

			except  shutil.SameFileError:
				#case where the image is already in the folder
				parent.progress_bar.step(1)
				pass
		label.destroy()


		parent.progress_bar.destroy()
		parent.progress_bar = None

	messagebox.showinfo("Importation done", "All the images were imported successfully")
	return #stops the associated thread



def check_subsets(Classes_df):
	# checks if the user already has created 2 subets for training and validation 
	# if not, it creates them
	
	Nbr_Classes = len(Classes_df)
	
	for i in range(Nbr_Classes):
		Path = Classes_df.loc[i,"Path"]

		if len(File_Manager_Tool.get_immediate_subdirectories(Path)) !=2 : #in case there is not 2 subsets for the class, we create the folders and move the images
			Create_Subsets(Path,Classes_df,i)

	

def Create_Classes_Data(Project_Dir,batch_size=32,Seed=None): #Aux function
	#function which creates and returns the training and validation data from the classes in the project dir
	#the data is returned as a tf.data.Dataset object which can be used to train the model

	Data_dir= Project_Dir + "/Data"

	Train_Data = tf.keras.utils.image_dataset_from_directory(
		Data_dir+"/Training",
		seed=Seed,
		color_mode='grayscale',
		batch_size = batch_size)

	Val_Data = tf.keras.utils.image_dataset_from_directory(
		Data_dir+"/Validation",
		seed=Seed,
		color_mode='grayscale',
		batch_size = batch_size)

	return Train_Data,Val_Data


def sort_folder(folder_path,model): #aux function
	#function which sorts the images in a folder according to the keras model given in parameter
	#the images are sorted in subfolders with the name of the class predicted by the model

	Images_List = os.listdir(folder_path) # gets the list of images in the training subset
	Images_List = [ fname for fname in Images_List if fname.endswith(".jpg")]

	classes_count = model.output_shape[1] # gets the number of classes in the model

	for i in range(classes_count):
		try:
			os.mkdir(folder_path + "/" + model.output_names[i]) # creates the subfolders for each class
		except FileExistsError:
			pass


	for image in Images_List:

		img = image.load_img(folder_path + "/" + image, color_mode='grayscale', target_size=(400, 400))
		img = image.img_to_array(img)
		img = np.expand_dims(img, axis=0)

		prediction = np.argmax(model.predict(img)) # gets the class predicted by the model

		shutil.move(folder_path + "/" + image , folder_path + "/" + model.output_names[prediction] + "/" + image) # moves the image to the right folder
