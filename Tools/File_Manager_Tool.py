
import os

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_active_dir():
    path = os.getcwd()
    path = path.replace("\\","/")
    return path
