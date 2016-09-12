5 198import os
import sys
import csv
from Npp import *
from Npp import Notepad
filePathSrc = "D:/training/TWG_overall/twg_copy/trial/"
#print "ashu"
for root, dirs, files in os.walk(filePathSrc):
	for fn in files:
		g=[0]
		fin=[]
		fin2=[]
		s=[]
		notepad.open (root + "/" + fn)
		firstLine = editor.getText()
		notepad.close()
		for i in range(len(firstLine)):
			if(firstLine[i]=='\n'):
				g.append(i)
		print g
		for k in range(len(g)-1):
			l = firstLine[g[k]:g[k+1]]
			print l[0:5]
			print type(l[0:5])
			try:
				x = int(l[0:5)
			except ValueError as verr:
				pass
			except Exception as ex:
				pass
			print x
			print type(x)
			l = l.replace('\n', ' ').replace('\r', '')
			if type(x) == int:
				fin2.append(s)
				s=[l.rstrip()]
			else:
				#print l[0]
				#print type(l[0])
				#l=' '+l
				if(l[0]=='\n'):
					l=l[1:len(l)]
				l = l.replace('\n', ' ').replace('\r', '')
				s.append(l)
				#if type(firstLine[0:4]) ==int:
				#	print "Yes"
				#else:
				#	print "No"
				#print " "
			x=None
			op = ''.join(s)
			print op
			if op[0]==' ':
				op=op[1:len(op)]
			print op
			fin.append(op)
		print "now printing to file %s" %fn
		lc = filePathSrc+fn[:(len(fn)-4)].lower()+"_new.csv"
		print lc
		with open(lc, "wb") as output:
			#writer = csv.writer(output)
			for val in fin2[1:len(fin2)]:
				sto=""
				print "val = %s" %val
				for y in val:
					print "y = %s" %y
					sto=sto+" "+y
				print "sto=%s" %sto
				sto = sto.rstrip()
				output.write(sto+"\n" )
