# Author: Garvan Doyle
# Email: garvandoyle@gmail.com






import glob, os, shutil
from bs4 import BeautifulSoup
class PDF_2_HOCR:
    # Description:
    # Function for trimming PDF pages
    # Inputs: 
    # path = parent folder for pdf
    # filename = filename of pdf
    # start = first page of trimmed pdf
    # end = last page of trimmed pdf
    # Outputs:
    # orignal_pdf_trim.pdf = a pdf trimmed to the specified pages
    def qpdf(self,filename,path,start,end):
        os.chdir(self.packagesDir + r"\qpdf\bin")
        cmd = 'qpdf ' + path + '\\' + filename + ' --pages . ' + str(start) +'-' + str(end) + ' -- ' + path + '\\' + filename.replace('.pdf','_trim.pdf')
        os.system(cmd)
    
    # Description:
    # Function for converting PNG to HOCR
    # Inputs: 
    # file = png file to convert
    # filename = new filename of png stemmed to remove .pdf
    # outfolder = the folder path to output the HOCR file
    # Outputs:
    # orignal_png.hocr = a hocr file of the png input
    def convertToHocr(self,file, outFolder, filename):
        os.chdir(self.packagesDir + r"\tesseract")
        print("\nDocument Output Folder: " + outFolder)
        print("Page: " + filename)
        os.chdir(outFolder)
        folderName = filename[:-2]
        if not os.path.isdir(folderName):
                os.mkdir(folderName)
        os.chdir(self.packagesDir + '\\tesseract')
        hout = filename[-1:]
        cmd = 'tesseract.exe ' + self.png_dir + '\\' + file + ' ' + outFolder + '\\' + folderName + '\\' + hout + ' hocr'
        os.system(cmd)
    
    # Description:
    # Function for converting PDF to PNG
    # Inputs: 
    # file = pdf file to convert
    # path = path to parent folder of pdf
    # outfolder = path to pdf output folder
    # Outputs:
    # orignal_pdf.png = a png file of the pdf input
    def convertToPng(self,file,path,outFolder):
        os.chdir(self.packagesDir + r"\poppler\bin")
        cmd = 'pdftoppm.exe -png ' + path + '\\' + file + ' ' + outFolder + '\\' + file.replace('.pdf','')
        print (cmd)
        os.system(cmd)


    def __init__(self):
        #Get reference to parent directory and packages directory
        self.scriptDir = os.getcwd()
        os.chdir('Packages')
        self.packagesDir = os.getcwd()
        os.chdir(self.scriptDir)
        #Create Folders
        folders = ['PNG_OUT','hOCR_OUT','PDF_INPUT']
        for folder in folders:
            if not os.path.isdir(folder):
                os.mkdir(folder)
            else:
                shutil.rmtree(folder)
                os.mkdir(folder)
            os.chdir(self.scriptDir)
        #Await User PDF Input
        user_check = input("Copy PDF's into 'PDF_INPUT'\nConfirm? [yes]/[no]\n")
        if user_check.lower() == "yes":
            #Get reference to all folders
            os.chdir(self.scriptDir)
            os.chdir('PNG_OUT')
            self.png_dir = os.getcwd()
            os.chdir(self.scriptDir)
            os.chdir('hOCR_OUT')
            self.hocr_dir = os.getcwd()
            os.chdir(self.scriptDir)
            os.chdir('PDF_INPUT')
            self.pdf_dir = os.getcwd()
            pdf_files = glob.glob('*.pdf')
            # Convert all PDF's to PNG
            for pdf in pdf_files:
                self.convertToPng(pdf,self.pdf_dir,self.png_dir)  
            os.chdir(self.png_dir)
            # Convert all PNG to HOCR's
            png_trimmed = glob.glob('*.png')
            for png in png_trimmed:
                self.convertToHocr(png,self.hocr_dir,png.replace('.png',''))
        else:
            print("Program Terminate.....")
            
    
