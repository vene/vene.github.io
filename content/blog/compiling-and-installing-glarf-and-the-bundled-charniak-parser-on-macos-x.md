Title: Compiling and Installing GLARF and the bundled Charniak parser on MacOS X
Date: 2012-06-21 12:32
Author: vene
Category: nlp
Tags: bllip, charniak, glarf, installation, parser, nlp
Slug: compiling-and-installing-glarf-and-the-bundled-charniak-parser-on-macos-x

It seems that I keep getting handed buggy code to install. These are
cases of research software where the developers didn't make the effort
to make sure their tool works on the platforms it should.

[GLARF][] (Grammatical and Logical Argument Representation Framework)
is, in their words, "a typed feature structure framework for
representing regularizations of parse trees". It is a processing
pipeline from NYU with rich output including many types of structure in
the given text. However, it is clearly a case of software whose
maintenance was abandoned when it "worked" for them. The whole install
and run procedure is pretty messy, but at least it's documented. The
problem is, following it step by step doesn't work on my MacBook. As
usual, I needed to hack through it a bit.

The Charniak parser distributed with GLARF has now been superseded by
the [BLLIP parser][]. The new one is tricky to compile as well, but I
have yet to see if it plugs into GLARF, so I leave this for a future
post.

Here are the steps I needed to take to make GLARF work:

<ol>
<li>
Download and unzip the GLARF package.

</li>
<li>
Make sure you have `sbcl` in your path, and your `perl` is in (or linked
from) `/usr/bin/perl`

</li>
<li>
Set the environment variables. I like to make a shell script to set them
so I don't have to do it every time. So I write something looking like
this:

[sourcecode lang="bash"]  
\# glarf\_env.sh

export GLARF=/Users/vene/code/GLARF  
export GLARF\_JET=\${GLARF}/JET  
export PATH=\$PATH:.  
[/sourcecode]

<p>
Then for every session when I want to use GLARF, I do
`source glarf_env.sh`.

</li>
<li>
Compile GLARF by running `$GLARF/commands-2010/compile-glarf`. *Note:*
this only compiles the pipeline lisp code.

</li>
<li>
Now, according to their instructions, you're done. However, if you try
to run it, you'd notice the output is incomplete. (It goes through the
named entity extraction part, but it doesn't run the parser.) The reason
for this is that they distribute the Charniak parser with a precompiled
binary that runs on Linux, but not on the Mac. So we need to recompile
it. So go to `$GLARF/charniak-parser-2005/parser05Aug16-static/PARSE2 `,
run `make clean` and roll up your sleeves.

</li>
<li>
Obviously, simply running `make` doesn't work. [As documented by Pawel
Mazur][], we need to edit `BchartSm.C` to add the line
`#include "GotIter.h"`

</li>
<li>
On my system this still isn't enough, and I get some linker errors. By
poking through the Makefile, I noticed I could fix it by commenting out
the 5th line: `LDFLAGS=-static`.

</li>
<li>
Now run make and watch it work, hurrah! \\o/

</li>
<li>
To see if GLARF itself works now, go to
`$GLARF/commands-2010/run-glarf/` and run
`make-all-glarf-a sample-files-a N`. You should get beautiful, beautiful
GLARF output files.

</li>
</ul>
Phew, now that was quite an effort!

  [GLARF]: http://nlp.cs.nyu.edu/meyers/GLARF.html
  [BLLIP parser]: https://github.com/BLLIP/bllip-parser
  [As documented by Pawel Mazur]: http://web.science.mq.edu.au/~mpawel/resources/notes/compilingCharniakJohnson.htm
