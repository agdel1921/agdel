import os
import sys
from Npp import *
filePathSrc = "D:\\training\\TWG_overall\\twg_copy\\ro_header\\"
#print "ashu"
for root, dirs, files in os.walk(filePathSrc):
	for fn in files:
		if (fn== 'try.txt'):
			s=[]
			for m in range(10):
				notepad.open (root + "/" + fn)
				firstLine = editor.getLine(m)
				notepad.close()
				print firstLine[0:4]
				print type(firstLine[0:4])
				try:
					x = int(firstLine[0:4])
				except ValueError as verr:
					pass
				except Exception as ex:
					pass
				print x
				print type(x)
				if type(x) == int:
					s=[firstLine]
				else:
					print firstLine[0]
					print type(firstLine[0])
					firstLine=' '+firstLine
					s.append(firstLine)
				#if type(firstLine[0:4]) ==int:
				#	print "Yes"
				#else:
				#	print "No"
				print " "
				x=None
				print ''.join(s)
