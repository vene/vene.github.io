Title: Memory benchmarking with vbench
Date: 2012-07-05 12:38
Author: vene
Category: benchmarking
Tags: memit, memory, vbench, python, scikit-learn
Slug: memory-benchmarking-with-vbench

The [scikit-learn-speed project][] now has memory usage benchmarking!

This was accomplished by building on what I described in my recent
posts, specifically the extensions to Fabian's [memory\_profiler][] that
you can find in [my fork][], but they will be merged upstream soon. The
key element is the `%magic_memit` function whose development I blogged
about [on][] [several][] [occasions][]. I plugged this into [vbench][]
in a similar way to how the timings are computed, all with great
success.

Here is a screenshot of the way a simple benchmark looks now, with just
a few data points.

[caption id="attachment\_464" align="aligncenter" width="600"][![A
screenshot showing generated output from the scikit-learn-speed project,
illustrating memory usage benchmarking.][]][] Memory benchmarking in
scikit-learn-speed powered by vbench.[/caption]

You can check it out and use it yourself for your benchmarks, but you
need to use the vbench from the [memory branch on my fork][].

Of course, there are some important caveats. I am running this on my
laptop, which runs OS X Lion, so, under the effect of [this
bug][occasions], I hardcoded the '`-i`' so the memory benchmarks are not
realistic. Also, the y-range should probably be forced wider, because
the plots look erratic, showing the very small noise at a large-scale.

  [scikit-learn-speed project]: https://github.com/vene/scikit-learn-speed
  [memory\_profiler]: https://github.com/fabianp/memory_profiler
  [my fork]: https://github.com/vene/memory_profiler
  [on]: http://localhost:8001/2012/06/30/quick-memory-usage-benchmarking-in-ipython/
    "Quick memory usage benchmarking in IPython"
  [several]: http://localhost:8001/2012/07/02/more-on-memory-benchmarking/
    "More on memory benchmarking"
  [occasions]: http://localhost:8001/2012/07/04/on-why-my-memit-fails-on-osx/
    "On why my %memit fails on OSX"
  [vbench]: http://wesmckinney.com/blog/?p=373
  [A screenshot showing generated output from the scikit-learn-speed
  project, illustrating memory usage benchmarking.]: http://localhost:8001/wp-content/uploads/2012/07/vbench1.png
    "Memory benchmarking in scikit-learn-speed powered by vbench."
  [![A screenshot showing generated output from the scikit-learn-speed
  project, illustrating memory usage benchmarking.][]]: http://localhost:8001/wp-content/uploads/2012/07/vbench1.png
  [memory branch on my fork]: https://github.com/vene/vbench/tree/memory
