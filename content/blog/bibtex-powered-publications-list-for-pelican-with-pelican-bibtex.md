Title: BibTeX-powered publications list for Pelican with pelican-bibtex
Date: 2013-04-22 10:45
Author: vene
Category: python
Tags: bibtex, blog, citations, pelican, publications, pybtex, references, static blog, static website, Uncategorized
Slug: bibtex-powered-publications-list-for-pelican-with-pelican-bibtex

Hook
----

Wouldn't you like to manage your academic publications list easily
within the context of your static website? Without resorting to external
services, or to software like *bibtex2html*, which is very nice but will
then require restyling to fit your templates?

Look no more, with the help of [pelican-bibtex][] you can now manage
your papers from within Pelican!

Backstory
---------

At [Fabian][]'s advice, I started playing around with [Pelican][], a
static website/blog generator for Python. I like it better than the
other generators I used before, so I chose it the next time I had to set
up a website. I still didn't make the courage to migrate my current
website and blog to it, but I promise I will.

Pelican has a public plugins repository, but they have a license
constraint for all contributions. My plugin isn't complicated, but I had
to "reverse engineer" undocumented parts of the [pybtex][] API. I think
that maybe that code that I used to render citations programatically can
be useful to others, so I don't want to release it under a restrictive
license. For this reason, I publish [pelican-bibtex][] in my personal
GitHub account.

You can see it in action in the [source code][] for the website I am
working on at the moment, the home page of my research group. Example
output generated using pelican-bibtex can be seen [here][].

Possible extensions
-------------------

I have not dug in too deeply but I believe this plugin can be extended,
with not much difficulty, to support referencing in Pelican blogs, and
render BibTeX references at the end of every post. This idea was
suggested by Avaris on \#pelican, and I find it very cool. Since I don't
need this feature at the moment, it's not a priority, but it's something
that I would like to see at some point.

  [pelican-bibtex]: https://github.com/vene/pelican-bibtex
  [Fabian]: http://fseoane.net
  [Pelican]: http://getpelican.com
  [pybtex]: http://pybtex.sourceforge.net
  [source code]: https://github.com/nlp-unibuc/nlp-unibuc-website/
  [here]: http://nlp-unibuc.github.io/publications.html
