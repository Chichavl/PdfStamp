from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4
from StringIO import StringIO
import argparse
import os
from PIL import Image

parser = argparse.ArgumentParser(description="TODO Desc here", add_help=True, version="1")
parser.add_argument("-i", "--input", action="store", default="./", type=str,
                    help="path to input files folder DEFAULT: ./")
parser.add_argument("-o", "--output", action="store", default="./output", type=str,
                    help="path to output files folder DEFAULT: ./output")
parser.add_argument("-s", "--stamp", action="store",
                    help="path to png stamp")
args = parser.parse_args()
#debug
print args

# Get dimentions of the stamp
im=Image.open(args.stamp)
width, height = im.size
#debug
print width, height
# Create output directory if doest`t exist
if not os.path.exists(args.output):
    os.makedirs(args.output)

    #debug
#myCanvas = canvas.Canvas('myfile.pdf', pagesize=A4)#
#wid, heig = A4 #keep for later
#print wid, heig
    
for sourceFile in os.listdir(str(args.input)):
    if sourceFile[-4:] != ".pdf" :
        continue
	#debug
    print sourceFile
    
    # Using ReportLab to insert image into PDF
    imgTemp = StringIO()
    imgDoc = canvas.Canvas(imgTemp)

    # Draw image on Canvas and save PDF in buffer
    imgPath = args.stamp
    imgDoc.drawImage(imgPath, 0, 0, width, height, mask='auto')    ## at (399,760) with size width x height
    imgDoc.save()

    # Use PyPDF to merge the image-PDF into the template
    page = PdfFileReader(file(sourceFile,"rb")).getPage(0)
    overlay = PdfFileReader(StringIO(imgTemp.getvalue())).getPage(0)
    page.mergePage(overlay)

    #Save the result
    outputFile = os.path.join(args.output, sourceFile)
    output = PdfFileWriter()
    output.addPage(page)
    output.write(file( outputFile,"w"))