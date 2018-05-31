from print_txt import \
    print_title, \
    print_reldate, \
    print_header, \
    print_var_name, \
    print_var_desc, \
    print_var_val, \
    print_note
from docx_output import \
    initialize_doc, \
    docx_out_title, \
    docx_out_reldate, \
    docx_out_header, \
    docx_out_var_name, \
    docx_out_var_desc, \
    docx_out_var_val, \
    docx_out_note

def output_title( title, ofile, doc ):
    print_title   ( title, ofile )
    docx_out_title( title, doc )
    return;

def output_reldate( reldate, ofile, doc ):
    print_reldate   ( reldate, ofile )
    docx_out_reldate( reldate, doc )
    return;

def output_header(name,level,ofile,dfile):
    print_header(name,ofile)
    docx_out_header(name,level,dfile)
    return;

def output_var_name( var_name, var_type, var_len, var_desc, ofile, doc, vfile, tabsep = 'NO' ):
    if len(var_name) > 10:
        print('WARNING: ' + var_name + ' has length ' + str(len(var_name)))
        print('-------: A variable of length 12 will not have any whitespace separation.')
    if var_type == 'C':
        var_type_str = 'Character'
    elif var_type == 'N':
        var_type_str = 'Numeric'
    vfile.write( 'NAME,' + var_name + ',' + var_type + ',' + str(var_len) + ',"' + var_desc + '"\n' )
    print_var_name   ( var_name, var_type_str, var_len, ofile, tabsep )
    docx_out_var_name( var_name, var_type_str, var_len, doc )
    return;

def output_var_desc( var_desc, ofile, doc, wrap_text = 'NO', indent = 'NO', tabindent = 'NO' ):
    print_var_desc   ( var_desc, ofile, wrap_text, indent, tabindent )
    docx_out_var_desc( var_desc, doc )
    return;

def output_var_val( var_name, var_type, var_len, var_val, var_val_desc, ofile, doc, vfile,
                    wrap_text = 'NO', tabindent = 'NO', tabsep = 'NO', cust_width = 'NO' ):
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
    vfile.write( 'VAL,' + var_name + ',' + var_type + ',' + str(var_len) + ',' + var_low + ',' + var_hi
                 + ',"' + var_val_desc +'"\n') 
    print_var_val   ( var_val, var_val_desc, var_len, ofile, wrap_text, tabindent, tabsep )
    docx_out_var_val( var_val, var_val_desc, var_len, doc, wrap_text='YES', custom_width=cust_width)
    return;

def output_note( note, ofile, doc, wrap_text = 'NO', urls = 'YES'):
    print_note   ( note, ofile, wrap_text )
    docx_out_note( note, doc,   urls )
    return;

def output_var_block(pl,dd,ofile,dfile,cfile,custom='DEFAULT'):
    output_title(pl.title, ofile, dfile)
    output_reldate(pl.reldate, ofile, dfile)

    for nrt in range(len(pl.rts)):
        rt = pl.rts[nrt]
        desc = rt.desc
        level = 1
        output_header(desc, level, ofile, dfile)
        
        for nsrt in range(len(rt.srts)):
            srt = rt.srts[nsrt]
            desc = srt.desc
            level = 2

            if len(rt.srts) > 1:
                output_header(desc, level, ofile, dfile)
            
            for varname in srt.vars:
                v = dd.vars[dd.vardict[varname]]
                varlen = v.varlen
                vartype = v.vartype
                vardesc = v.vardesc
                valdict = v.valdict
              
                output_var_name(varname, vartype, varlen, vardesc, ofile, dfile, cfile, tabsep = 'NO')
                output_var_desc(vardesc, ofile, dfile, wrap_text='NO',indent='NO',tabindent='NO')

                if custom != 'DEFAULT':
                    maxlen = varlen
                    for key in valdict.keys():
                        if len(key) > maxlen:
                            maxlen = len(key)
                    if maxlen > varlen:
                        custom_wid = 'NO'
                    else:
                        custom_wid = 'YES'
                else:
                    custom_wid = 'NO'
                for varval in valdict.keys():
                    valdesc = valdict[varval]
                    output_var_val(varname, vartype, varlen, varval, valdesc, ofile, dfile, cfile,
                                   wrap_text='NO',tabindent='NO',tabsep='NO',cust_width=custom_wid)
