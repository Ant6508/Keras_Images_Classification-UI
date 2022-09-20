def importlib_check():
	try:
		import importlib
		return True
	except ModuleNotFoundError:
		return False

	
Liste_Ext = ["tensorflow","numpy","os","PIL","matplotlib","pandas","test","cv2","pathlib","glob"] # requirements list for the ia to work

def Add_ext(string): #extensions to include in the final code
	L = string.split(",")
	return Liste_Ext + L

def dependency_check(List):
	missing =  [] # missing extensions list

	for ext in List:
		exists = importlib.util.find_spec(ext) is not None # check if the module exists
		if exists == False :
			missing.append(ext)
	return missing

#print(dependency_check(Add_ext("not_existing_module")))   #code test



	
