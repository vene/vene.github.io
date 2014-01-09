Title: Quick memory usage benchmarking in IPython
Date: 2012-06-30 08:53
Author: vene
Category: benchmarking
Tags: benchmark, IPython, magic, memory, memory_profiler, profiling, benchmarking, python
Slug: quick-memory-usage-benchmarking-in-ipython

Everybody loves `%timeit`, there's no doubt about it. So why not have
something like that, but for measuring how much memory your line takes?
Well, now you can; grab a hold of the script in the following gist and
run it like in the example.

[gist id=3022718]

Instead of taking care of the dirty process inspection stuff myself, I
decided to delegate this to Fabian's simple but very good
[`memory_profiler`][]. There is also [Guppy][] available, but its design
seems a bit and overkill for this task.

Please contact me if you find problems with this implementation, this is
a preliminary, quick hack-y version. :)

  [`memory_profiler`]: https://github.com/fabianp/memory_profiler
  [Guppy]: http://guppy-pe.sourceforge.net/
