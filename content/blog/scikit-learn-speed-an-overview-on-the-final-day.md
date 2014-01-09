Title: Scikit-learn-speed: An overview on the final day
Date: 2012-08-20 02:44
Author: vene
Category: benchmarking, python, scikit-learn
Tags: gsoc, optimization, scikit-learn-speed, speedup, summary, vbench
Slug: scikit-learn-speed-an-overview-on-the-final-day

This summer, I was granted the project called *scikit-learn-speed*,
consisting of developing a benchmarking platform for *scikit-learn* and
using it to find potential speedups, and in the end, make the library go
faster wherever I can.

On the official closing day of this work, I'd like to take a moment and
recall the accomplishments and failures of this project, and all the
lessons to be learned.

The *scikit-learn-speed* benchmark platform
-------------------------------------------

[![][]][]  
[*Scikit-learn-speed*][![][]] is a continuous benchmark suite for the
[*scikit-learn*][] library. It has the following features:

-   *vbench*-powered integration with Git
-   Easily triggered build and report generation: just type `make`
-   Easily readable and writeable template for benchmarks:
    <p>
    [sourcecode lang="python"]  
    {  
    'obj': 'LogisticRegression',  
    'init\_params': {'C': 1e5},  
    'datasets': ('arcene', 'madelon'),  
    'statements': ('fit', 'predict')  
    }, ...  
    [/sourcecode]
-   Many attributes recorded: time (w/ estimated standard deviation),
    memory usage, cProfiler output, line\_profiler output, tracebacks
-   Multi-step benchmarks: i.e. `fit` followed by `predict`

What were the lessons I learned here?

### Make your work reusable: the trade-off between good design and get-it-working-now

For the task of rolling out a continuous benchmarking platform, we
decided pretty early in the project to adopt Wes McKinney's *vbench*. If
my goal would've been to maintain *vbench* and extend it into a
multi-purpose, reusable benchmarking framework, the work would've been
structured differently. It also would have been very open-ended and
difficult to quantify.

The way things have been, I came up with features that we need in
*scikit-learn-speed*, and tried to implement them in *vbench* without
refactoring too much, but still by trying to make them as reusable as
possible.

The result? I got all the features for *scikit-learn-speed*, but the
implementation is not yet clean enough to be merged into *vbench*. This
is fine for a project with a tight deadline such as this one: after it's
done, I will just spend another weekend on cleaning the work up and
making sure it's appreciated upstream. This will be easier because of
the constraint to keep compatibility with *scikit-learn-speed*.

### Never work quietly (unless you're a ninja)

I know some students who prefer that the professor doesn't even know
they exist until the final, when they would score an A, and (supposedly)
leave the professor amazed. In real life, plenty of people would be
interested in what you are doing, as long as they know about it. The PSF
goes a long way to help this, with the "blog weekly" rule. In the end,
however, it's all up to you to make sure that everybody who should know
finds out about your work. It will spare the world the duplicated work,
the abandoned projects, but most importantly, those people could point
you to things you have missed. Try to mingle in real-life as well,
attend conferences, meetups, coding sprints.

I was able to slightly "join forces" with a couple of people who
contacted me about my new *vbench* features (Hi Jon and Joel!), I have
shaped my design slightly towards their requirements as well, and
hopefully the result will be a more general *vbench*.

The speedups
------------

Once *scikit-learn-speed* was up and running, I couldn't believe how
useful it is to be able to scroll, catch slow code and jump straight at
the profiler output with one click. I jumped on the following speed-ups:

-   Multiple outputs in linear models. ([PR][])
    <p>
    Some of them proved trickier than expected, so I didn't implement it
    for all the module yet, but it is ready for some estimators.
-   Less callable functions passed around in `FastICA` ([merged][])
-   Speed up `euclidean_distances` by rewriting in Cython. ([PR][1])
    <p>
    This meant making more operations support an `out` argument, for
    passing preallocated memory. This touches many  
    different objects in the codebase: clustering, manifold learning,
    nearest neighbour methods.
