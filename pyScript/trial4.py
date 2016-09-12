import os
import sys
import csv
import re
from Npp import *
from Npp import Notepad
filePathSrc = "D:/training/TWG_overall/twg_copy/trial/"
#print "ashu"
chk=0
chk2=0
rem=[]
rem.append("vidyut")
for root, dirs, files in os.walk(filePathSrc):
	for fn in files:
		g=[0]
		fin=[]
		fin2=[]
		s=[]
		if chk==1:
			fin2.append(s)
			s.append(rem[0])
			chk2=1
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
			print l[0:5]
			print type(l[0:5])
			try:
				x = int(l[0:5])
			except ValueError as verr:
				pass
			except Exception as ex:
				pass
			print x
			print type(x)
			l = l.replace('\n', ' ').replace('\r', '')
			if (len(l)>1):
				if type(x) == int:
					fin2.append(s)
					s=[l.rstrip()]
					if '"' in l:
						ct=1
				else:
					po = l[0:5].replace('\n', ' ').replace('\r', '')
					print po, type(po), len(po), len(l)
					if len(l)>4:
						if chk2==1:
							s.append(l)
						else:
							if((po[len(po)-1]==",") or (po[3]==",") or (po[4]==",")):
								if ct==0:
									s=[l.replace('\n', ' ').replace('\r', '')]
								else:
									s.append(l)
							else:
								print "reached outer"
								if(l[0]=='\n'):
									l=l[1:len(l)]
									print "removed newline"
								print "finished outer"
								l = l.replace('\n', ' ').replace('\r', '')
								print l
								s.append(l)
							print l
					else:
						print "small string"
						print l
						s.append(l)
					if '"' in l:
						ct=0
			if ct==1:
				rem[0]=l
			else:
				rem[0]="vidyut"
			x=None
		print "now printing to file %s" %fn
		lc = filePathSrc+fn[:(len(fn)-4)].lower()+"_new.csv"
		print lc
		if rem[0]=="vidyut":
			chk=0
		else:
			chk=1
		with open(lc, "wb") as output:
			if chk==0:
				rt = fin2[1:len(fin2)]
			else:
				rt=fin2[1:(len(fin2)-1)]
			for val in rt:
				sto=""
				#print "val = %s" %val
				for y in val:
					#print "y = %s" %y
					sto=sto+" "+y
				#print "sto=%s" %sto
				sto = sto.rstrip()
				output.write(sto+"\n" )
