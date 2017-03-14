import os
import sys

from Npp import notepad
filePathSrc = "D:/training/twg_copy/Contract Detail 5/"
#print "ashu"
for root, dirs, files in os.walk(filePathSrc):
                for fn in files:
                                if (fn[-4:] == '.csv'):
                                                notepad.open (root + "/" + fn)
                                                notepad.runMenuCommand("Macro", "convert")
                                                #notepad.save()
                                                notepad.runMenuCommand("Encoding", "Convert to UTF-8")
                                                notepad.save()
                                                #notepad.messageBox("{}{}".format(root+"\\"+fn[:-4],'_trans.csv'),0,"Done")
                                                notepad.messageBox("File: %s " % (fn))
                                                notepad.close()
                                                #notepad.saveAs("{}{}".format(root+"\\"+fn[:-4],'_trans.csv')) 
                #notepad.close()
