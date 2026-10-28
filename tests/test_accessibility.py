"""Offline structural/CSS checks, not a browser or screen-reader certification."""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_OUTBOUND_LINKS = {'https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/'}


def contrast(fg, bg):
    def luminance(color):
        values = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
        v = [x/12.92 if x <= .04045 else ((x+.055)/1.055)**2.4 for x in values]
        return sum(a*b for a, b in zip(v, (.2126, .7152, .0722)))
    a, b = sorted((luminance(fg), luminance(bg)))
    return (b+.05)/(a+.05)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


class AccessibilityTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT/'index.html').read_text()
        self.css = (ROOT/'styles.css').read_text()
        self.page = Page(self.html)

    def test_landmarks_heading_language_and_skip_link(self):
        self.assertEqual(sum(tag == 'main' for tag, _ in self.page.nodes), 1)
        self.assertEqual(sum(tag == 'h1' for tag, _ in self.page.nodes), 1)
        self.assertIn(('html', {'lang': 'en'}), self.page.nodes)
        main = next(a for t, a in self.page.nodes if t == 'main')
        self.assertEqual(main['id'], 'main')
        self.assertEqual(main['tabindex'], '-1')
        self.assertTrue(any(t == 'a' and a.get('href') == '#main' for t, a in self.page.nodes))
        self.assertTrue(any(t == 'nav' and a.get('aria-label') for t, a in self.page.nodes))

    def test_ids_fragments_local_assets_and_no_external_requests(self):
        ids = [a['id'] for _, a in self.page.nodes if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))
        for tag, attrs in self.page.nodes:
            self.assertNotIn(tag, ('script', 'iframe', 'form'))
            for key in ('href', 'src'):
                if key not in attrs:
                    continue
                link = attrs[key]
                if link.startswith('#'):
                    self.assertIn(link[1:], ids)
                elif tag == 'a' and key == 'href' and link.startswith('https://'):
                    self.assertIn(link, REVIEWED_OUTBOUND_LINKS)  # reviewed outbound link, nothing loaded
                else:
                    self.assertFalse(re.match(r'(?:[a-z]+:)?//', link))
                    self.assertTrue((ROOT/link).is_file(), link)
        self.assertNotIn('@import', self.css)
        self.assertNotIn('url(', self.css)

    def test_responsive_and_reduced_motion_rules(self):
        self.assertTrue(any(t == 'meta' and a.get('name') == 'viewport'
                            and 'width=device-width' in a['content'] for t, a in self.page.nodes))
        self.assertIn('@media(max-width:710px)', self.css)
        self.assertIn('@media(max-width:420px)', self.css)
        self.assertIn('grid-template-columns:1fr', self.css)
        self.assertIn('.person-card{flex-direction:column', self.css)
        self.assertIn('min-width:0', self.css)
        self.assertIn('overflow-wrap:anywhere', self.css)
        self.assertIn('@media(prefers-reduced-motion:reduce)', self.css)
        self.assertIn(':focus-visible', self.css)
        self.assertNotIn('outline:none', self.css.replace(' ', ''))

    def test_reviewed_text_and_focus_contrast_pairs(self):
        # Purdue web palette (https://www.purdue.edu/brand-studio/digital/design-copy/): every text
        # role's foreground/background pair, as used in styles.css.
        css = (ROOT/'styles.css').read_text(encoding='utf-8').lower()
        text_pairs = [('#000000', '#ffffff'),   # body text, headings
                      ('#555960', '#ffffff'),   # Steel: muted text, identity bar, notes
                      ('#8e6f3e', '#ffffff'),   # Aged: section labels, theme numbers
                      ('#000000', '#ebd99f'),   # button hover (Dust)
                      ('#000000', '#cfb991'),   # primary button (Boilermaker Gold)
                      ('#000000', '#fbf6e8'),   # status badge
                      ('#cfb991', '#000000'),   # gold on black: eyebrow, logo, footer name
                      ('#ffffff', '#000000'),   # navigation
                      ('#c4bfc0', '#000000'),   # Steam: lede, footer text
                      ('#c4bfc0', '#2a2c30'),   # lede over the hero glow
                      ('#9d9795', '#000000')]   # Railway Gray: footer notes
        for fg, bg in text_pairs:
            with self.subTest(fg=fg, bg=bg):
                for color in (fg, bg):
                    self.assertTrue(color in css or (color == '#ffffff' and ('#fff' in css or 'white' in css)),
                                    color+' is not used in styles.css; update this list')
                self.assertGreaterEqual(contrast(fg, bg), 4.5)
        self.assertGreaterEqual(contrast('#8e6f3e', '#ffffff'), 3)   # focus outline on light
        self.assertGreaterEqual(contrast('#cfb991', '#000000'), 3)   # focus outline on dark

    def test_renderer_idempotence(self):
        before = (ROOT/'index.html').read_bytes()
        subprocess.run([sys.executable, ROOT/'tools/render_site.py'], check=True, capture_output=True)
        self.assertEqual(before, (ROOT/'index.html').read_bytes())


if __name__ == '__main__':
    unittest.main()
