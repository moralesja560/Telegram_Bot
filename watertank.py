#this code will supervise the water tank level and will send warnings through Telegram
#developed by Ing. Jorge Morales, MBA.
#Control and Automation Engineering Department

import os
import sys
import subprocess

#get the info

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def My_Documents(location):
	import ctypes.wintypes
		#####-----This section discovers My Documents default path --------
		#### loop the "location" variable to find many paths, including AppData and ProgramFiles
	CSIDL_PERSONAL = location       # My Documents
	SHGFP_TYPE_CURRENT = 0   # Get current, not default value
	buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
	ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
	#####-------- please use buf.value to store the data in a variable ------- #####
	#add the text filename at the end of the path
	temp_docs = buf.value
	return temp_docs


################## end of the auxiliary functions

#convert from HST to TXT
#recover the file using the filepath

mis_docs = My_Documents(5)
ruta = str(mis_docs)+ r'\watertank.hst'
response = subprocess.call([resource_path(r"images/HST2TXT.exe"), ruta])
ruta2 = str(mis_docs)+ r'\watertank.txt'
file_exists2 = os.path.exists(ruta2)







