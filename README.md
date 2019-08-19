# PDF OCR Toolkit
## Author: Garvan Doyle
## Email: [garvandoyle@gmail.com](mailto:garvandoyle@gmail.com)
## Description:
- This is a toolkit for extracting structured information from un-searchable PDF's.

## Setup:
- Use 7zip to unzip the packages file
- File Structure:
  Parent Folder[Packages, pdf_toolkit.py]
  

## Basic Usage:

#### Example PDF:
##### The following PDF was chosen as it shows some limitations to the OCR engine as it struggles with none standard fonts
![Example PDF](https://github.com/GarvanD/PDF-Toolkit/blob/master/PDF_Example/Resume-1.png "Resume.png")
#### How to convert PDF to HOCR:

```python
from pdf_toolkit import PDF_2_HOCR

pdfCoverter = PDF_2_HOCR()
```
###### At this step copy all PDF's into PDF_INPUT Folder in parent directory
```
Copy PDF's into 'PDF_INPUT'
Confirm? [yes]/[no]
```
### Navigating HOCR Documents
#### How to find the id of a line
```python
line_1 = HOCR_TOOLKIT.findId("Roles",soup,["Roles","Projects"])
line_2 = HOCR_TOOLKIT.findId("Awards",soup,["Awards"])
print(line_1,line_2)
```
![Example of Lines](https://github.com/GarvanD/PDF-Toolkit/blob/master/PDF_Example/find_lines.png "Lines-Example.png")
```python
line_1_21 line_1_43
```
#### How to iterate and print each line.
 ```python
range_of_children = HOCR_TOOLKIT.getAllChildernInRange(line_1,line_2,soup)

for line in range_of_children:
    line_string = ""
    for text in line:
        line_string += " " + text.string
    print(line_string)
```
```
Roles & Projects
Western Rocketry Avionics Executive London, ON
RESPONSIBLE FOR OVERSEEING SOFTWARE DESIGN & IMPLEMENTATION IN ROCKET AND DEVELOPING WEBSITE.
OPTIMIZED COMMUNICATION PROTOCOL FROM GROUND TO ROCKET WHICH MINIMIZED BANDWIDTH USAGE. werocketry.com
DEVISED A SIMULATION PROTOCOL FROM WHICH AIR STABILIZATION AND BRAKE TECHNOLOGY CAN BE OPTIMIZED.
FinTech Innovation Developer Lead London, ON
CREATED A STOCK TRADING SIMULATOR WEB APP FOR WESTERN STUDENTS BUILT WITH REACT AND JAVASCRIPT.

github.com/GarvanD/Fintech_Full
RESPONSIBLE FOR PROJECT DIRECTION AND ORGANIZATION OF 8 OTHER DEVELOPERS AS WELL AS IMPLEMENTATION.
FinTech VP of Education London, ON
RESPONSIBLE FOR DELIVERING WORKSHOPS ON CURRENT TECHNOLOGIES WITHIN THE FINTECH DOMAIN.
Reinforcement Learning Game Agent Python, C#, OpenCy, Tensorflow
âAN ML AGENT WHICH USES DEEP Q LEARNING TO PLAY A S.H.U.M.P GAME DEVELOPED IN UNITY. USING A CNN To
PROCESS SCREENSHOTS FROM THE GAME, THE MODEL CAN RETURN INTELLIGENT INPUTS WHICH RESULTED IN
BEATING THE GAME.

/GarvanD/Deep-Q-Agent
NLP Analysis of Legal Documents. Python, NLTK, Keras
DEVISED A PREDICTIVE MODEL TO SUGGEST WHETHER THE PROSPECTIVE OUTCOME OF LAWSUITS WERE TO BE
PROFITABLE. MODEL UTILIZES DEEP SENTIMENT ANALYSIS ON DOMAIN EXPERT'S CORPORA BY EMPLOYING Augusta Ventures
Worb2VEc AND SENTENCE2VEC EMBEDDINGâs RNN.
```

#### Searching for sentences by contained string.
```python
test_sentence = HOCR_TOOLKIT.findTextByString("ROCKET",["ROCKET"],soup)
print(test_sentence)
```
```
 RESPONSIBLE
 FOR
 OVERSEEING
 SOFTWARE
 DESIGN
 &
 IMPLEMENTAT
 IN
 ROCKET
 AND
 DEVELOPING
 WEBSITE.
```

#### Searching a line with coordinate parameters.
```python
reinforcement_line = HOCR_TOOLKIT.findId("Reinforcement",soup,["Reinforcement"])

title = HOCR_TOOLKIT.findTextById(reinforcement_line,soup,100,500)
frameworks_used = HOCR_TOOLKIT.findTextById(reinforcement_line,soup,900,1200)

```
![Example of Searching By Coordinates](https://github.com/GarvanD/PDF-Toolkit/blob/master/PDF_Example/searching-by-coordinates.png "Example of Searching By Coordinates")
```python
print("Project Title: %s\nFrameworks Used: %s" % (title,frameworks_used))
```
```
Project Title: Reinforcement Learning Game Agent
Frameworks Used: Python, C#, OpenCy, Tensorflow
```
#### Known Exceptions:
- PDF file names cannont contain whitespace, this is due to the format in which the compiled packages accept input.
- None standard font's can be troublesome, see example PDF above.
