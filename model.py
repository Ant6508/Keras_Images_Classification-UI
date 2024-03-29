
import tensorflow as tf
from tensorflow import keras
from keras import layers

def Load_Premade(Size,Classes_Count):
	
	model = tf.keras.Sequential([
		
    	layers.Rescaling(1./255,input_shape = (Size,Size,1)),
	    layers.Conv2D(128,2,activation = "relu"),
    	layers.MaxPooling2D(),
    	layers.Conv2D(64,2,activation = "relu"),
    	layers.MaxPooling2D(),
	    layers.Conv2D(32,2,activation = "relu"),
	    layers.MaxPooling2D(),
	    layers.Conv2D(16,2,activation = "relu"),
	    layers.MaxPooling2D(),
	    layers.Flatten(),
	    layers.Dense(16,activation="relu"),
	    layers.Dense(Classes_Count,activation = "softmax")
		])

	return model

p = Load_Premade(256,2)
p.save("model")
print(p.summary())


"""    	layers.Conv2D(128,2,activation = "relu"),
    	layers.MaxPooling2D(),
    	layers.Conv2D(64,2,activation = "relu"),
    	layers.MaxPooling2D(),

"""