import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REVIEWED_OUTBOUND_LINKS={
    'https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/',  # EDR|AI open manual (checked live 2026-10-27)
}

class SiteTests(unittest.TestCase):
    def test_generated_page_matches_config(self):
        config=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
        html=(ROOT/'index.html').read_text(encoding='utf-8')
        for key in ('umbrella','director','current_affiliation','program'):
            self.assertIn(config[key],html)
        self.assertIn('./styles.css',html)
        self.assertNotIn('{{',html)
        self.assertTrue((ROOT/'styles.css').is_file())
        self.assertTrue((ROOT/'.nojekyll').is_file())

    def test_index_is_freshly_rendered(self):
        spec=importlib.util.spec_from_file_location('render_site',ROOT/'tools/render_site.py')
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        self.assertEqual((ROOT/'index.html').read_text(encoding='utf-8'),module.build(),
                         'index.html is stale: run python3 tools/render_site.py')

    def test_page_is_self_contained(self):
        # Outbound links are allowed only from this reviewed list; nothing external is loaded.
        html=(ROOT/'index.html').read_text(encoding='utf-8')
        for external in ('http://','//fonts.','<script'):
            self.assertNotIn(external,html)
        for url in re.findall(r'https://[^"\'\s<>]+',html):
            self.assertIn(url,REVIEWED_OUTBOUND_LINKS)
            self.assertIn('href="'+url+'"',html)

if __name__=='__main__':
    unittest.main()
