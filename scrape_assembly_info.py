#!/usr/bin/env python3
import sys
import csv
import requests
from bs4 import BeautifulSoup

accession = sys.argv[1]

URL = 'https://www.ncbi.nlm.nih.gov/assembly/' + accession
page = requests.get(URL)
# print(page.content.decode())

soup = BeautifulSoup(page.content, 'html.parser')
summary_continued = soup.find(id="summary_cont")

# Make the summary easier to read
pretty_summary = summary_continued.prettify()

# Pretty_summary is a string, use split to parse into list
bits = pretty_summary.strip().split("  ")


assembly_index = False
genome_index = False
sequencing_index = False
submitter_index = False

# loop through list, get index of desired info
for i, item in enumerate(bits):
    if "Assembly method:" in item:
        assembly_index = i + 6 #6 is the magic number to add for this URL, hopefully it's the same for the rest
    elif "Genome coverage" in item:
        genome_index = i + 6
    elif "Sequencing technology" in item:
        sequencing_index = i + 6
    elif "Submitter:" in item:
        submitter_index = i + 6


# for num in range(20):
    #print(bits[genome_index + num])

# get info using index, print to verify, store in dictionary
if assembly_index != False:
    assembly_info = bits[assembly_index].strip()
else:
    assembly_info = "N/A"

if genome_index != False:
    genome_info = bits[genome_index].strip()
else:
    genome_info = "N/A"

if sequencing_index != False:
    sequencing_info =  bits[sequencing_index].strip()
else:
    sequencing_info = "N/A"
    
if submitter_index != False:
    submitter_info =  bits[submitter_index].strip()
else:
    submitter_info = "N/A"

# Print tsv
fields = ['Accession', 'Assembler', 'Genome coverage', 'Sequencing technology', 'Submitter']
rows = [accession, assembly_info, genome_info, sequencing_info, submitter_info]

print("\t".join(fields), file=sys.stderr)
print("\t".join(rows))
