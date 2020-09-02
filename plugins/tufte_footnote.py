import re
from pelican import signals

REF_RE = re.compile(r"\[ref\](.*?)\[/ref\]", re.DOTALL)

class FootnoteUniqueSpan(object):
    # elegant solution from https://stackoverflow.com/a/26678944
    def __init__(self):
        self.counter = 0

    def __call__(self, match):
        self.counter += 1
        res = '\
<label for="sn-{0}" class="margin-toggle sidenote-number"></label>\
<input type="checkbox" id="sn-{0}" class="margin-toggle"/>\
<span class="sidenote">{1}</span>'.format(self.counter, match.group(1))
        return res

# counter = FootnoteUniqueSpan()
# ex = "hi [ref]abc[/ref] ghi"
# ex = re.sub(REF_RE, counter, ex)


def sequence_gen(genlist):
    for gen in genlist:
        for elem in gen:
            yield elem

def replace_footnotes(generator):

    all_content = []

    if hasattr(generator, "articles"):
        all_content.extend(generator.articles)
    if hasattr(generator, "drafts"):
        all_content.extend(generator.drafts)

    all_content = [c for c in all_content if c is not None]
    for article in all_content:
        counter = FootnoteUniqueSpan()
        article._content = re.sub(REF_RE, counter, article._content)


def register():
    signals.article_generator_finalized.connect(replace_footnotes)

