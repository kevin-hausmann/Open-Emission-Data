import csv
from lxml import etree

INPUT_FILE = 'input.csv'
OUTPUT_FILE = 'submission.xml'

CVS_DELIMITER = ';'

START_YEAR = 1990
END_YEAR = 2015

CSV_SOURCE = 'source'
CVS_SUBSTANCE = 'gas'
CVS_UNIT = 'unit'

XML_ROOT = 'submission'
XML_SOURCE = 'source'
XML_SUBSTANCE = 'substance'
XML_EMISSION = 'emission'

XML_ID = 'id'
XML_UNIT = 'unit'
XML_YEAR = 'year'

def appendSubstance():
    substanceXml = etree.SubElement(sourceXml, XML_SUBSTANCE)
    substanceXml.set(XML_ID, row[CVS_SUBSTANCE])
    substanceXml.set(XML_UNIT, row[CVS_UNIT])

    for year in range(START_YEAR, END_YEAR + 1):
        if row[str(year)]:
            emissionXml = etree.SubElement(substanceXml, XML_EMISSION)
            emissionXml.set(XML_YEAR, str(year))
            emissionXml.text = "{:.2f}".format(float(row[str(year)].replace(',', '.')))


xml = etree.XML('<?xml version="1.0"?><submission year="2017" xmlns="https://www.umweltbundesamt.de/2017/emissionen"></submission>')

with open(INPUT_FILE) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=CVS_DELIMITER)
    sourceXml = None

    for row in reader:
        if sourceXml == None or row[CSV_SOURCE] != sourceXml.get(XML_ID):
            sourceXml = etree.SubElement(xml, XML_SOURCE)
            sourceXml.set(XML_ID, row[CSV_SOURCE])
            appendSubstance()
        else:
            appendSubstance()

etree.ElementTree(xml).write(OUTPUT_FILE, pretty_print=True)

