import html
import json
from pathlib import Path

from sanity_html import SanityBlockRenderer


def load_fixture(fixture_name) -> dict:
    fixture_file = Path(__file__).parent / 'fixtures' / fixture_name
    return json.loads(fixture_file.read_text())


def test_simple_span():
    simple_span_def = load_fixture('simple_span.json')
    output = SanityBlockRenderer.render(simple_span_def)
    assert output == '<p>Otovo guarantee is good</p>'


def test_multiple_simple_spans_in_single_block():
    fixture = load_fixture('multiple_simple_spans.json')
    output = SanityBlockRenderer.render(fixture)
    assert output == '<p>Otovo guarantee is good for all</p>'


def test_simple_xss_escaping():
    simple_span_def = load_fixture('simple_xss.json')
    output = SanityBlockRenderer.render(simple_span_def)
    danger = html.escape("<script>alert(1)</script>")
    assert output == f"<p>Otovo guarantee is {danger} good</p>"


def test_basic_mark():
    fixture = load_fixture("basic_mark.json")
    output = SanityBlockRenderer.render(fixture)
    assert output == "<p><code>sanity</code> is the name of the CLI tool.</p>"


def test_multiple_adjecent_marks():
    fixture = load_fixture("multiple_adjecent_marks.json")
    output = SanityBlockRenderer.render(fixture)
    assert output == "<p><strong>A word of warning;</strong> Sanity is addictive.</p>"
