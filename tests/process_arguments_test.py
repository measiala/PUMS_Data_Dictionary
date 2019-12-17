#!/usr/bin/python3

import pytest

from process_arguments import *

class fakeparse:
    def __init__(self,yyyy,period):
        self.yyyy = yyyy
        self.period = period
        self.ifile = ''
        self.outdir = ''
        self.replace = False

args = fakeparse(2017,1)

def create_file(filename):
    file = open(filename,'w')
    file.close()

def remove_file(filename):
    try:
        os.remove(filename)
        print("NOTE: %s removed." % filename)
    except:
        print("NOTE: %s does not exist." % filename)

def create_dir(dirname):
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)
        
def remove_dir(dirname):
    try:
        os.rmdir(dirname)
        print("NOTE: %s removed." % dirname)
    except:
        print("NOTE: %s does not exist." % dirname)

def test_assign_yyyy():
    """ We broadly allow the third millenium """
    args.yyyy = 1999
    assert assign_yyyy(args) == None
    args.yyyy = 2000
    assert assign_yyyy(args) == 2000
    args.yyyy = 2017
    assert assign_yyyy(args) == 2017
    args.yyyy = 2099
    assert assign_yyyy(args) == 2099
    args.yyyy = 3000
    assert assign_yyyy(args) == None

def test_assign_period():
    """ For each period test boundaries, 2010 which had all 3, and 2017 """

    """ Period 1 is allowed for all allowable years yyyy """
    args.period = 1
    args.yyyy = 1999
    assert assign_period(args) == None
    args.yyyy = 2000
    assert assign_period(args) == 1
    args.yyyy = 2010
    assert assign_period(args) == 1
    args.yyyy = 2017
    assert assign_period(args) == 1
    args.yyyy = 2099
    assert assign_period(args) == 1
    args.yyyy = 3000
    assert assign_period(args) == None

    """ Period 3 is only allowed for 2007-2013 """
    args.period = 3
    args.yyyy = 2006
    assert assign_period(args) == None
    args.yyyy = 2007
    assert assign_period(args) == 3
    args.yyyy = 2010
    assert assign_period(args) == 3
    args.yyyy = 2013
    assert assign_period(args) == 3
    args.yyyy = 2014
    assert assign_period(args) == None
    args.yyyy = 2017
    assert assign_period(args) == None

    """ Period 5 is only allowed for 2009 forward """
    args.period = 5
    args.yyyy = 2008
    assert assign_period(args) == None
    args.yyyy = 2009
    assert assign_period(args) == 5
    args.yyyy = 2010
    assert assign_period(args) == 5
    args.yyyy = 2017
    assert assign_period(args) == 5
    args.yyyy = 2099
    assert assign_period(args) == 5
    args.yyyy = 3000
    assert assign_period(args) == None

def test_assign_infile():
    """ Initialize args """
    args.yyyy = 2017
    args.period = 1
    args.ifile = ''

    """ Create two temporary directories """
    indir = '/tmp/pumsin'
    indir2 = '/tmp/pumsin2'
    create_dir(indir)
    create_dir(indir2)

    """ Define the default and secondary name """
    base = os.path.join(indir,'PageFooter.docx')
    base2 = os.path.join(indir2,'PageFooter.docx')
    
    ifile = os.path.join(indir,'2017 1-year data dictionary.docx')
    ifilea = os.path.join(indir,'2017 1-year data dictionary v2.docx')
    ifile2 = os.path.join(indir2,'2017 1-year data dictionary.docx')
    ifile2a = os.path.join(indir2,'2017 1-year data dictionary v2.docx')

    remove_file(base)
    remove_file(base2)
    remove_file(ifile)
    remove_file(ifilea)
    remove_file(ifile2)
    remove_file(ifile2a)

    """ Test before creation of files  """
    assert assign_infile(args,indir) == None

    """ Create default base file but should fail with absence of default input file """
    create_file(base)
    assert assign_infile(args,indir) == None

    """ Create input file and should pass """
    create_file(ifile)
    assert assign_infile(args,indir) == [ ifile, base ]

    """ Change year and the default ifile changes but does not exist """
    args.yyyy = 2016
    assert assign_infile(args,indir) == None
    args.yyyy = 2017

    """ Delete the default base file and it should fail again """
    remove_file(base)
    assert assign_infile(args,indir) == None

    """ Test custom file name in same directory but no base file """
    remove_file(ifile)
    create_file(ifilea)
    args.ifile = ifilea
    assert assign_infile(args,indir) == None

    """ Recreate the base file and continue using custom name """
    create_file(base)
    assert assign_infile(args,indir) == [ ifilea, base ]

    """ Test default file name but in alternate directory, base file unmoved """
    remove_file(ifilea)
    create_file(ifile2)
    args.ifile = ''
    assert assign_infile(args,indir2) == None

    """ Test default input file name but in alternate directory, delete base file """
    remove_file(base)
    assert assign_infile(args,indir2) == None

    """ Test both default input file and base in alternate directory """
    create_file(base2)
    assert assign_infile(args,indir2) == [ ifile2, base2 ]

    """ Test both default custom input file and base in alternate directory """
    remove_file(ifile2)
    create_file(ifile2a)
    args.ifile = ifile2a
    assert assign_infile(args,indir2) == [ ifile2a, base2 ]
    assert assign_infile(args,indir) == [ ifile2a, base2 ]

    """ If base does not exist in either default or custom directory it fails """
    remove_file(base2)
    assert assign_infile(args,indir2) == None
    assert assign_infile(args,indir) == None

    """ If base is not in custom directory but is in default it will choose default """
    create_file(base)
    assert assign_infile(args,indir2) == None
    assert assign_infile(args,indir) == [ ifile2a, base ]

    """ If base exists in both default and custom directory it will choose the custom """
    create_file(base2)
    assert assign_infile(args,indir2) == [ ifile2a, base2 ]
    assert assign_infile(args,indir) == [ ifile2a, base2 ]
    
    """ Clean up temporary files in indir """
    remove_file(base)
    remove_file(ifile)
    remove_file(ifilea)
    remove_dir(indir)
    
    remove_file(base2)
    remove_file(ifile2)
    remove_file(ifile2a)
    remove_dir(indir2)

