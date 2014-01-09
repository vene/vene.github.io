Title: Optimizing Orthogonal Matching Pursuit code in Numpy, part 2
Date: 2011-08-11 19:39
Author: vene
Category: dictionary learning, python, scikit-learn
Tags: blas, efficient, lapack, numpy, omp, orthogonal matching pursuit, potrs, scipy
Slug: optimizing-orthogonal-matching-pursuit-code-in-numpy-part-2

EDIT: There was a bug in the final version of the code presented here.
It is fixed now, for its backstory, check out [my blog post on it][].

When we last saw our hero, he was fighting with the dreaded
implementation of least-angle regression, knowing full well that it was
his destiny to be faster.

We had come up with a more robust implementation, catching malformed
cases that would have broken the naive implementation, and also it was
orders of magnitude faster than said implementation. However, our
benchmark [[1][]] showed that it was a couple of times slower than
least-angle regression.

By poking around the `scikits.learn` codebase, I noticed that there is a
triangular system solver in `scikits.learn.utils.arrayfuncs`. Unlike the
`scipy.linalg` one, this one only works with lower triangular arrays,
and it forcefully overwrites `b`. Even though if weren't faster, it
should still be used: `scikits.learn` aims to be as backwards-compatible
with SciPy as possible, and `linalg.solve_triangular` was added in
0.9.0. Anyway, let's just see whether it's faster:

[sourcecode language="python"]  
In [1]: import numpy as np

In [2]: from scipy import linalg

In [3]: from scikits.learn.datasets import make\_spd\_matrix

In [4]: from scikits.learn.utils.arrayfuncs import solve\_triangular

In [5]: G = make\_spd\_matrix(1000)

In [6]: L = linalg.cholesky(G, lower=True)

In [7]: x = np.random.randn(1000)

In [8]: y = x.copy()

In [9]: timeit solve\_triangular(L, x)  
100 loops, best of 3: 3.45 ms per loop

In [10]: timeit linalg.solve\_triangular(L, y, lower=True,
overwrite\_b=True)  
10 loops, best of 3: 134 ms per loop  
[/sourcecode]

Wow! That's 40x faster. We're catching two rabbits with one stone here,
let's do the change! Notice that we can just copy [latex]
\\mathbf{v}[/latex] into the appropriate place in [latex] L[/latex] and
then solve in place.

But whoops! When solving the [latex] LL'[/latex] system, we take
advantage of the `transpose` attribute in `linalg.solve_triangular`,
which the `scikits.learn` version does not expose. We could think of a
solution, but here's a better idea: Shouldn't there be some way to
directly solve the entire system in one go?

Well, there is. It is an LAPACK function by the name of `potrs`. If you
are not aware, LAPACK is a Fortran library with solvers for various
types of linear systems and eigenproblems. LAPACK along with BLAS (on
which it is based) pretty much powers all the scientific computation
that happens. BLAS is an API with multiple implementations dating from
1979, while LAPACK dates from 1992. If you ever used Matlab, this is
what was called behind the scenes. SciPy, again, provides a high-level
wrapper around this, the `linalg.cho_solve` function.

But SciPy also gives us the possibility to import functions directly
from LAPACK, through the use of `linalg.lapack.get_lapack_funcs`. Let's
see how the low-level LAPACK function compares to the SciPy wrapper, for
our use case:

[sourcecode language="python"]  
In [11]: x = np.random.randn(1000)

In [12]: y = x.copy()

In [13]: timeit linalg.cho\_solve((L, True), x)  
1 loops, best of 3: 95.4 ms per loop

In [14]: potrs, = linalg.lapack.get\_lapack\_funcs(('potrs',), (G,))

In [15]: potrs  
Out[15]: &lt;fortran object&gt;

In [16]: timeit potrs(L, y)  
100 loops, best of 3: 9.49 ms per loop  
[/sourcecode]

That's 10 times faster! So now we found an obvious way to optimize the
code:

[sourcecode language="python"]  
def cholesky\_omp(X, y, n\_nonzero\_coefs, eps=None):  
min\_float = np.finfo(X.dtype).eps  
potrs, = get\_lapack\_funcs(('potrs',), (X,))  
alpha = np.dot(X.T, y)  
residual = y  
n\_active = 0  
idx = []

max\_features = X.shape[1] if eps is not None else n\_nonzero\_coefs  
L = np.empty((max\_features, max\_features), dtype=X.dtype)  
L[0, 0] = 1.

