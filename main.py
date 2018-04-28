#!/usr/bin/python3

import argparse
import os

from docx import Document
from docx.shared import Inches, Pt

from class_defs import *
from process_arguments import *
from classify_line import classify_line
from process_line import process_line

from docx_output import *

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
dd = DataDict('PUMS Data Dictionary')
pltype = 'Blank'
pvar = ''
pval = ''

""" Iterate over all paragraphs in document """
for par in origpars:
    """
    The loop first classifies the line based on the current line and the preceding line type.
    Next, we process the line once we know what type of data it is.
    Lastly we initialize the previous line type variable for the next pass.
    """
    p = par.text.strip()
    
    ltype = classify_line(p,pltype)
    tmp = process_line(p,dd,ltype,pvar,pval)
    if ltype == 'Var Name' and tmp != None:
        pvar = tmp
    if ltype == 'Var Value' and tmp != None:
        pval = tmp
    pltype = ltype

for i in range(len(dd.vars)):
    v = dd.vars[i]
    varname = v.name
    varlen = v.varlen
    vardesc = v.vardesc
    valdict = v.valdict

    print("%-15s%3s" % (varname,str(varlen)))
    print("    %s" % vardesc)
    for key in valdict.keys():
        print("    %18s .%-40s" % (key,valdict[key]))

ddtext.close()
ddcsv.close()

ddword.save(outdoc)
