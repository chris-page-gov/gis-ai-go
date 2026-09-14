"""Publication regressions: escaping, fixed scope and generated-source identity."""
import unittest
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

from scripts import build_chronicle as build


class ChronicleBuilderTests(unittest.TestCase):
    def test_prose_and_link_labels_are_escaped(self):
        value = build.inline('<script> [<img>](https://example.org/)', 'README.md')
        self.assertNotIn('<script>', value)
        self.assertIn('&lt;script&gt;', value)
        self.assertIn('&lt;img&gt;', value)

    def test_repository_link_cannot_escape(self):
        with self.assertRaises(ValueError):
            build.url('../../../../outside', 'README.md')

    def test_internal_chapter_link_uses_reader_anchor(self):
        self.assertEqual(build.url('LEARNING_PATH.md', 'README.md'), '#learning-path-md')

    def test_heading_fragments_match_generated_ids(self):
        document = build.build_html([('README.md', '# Reader\n\n## Next step\n\n## Next step')], {})
        self.assertIn('id="readme-md--next-step"', document)
        self.assertIn('id="readme-md--next-step-1"', document)
        self.assertEqual(build.url('README.md#next-step', 'README.md'), '#readme-md--next-step')
        self.assertEqual(build.url('#next-step', 'README.md'), '#readme-md--next-step')

    def test_angle_wrapped_external_url(self):
        self.assertEqual(build.url('<https://example.org/>', 'README.md'), 'https://example.org/')

    def test_ordered_steps_keep_explicit_numbers(self):
        parsed = list(build.blocks('2. second\n  continuation\n4. fourth\n\n- bullet'))
        self.assertEqual(parsed, [('ordered_item', (2, 'second continuation')),
                                  ('ordered_item', (4, 'fourth')), ('item', 'bullet')])
        document = build.build_html([('README.md', '# Reader\n\n2. second\n4. fourth\n\n- bullet')], {})
        self.assertIn('<ol>\n<li value="2">second</li>\n<li value="4">fourth</li>\n</ol>\n<ul>', document)

    def test_code_source_is_bound_to_baseline(self):
        value = build.url('../../packages/contracts/README.md', 'README.md')
        self.assertIn('/blob/' + build.BASELINE + '/packages/contracts/README.md', value)

    def test_unclosed_fence_is_rejected(self):
        with self.assertRaises(ValueError):
            list(build.blocks('```python\nprint(1)'))

    def test_table_separator_is_not_content(self):
        parsed = list(build.blocks('| A | B |\n| --- | --- |\n| C | D |'))
        self.assertEqual(parsed, [('table', [['A', 'B'], ['C', 'D']])])

    def test_multiline_list_retains_continuation(self):
        self.assertEqual(list(build.blocks('- first\n  second\n\nend')),
                         [('item', 'first second'), ('paragraph', 'end')])

    def test_svg_text_is_escaped_and_repeatable(self):
        spec = {'title': '<title>', 'description': 'A & B', 'steps': [['One', '<two>']]}
        one = build.svg(spec)
        self.assertEqual(one, build.svg(spec))
        self.assertIn(b'&lt;two&gt;', one)
        self.assertNotIn(b'<two>', one)

    def test_reader_has_no_executable_script(self):
        document = build.build_html([('README.md', '# Reader\n<script>')], {})
        self.assertIn('lang="en-GB"', document)
        self.assertIn('Content-Security-Policy', document)
        self.assertNotIn('<script>', document)

    def test_reader_asset_links_and_anchors_resolve(self):
        class Links(HTMLParser):
            def __init__(self):
                super().__init__()
                self.links = []
                self.ids = set()

            def handle_starttag(self, tag, attrs):
                values = dict(attrs)
                if 'id' in values:
                    self.ids.add(values['id'])
                if tag == 'a' and 'href' in values:
                    self.links.append(values['href'])

        import json
        chapters = [(name, build.source_bytes(name).decode()) for name in build.CHAPTERS]
        parsed = Links()
        parsed.feed(build.build_html(chapters, json.loads(build.source_bytes('figures.json'))))
        assets = {Path(name).name for name in build.DATA_NAMES}
        for target in parsed.links:
            if target.startswith('#'):
                self.assertIn(target[1:], parsed.ids)
            elif not target.startswith(('https://', 'http://', 'mailto:')):
                self.assertIn(target, assets)

    def test_source_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'source.md').symlink_to(root / 'missing.md')
            with self.assertRaises(ValueError):
                build.checked_path(root, 'source.md')

    def test_source_ancestor_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'real' / 'chronicle').mkdir(parents=True)
            (root / 'real' / 'chronicle' / 'README.md').write_text('not admitted')
            (root / 'docs').symlink_to(root / 'real', target_is_directory=True)
            with patch.object(build, 'ROOT', root):
                with self.assertRaises(ValueError):
                    build.source_bytes('README.md')

    def test_output_with_extra_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'unrelated.txt').touch()
            with self.assertRaises(ValueError):
                build.validate_output(root, ['index.html'])

    def test_output_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'index.html').symlink_to(root / 'missing.html')
            (root / 'manifest.json').touch()
            with self.assertRaises(ValueError):
                build.validate_output(root, ['index.html'])

    def test_changed_source_aborts_before_output_publication(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'docs' / 'chronicle'
            (source / 'data').mkdir(parents=True)
            (source / 'README.md').write_text('# Original')
            (source / 'figures.json').write_text('{}')
            (source / 'requirements-print.txt').write_text('')
            (source / 'data' / 'claims.json').write_text('{}')

            def mutate(chapters, figures):
                (source / 'README.md').write_text('# Changed')
                return '<html>original snapshot</html>'

            with patch.object(build, 'ROOT', root), \
                 patch.object(build, 'SOURCE', source), \
                 patch.object(build, 'CHAPTERS', ('README.md',)), \
                 patch.object(build, 'DATA_NAMES', ('data/commits.csv', 'data/claims.json')), \
                 patch.object(build, 'commit_ledger', return_value=b'header\n'), \
                 patch.object(build, 'build_html', side_effect=mutate), \
                 patch('sys.argv', ['build_chronicle.py', '--refresh-source-assets']):
                with self.assertRaisesRegex(ValueError, 'Source changed during rendering'):
                    build.main()
            self.assertFalse((root / 'artifacts' / 'chronicle').exists())


if __name__ == '__main__':
    unittest.main()
