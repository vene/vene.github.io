Title: The scikit-learn-speed ship has set sail! Faster than ever, with multi-step benchmarks!
Date: 2012-08-11 17:32
Author: vene
Category: benchmarking, python, scikit-learn
Tags: multi-step, multistep, vbench
Slug: the-scikit-learn-speed-ship-has-set-sail-faster-than-ever-with-multi-step-benchmarks

I am pleased to announce that last night at 2:03 AM, the first fully
automated run of the scikit-learn-speed test suite has run on our
Jenkins instance! You can admire it at [its temporary home][] for now.
As soon as we verify that everything is good, we will move this to the
official scikit-learn page.

I would like to take this opportunity to tell you about our latest
changeset. We made running the benchmark suite tons simpler by adding a
friendly Makefile. You can read more about its usage in the guide. But
by far, our coolest new toy is:

Multi-step benchmarks
---------------------

A standard vbench benchmark has three units of code, represented as
strings: `code`, `setup` and `cleanup`. With the original timeit-based
benchmarks, this means that for every run, the setup would be executed
once. Then, the main loop runs `repeat` times, and within each
iteration, the `code` is run `ncalls` times. Then `cleanup` happens, the
best time is returned, and everybody is happy.

In scikit-learn, most of our interesting objects go through a state
change called *fitting*. This metaphor is right at home in the machine
learning field, where we separate the learning phase for the prediction
phase. The prediction step cannot be invoked on an object that hasn't
been fitted.

For some algorithms, one of these steps is trivial. A brute force
Nearest Neighbors classifier can be instantaneously fit, but prediction
takes a while. On the opposite end we have linear models, with tons of
complicated algorithms to fit them, but evaluation is a simple
matrix-vector product that Numpy handles perfectly.

But many of scikit-learn's estimators have both steps interesting. Let's
take Non-negative Matrix Factorization. It has three interesting
functions: The `fit` that computes \$latex X = WH \$, the `transform`
that computes a non-negative projection on the components learned in
`fit`, and `fit_transform` that takes advantage of the observation that
when fitting, we also get the transformed \$latex X \$ for free.

When benchmarking NMF, we initially had to design 3 benchmarks:

-   `setup = `standard, `code = obj.fit(X)`
-   `setup = `standard, `code = obj.fit_transform(X)`
-   `setup = `standard` + obj.fit(X)`, `code = obj.transform(X)`

How much time were we wasting?
------------------------------

Let's say it takes 10 seconds. For every benchmark, we time the code by
running it 3 times. We run it once more to measure memory usage, once
more for `cProfile` and one last time for `line_profiler`. This is a
total of 6 times per benchmark. We need to multiply this by 2 again for
running on two datasets. So when benchmarking `NMF`, because we need to
fit before predicting, we do it 12 extra times. If a fit takes 5
seconds, this means one minute wasted on benchmarking just one
estimator. *Wouldn't it be nice to `fit`, `fit_transform` and
`transform` in a sequence?*

Behind the scenes
-----------------

We made the `PythonBenchmark code` parameter also support getting a
sequence of strings, instead of just a string. On the database side,
every benchmark result entry gets an extra component in the primary key,
the number of the step it measures.

In the benchmark description files, nothing is changed:

[sourcecode lang="python"]  
{  
'obj': 'NMF',  
'init\_params': {'n\_components': 2},  
'datasets': ('blobs',),  
'statements': ('fit\_unsup', 'transform\_unsup', 'fit\_transform')  
},  
[/sourcecode]

But before, we would take the cartesian product of datasets and
statements, and build a `Benchmark` object for every pairing. Now, we
just pass the tuple as it is, and vbench is smart enough to do the right
thing.  
We avoided the extra calls to `fit` in a lot of benchmarks. The whole
suite now takes almost half the time to run!

*Note:* This trick is currently hosted in the
`abstract_multistep_benchmarks` vbench branch in my fork.

  [its temporary home]: http://jenkins-scikit-learn.github.com/scikit-learn-speed/
