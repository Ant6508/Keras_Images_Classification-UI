

#imports

import tensorflow as tf 
from tensorflow import keras
import pandas
import numpy as np
from keras import layers
import matplotlib.pyplot as plt

#functions

def Load_Keras_Model(Model_Path):
	model = tf.keras.models.load_model(Model_Path)
	return model

def Save_Keras_Model(Model,Model_Path):
	Model.save(Model_Path)


def Load_Premade(Size,Classes_Count):
	
	model = tf.keras.Sequential([
    	
		layers.Rescaling(1./255, input_shape=(Size, Size, )),
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
	    layers.Dense(Classes_Count,activation = "softmax")
		])

	return model

"""p = Load_Premade(256,2)
p.save("D:/temp/model")"""

def Compile_Model(Model,optimizer = 'adam'):
	Model.compile(optimizer = optimizer,
                loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

def Fit_Model(Model,Train_Data,Val_Data,Custom_Call_Object,Epochs=3):
 
	hist = Model.fit( 
	    Train_Data,
	  validation_data=Val_Data,
	  epochs=Epochs,
	  verbose=0,
	  callbacks=[Custom_Call_Object])

	return hist.history['accuracy']


def Get_Args_Names(Function):
	return Function.__code__.co_varnames

def Get_Args_Count(Function):
	return Function.__code__.co_argcount


def Match_Layer(layer,Arg_List):

	layer = "layers." + layer

	if Arg_List != []:


		layer += "(" + str(Arg_List[0])

		for arg in Arg_List[1:] :

			layer += "," + str(arg)

		layer += ")"
	return eval(layer)

def Create_Model(Layers_List,Options_List):

	Model = tf.keras.Sequential([layers.experimental.preprocessing.Rescaling(1.255)])

	for layer in Layers_List:
		layer = Match_Layer(layer)
		Model.add(layer)

	return Model


