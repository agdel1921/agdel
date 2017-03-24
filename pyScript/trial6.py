import os
import sys
import csv
import re
from Npp import *
from Npp import Notepad
print "start"
filePathSrc = "D:/training/TWG_overall/data_harmonisation/regen/ignore/"
print "ashu"
for root, dirs, files in os.walk(filePathSrc):
	for fn in files:
		print  fn
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
		ct=0
		for k in range(len(g)-1):
			l = firstLine[g[k]:g[k+1]]
			print l[0:5], type(l[0:5])
			try:
				x = int(l[0:5])
			except ValueError as verr:
				pass
			except Exception as ex:
				pass
			print x, "x is %s" %type(x)
			l = l.replace('\n', ' ').replace('\r', '')
			print "l = %s" %l
			if (len(l)>1):
				if type(x) == int:
					print "1"
					s.append(\n')
					print "3"
					fin2.append(s.strip())
					print "4"
					s=[l.strip()]
					print "5"
					ct=l.count('"')
					print "2"					
				else:
					po = l[0:5].replace('\n', ' ').replace('\r', '')
					print po, type(po), len(po), len(l)
					print ct
					if len(l)>4:
						if((po[len(po)-1]==",") or (po[3]==",") or (po[4]==",")):
							if ((ct%2)==0):
								s.append['\n']
								fin2.append(s)
								s=[l.replace('\n', ' ').replace('\r', '')]
								ct=l.count('"')	
							else:
								s.append(l)
								ct=ct+l.count('"')	
						else:
							#print "reached outer"
							if(l[0]=='\n'):
								l=l[1:len(l)]
								#print "removed newline"
							#print "finished outer"
							l = l.replace('\n', ' ').replace('\r', '')
							print l
							s.append(l)
							ct=ct+l.count('"')	
						print l
					else:
						print "small string"
						print l
						s.append(l)
						ct=ct+l.count('"')
			x=None
			print s
			print k
		print "length of fin2 = %d" %len(fin2)
		print "now printing to file %s" %fn
		lc = filePathSrc+fn[:(len(fn)-4)].lower()+"_new.csv"
		print lc
		with open(lc, "wb") as output:
			for val in fin2[1:len(fin2)]:
				sto=""
				#print "val = %s" %val
				for y in val:
					#print "y = %s" %y
					sto=sto+" "+y
				#print "sto=%s" %sto
				sto = sto.strip()
				output.write(sto+"\n" )
