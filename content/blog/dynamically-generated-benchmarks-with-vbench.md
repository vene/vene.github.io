Title: Dynamically generated benchmarks with vbench
Date: 2012-06-07 01:57
Author: vene
Category: benchmarking, python, scikit-learn
Tags: gsoc, vbench
Slug: dynamically-generated-benchmarks-with-vbench

To construct a `vbench` benchmark you need a setup string and a code
string. The constructor's signature is:  

`Benchmark(self, code, setup, ncalls=None, repeat=3, cleanup=None, name=None, description=None, start_date=None, logy=False)`.

Why generate benchmarks dynamically?
------------------------------------

For most `scikit-learn` purposes, the `code` string will be very close
to `"algorithm.fit(X, y)"`, `"algorithm.transform(X)"` or
`"algorithm.predict(X)"`. We can generate a lot of benchmarks by
changing what the algorithm is, and changing what the data is or the way
it is generated.

A possible idea would be to create a
<abbr title="domain-specific language" lang="en">DSL</abbr> in which to
specify scikit-learn tests and create benchmarks from them. However,
before engineering such a solution, I wanted to test out how to generate
three related benchmarks using different arguments for the dataset
generation function.

This is what I came up with:

[sourcecode language="python"]  
from vbench.benchmark import Benchmark

\_setup = """  
from deps import \*

kwargs = %s  
X, y = make\_regression(random\_state=0, \*\*kwargs)  
lr = LinearRegression()  
"""

\_configurations = [  
('linear\_regression\_many\_samples',  
{'n\_samples': 10000, 'n\_features': 100}),  
('linear\_regression\_many\_features',  
{'n\_samples': 100, 'n\_features': 10000}),  
('linear\_regression\_many\_targets',  
{'n\_samples': 1000, 'n\_features': 100, 'n\_targets': 100})  
]

\_statement = "lr.fit(X, y)"

\_globs = globals()  
\_globs.update({name: Benchmark(\_statement, \_setup % str(kwargs),
name=name)  
for name, kwargs in \_configurations})

[/sourcecode]

It works perfectly, but I don't like having to hack the globals to make
the benchmarks detectable. This is because of the way the vbench suite
gathers benchmarks. In `__init__.py` we have to do
`from linear_regression import *`. With a small update to the detection
method, we could replace the hacky part with a public lists of Benchmark
objects.

Exposed issues
--------------

While working on this, after my first attempt, I was surprised to see
that there were no results added to the database, and output plots were
empty. It turns out that the generated benchmarks weren't running, even
though if I copied and pasted their source code from the generated html,
it would run. Vbench was not issuing any sort of message to let me know
that anything was wrong.

So what was the problem? My fault, of course, whitespace. But in all
fairness, we should add better feedback.

This is what I was doing to generate the setup string:

[sourcecode lang="python"]  
def \_make\_setup(kwargs):  
return """  
from deps import \*

kwargs = %s  
X, y = make\_regression(random\_state=0, \*\*kwargs)  
lr = LinearRegression()  
""" % str(kwargs)  
[/sourcecode]

It's clear as daylight now that I overzealously indented the multiline
string. But man, was it hard to debug! Also, in this example, the bug
led to a refactoring that made the whole thing nicer and more direct.
Hopefully, my experience with vbench will lead to some improvements to
this cool and highly useful piece of software.
