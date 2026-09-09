"""Source-export and worked-example checks; intentionally no PDF compilation."""
import importlib.util
import math
from pathlib import Path
import re
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('textbook_builder',ROOT/'scripts/build-textbook.py')
builder=importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class ExportTests(unittest.TestCase):
    def test_special_characters(self):
        self.assertEqual(builder.escape('a_b & 5% {x}'),r'a\_b \& 5\% \{x\}')
    def test_inline_math_and_code_are_not_double_escaped(self):
        result=builder.inline(r'Use $x_i^2$ and `item_id`.',{})
        self.assertEqual(result,r'Use \(x_i^2\) and \texttt{item\_id}.')
    def test_multiple_citations(self):
        self.assertEqual(builder.inline('See [@a; @b].',{'a':{},'b':{}}),r'See \cite{a,b}.')
    def test_unknown_citation(self):
        with self.assertRaises(ValueError): builder.inline('[@missing]',{})
    def test_unclosed_inline(self):
        for text in ['$x','`field','**bold','[@bad!]' ]:
            with self.subTest(text=text), self.assertRaises(ValueError): builder.inline(text,{})
    def test_unclosed_blocks(self):
        for source in ['```python\nx=1','$$\nx=1']:
            with self.subTest(source=source), self.assertRaises(ValueError): builder.to_latex(source,{})
    def test_verbatim_escape(self):
        with self.assertRaises(ValueError): builder.to_latex('```text\n\\end{Verbatim}\n```',{})
    def test_lists_end_before_new_heading(self):
        result=builder.to_latex('# A\n\n1. One\n2. Two\n\n## B\nText',{})
        self.assertIn('\\end{enumerate}\n\n\\section{B}',result)
        self.assertEqual(result.count('\\item '),2)
    def test_unsupported_table_fails(self):
        with self.assertRaises(ValueError): builder.to_latex('| a | b |',{})
    def test_nested_list_fails(self):
        with self.assertRaises(ValueError): builder.to_latex('1. First\n  - Nested',{})
    def test_archive_contains_all_latex_inputs(self):
        texdir=ROOT/'textbook/latex'
        with zipfile.ZipFile(ROOT/'textbook/agentic-ai-textbook-latex.zip') as archive:
            self.assertIsNone(archive.testzip())
            for path in texdir.rglob('*.tex'):
                self.assertEqual(archive.read(str(path.relative_to(texdir))),path.read_bytes())
    def test_empty_source(self):
        self.assertEqual(builder.to_latex('',{}),'\n')
    def test_empty_math(self):
        with self.assertRaises(ValueError): builder.to_latex('$$\n$$',{})
    def test_untrusted_link_syntax(self):
        with self.assertRaises(ValueError): builder.inline('[label](https://x/{bad})',{})
    def test_markdown_citations_resolve(self):
        self.assertEqual(builder.markdown('See [@a; @b].',{'a':1,'b':2}), 'See [1](#ref-a) [2](#ref-b).')
    def test_generated_outputs_current(self):
        builder.build(check=True)
    def test_latex_references_and_inputs_resolve(self):
        texdir=ROOT/'textbook/latex'
        sources='\n'.join(p.read_text() for p in texdir.rglob('*.tex'))
        defined=set(re.findall(r'\\bibitem\{([^}]+)\}',sources))
        for group in re.findall(r'\\cite\{([^}]+)\}',sources):
            self.assertTrue(set(group.split(','))<=defined)
        for name in re.findall(r'\\input\{([^}]+)\}',(texdir/'main.tex').read_text()):
            self.assertTrue((texdir/name).is_file(),name)
        for environment in ['document','equation','enumerate','itemize','Verbatim','thebibliography']:
            self.assertEqual(sources.count('\\begin{'+environment+'}'),sources.count('\\end{'+environment+'}'))
        self.assertNotIn('[@',sources)

class WorkedExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source=(ROOT/'chapters/05-tools-mcp.md').read_text()
        code=re.search(r'```python\n(.*?)\n```',source,re.S)[1]
        namespace={};exec(compile(code,'chapter-5-example','exec'),namespace)
        cls.add=staticmethod(namespace['bounded_add'])
    def test_numeric_valid_boundaries(self):
        self.assertEqual(self.add(1_000_000,-1_000_000),0)
        self.assertEqual(self.add(1_000_000,0),1_000_000)
        self.assertEqual(self.add(-1_000_000,0),-1_000_000)
    def test_numeric_invalid_inputs(self):
        for value in [True,False,None,'1',[],{},1+2j]:
            with self.subTest(value=value), self.assertRaises(TypeError): self.add(value,0)
    def test_numeric_overflow_and_nonfinite(self):
        for value in [10**10000,1_000_001,float('inf'),float('-inf'),float('nan')]:
            with self.subTest(kind=type(value)), self.assertRaises(ValueError): self.add(value,0)
        with self.assertRaises(ValueError):self.add(1_000_000,1_000_000)
    def test_worked_calculations(self):
        self.assertAlmostEqual(.95**4,.81450625)
        self.assertAlmostEqual(3*.7**2*.3+.7**3,.784)
        self.assertAlmostEqual(3*.6**2*.4+.6**3,.648)
        self.assertEqual(sum(3**i for i in range(5)),121)
        self.assertEqual(sum(2**i for i in range(6)),63)
        self.assertEqual(8192-1024-1536,5632)
        self.assertAlmostEqual(1/(1+math.sqrt(3)),.36602540378443865)
        self.assertAlmostEqual(20/80,.25)
        self.assertAlmostEqual(18/60,.3)
        self.assertAlmostEqual(8*.1*10+.15*0+.05*(-100),3)
        self.assertEqual(8*7//2,28)
    def test_answer_arithmetic(self):
        self.assertEqual(9/12,.75);self.assertEqual(9/10,.9)
        self.assertEqual(3/5,.6);self.assertEqual(3/6,.5)
        self.assertEqual(12/40,.3);self.assertEqual(12/30,.4)

if __name__=='__main__':unittest.main()
