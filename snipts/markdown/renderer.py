import misaka as m
from houdini import escape_html
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# Create a custom renderer
class MardownEmbbedCodeRenderer(m.HtmlRenderer, m.SmartyPants):
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % escape_html(text.strip())
        
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

def markdown(code):
    md = m.Markdown(MardownEmbbedCodeRenderer(),
                    extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
    return md.render(code)