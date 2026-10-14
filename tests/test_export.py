"""Regression checks for resource portability and safe scaffolding; no browser needed."""
import base64
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from export_deck import BundleError,bundle_html
from validate_skill import ROOT,validate


class Bundling(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def write(self,name,text):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
    def test_local_css_script_font_and_inline_image(self):
        self.write('index.html','<head><link rel="stylesheet" href="sub/style.css" media="print"></head><body style="background:url(art.svg)"><script src="deck.js"></script></body>')
        self.write('sub/style.css','@import "other.css"; @font-face{src:url("font.woff2")}')
        self.write('sub/other.css','body{color:red}')
        self.write('sub/font.woff2','font-bytes');self.write('art.svg','<svg/>')
        self.write('deck.js','window.example = "</SCRIPT>";')
        html,_=bundle_html(self.root)
        self.assertIn('media="print"',html);self.assertIn('body{color:red}',html)
        self.assertIn('data:font/woff2;base64,',html);self.assertIn('data:image/svg+xml;base64,',html)
        self.assertIn('<\\/SCRIPT>',html)
    def test_rejects_unresolved_resources(self):
        for markup in ['<script src="https://example.com/lib.js"></script>',
                       '<img src=missing.png>', '<img src="missing.png">',
                       '<style>body{background:url(https://example.com/a.png)}</style>',
                       '<base href="https://example.com/">',
                       '<img srcset="a.png 1x,b.png 2x">',
                       '<script src="../escape.js"></script>']:
            with self.subTest(markup=markup):
                self.write('index.html',markup)
                with self.assertRaises(BundleError):bundle_html(self.root)
    def test_rejects_css_cycles_and_module_imports(self):
        self.write('index.html','<link rel="stylesheet" href="a.css">')
        self.write('a.css','@import "b.css";');self.write('b.css','@import "a.css";')
        with self.assertRaises(BundleError):bundle_html(self.root)
        self.write('index.html','<script src="deck.js"></script>')
        self.write('deck.js','import thing from "./dependency.js";')
        with self.assertRaises(BundleError):bundle_html(self.root)
    def test_encoded_paths_and_svg_fragment(self):
        self.write('index.html','<svg><use href="my%20icons.svg#arrow"></use></svg>')
        self.write('my icons.svg','<svg/>')
        html,_=bundle_html(self.root);self.assertIn('#arrow',html)
        self.assertIn(base64.b64encode(b'<svg/>').decode(),html)
    def test_scaffold_refuses_file_or_nonempty_directory(self):
        self.write('existing','keep')
        for target in [self.root/'existing',self.root]:
            result=subprocess.run([sys.executable,str(ROOT/'scripts/create_deck.py'),'--output',str(target)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0);self.assertNotIn('Traceback',result.stderr)
        self.assertEqual((self.root/'existing').read_text(),'keep')


class Packaging(unittest.TestCase):
    def test_installable_package_is_self_contained(self):
        errors,paths=validate();self.assertEqual(errors,[])
        self.assertFalse(any('resources' in p.relative_to(ROOT).parts for p in paths))
        self.assertEqual(sum(p.name=='SKILL.md' for p in paths),1)

if __name__=='__main__':unittest.main()
