Title: Profiler output, benchmark standard deviation and other goodies in scikit-learn-speed
Date: 2012-07-27 11:01
Author: vene
Category: benchmarking, python, scikit-learn
Tags: gsoc, memory_profiler, scikit-learn-speed, vbench
Slug: profiler-output-benchmark-standard-deviation-and-other-goodies-in-scikit-learn-speed

This post is about the [scikit-learn][]benchmarking project that I am
working on, called [scikit-learn-speed][]. This is a continuous
benchmarking suite that runs and generates HTML reports using Wes
McKinney's [vbench][] framework, to which I had to make some (useful, I
hope) additions.

What it looks like now
----------------------

You can check out a [teaser/demo][] that was run on equidistant releases
from the last two months. What has changed since the last version?
Here's a list in order of obviousness:

-   We now use the lovely scikit-learn theme
-   Timing graphs now show the ±1 standard deviation range
-   cProfile output is displayed for all the benchmarks, so we can
    easily see at a glance what's up
-   Said profiler output is collapsible using [JQueryUI goodness][]
-   There now is an improved [Quick Start guide][] to running vbench on
    your machine

What made this possible
-----------------------

I have done some more refactoring in my vbench fork, because I didn't
want to have a huge, monolithic `Benchmark` class that was specific to
what we want in scikit-learn-speed. So on this branch, I set up a
mixin/multiple inheritance hierarchy of benchmark classes.

The `Benchmark` class in vbench is now an abstract base class, with some
common functionality and structure.  
Our `SklBenchmark` class is defined in scikit-learn-speed as:

`class SklBenchmark(CProfileBenchmarkMixin,  MemoryBenchmarkMixin, PythonBenchmark): `

Let's read this from right to left:

-   `PythonBenchmark`: This class stores `code`, `setup` and `cleanup`
    Python code as strings, and implements simple timing mechanisms
    using the `time` module.
-   Bonus: `TimeitBenchmark`: This class extends `PythonBenchmark` with
    the `timeit` micro-benchmark timing method previously used in
    vbench. We turned this off in scikit-learn-speed.
-   `MemoryBenchmarkMixin`: This adds memory benchmarking using
    [memory\_profiler][].
-   `CProfileBenchmarkMixin`: This runs the code through [cProfile][]
    and implements mechanisms to report the output.</code>

The database is not flexible enough to adapt to arbitrary benchmark
structure right now, so if anybody would like to help the effort, it
would be very appreciated.

  [scikit-learn]: http://scikit-learn.org
  [scikit-learn-speed]: https://github.com/vene/scikit-learn-speed
  [vbench]: http://wesmckinney.com/blog/?p=373
  [teaser/demo]: http://vene.github.com/scikit-learn-speed
  [JQueryUI goodness]: http://www.jqueryui.com/demos/accordion/
  [Quick Start guide]: http://vene.github.com/scikit-learn-speed/quick_start.html
  [memory\_profiler]: http://pypi.python.org/pypi/memory_profiler
  [cProfile]: http://docs.python.org/library/profile.html#module-cProfile
