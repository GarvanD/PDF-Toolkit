# PDF OCR Toolkit
## Author: Garvan Doyle
## Email: [garvandoyle@gmail.com](mailto:garvandoyle@gmail.com)

### Setup
- Use 7zip to unzip the packages file
- File Structure:
  Parent Folder[Packages, pdf_toolkit.py]
  

### Basic Usage:

#### How to convert PDF to HOCR:

```python
from pdf_toolkit import PDF_2_HOCR

pdfCoverter = PDF_2_HOCR()
```
### Navigating HOCR Documents



#### Known Exceptions:
- PDF file names cannont contain whitespace, this is do to the format in which the compiled packages accept input
