from print_txt import \
    print_title, \
    print_date, \
    print_header, \
    print_var_name, \
    print_var_desc, \
    print_var_val, \
    print_note
from docx_output import \
    initialize_doc, \
    docx_out_title, \
    docx_out_date, \
    docx_out_header, \
    docx_out_var_name, \
    docx_out_var_desc, \
    docx_out_var_val, \
    docx_out_note

def output_title( title, ofile, doc ):
    print_title   ( title, ofile )
    docx_out_title( title, doc )
    return;

def output_date( reldate, ofile, doc ):
    print_date   ( reldate, ofile )
    docx_out_date( reldate, doc )
    return;

def output_header(name,level,ofile,dfile):
    print_header(name,ofile)
    docx_out_header(name,level,dfile)
    return;

def output_var_name( var_name, var_type, var_len, ofile, doc, vfile, tabsep = 'NO' ):
    if len(var_name) > 10:
        print('ERROR: ' + var_name + ' has length ' + str(len(var_name)))
    vfile.write( 'N: ' + var_type + ',' + var_name + ',' + str(var_len) + '\n' )
    print_var_name   ( var_name, var_len, ofile, tabsep )
    docx_out_var_name( var_name, var_len, doc )
    return;

def output_var_desc( var_desc, ofile, doc, wrap_text = 'NO', indent = 'NO', tabindent = 'NO' ):
    print_var_desc   ( var_desc, ofile, wrap_text, indent, tabindent )
    docx_out_var_desc( var_desc, doc )
    return;

def output_var_val( var_name, var_type, var_len, var_val, var_val_desc, ofile, doc, vfile,
                    wrap_text = 'NO', tabindent = 'NO', tabsep = 'NO' ):
    vwords = var_val.split('..')
    if len(vwords) == 1:
        var_low = var_val
        var_hi  = var_val
    elif len(vwords) == 2:
        var_low = vwords[0]
        var_hi  = vwords[1]
    else:
        var_low = 'ERR'
        var_hi  = 'ERR'
    vfile.write( 'V: ' + var_type + ',' + var_name + ',' + str(var_len) + ',' + var_low + ',' + var_hi + '\n') 
    print_var_val   ( var_val, var_val_desc, var_len, ofile, wrap_text, tabindent, tabsep )
    docx_out_var_val( var_val, var_val_desc, var_len, doc  , wrap_text = 'YES')
    return;

def output_note( note, ofile, doc, wrap_text = 'NO', urls = 'YES'):
    print_note   ( note, ofile, wrap_text )
    docx_out_note( note, doc,   urls )
    return;

def output_var_block(dd,ofile,dfile,cfile):
    for vi in range(len(dd.vars)):
        for hi in range(len(dd.headers)):
            if dd.headers[hi].pos == vi:
                h = dd.headers[hi]
                name = h.name
                level = h.level
                htype = h.htype
                output_header(name, level, ofile, dfile)
        v = dd.vars[vi]
        varname = v.name
        varlen = v.varlen
        vartype = v.vartype
        vardesc = v.vardesc
        valdict = v.valdict

        output_var_name(varname, vartype, varlen, ofile, dfile, cfile, tabsep = 'NO')
        output_var_desc(vardesc, ofile, dfile, wrap_text='NO',indent='NO',tabindent='NO')
        for varval in valdict.keys():
            valdesc = valdict[varval]
            output_var_val(varname, vartype, varlen, varval, valdesc, ofile, dfile, cfile,
                           wrap_text='NO',tabindent='NO',tabsep='NO')
