import os

def assign_yyyy(args):
    if args.yyyy < 2000 or args.yyyy > 2099:
        print("ERROR: YYYY must be in [2000,3000).")
    else:
        return args.yyyy
    return None

def assign_period(args):
    if args.period == 1:
        if args.yyyy > 1999 and args.yyyy < 3000:
            return args.period
    elif args.period == 3:
        if args.yyyy > 2006 and args.yyyy < 2014:
            return args.period
        else:
            print("ERROR: ERROR: PERIOD = 3 must have YYYY in (2007,2013)")
    elif args.period == 5:
        if args.yyyy > 2008 and args.yyyy < 3000:
            return args.period
        else:
            print("ERROR: ERROR: PERIOD = 5 must have YYYY in (2009,2017)")
    return None

def assign_infile(args,indir):
    """ Check if custom ifile specified """
    if args.ifile:
        """ ifile is specified check if it exists """
        if os.path.isfile(args.ifile):
            """ Check custom directory for PageFooter.docx """
            cindir = os.path.split(args.ifile)[0]
            def_base = os.path.join(cindir,'PageFooter.docx')
            if os.path.isfile(def_base):
                """ PageFooter.docx found in custom directory """
                return [args.ifile,def_base]
            else:
                """ Check default directory for PageFooter.docx """
                def_base = os.path.join(indir,'PageFooter.docx')
                if os.path.isfile(def_base):
                    """ PageFooter.docx found in default directory """
                    return [args.ifile,def_base]
                else:
                    print("ERROR: PageFooter.docx not found in %s or in %s." % (cindir,indir))
        else:
            print("ERROR: Custom input file %s specified but does not exist." % args.ifile)
    else:
        """ If no custom ifile then we look in default directory using default name """
        if os.path.exists(indir):
            def_ifile = os.path.join(
                indir,str(args.yyyy) + ' ' + str(args.period) + '-year data dictionary.docx')
            def_base = os.path.join(indir,'PageFooter.docx')
            if os.path.isfile(def_ifile):
                if os.path.isfile(def_base):
                    return [def_ifile,def_base]
                else:
                    print("ERROR: Default input file %s not found." % def_base)
            else:
                print("ERROR: Default input file %s not found." % def_ifile)
        else:
            print("ERROR: The default input directory %s does not exist." % indir)
    return None
        
def assign_outdir(args,outdir):
    """ Check if outdir was specified """
    if args.outdir:
        """ Check if custom outdir exists """
        if os.path.exists(args.outdir):
            return args.outdir
        else:
            print("ERROR: Custom output path %s specified but does not exist." % args.outdir)
    else:
        """ Otherwise evaluate default outdir """
        if os.path.exists(outdir):
            return outdir
        else:
            print("ERROR: Default output path %s does not exist." % outdir)
    return None
        
def assign_outfiles(args,outdir):
    if args.period == 1:
        yr_rng = str(args.yyyy)
    else:
        yr_rng = str(args.yyyy - args.period + 1) + '-' + str(args.yyyy)

    outtxt = os.path.join(outdir,'PUMS_Data_Dictionary_' + yr_rng + '.txt')
    outdoc = os.path.join(outdir,'PUMS_Data_Dictionary_' + yr_rng + '.docx')
    outcsv = os.path.join(outdir,'PUMS_Data_Dictionary_' + yr_rng + '.csv')
    outlog = os.path.join(outdir,'PUMS_Data_Dictionary_' + yr_rng + '.log')

    if args.replace:
        return [ outdoc, outtxt, outcsv, outlog ]
    else:
        if os.path.exists(outdoc):
            print("ERROR: User did not choose replace option and output Word document exists.")
        elif os.path.exists(outtxt):
            print("ERROR: User did not choose replace option and output Text document exists.")
        elif os.path.exists(outcsv):
            print("ERROR: User did not choose replace option and output CSV document exists.")
        else:
            return [ outdoc, outtxt, outcsv, outlog ]
    return None