def test_assign_outfiles():
    outdir = '/tmp/pumsout'
    outdir2 = '/tmp/pumsout2'
    remove_dir(outdir)
    remove_dir(outdir2)

    args.yyyy = 2017
    args.period = 1
    args.ifile = ''
    args.outdir = ''

    """ Test before create directory """
    assert assign_outdir(args,outdir) == None

    """ Test default path """
    create_dir(outdir)
    assert assign_outdir(args,outdir) == outdir

    """ Test alternate path before create but with default exist """
    args.outdir = outdir2
    assert assign_outdir(args,outdir) == None

    """ Test alternate path before create but with default does not exist """
    remove_dir(outdir)
    assert assign_outdir(args,outdir) == None

    """ Test alternate path after create alternate path """
    create_dir(outdir2)
    assert assign_outdir(args,outdir) == outdir2

    """ Test alternate path after recreate default path """
    create_dir(outdir)
    assert assign_outdir(args,outdir) == outdir2

    remove_dir(outdir)
    remove_dir(outdir2)
    
def test_assign_outfiles():
    outdir = '/tmp/pumsout'
    outdir2 = '/tmp/pumsout2'
    create_dir(outdir)
    create_dir(outdir2)
    args = fakeparse(2017,1)

    prefix = 'PUMS_Data_Dictionary_'
    
    """ Test with 2017 1-year """
    assert assign_outfiles(args,outdir) == \
        [ os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.docx'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.txt'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.csv'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.log')]

    """ If any of the output files already exist with replace = False, will fail """
    create_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.docx'))
    assert assign_outfiles(args,outdir) == None
    remove_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.docx'))
                
    create_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.txt'))
    assert assign_outfiles(args,outdir) == None
    remove_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.txt'))
                
    create_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.csv'))
    assert assign_outfiles(args,outdir) == None
    remove_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.csv'))
                
    """ If any of the output files already exist with replace = True, will pass """
    args.replace = True
                
    create_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.docx'))
    assert assign_outfiles(args,outdir) == \
        [ os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.docx'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.txt'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.csv'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.log')]
    remove_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.docx'))
                
    create_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.txt'))
    assert assign_outfiles(args,outdir) == \
        [ os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.docx'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.txt'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.csv'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.log')]
    remove_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.txt'))
                
    create_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.csv'))
    assert assign_outfiles(args,outdir) == \
        [ os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.docx'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.txt'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.csv'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.log')]
    remove_file(os.path.join(outdir,'PUMS_Data_Dictionary_2017' + '.csv'))
                
    """ Test 2017 5-year """
    args.period = 5
    assert assign_outfiles(args,outdir) == \
        [ os.path.join(outdir,'PUMS_Data_Dictionary_2013-2017' + '.docx'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2013-2017' + '.txt'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2013-2017' + '.csv'),
          os.path.join(outdir,'PUMS_Data_Dictionary_2013-2017' + '.log')]
    
    """ Test with 2017 1-year """
    args.period = 1
    assert assign_outfiles(args,outdir2) == \
        [ os.path.join(outdir2,'PUMS_Data_Dictionary_2017' + '.docx'),
          os.path.join(outdir2,'PUMS_Data_Dictionary_2017' + '.txt'),
          os.path.join(outdir2,'PUMS_Data_Dictionary_2017' + '.csv'),
          os.path.join(outdir2,'PUMS_Data_Dictionary_2017' + '.log')]

