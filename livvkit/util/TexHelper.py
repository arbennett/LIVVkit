"""
TODO
"""
import os
import glob
import pprint

import livvkit
from livvkit.util import TexHelper as th
from livvkit.util import functions

def write_tex():
    """
    TODO
    """
    datadir = livvkit.index_dir 
    outdir = os.path.join(datadir, "tex")
    functions.mkdir_p(outdir)
    
    data_files = glob.glob(datadir + "/**/*.json", recursive=True)
    
    for each in data_files:
        data = functions.read_json(each)
        tex = th.translate_page(data)
        outfile = os.path.join(outdir, os.path.basename(each).replace('json', 'tex'))
        with open(outfile, 'w') as f:
            f.write(tex)


def translate_page(data):
    """
    TODO
    """
    if "Page" != data["Type"]:
        return ""

    tex_str =  (
r'''
\documentclass{article} 
\usepackage{placeins}
\title{LIVVkit}
\author{$USER}
\begin{document}
\maketitle
'''.replace('$USER', livvkit.user)
)                  

    content = data["Data"]
    for tag_name in ["Elements", "Tabs"]:
        for tag in content.get(tag_name, []):
            try:
                tex_str += translate_map[tag["Type"]](tag)
            except:
                continue
 
    tex_str += (
r'''
\end{document}
'''
)
    return tex_str


def translate_section(data):
    raise NotImplementedError


def translate_tab(data):
    pass


def translate_summary(data):
    summary = '\\FloatBarrier \n \\section{$NAME} \n'.replace('$NAME', data.get("Title", "Summary"))
    summary += '\\begin{table} \n \\begin{center} \n \\begin{tabular}{lccc} \n'
    
    headers = data.get("Headers", [])
    n_cols = len(headers)
    spacer =  ' &' * n_cols + r'\\[.5em]'
    for header in headers:
        summary += '& $HEADER '.replace('$HEADER', header).replace('%', '\%')
    summary += ' \\\\ \hline \n'
    
    names = sorted(data.get("Data", []).keys())
    for name in names:
        summary += '\n\n \\textbf{$NAME} $SPACER \n'.replace('$NAME', name).replace('$SPACER', spacer)
        cases = data.get("Data", []).get(name, {})
        for case, c_data in cases.items():
            summary += ' $CASE & '.replace('$CASE', str(case))
            for header in headers:
                h_data = c_data.get(header, "")
                if list is type(h_data) and len(h_data) == 2:
                    summary += (' $H_DATA_0 of $H_DATA_1 &'
                                .replace('$H_DATA_0', str(h_data[0]))
                                .replace('$H_DATA_1', str(h_data[1]))
                                .replace('%', '\%'))
                else:
                    summary += ' $H_DATA &'.replace('$H_DATA', str(h_data)).replace('%','\%')

            # This takes care of the trailing & that comes from processing the headers.  
            summary = summary[:-1] + r' \\'
    
    summary += '\n \end{tabular} \n \end{center} \n \end{table}\n'
    return summary 


def translate_table(data):
    pass


def translate_bit_for_bit(data):
    pass


def translate_gallery(data):
    pass


def translate_image(data):
    pass


def translate_file_diff(data):
    pass


def translate_error(data):
    pass

# Map element types to translations
translate_map = {
           "Summary"     : translate_summary,
           "Section"     : translate_section,
           "Tab"         : translate_tab,
           "Table"       : translate_table,
           "Bit for Bit" : translate_bit_for_bit,
           "Gallery"     : translate_gallery,
           "Image"       : translate_image,
           "File Diff"   : translate_file_diff,
           "Error"       : translate_error
       }   


