# plugin to wrap $ $ and $$ $$ with a span to prevent typogrify

import os
import sys
import re

from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
from markdown.util import etree

from pelican import signals


DOLLAR_RE = r"""
^(.*?)
((?<!\\)   # negative look-behind to make sure start is not escaped
((?<!\$)\${1,2}(?!\$))     # match one or two dollars, not escaped
.*?                        # nongreedy body
(?<!\\)                    # exactly the same tag as opening one, but not escaped.
(?<!\$)\3(?!\$))
(.*)$
"""

DOLLAR_REC = re.compile(DOLLAR_RE, re.VERBOSE | re.MULTILINE | re.DOTALL)


class DollarPattern(InlineProcessor):
    def __init__(self):
        self.compiled_re = DOLLAR_REC

    def handleMatch(self, m, data):
        el = etree.Element("span", attrib={"class": "mathskip"})
        el.text = m.group(2)
        return el, m.start(2), m.end(2)


class WrapMathExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('mathskip', DollarPattern(), "_begin")


def pelican_init(pelicanobj):
    # Instantiate Markdown extension and append it to the current extensions
    try:
        if isinstance(pelicanobj.settings.get('MD_EXTENSIONS'), list):  # pelican 3.6.3 and earlier
            pelicanobj.settings['MD_EXTENSIONS'].append(WrapMathExtension())
        else:
            pelicanobj.settings['MARKDOWN'].setdefault('extensions', []).append(WrapMathExtension())
    except:
        sys.excepthook(*sys.exc_info())
        sys.stderr.write("\nError. Wrap Math extension not working.\n")
        sys.stderr.flush()


def register():
    signals.initialized.connect(pelican_init)