-   [Insight into inverse and pseudoinverse computation][], new `pinvh`
    function for inverting symmetric/hermitian matrices. ([PR][2])
    <p>
    This speeds up the covariance module (especially `MinCovDet`),
    `ARDRegression` and the mixture models. It also lead to an [upstream
    contribution to Scipy][]
-   `OrthogonalMatchingPursuit` forward stepwise path for
    cross-validation ([PR][3])
    <p>
    This is only halfway finished, but it will lead to faster and easier
    optimization of the `OMP` sparsity parameter.

Lessons? These will be pretty obvious.

### Write tests, tests, tests!

This is a no-brainer, but it still didn't stick. In that one case out of
10 that I didn't explicitly test, a bug was obviously hiding. When you
want to add a new feature, it's best to start by writing a failing test,
and then [making it pass][]. Sure, you will miss tricky bugs, but you
will never have embarrassing, obvious bugs in your code :)

### Optimization doesn't have to be ugly

Developers often shun optimization. It's true, you should profile first,
and you shouldn't focus on speeding up stuff that is dominated by other
computations that are orders of magnitude slower. However, there is an
elephant in the room: the assumption that making code faster invariably
makes it less clear, and takes a lot of effort.

The following code is a part of scipy's `pinv2` function as it currently
is written:  
[sourcecode lang="python"]  
cutoff = cond\*np.maximum.reduce(s)  
psigma = np.zeros((m, n), t)  
for i in range(len(s)):  
if s[i] \> cutoff:  
psigma[i,i] = 1.0/np.conjugate(s[i])  
return np.transpose(np.conjugate(np.dot(np.dot(u,psigma),vh)))  
[/sourcecode]

`psigma` is a diagonal matrix, and some time and memory can be saved
with simple vectorization. However, this part of the code dominated by
an above call to `svd`. The profiler output would say that we shouldn't
bother, but is it really a bother? Look at Jake's new version:

[sourcecode lang="python"]  
above\_cutoff = (s \> cond \* np.max(s))  
psigma\_diag = np.zeros\_like(s)  
psigma\_diag[above\_cutoff] = 1.0 / s[above\_cutoff]

return np.transpose(np.conjugate(np.dot(u \* psigma\_diag, vh)))  
[/sourcecode]

It's shorter, more elegant, easier to read, and nevertheless faster. I
would say it is worth it.

### Small speed-ups can propagate

Sure, it's great if you can compute an inverse two times faster, say in
0.5s instead of 1s. But if some algorithm calls this function in a loop
that might iterate 100, 300, or 1000 times, this small speed-up seems
much more important, doesn't it?

What I'm trying to say with this is that in a well-engineered system, a
performance improvement to a relatively small component (such as the
function that computes a pseudoinverse) can lead to multiple spread out
improvements. Be careful of the double edge of this sword, a bug
introduced in a small part can cause multiple failures downstream. But
you *are* fully covered by your test suite, aren't you?

Overall it has been a fruitful project that may have not resulted in a
large number of speed-ups, but a few considerable ones nonetheless. And
I venture the claim that the *scikit-learn-speed* tool will prove useful
over time, and that the efforts deployed during this project have
stretched beyond the boundary of the *scikit-learn*.

  []: http://localhost:8001/wp-content/uploads/2012/08/skl-speed-300x163.png
    "skl-speed"
  [![][]]: http://jenkins-scikit-learn.github.com/scikit-learn-speed/
  [*scikit-learn*]: http://scikit-learn.org
  [PR]: https://github.com/scikit-learn/scikit-learn/pull/913
  [merged]: https://github.com/scikit-learn/scikit-learn/pull/927
  [1]: https://github.com/scikit-learn/scikit-learn/pull/1006
  [Insight into inverse and pseudoinverse computation]: http://localhost:8001/2012/08/18/inverses-pseudoinverses-numerical-issues-speed-symmetry/
    "Inverses and pseudoinverses. Numerical issues, speed, symmetry."
  [2]: https://github.com/scikit-learn/scikit-learn/pull/1015
  [upstream contribution to Scipy]: https://github.com/scipy/scipy/pull/289
  [3]: https://github.com/scikit-learn/scikit-learn/pull/1042
  [making it pass]: http://c2.com/cgi/wiki?MakeItWorkMakeItRightMakeItFast
