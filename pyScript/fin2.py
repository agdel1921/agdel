import os
import sys
from Npp import *
filePathSrc="D:\\training\\twg_copy\\Customer\\"
for root, dirs, files in os.walk(filePathSrc):
	print (files)
	for fn in files:
		print (root + "\\" + fn)
		notepad.open(root + "\\" + fn)
		notepad.MenuCommand("Macro", "Convert")
		#print ("#")
		notepad.runMenuCommand("Encoding", "Convert to UTF-8")
		notepad.save()
		#print (fn)
#notepad.close()
