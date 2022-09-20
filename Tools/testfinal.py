import Data_From_Dir_manager
import File_Manager_Tool
import Keras_Model_Manager
import Project_Setup
import Req_Manager
import pandas


#Project_Setup.Create_Project("Cancer_Sein","D:\\Projets_info\\Class_Auto\\Tools")
Project_dir = "D:\\Projets_info\\Class_Auto\\Tools\\Cancer_Sein"

df = pandas.read_csv(Project_dir+"\\Project_Classes_List.csv")

#Data_From_Dir_manager.Import_Classes_Images(df,Project_dir+"\\Data")

train_data,val_data = Data_From_Dir_manager.Create_Classes_Data(Project_dir,size=400,batch_size=16,Seed=None)

model = Keras_Model_Manager.Load_Premade()

Keras_Model_Manager.Compile_Model(model)

Keras_Model_Manager.Fit_Model(model,train_data,val_data,Epochs=3)