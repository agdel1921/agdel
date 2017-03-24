import os
import sys
import csv
import re
from Npp import *
from Npp import Notepad
filePathSrc = "D:/training/TWG_overall/twg_copy/trial/"
#print "ashu"
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
			print x, type(x)
			l = l.replace('\n', ' ').replace('\r', '')
			if (len(l)>1):
				if type(x) == int:
					fin2.append(s)
					s=[l.rstrip()]
					ct=l.count('"')	
				else:
					po = l[0:5].replace('\n', ' ').replace('\r', '')
					print po, type(po), len(po), len(l)
					print ct
					if len(l)>4:
						if((po[len(po)-1]==",") or (po[3]==",") or (po[4]==",")):
							if ((ct%2)==0):
								s=[l.replace('\n', ' ').replace('\r', '')]
								ct=l.count('"')	
							else:
								s.append(l)
								ct=ct+l.count('"')	
						else:
							#print "reached outer"
							if(l[0]=='\n'):
								l=l[1:len(l)]
								print "removed newline"
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
				sto = sto.rstrip()
				output.write(sto+"\n" )