while 1:  
lam = np.abs(np.dot(X.T, residual)).argmax()  
if lam &lt; n\_active or alpha[lam] \*\* 2 &lt; min\_float:  
\# atom already selected or inner product too small  
warn(&quot;Stopping early&quot;)  
break  
if n\_active &gt; 0:  
\# Updates the Cholesky decomposition of X' X  
L[n\_active, :n\_active] = np.dot(X[:, idx].T, X[:, lam]  
solve\_triangular(L[:n\_active, :n\_active], L[n\_active, :n\_active])  
d = np.dot(L[n\_active, :n\_active].T, L[n\_active, :n\_active])  
if 1 - d &lt;= min\_float: \# selected atoms are dependent  
warn(&quot;Stopping early&quot;)  
break  
L[n\_active, n\_active] = np.sqrt(1 - d)  
idx.append(lam)  
\# solve LL'x = y in two steps:  
gamma, \_ = potrs(L[:n\_active, :n\_active], alpha[idx], lower=True,  
overwrite\_b=False)  
residual = y - np.dot(X[:, idx], gamma)  
if eps is not None and np.dot(residual.T, residual) &lt;= eps:  
break  
elif n\_active == max\_features:  
break  
return gamma, idx  
[/sourcecode]

Woohoo! But we still lag behind. Now that we delegated the trickiest
parts of the code to fast and reliable solvers, it's time to use a
profiler and see what the bottleneck is now. Python has excellent tools
for this purpose. What solved the problem in this case was
`line_profiler` [[2][]]. There is a great article by Olivier Grisel here
[2] regarding how to use these profilers. I'm just going to say that
`line_profiler`'s output is very helpful, basically printing the time
taken by each line of code next to that line.

Running the profiler on this code, we found that 58% of the time is
spent on line 14, 20.5% on line 21, and 20.5% on line 32, with the rest
being insignificant (`potrs` takes 0.1%!). The code is clearly dominated
by the matrix multiplications. By running some more timings with
IPython, I found that multiplying such column-wise views of the data as
`X[:, idx]` is considerably slower then multiplying a contiguous array.
The least-angle regression code in `scikits.learn` avoids this by
swapping columns towards the front of the array as they are chosen, so
we can replace `X[:, idx]` with `X[:, :n_active]`. The nice part is that
if the array is stored in Fortran-contiguous order (ie. column
contiguous order, as opposed to row contiguous order, as in C), swapping
two columns is a very fast operation!. Let's see some more benchmarks!

[sourcecode language="python"]  
In [17]: X = np.random.randn(5000, 5000)

In [18]: Y = X.copy('F') \# fortran-ordered

In [19]: a, b = 1000, 2500

In [20]: swap, = linalg.get\_blas\_funcs(('swap',), (X,))

In [21]: timeit X[:, a], X[:, b] = swap(X[:, a], X[:, b])  
100 loops, best of 3: 6.29 ms per loop

In [22]: timeit Y[:, a], Y[:, b] = swap(Y[:, a], Y[:, b])  
10000 loops, best of 3: 111 us per loop  
[/sourcecode]

We can see that using Fortran-order takes us from the order of
miliseconds to the order of microseconds!

Side note: I almost fell into the trap of swapping columns the pythonic
way. That doesn't work:  
[sourcecode language="python"]  
In [23]: X[:, a], X[:, b] = X[:, b], X[:, a]

In [24]: np.testing.assert\_array\_equal(X[:, a], X[:, b])

In [25]:  
[/sourcecode]

However this trick works great for swapping elements of one-dimensional
arrays.

Another small optimization that we can do: I found that on my system,
it's slightly faster to compute the norm using the BLAS function `nrm2`.
So by putting all of these together, we end up with the final version of
our code:

[sourcecode language="python"]  
def cholesky\_omp(X, y, n\_nonzero\_coefs, eps=None,
overwrite\_X=False):  
if not overwrite\_X:  
X = X.copy('F')  
else: \# even if we are allowed to overwrite, still copy it if bad
order  
X = np.asfortranarray(X)

min\_float = np.finfo(X.dtype).eps  
nrm2, swap = linalg.get\_blas\_funcs(('nrm2', 'swap'), (X,))  
potrs, = get\_lapack\_funcs(('potrs',), (X,))

indices = range(len(Gram)) \# keeping track of swapping  
alpha = np.dot(X.T, y)  
residual = y  
n\_active = 0

max\_features = X.shape[1] if eps is not None else n\_nonzero\_coefs  
L = np.empty((max\_features, max\_features), dtype=X.dtype)  
L[0, 0] = 1.

while True:  
lam = np.abs(np.dot(X.T, residual)).argmax()  
if lam &lt; n\_active or alpha[lam] \*\* 2 &lt; min\_float:  
\# atom already selected or inner product too small  
warn(&quot;Stopping early&quot;)  
break  
if n\_active &gt; 0:  
\# Updates the Cholesky decomposition of X' X  
L[n\_active, :n\_active] = np.dot(X[:, :n\_active].T, X[:, lam])  
solve\_triangular(L[:n\_active, :n\_active], L[n\_active, :n\_active])  
v = nrm2(L[n\_active, :n\_active]) \*\* 2  
if 1 - v &lt;= min\_float: \# selected atoms are dependent  
warn(&quot;Stopping early&quot;)  
break  
L[n\_active, n\_active] = np.sqrt(1 - v)  
X.T[n\_active], X.T[lam] = swap(X.T[n\_active], X.T[lam])  
alpha[n\_active], alpha[lam] = alpha[lam], alpha[n\_active]  
indices[n\_active], indices[lam] = indices[lam], indices[n\_active]  
n\_active += 1  
\# solves LL'x = y as a composition of two triangular systems  
gamma, \_ = potrs(L[:n\_active, :n\_active], alpha[:n\_active],
lower=True,  
overwrite\_b=False)

residual = y - np.dot(X[:, :n\_active], gamma)  
if eps is not None and nrm2(residual) \*\* 2 &lt;= eps:  
break  
elif n\_active == max\_features:  
break

return gamma, indices[:n\_active]  
[/sourcecode]

Now, the benchmark at [[1][]] indicates victory over least-angle
regression! I hope you have enjoyed this short tour. See you next time!

[<span id="footnote-1">1</span>] [OMP vs. Lars benchmark][]  
[<span id="footnote-2">2</span>] [Profiling Python code][]

  [my blog post on it]: http://venefrombucharest.wordpress.com/2011/11/18/the-nasty-bug-crawling-in-my-orthogonal-matching-pursuit-code/
    "The nasty bug crawling in my Orthogonal Matching Pursuit code"
  [1]: #footnote-1
  [2]: #footnote-2
  [OMP vs. Lars benchmark]: https://github.com/scikit-learn/scikit-learn/blob/master/benchmarks/bench_plot_omp_lars.py
    "Orthogonal matching pursuit versus least-angle regression"
  [Profiling Python code]: http://scikit-learn.sourceforge.net/dev/developers/performance.html#profiling-python-code
    "Profiling Python code"
