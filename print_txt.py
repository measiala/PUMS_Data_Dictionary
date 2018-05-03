#!/usr/bin/python3

import textwrap
import sys
#from string import maketrans

def print_line( line, ofile='print', platform='unix' ):
    indblq = '“”'
    outdblq = '""'
    insq = "’"
    outsq = "'"
    inemd = '—–'
    outemd = '--'
    trdbl = str.maketrans(indblq, outdblq)
    trsng = str.maketrans(insq,   outsq)
    tremd = str.maketrans(inemd,  outemd)
    line = line.translate(trdbl).translate(trsng).translate(tremd)
    if ofile == 'print':
        print(line)
    else:
        # DOS platform ends lines with CRLF
        if platform == 'dos':
            line = line.replace('\n', '\r\n')
            ofile.write(line + '\r\n')
        # Older MAC platform ends lines with CR only
        elif platform == 'mac':
            line = line.replace('\n', '\r')
            ofile.write(line + '\r')
        # Otherwise default to UNIX ending of LF     
        else:
            ofile.write(line + '\n')
    return line

def print_title( title, ofile='print' ):
    line = title
    print_line(line, ofile)
    return line

def print_date( reldate, ofile='print' ):
    line = reldate + '\n'
    print_line(line, ofile)
    return line

def print_header( header, ofile='print' ):
    line = '\n' + header
    print_line(line, ofile)
    return line

def print_var_name( var_name, var_len, ofile='print', tabsep = 'NO' ):
    if len(var_name) < 12:
        if tabsep == 'YES':
            line = '\n{0}\t{1}'.format(var_name, var_len)
        else:
            line = '\n{0:12}{1}'.format(var_name, var_len)
            print_line(line, ofile)
        return line
    return None

def print_var_desc( var_desc, ofile='print', wrap_text = 'YES',
                    indent = 'NO', tabindent = 'NO' ):
    if indent == 'NO':
        indtxt = ''
    elif tabindent == 'YES':
        indtxt = '\t'
    else:
        indtxt = '{:6}'.format('')
        
    if wrap_text == 'YES':
        lines = textwrap.wrap(textwrap.dedent(var_desc).strip(), width=72)
        for i in range(len(lines)):
            lines[i] = indtxt + lines[i]
            print_line( lines[i], ofile )
        return lines
    else:
        line = indtxt + var_desc
        print_line(line, ofile)
        return line

def print_var_val( var_val, var_val_desc, var_len, ofile='print',
                   wrap_text = 'NO', tabindent = 'NO', tabsep = 'NO' ):
    if tabindent == 'YES':
        indtxt = '\t\t'
    else:
        indtxt = '{:12}'.format('')

    def fmtval( varval, varlen, varvaldesc, tabsepflag = tabsep ):
        if tabsepflag == 'YES':
            fmtline = '{0}\t.{1}'.format(varval, varvaldesc)
        else:
            fmtline = '{0:{1}}.{2}'.format(str(varval),str(2*int(varlen) + 3),varvaldesc)
        return fmtline;

    if wrap_text == 'YES':
        max_wd = 78 - 12 - 2*var_len - 2 - 1
        rlines = textwrap.wrap(textwrap.dedent(var_val_desc).strip(), width=max_wd)
        fmtline = fmtval( var_val, var_len, rlines[0], tabsep )
        lines = [ indtxt + fmtline ]
        print_line( lines[0], ofile )
        
        if len(rlines) > 1:
            for i in range(1,len(rlines)):
                fmtline = fmtval( '', var_len, rlines[i], tabsep )
                lines.append(indtxt + fmtline)
                print_line( lines[i], ofile )
        return lines    
    else:
        fmtline = fmtval( var_val, var_len, var_val_desc, tabsep )
        line = indtxt + fmtline
        print_line( line, ofile)
        return line

def print_note( note, ofile='print', wrap_text = 'YES' ):
    if wrap_text == 'YES':
        line = '\n' + textwrap.fill(textwrap.dedent(note).strip(), width=78)
    else:
        line = '\n' + note
    print_line(line, ofile)
    return line

