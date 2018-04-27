#!/usr/bin/python3

import argparse
import os

from docx import Document
from docx.shared import Inches, Pt

from process_arguments import *
from classify_line import classify_line

INDIR = './input'
OUTDIR = './output'
    
argp = argparse.ArgumentParser(description='Provide input data dictionary parameters')

argp.add_argument('yyyy',metavar='YYYY',type=int,help='Ending 4-digit data year for data dictionary')
argp.add_argument('period',metavar='PERIOD',type=int,choices=[1,3,5],help='Length of period (1/3/5)')
argp.add_argument('--ifile','-i',metavar='InFile',type=str,help='Path to input data dictionary')
argp.add_argument('--outdir','-o',metavar='OutDir',type=str,help='Path to output directory')
argp.add_argument('--replace','-r',action='store_true',help='Replace existing output files')

args = argp.parse_args()

yyyy = assign_yyyy(args)
if yyyy == None:
    exit(2)
    
period = assign_period(args)
if period == None:
    exit(2)

[ infile, basefile ] = assign_infile(args,INDIR)
if infile == None:
    exit(2)

[ outdoc, outtxt, outcsv ] = assign_outfiles(args,OUTDIR)
if outdoc == None:
    exit(2)

""" Setup base output Word document """
ddword = Document(basefile)
initialize_doc(ddword)
ddword.core_properties.author = 'US Census Bureau'
ddword.core_properties.title = os.path.splitext(os.path.basename(outdoc))[0]

""" Open text and csv files for writing """
ddtext = open(outtxt,'w')
ddcsv = open(outcsv,'w')

""" Begin read of input Word document """
ddorig = Document(infile)
origpars = ddorig.paragraphs

""" Initialize lag variables """
pltype = 'Blank'
pvar = ''

""" Iterate over all paragraphs in document """
for par in origpars:
    """
    The loop first classifies the line based on the current line and the preceding line type.
    Next, we process the line once we know what type of data it is.
    Lastly we initialize the previous line type variable for the next pass.
    """

    ltype = classify_line(p,pltype)
    tmp = process_line(p,ltype,pvar)
    if ltype == 'Var Name' and tmp != None:
        pvar = tmp
    pltype = ltype

ddtext.close()
ddcsv.close()

ddword.save(outdoc)
