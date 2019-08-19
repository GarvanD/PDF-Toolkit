import os, glob
scriptDir = os.getcwd()
from pdf_toolkit import PDF_2_HOCR, HOCR_TOOLKIT
from bs4 import BeautifulSoup

#Convert PDF to HOCR
pdfCoverter = PDF_2_HOCR()

#Create Soup
soup = HOCR_TOOLKIT.createSoup(scriptDir +'//hOCR_OUT//Resume//1.hocr')

#How to find the id of a line
line_1 = HOCR_TOOLKIT.findId("Roles",soup,["Roles","Projects"])
line_2 = HOCR_TOOLKIT.findId("Awards",soup,["Awards"])
print(line_1,line_2)

#Find all children objects between two lines
range_of_children = HOCR_TOOLKIT.getAllChildernInRange(line_1,line_2,soup)

#Iterate through and print all children objects
for line in range_of_children:
    line_string = ""
    for text in line:
        line_string += " " + text.string
    print(line_string)

#Find sentence by keyword
test_sentence = HOCR_TOOLKIT.findTextByString("ROCKET",["ROCKET"],soup)
print(test_sentence)

#Find line by term
reinforcement_line = HOCR_TOOLKIT.findId("Reinforcement",soup,["Reinforcement"])

#Return string of line by x-coordinate bounds
title = HOCR_TOOLKIT.findTextById(reinforcement_line,soup,100,500)
frameworks_used = HOCR_TOOLKIT.findTextById(reinforcement_line,soup,900,1200)

print("Project Title: %s\nFrameworks Used: %s" % (title,frameworks_used))