class HOCR_TOOLKIT:
    # Description:
    # Function for creating 'soup' which is a BeutifulSoup object allowing for navigation of the hocr file
    # Inputs: 
    # hocrFile = the file used to create the soup
    # Outputs:
    # soup = a soup object which is navigated using BeutifulSoup functions and the helper functions below.
    def createSoup(hocrFile):
        with open(hocrFile, encoding = "Latin-1") as f:
            open_hocr = f.read()
            return BeautifulSoup(open_hocr,'lxml')

    # Description:
    # Function for creating an iterable collection of all the children objects between two ocr_lines in a soup object
    # Inputs: 
    # soup = this is the soup object which is to be naviagated 
    # line_1 = upper line bound
    # line_2 = lower line bound
    # Outputs:
    # collection_of_children_elements = an array of line objects between the two lines inputted (exclusive)
    def getAllChildernInRange(line_1,line_2,soup):
        if line_1 == None or line_2 == None:
           return [] 
        id_1 = line_1.split('_')
        id_2 = line_2.split('_')
        collection_of_children_elements = []
        for line in range(int(id_1[2]),int(id_2[2])):
            parent = soup.body.find(id = line_1.replace(id_1[2],str(line)))
            collection_of_children_elements.append(parent.findChildren())
        return collection_of_children_elements
    
    # Description:
    # Function for finding the id of a word within a soup object with the option to offset the selection.
    # Inputs: 
    # anchor = this is the search term that is used to anchor the search
    # soup = this is the soup object which is to be naviagated 
    # validation = this is an array of strings which are expected to be in the same line as the anchor term in order to validate that the term is the desired one
    # Outputs:
    # id = a string of the id of the desired line
    def findId(anchor,soup,validation,offset = 0):
            words = soup.body.findAll("span",{"class":"ocrx_word"})
            id = None
            for word in words:
                if word.string == anchor:
                    output =""
                    for data in word.parent.contents:
                            output += data.string.replace('\n', ' ').replace('\r', '')
                    for valid in validation:
                        if valid not in output:
                            flag = False
                        else:
                            flag = True
                        if flag:
                            id = word.parent['id'] 
            if offset != 0 and id != None:                   
                id = id.split('_')
                offset_digit = int(id[-1])
                offset_digit += offset
                id[-1] = str(offset_digit)
                id = "_".join(id)
            return id

    # Description:
    # Function for finding a string by its line id
    # Inputs: 
    # search_id = this is a string of the id of the desired line which has the text
    # soup = this is the soup object which is to be naviagated 
    # xmin, xmax = this an optional paramter for setting x bounds for the search term
    # ymin, ymax = this an optional parameter for setting y bounds for the search term
    # Outputs:
    # text = return the string which coressponds to the line_id within the bounds
    def findTextById(search_id,soup,xmin = 0, xmax = 5000, ymin = 0, ymax = 5000):
        words = soup.body.find(id = search_id)
        output = ""
        for word in words.findChildren():
            bbox = word['title']
            coords = bbox.split()
            yStart = int(coords[2])
            yEnd = coords[4]
            yEnd = int(yEnd[:-1])
            xStart = int(coords[1])
            xEnd = int(coords[3])
            if (yStart > ymin) and (yEnd < ymax) and (xStart > xmin) and (xEnd < xmax):
                output += " " + word.string.replace('\n', ' ').replace('\r', '')
        return " ".join(output.split())

    # Description:
    # Function for finding a string by an anchor term and a series of validation strings.
    # Inputs: 
    # anchor = this is the search term that is used to anchor the search
    # soup = this is the soup object which is to be naviagated 
    # validation = this is an array of strings which are expected to be in the same line as the anchor term in order to validate that the term is the desired one
    # Outputs:
    # output = return the entire string which contains the anchor word and is validated by the validation strings.
    def findTextByString(anchor,validation,soup):
        words = soup.body.findAll("span", {"class": "ocrx_word"})
        for word in words:
            if word.string.lower() == anchor.lower():
                output = ""
                for data in word.parent.contents:
                    output += " " + data.string    
                if len(validation) > 0:
                    for valid in validation:
                        if valid not in output:
                            flag = False
                        else:
                            flag = True
                    if flag:
                        return output
                else:
                    return output
    
    # Description:
    # Function for editing a line in the specific format used to search by id
    # Inputs: 
    # line = the orignal line you wish to add to
    # change = the delta you wish to add to change the line number
    # Outputs:
    # output = return the new line id string.
    def editLineNumber(line,change):
        line = line.split('_')
        num = int(line[-1])
        num += change
        line[-1] = str(num)
        return "_".join(line)