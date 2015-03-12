import os
import sys
import subprocess
import xml.etree.ElementTree as ET
import glob


ZBAR = ".\\lib\\ZBar\\bin\\zbarimg.exe"
SEJA = ".\\lib\\sejda-console-1.0.0.M9\\bin\\sejda-console.bat"
WORKING_DIR = ".\\split\\"

# We check the file_prefix
try:
    filename = sys.argv[1]
except IndexError:
    print "Usage splitscan.py filename.pdf"
    print "Taking first pdf found"
    filename = glob.glob("*.pdf")[0]

print "Scanning for barcodes"
try:
    xml = subprocess.check_output([ZBAR, "--xml", "--quiet", filename])
    root = ET.fromstring(xml)
    lookup = {}
    for index in root[0]:
        lookup[int(index.attrib["num"]) + 1 ] = index[0][0].text
except Exception as e:
    print e
    
print lookup
pages = lookup.keys()
pages.sort()
pages = [str(x) for x in  pages]
print "Splitting into", len(pages), "files"
try:
    args = [SEJA, "splitbypages", "-f", filename, "-o", WORKING_DIR, "--overwrite", "-n"]
    subprocess.call(args + pages)
except Exception as e:
    print e.output
    
print "Renaming files"

for index in pages:
    os.rename( WORKING_DIR + index + "_" + filename, WORKING_DIR + lookup[int(index)] + ".pdf")
print "Done"
