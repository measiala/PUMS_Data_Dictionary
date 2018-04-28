import os

def assign_yyyy(args):
    if args.yyyy < 2000 or args.yyyy > 2017:
        print("Error: YYYY must be in (2000,2017).")
    else:
        return args.yyyy
    return None

def assign_period(args):
    if args.period == 1:
        if args.yyyy > 1999:
            return args.period
    elif args.period == 3:
        if args.yyyy > 2006 and args.yyyy < 2014:
            return args.period
        else:
            print("Error: PERIOD = 3 must have YYYY in (2007,2013)")
    elif args.period == 5:
        if args.yyyy > 2008 and args.yyyy < 2018:
            return args.period
        else:
            print("Error: PERIOD = 5 must have YYYY in (2009,2017)")
    return None

def assign_infile(args,indir):
    """ Input file incomplete """
    if args.ifile and os.path.isfile(args.ifile):
        return args.ifile
    else:
        if os.path.exists(indir):
            def_ifile = os.path.join(
                indir,str(args.yyyy) + ' ' + str(args.period) + '-year data dictionary.docx')
            def_base = os.path.join(indir,'PageFooter.docx')
            if os.path.isfile(def_ifile) and os.path.isfile(def_base):
                return [def_ifile,def_base]
            else:
                print("Error: Neither the default input file nor user-provided input files exists.")
        else:
            print("Error: The default input directory does not exist.")
    return None
        
def assign_outdir(args,outdir):
    if args.outdir and os.path.exists(args.outdir):
        return args.outdir
    elif os.path.exists(outdir):
        return outdir
    else:
        print("Error: Neither the default output directory nor user-provided output directory exists.")
    return None
        
def assign_outfiles(args,outdir):
    if args.period == 1:
        yr_rng = str(args.yyyy)
    else:
        yr_rng = str(args.yyyy - args.period + 1) + '-' + str(args.yyyy)

    outtxt = os.path.join(outdir,'PUMS_Data_Dictionary_' + yr_rng + '.txt')
    outdoc = os.path.join(outdir,'PUMS_Data_Dictionary_' + yr_rng + '.docx')
    outcsv = os.path.join(outdir,'PUMS_Data_Dictionary_' + yr_rng + '.csv')

    if args.replace:
        return [ outdoc, outtxt, outcsv ]
    else:
        if os.path.exists(outdoc):
            print("Error: User did not choose replace option and output Word document exists.")
        elif os.path.exists(outtxt):
            print("Error: User did not choose replace option and output Text document exists.")
        elif os.path.exists(outcsv):
            print("Error: User did not choose replace option and output CSV document exists.")
        else:
            return [ outdoc, outtxt, outcsv ]
    return [ None, None, None ]
