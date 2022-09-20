#imports

import tensorflow as tf 
import pandas
import numpy as np
from tensorflow.keras import layers

#functions

def Load_Keras_Model(Model_Path):
	model = tensorflow.keras.models.load_model(Model_Path)
	return models

def Save_Keras_Model(Model,Model_Path):
	Model.save(Model_Path)


def Load_Premade():
	model = tf.keras.Sequential([
    	layers.experimental.preprocessing.Rescaling(1.255),
    	layers.Conv2D(128,2,activation = "relu"),
    	layers.MaxPooling2D(),
    	layers.Conv2D(64,2,activation = "relu"),
    	layers.MaxPooling2D(),
	    layers.Conv2D(32,2,activation = "relu"),
	    layers.MaxPooling2D(),
	    layers.Conv2D(16,2,activation = "relu"),
	    layers.MaxPooling2D(),
	    layers.Flatten(),
	    layers.Dense(64,activation="relu"),
	    layers.Dense(2,activation = "softmax")
		])

	return model


def Compile_Model(Model,optimizer = 'adam'):
	Model.compile(optimizer = optimizer,
                loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

def Fit_Model(Model,Train_Data,Val_Data,Epochs=3):
 
	Model.fit( 
	    Train_Data,
	  validation_data=Val_Data,
	  epochs=Epochs)


def Get_Args_Names(Function):
	return Function.__code__.co_varnames

def Get_Args_Count(Function):
	return Function.__code__.co_argcount



def Match_Layer(layer,Arg_List):

	layer = "layers." + layer

	if Arg_List != []:


		layer += "(" + str(Arg_List[0])

		for i in range(1,len(Arg_List)):

			layer += "," + str(Arg_List[i])

		layer += ")"
	return eval(layer)


Match_Layer("Conv2D",[32,3,"activation = 'relu'"])


def Create_Model(Layers_List,Options_List):

	Model = tf.keras.Sequential([layers.experimental.preprocessing.Rescaling(1.255)])

	for layer in Layers_List:
		layer = Match_Layer(layer)
		Model.add(layer)

	return Model
