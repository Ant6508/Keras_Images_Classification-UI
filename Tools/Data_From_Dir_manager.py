#imports

import tensorflow as tf
import pandas
import os
import shutil
import glob
import File_Manager_Tool



#Aux functions

def Create_Subsets(Path,Classes_df,i):
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



def Subsets_Check(Path): # check if the user already has created 2 subets for training and validation 
	List_Dir = File_Manager_Tool.get_immediate_subdirectories(Path) #returns the direct folder list
	if len(List_Dir)==2:
		return True

	return False


def Import_Classes_Images(Classes_df,Data_dir): # Classes_df is the csv file containing the Classes to import , data_dir the global data folder of the projet where all the other Classes are located

	Nbr_Classes = len(Classes_df)

	for i in range(Nbr_Classes):
		Path = Classes_df.loc[i,"Path"]
		Class_name = Classes_df.loc[i,"Class_Name"]

		if Subsets_Check(Path) == True : #in case there exists 2 subsets for the class, we move all images to the dedicated dir accordingly

			try :

				os.mkdir(Data_dir + "/Training/" + Class_name)    # creates the dirs of the new class
				os.mkdir( Data_dir + "/Validation/" + Class_name)

			except FileExistsError :  #if it already exists, it means some images were already given for this class
				pass


			Train_Images_Path = Path + "/Training"
			Val_Images_Path = Path + "/Validation"

			Images_List = os.listdir(Train_Images_Path)
			Train_Images_Count = len(Images_List)    

			for image in Images_List:
				os.rename(Train_Images_Path + "/" + image , Data_dir + r"/Training/"+ Class_name + "/" + image)  #moves each images to prepare it right for the IA

			Images_List = os.listdir(Val_Images_Path)
			Val_Images_Count = len(Images_List)  

			for image in Images_List:
				os.rename(Val_Images_Path + "/" + image , Data_dir + r"/Validation/"+ Class_name+ "/" + image )

			#Classes_df.loc[i,"Val_Split"] = Val_Images_Count / (Train_Images_Count + Val_Images_Count)

		else :

			Create_Subsets(Path,Classes_df,i)
			Import_Classes_Images(Classes_df,Data_dir)

def Create_Classes_Data(Project_Dir,size=400,batch_size=32,Seed=None):

	Data_dir= Project_Dir + "/Data"

	Train_Data = tf.keras.preprocessing.image_dataset_from_directory(
		Data_dir+"/Training",
		seed=Seed,
		color_mode='grayscale',
		image_size= (size,size) ,
		batch_size = batch_size)

	Val_Data = tf.keras.preprocessing.image_dataset_from_directory(
		Data_dir+"/Validation",
		seed=Seed,
		color_mode='grayscale',
		image_size= (size,size) ,
		batch_size = batch_size)

	return Train_Data,Val_Data


	