Title: First contact with vbench
Date: 2012-05-29 12:57
Author: vene
Category: scikit-learn
Tags: benchmarks, perf.py, performance, vbench
Slug: first-contact-with-vbench

With a slight delay caused by going to lovely lovely Istanbul for the
LREC conference where I presented a [poster][], I am back to work on the
Google Summer of Code project. By the way, this year's logo and swag
looks a lot nicer than last year's, thank you Google!  
[![][]][]  
The backbone of my GSoC consists of putting together a continuous
benchmark platform. I took a good look at [vbench][] and spent an
evening hacking Wes's benchmarks suite config into something that will
run on my machine. These are the key points I got from this experience.

-   vbench is, at least for the moment, very specific to [Wes' and
    Pandas' needs][]. This is also because there weren't so many other
    users that could have brought contributions.
-   Even though it has support for some configuration and automation,
    vbench seems largely suited for running on a local machine.
    Specifically, it is NOT designed to run continuously but in one-off
    runs, going back in git history and getting the last commit for each
    day, and running the benchmark with it. Of course, it is trivial to
    patch it into getting just one commit.
-   The *code-as-strings* approach is not ideal. The first thought is
    that it should be replaced with reading `.py` files into strings,
    but there are two issues with this:
    1.  One benchmark file can have a lot of setup code and several key
        lines that need to actually be benched. This can be fixed using
        convensions (ie. setup functions and `bench_*` functions) in the
        spirit of testing suites, or using decorators.
    2.  I would like to be able to run bench files as python scripts,
        but the vbench import system breaks this. This can be fixed by
        hijacking the imports when reading the file.

Our project has different dynamics than Pandas, so it's important that
the published results run on an independent machine, but it would be
great if an individual developer can run the benchmark himself while
coding but before pushing his changes upstream. Of course, his numbers
would only be comparable to the numbers he gets on his own machine
before his changes, but a developer shouldn't wait for the daily
benchmark for knowing if he made an improvement.

On the other hand there is [unladen-swallow][]'s [benchmark system][]
using the [`perf.py`][] file. I didn't try it out yet, so I would like
feedback, but there are some key things that can be taken from them:

-   Memory usage benchmarking
-   Python scripts as benchmarks, with a simple but efficient Benchmark
    object hierarchy

What's missing is:

-   A system to remember previous results and compare them, similar to
    vbench's database
-   The ability to bench only an area of the code without rerunning the
    setup. (Not really sure whether vbench's way is actually better)

At a first glance, it seems that a very good system can be obtained by
combining these two excellent projects (or rather, improving vbench with
features from `perf.py`). While I continue exploring this, I would like
to hear feedback from people who had to do with similar issues. As for
the GSoC timeline, I plan to join forces with Immanuel and design a
solid benchmark suite for the linear models over the next 2 weeks.

  [poster]: http://vene.ro/papers/lrec12-poster.pdf
  []: http://localhost:8001/wp-content/uploads/2012/05/P5280194-300x225.jpg
    "GSoC swag"
  [![][]]: http://localhost:8001/wp-content/uploads/2012/05/P5280194.jpg
  [vbench]: https://github.com/pydata/vbench
  [Wes' and Pandas' needs]: http://pandas.pydata.org/pandas-docs/vbench/
  [unladen-swallow]: http://code.google.com/p/unladen-swallow/
  [benchmark system]: http://code.google.com/p/unladen-swallow/wiki/Benchmarks
  [`perf.py`]: http://code.google.com/p/unladen-swallow/source/browse/tests/perf.py
