Written by RONGERE Julien


The purpose of this project is to democratize the use of neural networks with layers of convolution
in the framework of images classification according to their belonging to a given class.

In fact, images classification with ia has never been so accessible but some people still think it is reserved for I.T Genius or something like this,
and I hope this ui will make it even more accessible for the Python community.

The ui is here to make it easier for IA begginers to create their first images class project and (way) faster for
experienced keras enjoyer to group, sort the data and train as many different Sequential models as you want.

The application will help You create a working directory to setup your project where You will be able to import images, save IA models and even generate Python code.

The project was written only in python using tkinter and the keras library which provides highly powerful methods to train models with data.

As you might have understood, I am far from being a pro python developper and thus the code I wrote is meant to be easy to read and change,
and the different functionalities this ui has to offer are pretty limited if you have been coding with the tensorflow framework for a long time.

I am also not from an english speaking country so if an english mistake in the code comments burns one of your eye, feel free to contact me about It.
I wrote the whole app using english because It is more likely the user will speak english than French.

If you are new to ia, images classification, Keras..., just know for the rest of this readme that when We talk about a "class",It can be any object you want.
For exemple, If you want to train an Ia to recognise some animals, you might want to import the cat class along with the dog class etc...
If you want It to recognise some handwritten digits, you want to import the "1" class ...



------HOW TO USE THIS APPLICATION-------


-----Requirements------

You first must install some required librairies for the code to work.
To do so, get pip installed on your computer (I let the get-pip.py fil in the root folder, just Python it and thats all)
Then open the windows cmd in the root folder of the application and type "pip install requirements.txt".
That will proceed to the installation of the required librairies including tensorflow, pandas...


-----Getting started------

The application Itself is pretty straight forward, you firstly got a menu bar with differents sub scrolling menu which allows you to interract with the project you
want to create.

The "project menu" allows you to create or open an existing project.

Then you got (for now at least) 4 different tabs Classes Importer, Model Manager, Fit and Predictions that are meant to be used roughly in this order.


---------Classes Importer------------

The images importation is the first step when creating a images classification project.
You must prepare by yourself a folder named after the class you want to import (for exemple dog) filled with pictures representing the class (images of dogs literraly).
Then just add this folder by hitting the green + button, the application has now registered You want to work with this specific set of images
and then name of the class along with the number of images present in the the directory should appear in the Treeview

If You do not want to work with a specific class anymore, simply click the row of the class you want to delete from your projet directory
and hit the red trash button. Now the row should be deleted from the Treeview as well.

Finally, when you are done selecting the class you want to work with, hit the 'import images' button which will copy all the images in your "data" directory 
that you can find on the folder you have created your project in.

If you forgot to add a class, just add It with the + button then re-hit the import images button, everything should be ok.



--------Model Manager--------

 
This tab is from far the most difficult to use even if I tried to keep It simple, let's go step by step.

The Treeview you see on the left will display the different layers your model contains.
If you do not know how keras layers work, try to understand as many things as you can on the keras website : https://keras.io/api/layers/ , or others website
(chatGPT also provides really clear and detailled informations about IA, convolutional layers and Python in general)

The "import a model" button allows You to select a folder where a Keras model has been saved and will load the model in the treeview.
If you import a model without the will to modyfing It, you are good to go with this whole section.

------Adding a layer to your model--------
If not, You surely want to create and add a layer to your model using the 'add a layer' button.
A toplayer should open where you can select any keras layer you want, just select one in the combobox
( for exemple CONV2D which the convolutional layer for 2d arrays like images)

Depending on which layer you selected, you might must have to enter some mandatory arguments which are always displayed in red.
You then must enter a value for those red parameters or You will not be able to add the layer.

------------------
Very important : When you want to enter a value which is a string (for exemple the activation function "relu"), You must place that strings between quotes just like in Python
exemple :    activation : "relu"   
            kernel_size : 64 
Just do not do It with numbers, that will lead to errors.
------------------

You can also add some non-mandatory arguments to modify in depth the layer You want to add by chosing one of the avaible ones in the bottom combobox,
and hitting the "add this parameter" button.
That should create 3 widgets (the label is in blue to precise Its non-mandatoryness) : a label with the name of the parameter, a textbox where You can enter the value
and a "del" button which delete the widgets related to the parameter which means It will not be taken in consideration when the layer will be created.

Once You are done entering the values, hit the "add this layer" button and the layer You just created should be added to both the Tree and your model.



------Modifying a layer of your model--------
By double clicking on a layer of the Treeview, a slightly different windows of the 'adding' one should open and allows you to modify the parameters of the layer.
This windows works the same as the adding and should (I am still working on It) display only the paramaters You have already modified.
If we take the CONV2D layer for exemple again, You must precise at Its creation 2 mandatory paramaters which are filters and kernel_size.
Now imaging you want to precise an activation function like "relu" for this layer, the "modify" windows should only display the filters, kernel_size and activation paramaters.


You must be very careful with this windows as It was the hardest to code for me and thus the most likely to crash....
For exemple if You modify the kernel_size of a convolutional layer, It is going to change Its output dimension and cause trouble...



-----Fitting your model--------

Once You have imported all the data you needed and created your mind-blowing Keras model, just go the "fit" tab and hit the fit button.
The training process will thus begin and the accuracy for each epoch will be display to you in the "console"
You are given the choice at the ed of the training to save once again your model as a folder (that you can open anothertime in the model manager tab).


------Making predictions with your trained model------

Once your model is trained with your data, you can make predictions on new images on the "Predictions" tab
You can even select a folder to sort, ie for each images present in the folder, the model will predict which class the image belongs to and then place It
in the according directory





------------------

I plan on adding a lot of other features to this project. You can see them in the TODOLIST file but for the moment I will let this file in my native language.
Feel free to write a feedback about this application and use It until its limit.