Title: Compiling MegaM on MacOS X
Date: 2012-06-08 11:45
Author: vene
Category: nlp
Tags: compile, install, maxent, megam
Slug: compiling-megam-on-macos-x

[MegaM][] is Hal Daumé III's maxent (logistic regression, and much more)
modeling software written in OCaml. It is feature-packed and seems to be
used a lot, despite being slightly dated. [NLTK][] is able to use it.

In order to compile it as of 2012, with the current version of OCaml, I
had to do some tricks that I would like to document here. It's no big
deal but it could save somebody precious minutes.

1.  Download and unpack the gzip archive.
2.  Install ocaml using macports: `sudo port install ocaml`. *Note:*
    this installed version 3.12.1\_5, YMMV with newer versions later.
3.  Point the compiler to the correct headers. First run `ocamlc -where`
    to find out the correct path. On my system it's
    `/opt/local/lib/ocaml/caml`. Change the `WITHCLIBS` line (\#73) in
    the Makefile to point there.
4.  As of OCaml 3.12.0, the `-lstr` compiler flag should be replaced
    with `-lcamlstr`. It occurs on line \#62 within the definition of
    `WITHSTR`.
5.  Run `make` or `make opt` and enjoy.

  [MegaM]: http://hal3.name/megam
  [NLTK]: http://nltk.org "Natural Language Toolkit"
