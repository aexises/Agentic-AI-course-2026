"""Build matching Markdown and LaTeX from the course's restricted Markdown sources.

Only the documented source subset is accepted. No model, network, Pandoc, or TeX
process is invoked. Run from any directory with Python 3.10 or newer.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import io
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CITATION = re.compile(r'\[@([a-z0-9-]+)(?:;\s*@[a-z0-9-]+)*\]')
INLINE = re.compile(r'(`[^`\n]+`|\$[^$\n]+\$|\*\*[^*\n]+\*\*|\[@[a-z0-9-]+(?:;\s*@[a-z0-9-]+)*\]|\[[^\]\n]+\]\([^\s)]+\))')
ESCAPES = {'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}


def escape(text):
    return ''.join(ESCAPES.get(c,c) for c in text)


def keys(token):
    return re.findall(r'@([a-z0-9-]+)',token)


def inline(text, references):
    output=[]
    for part in INLINE.split(text):
        if part.startswith('`') and part.endswith('`'):
            output.append(r'\texttt{'+escape(part[1:-1])+'}')
        elif part.startswith('$') and part.endswith('$'):
            output.append(r'\('+part[1:-1]+r'\)')
        elif part.startswith('**') and part.endswith('**'):
            output.append(r'\textbf{'+escape(part[2:-2])+'}')
        elif CITATION.fullmatch(part):
            cited=keys(part)
            if any(k not in references for k in cited):
                raise ValueError('Unknown citation: '+part)
            output.append(r'\cite{'+','.join(cited)+'}')
        elif re.fullmatch(r'\[[^\]]+\]\([^\s)]+\)',part):
            label,url=re.fullmatch(r'\[([^\]]+)\]\(([^\s)]+)\)',part).groups()
            if any(c in url for c in '{}\\'):
                raise ValueError('Unsafe link syntax')
            output.append(r'\href{'+url.replace('%',r'\%').replace('#',r'\#')+'}{'+escape(label)+'}')
        else:
            if any(marker in part for marker in ('[@','`','$','**')):
                raise ValueError('Unclosed or unsupported inline syntax: '+part)
            output.append(escape(part))
    return ''.join(output)


def to_latex(source, references, unnumbered=False):
    out=[]; paragraph=[]; mode=None; buffer=[]; list_kind=None
    def flush():
        if paragraph:
            out.append(inline(' '.join(paragraph),references)+'\n')
            paragraph.clear()
    def close_list():
        nonlocal list_kind
        if list_kind:
            out.append(r'\end{'+list_kind+'}\n'); list_kind=None
    for line in source.splitlines():
        if mode=='code':
            if line=='```':
                if any(r'\end{Verbatim}' in x for x in buffer):
                    raise ValueError('Verbatim terminator in code')
                out.append(r'\begin{Verbatim}[breaklines=true,breakanywhere=true,fontsize=\small,frame=single]'+'\n'+'\n'.join(buffer)+'\n'+r'\end{Verbatim}'+'\n')
                mode=None; buffer=[]
            else: buffer.append(line)
            continue
        if mode=='math':
            if line=='$$':
                if not buffer: raise ValueError('Empty display math')
                out.append(r'\begin{equation}'+'\n'+'\n'.join(buffer)+'\n'+r'\end{equation}'+'\n')
                mode=None; buffer=[]
            else: buffer.append(line)
            continue
        if line.startswith('```'):
            if line not in ('```python','```text','```bash','```'):
                raise ValueError('Unsupported code fence: '+line)
            flush(); close_list(); mode='code'; continue
        if line=='$$':
            flush(); close_list(); mode='math'; continue
        if not line.strip():
            flush(); continue
        heading=re.fullmatch(r'(#{1,3}) (.+)',line)
        if heading:
            flush(); close_list()
            level,title=heading.groups(); command={1:'chapter',2:'section',3:'subsection'}[len(level)]
            if unnumbered:
                out.append('\\'+command+'*{'+inline(title,references)+'}')
                out.append(r'\addcontentsline{toc}{'+command+'}{'+escape(title)+'}')
            else: out.append('\\'+command+'{'+inline(title,references)+'}')
            continue
        item=re.fullmatch(r'(\d+\.|-) (.+)',line)
        if item:
            flush(); kind='itemize' if item[1]=='-' else 'enumerate'
            if kind!=list_kind:
                close_list(); list_kind=kind; out.append(r'\begin{'+kind+'}')
            out.append(r'\item '+inline(item[2],references)); continue
        if line.startswith(('>','|','#')) or (line[:1].isspace()):
            raise ValueError('Unsupported block syntax: '+line)
        close_list(); paragraph.append(line)
    if mode: raise ValueError('Unclosed '+mode+' block')
    flush(); close_list()
    return '\n'.join(out)+'\n'


def markdown(source, numbers):
    def replace(match):
        return ' '.join(f'[{numbers[k]}](#ref-{k})' for k in keys(match[0]))
    return CITATION.sub(replace,source)


def write(path, text, check):
    if check:
        if not path.is_file() or path.read_text()!=text:
            raise ValueError('Stale or missing generated file: '+str(path.relative_to(ROOT)))
    else:
        path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text)


def build(check=False):
    entries=json.loads((ROOT/'textbook/references.json').read_text())
    refs={r['key']:r for r in entries}
    if len(refs)!=len(entries): raise ValueError('Duplicate bibliography key')
    chapters=sorted((ROOT/'chapters').glob('[0-9][0-9]-*.md'))
    if len(chapters)!=13: raise ValueError('Expected thirteen chapters')
    front=ROOT/'textbook/preface.md'
    appendices=[ROOT/'textbook/appendix-mathematics.md',ROOT/'textbook/appendix-case-study.md',ROOT/'textbook/selected-answers.md']
    files=[front,*chapters,*appendices]
    sources={p:p.read_text() for p in files}
    used=[]
    for source in sources.values():
        for match in CITATION.finditer(source):
            for key in keys(match[0]):
                if key not in refs: raise ValueError('Unknown citation '+key)
                if key not in used: used.append(key)
    unused=set(refs)-set(used)
    if unused: raise ValueError('Unused references: '+','.join(sorted(unused)))
    numbers={key:i+1 for i,key in enumerate(used)}
    title='# Agentic AI: Principles, Systems, and Practice\n\nA course textbook · Source edition, 9 September 2026\n\n'
    toc=['## Contents\n']
    for index,p in enumerate(chapters,1):
        name=sources[p].splitlines()[0][2:]; toc.append(f'{index}. [{name}](#chapter-{index})')
    toc.extend(['','[Mathematical foundations](#appendix-1) · [End-to-end case](#appendix-2) · [Selected answers](#appendix-3) · [References](#references)',''])
    parts=[title,'\n'.join(toc),markdown(sources[front],numbers)]
    for i,p in enumerate(chapters,1): parts.append(f'<a id="chapter-{i}"></a>\n\n'+markdown(sources[p],numbers))
    for i,p in enumerate(appendices,1): parts.append(f'<a id="appendix-{i}"></a>\n\n'+markdown(sources[p],numbers))
    bibliography=['<a id="references"></a>\n\n# References\n\nYears for arXiv papers denote initial preprints unless stated otherwise. Documentation was accessed on 9 September 2026. Institutional attribution is used for institutional reports; see the linked work for its full contributor list.\n']
    bibtex=[]; texbib=[r'\begin{thebibliography}{99}']
    for key in used:
        r=refs[key]
        description=f"{r['author']} ({r['year']}). {r['title']}. {r['kind']}."
        bibliography.append(f'<a id="ref-{key}"></a>\n\n**[{numbers[key]}]** {r["author"]} ({r["year"]}). [{r["title"]}]({r["url"]}). {r["kind"]}.\n')
        texbib.extend([r'\bibitem{'+key+'}',escape(description)+r' \url{'+r['url']+'}.'])
        bibtex.append('@misc{'+key+',\n  author = {{'+escape(r['author'])+'}},\n  title = {{'+escape(r['title'])+'}},\n  year = {'+r['year']+'},\n  howpublished = {\\url{'+r['url']+'}},\n  note = {'+escape(r['kind']+'; accessed '+r['checked'])+'}\n}\n')
    texbib.append(r'\end{thebibliography}')
    parts.append('\n'.join(bibliography))
    write(ROOT/'STUDYBOOK.md','\n\n'.join(parts),check)
    texdir=ROOT/'textbook/latex'
    write(texdir/'preface.tex',to_latex(sources[front],refs,True),check)
    for p in chapters: write(texdir/'chapters'/p.with_suffix('.tex').name,to_latex(sources[p],refs),check)
    for p in appendices: write(texdir/p.with_suffix('.tex').name,to_latex(sources[p],refs),check)
    write(texdir/'bibliography.tex','\n'.join(texbib)+'\n',check)
    write(ROOT/'textbook/references.bib','\n'.join(bibtex),check)
    main=r'''\documentclass[11pt,oneside,openany]{book}
\usepackage[a4paper,margin=28mm]{geometry}
\usepackage{fontspec}
\setmainfont{Latin Modern Roman}
\setsansfont{Latin Modern Sans}
\setmonofont{Latin Modern Mono}
\usepackage{amsmath,amssymb}
\usepackage{microtype}
\usepackage{fvextra}
\usepackage{xcolor}
\usepackage{xurl}
\usepackage[unicode,colorlinks=true,linkcolor=blue!45!black,citecolor=blue!45!black,urlcolor=blue!45!black]{hyperref}
\hypersetup{pdftitle={Agentic AI: Principles, Systems, and Practice},pdfauthor={},pdfcreator={}}
\setlength{\emergencystretch}{3em}
\setcounter{tocdepth}{1}
\title{Agentic AI\\[0.5em]\Large Principles, Systems, and Practice}
\author{}
\date{Source edition\\9 September 2026}
\begin{document}
\frontmatter
\maketitle
\tableofcontents
\input{preface.tex}
\mainmatter
'''
    main+='\n'.join(r'\input{chapters/'+p.with_suffix('.tex').name+'}' for p in chapters)
    main+='\n\\appendix\n'+'\n'.join(r'\input{'+p.with_suffix('.tex').name+'}' for p in appendices)
    main+='\n\\backmatter\n\\cleardoublepage\n\\phantomsection\n\\addcontentsline{toc}{chapter}{Bibliography}\n\\input{bibliography.tex}\n\\end{document}\n'
    write(texdir/'main.tex',main,check)
    coverage=['# Textbook source checks\n\nChecked 9 September 2026. Citations identify external research or interface facts. The equipment examples, exercises, design proposals, and conditional mathematical derivations are original teaching material. No empirical result is inferred from an illustrative number.\n\nThe checks are (1) source identity/type/year, (2) support for the narrow attributed method or claim, and (3) scope and interpretation. This is not three independent replications.\n']
    for key in used:
        r=refs[key]
        cited=[p.name for p,s in sources.items() if any(key in keys(m[0]) for m in CITATION.finditer(s))]
        coverage.append(f'## {key}\n\n[{r["title"]}]({r["url"]}) — {r["kind"]}; {r["year"]}.\n\nChecked passage: {r["locator"]}.\n\nScope: {r["scope"]}\n\nUsed in: '+', '.join(cited)+'\n')
    write(ROOT/'textbook/SOURCE-CHECKS.md','\n'.join(coverage),check)
    manifest={'edition':'2026-09-09-textbook','chapters':13,'chapter_words':sum(len(sources[p].split()) for p in chapters),'instructional_words':sum(len(s.split()) for s in sources.values()),'references':len(used),'exercises':sum(len(re.findall(r'^\d+\. ',s.split('## Exercises\n')[1].split('## Further study')[0],re.M)) for p,s in sources.items() if p in chapters),'latex_compiled':False,'sources':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [*files,ROOT/'textbook/references.json']]}
    write(ROOT/'textbook/build-manifest.json',json.dumps(manifest,indent=2)+'\n',check)
    archive_files={str(p.relative_to(texdir)):p.read_bytes() for p in sorted(texdir.rglob('*.tex'))}
    archive_files['references.bib']=(ROOT/'textbook/references.bib').read_bytes()
    archive_files['COMPILE.txt']=b"Compile main.tex with XeLaTeX or LuaLaTeX, twice. No BibTeX/Biber or shell escape is needed. On Overleaf select main.tex and the XeLaTeX compiler. Required packages: geometry, fontspec, amsmath, amssymb, microtype, fvextra, xcolor, xurl, hyperref; fonts: Latin Modern. PDF compilation and page-layout review have not been performed for this source edition.\n"
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,contents in sorted(archive_files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,9,9,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,contents)
    archive_path=ROOT/'textbook/agentic-ai-textbook-latex.zip'
    if check:
        if not archive_path.is_file() or archive_path.read_bytes()!=buffer.getvalue():
            raise ValueError('Stale or missing LaTeX archive')
    else: archive_path.write_bytes(buffer.getvalue())
    print(json.dumps({k:v for k,v in manifest.items() if k!='sources'},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Check generated files without writing')
    build(parser.parse_args().check)
