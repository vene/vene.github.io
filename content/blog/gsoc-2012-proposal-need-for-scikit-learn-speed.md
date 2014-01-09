Title: GSoC 2012 proposal: Need for scikit-learn speed
Date: 2012-04-16 00:37
Author: vene
Category: scikit-learn
Tags: gsoc, proposal
Slug: gsoc-2012-proposal-need-for-scikit-learn-speed

This summer I hope to be able to put in another full-time amount of
effort into scikit-learn. After a successful Google Summer of Code
project last year on dictionary learning, I now plan to do some
low-level work. The title of my proposal is: "Need for scikit-learn
speed" and, in a nutshell, will make the scikit go faster and will help
it stay that way.

Scikit-learn has always enforced standards of quality that kept all
implementations at a non-trivial level (i.e. faster than using [the
generic optimizers in scipy][]). However, not all modules are equal:
some have received more attention for speed than others (for example the
SGD classes). I intend to raise the bar towards a more uniform level.

Are you crazy, can you really do this?
--------------------------------------

Well, of course. This might not the usual GSoC proposal, but I can show
how I can do it and how it's easily quantifiable. Actually, a very
important part of the work will be to make scikit-learn's speed easily
measurable.

As for the specific speed-ups, I have shown [in][] [the][] [past][] that
I can do algorithmic and memory layout optimizations in numerical code.
There are parts in the scikit-learn that can benefit from such work: for
example only recently Peter merged this [pull request][] significantly
improving SGDClassifier's test time performance by switching the memory
layout of the coefficients: they were laid out optimally for the
training phase, not for the prediction phase.

There are certainly more opportunities for such speed improvements in
the scikit. Of course there is a lot of code that can't reasonably be
made any faster (I have a feeling that SGDClassifier is at the moment
such a case, but we can't know for sure without heavy profiling). But
generally there are many speed fixes that could weigh a lot: for
example, a [Cython][] implementation of the `euclidean_distances`
function that is able to use preallocated memory will improve the
performance of raw NearestNeighbours queries as well as of the KMeans
and hierarchical clustering algorithms.

How will we be able to tell if you succeed?
-------------------------------------------

A key part of the GSoC project is setting up a
<abbr title="Continuous Integration">CI</abbr>-style benchmark platform.
The point is to be able to track how the speed of certain operations
evolves in time. For such purposes, Wes McKinney developed the
[vbench][] project, introduced in [this blog post][]. The goal is for
every scikit-learn module to have several such benchmarks, for
differently shaped and structured data.

Having such a benchmark suite available is the equivalent of a test
suite, in terms of performance. It makes developers be extra conscious
of the effect of their changes. It also makes it more fun to chase speed
improvements, thanks to the positive reinforcement it gives.

There are some static benchmarks comparing the performance of
scikit-learn algorithms with other well-known libraries in the
[ml-benchmarks][] project. It would be very helpful to have such a
benchmark suite that automatically keeps up-to-date.

Side effects
------------

The cool thing about such a project is that it should raise the overall
quality of the scikit. The refactoring will lead to an increase in test
coverage, because the low-coverage modules are expected to be less
optimized as well. Also, the benchmarks will lead to well-backed
summaries in the documentation, such as [the one recently added in the
clustering section][].

Since the scikit is reaching a state where many well-known algorithms
are available, the **1.0** release is slowly approaching. My Google
Summer of Code project should bring the scikit significantly closer to
that milestone.

  [the generic optimizers in scipy]: http://docs.scipy.org/doc/scipy/reference/optimize.html
  [in]: http://localhost:8001/2011/08/07/optimizing-orthogonal-matching-pursuit-code-in-numpy-part-1/
    "Optimizing Orthogonal Matching Pursuit code in Numpy, part 1"
  [the]: http://localhost:8001/2011/08/11/optimizing-orthogonal-matching-pursuit-code-in-numpy-part-2/
    "Optimizing Orthogonal Matching Pursuit code in Numpy, part 2"
  [past]: http://localhost:8001/2011/11/18/the-nasty-bug-crawling-in-my-orthogonal-matching-pursuit-code/
    "The nasty bug crawling in my Orthogonal Matching Pursuit code"
  [pull request]: https://github.com/scikit-learn/scikit-learn/pull/545
  [Cython]: http://cython.org/
  [vbench]: https://github.com/pydata/vbench
  [this blog post]: http://wesmckinney.com/blog/?p=373
  [ml-benchmarks]: http://scikit-learn.sourceforge.net/ml-benchmarks/
  [the one recently added in the clustering section]: http://scikit-learn.org/dev/modules/clustering.html#overview-of-clustering-methods
