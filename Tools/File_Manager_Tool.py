"""
This module contains the subfoncions that deals with folders and files 

All the methods are Interface independent

"""



from keras import layers
import os
import inspect
from inspect import signature
import threading



#functions for directory management
def get_immediate_subdirectories(a_dir): 
    #function that returns the direct subdirectories of a directory
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_active_dir(): 
    #function that returns the active directory the app was lunch from
    path = os.getcwd()
    path = path.replace("\\","/")
    return path
 
#functions for layer management
def get_default_args(layer): 
    #function that returns the couples (arg_name, default_value) of the default arguments of a layer which are not positional arguments or kwargs
    sig = signature(layer.__init__) #get the signature of the layer
    return {p.name : p.default for p in sig.parameters.values() if p.default is not inspect.Parameter.empty and p.name not in get_positional_arguments(layer) and p.name != 'kwargs'}

def get_positional_arguments(layer):
    sig = signature(layer.__init__)
    return [p.name for p in sig.parameters.values() if p.default == inspect.Parameter.empty and p.name != 'kwargs']

def get_non_default_args(layer):
    #function that returns the couples (arg_name, value) of any argument of a layer if the value is not the default value of the argument or if the argument is not positional or kwargs
    sig = signature(layer.__init__) #get the signature of the layer, we specity __init__ because we want to get the arguments of the constructor
    defaut_args = get_default_args(layer)
    config = layer.get_config()
    return {p.name : config[p.name] for p in sig.parameters.values() if  p.name != 'kwargs' and p.name not in get_positional_arguments(layer) and config[p.name] !=defaut_args[p.name] and "initializer" not in p.name}

def get_args_dict(fn, args, kwargs):
    args_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    return {**dict(zip(args_names, args)), **kwargs}

def count_files_in_dir(dir):
    #function that counts the number of files in a directory and its subdirectories
    
    nbr_files = 0
    for path, dirs, files in os.walk(dir):
        for f in files:
            nbr_files += 1

    return nbr_files

def to_string(value):
    if isinstance(value, str):
        return f"'{value}'"
    else:
        return str(value)

def create_thread(target, args=()):
    #function that creates a thread and starts it

    thread = threading.Thread(target=target, args=args)
    thread.start()
    return thread

def Open_Directory(path):
    #function that opens a directory in the file explorer
    
    path = path.replace("/","\\")
    os.startfile(path)
