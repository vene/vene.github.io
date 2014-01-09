Title: On why my %memit fails on OSX
Date: 2012-07-04 12:49
Author: vene
Category: benchmarking, python
Tags: IPython, magic, memit, mprun
Slug: on-why-my-memit-fails-on-osx

In my [last post][] I mentioned that I'm not satisfied with the current
state of `%memit`, because some more complicated numerical function
calls make it crash. I will start this post with a reminder of a pretty
important bug:

**[On MacOS X (10.7 but maybe more), after forking a new process, there
is a segfault in Grand Central Dispatch on the BLAS DGEMM function from
Accelerate.][]  
**

**EDIT 1:** In a hurry, I forgot to mention how [Olivier Grisel][] and
[David Cournapeau][] spent some time narrowing down this issue, starting
from an [odd testing bug in scikit-learn][]. They reported it to Apple,
but there was, as of the date of this post, no reaction.

**EDIT 2:** MinRK [confirms][], and I verified shortly after, that this
bug is fixed in Mountain Lion (10.8). Still not sure how far back it
goes, though, so feedback is welcome.

When I first tried to make the `%memit` magic, I thought about simply
measuring the current memory, running the command, and measuring the
memory again. The problem is the results are not consistent, because
Python [tries to reuse already allocated memory whenever it can][].

Using memory\_profiler, here's an example illustrating this elastic
memory management:  
[sourcecode lang="python"]  
\# mem\_test.py  
import numpy as np

def make\_a\_large\_array():  
return np.ones((1000, 1000))

def main():  
make\_a\_large\_array()  
make\_a\_large\_array()  
make\_a\_large\_array()

\# in IPython:  
In [1]: import mem\_test

In [2]: %mprun -f mem\_test.main mem\_test.main()  
Filename: mem\_test.py

Line \# Mem usage Increment Line Contents  
==============================================  
8 24.8477 MB 0.0000 MB def main():  
9 24.8633 MB 0.0156 MB make\_a\_large\_array()  
10 32.4688 MB 7.6055 MB make\_a\_large\_array()  
11 32.4688 MB 0.0000 MB make\_a\_large\_array()  
[/sourcecode]

If this was in an IPython environment, and one would like to see how
much memory `make_a_large_array()` uses, you could say we can simply run
it a few times and take the maximum. However, if you happened to
accidentally call `main()` once before, you will no longer get a good
result:

[sourcecode lang="python"]  
In [3]: %mprun -f mem\_test.main mem\_test.main()  
Filename: mem\_test.py

Line \# Mem usage Increment Line Contents  
==============================================  
8 32.4922 MB 0.0000 MB def main():  
9 32.5234 MB 0.0312 MB make\_a\_large\_array()  
10 32.5234 MB 0.0000 MB make\_a\_large\_array()  
11 32.5234 MB 0.0000 MB make\_a\_large\_array()  
[/sourcecode]

So how can we get consistent results for the memory usage of an
instruction? We could run it in a fresh, new process. I implemented this
in %memit and it shows:

[sourcecode lang="python"]  
In [5]: %memit mem\_test.make\_a\_large\_array()  
maximum of 3: 8.039062 MB per loop

In [6]: %memit mem\_test.make\_a\_large\_array()  
maximum of 3: 8.035156 MB per loop

In [7]: %memit mem\_test.make\_a\_large\_array()  
maximum of 3: 8.042969 MB per loop  
[/sourcecode]

This way you can also realistically benchmark assignments:

[sourcecode lang="python"]  
In [8]: %memit X = mem\_test.make\_a\_large\_array()  
maximum of 3: 8.054688 MB per loop

In [9]: %memit X = mem\_test.make\_a\_large\_array()  
maximum of 3: 8.058594 MB per loop

In [10]: %memit X = mem\_test.make\_a\_large\_array()  
maximum of 3: 8.058594 MB per loop  
[/sourcecode]

If we don't spawn a subprocess, `del` doesn't help, but allocating new
variables does:  
[sourcecode lang="python"]  
In [11]: %memit -i X = mem\_test.make\_a\_large\_array()  
maximum of 3: 7.632812 MB per loop

In [12]: del X

In [13]: %memit -i X = mem\_test.make\_a\_large\_array()  
maximum of 3: 0.000000 MB per loop

In [14]: %memit -i Y = mem\_test.make\_a\_large\_array()  
maximum of 3: 7.632812 MB per loop

In [15]: %memit -i Z = mem\_test.make\_a\_large\_array()  
maximum of 3: 7.632812 MB per loop  
[/sourcecode]

Now, the problem is that when the function that you are benchmarking
contains calls to `np.dot` (matrix multiplication), the subprocess will
consistently fail with SIGSEGV on affected OS X systems. These are
actually pretty much all the functions that I intended `%memit` for:
numerical applications. For that reason, I have made `%memit` notify the
user when all subprocesses fail, and to suggest the usage of the `-i`
flag.

I think that, with this update, `%memit` is flexible and usable enough
for actual use, and therefore for merging into memory\_profiler.

  [last post]: http://localhost:8001/2012/07/02/more-on-memory-benchmarking/
    "More on memory benchmarking"
  [On MacOS X (10.7 but maybe more), after forking a new process, there
  is a segfault in Grand Central Dispatch on the BLAS DGEMM function
  from Accelerate.]: https://gist.github.com/2027412
  [Olivier Grisel]: http://twitter.com/ogrisel/
  [David Cournapeau]: https://github.com/cournape
  [odd testing bug in scikit-learn]: https://github.com/scikit-learn/scikit-learn/issues/636
  [confirms]: https://twitter.com/minrk/status/228265246819774464
    "Min's tweet"
  [tries to reuse already allocated memory whenever it can]: http://effbot.org/pyfaq/why-doesnt-python-release-the-memory-when-i-delete-a-large-object.htm
