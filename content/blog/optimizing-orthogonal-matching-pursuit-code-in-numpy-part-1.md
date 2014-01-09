Title: Optimizing Orthogonal Matching Pursuit code in Numpy, part 1
Date: 2011-08-07 20:50
Author: vene
Category: dictionary learning, python, scikit-learn
Tags: efficient, numpy, omp, orthogonal matching pursuit, scipy
Slug: optimizing-orthogonal-matching-pursuit-code-in-numpy-part-1

After intense code optimization work, my implementation of OMP finally
beat least-angle regression! This was the primary issue discussed during
the pull request, so once performance was taken care of, the code was
ready for merge. Orthogonal matching pursuit is now available in
scikits.learn as a sparse linear regression model. OMP is a key building
block of the dictionary learning code that we are working on merging.

I will go through the process of developing this particular piece of
code as an example of code refining and iterative improvements, as well
as for the useful notes it will provide on optimizing numerical Python
code. In the first part we will see how the code got from pseudocode
state to a reasonably efficient code with smart memory allocation. In
the next part we will see how to make it blazing fast by leveraging
[[1][]] lower level BLAS and LAPACK routines, and how to use profiling
to find hot spots.

As stated before, orthogonal matching pursuit is a greedy algorithm for
finding a sparse solution [latex] \\gamma[/latex] to a linear regression
problem [latex] X\\gamma = y[/latex]. Mathematically, it approximates
the solution of the optimization problem:

\$\$ \\text{argmin} {\\big|\\big|} \\gamma {\\big|\\big|} \_0 \\text{
subject to }{\\big |\\big|}y-X\\gamma{\\big|\\big|}\_2\^2 \\leq
\\epsilon \$\$  
or (under a different parametrization):  
\$\$\\text{argmin} {\\big |\\big|}y - X\\gamma{\\big |\\big|}\_2\^2
\\text{ subject to } {\\big|\\big|}\\gamma{\\big|\\big|}\_0 \\leq
n\_{\\text{nonzero coefs}}\$\$

In the code samples in this post I will omit the docstrings, but I will
follow the notation in the formulas above.

**Important note:** The regressors/dictionary atoms (the columns of
[latex] X[/latex]) are assumed to be normalized throughout this post (as
well as usually any discussion of OMP). We also assume the following
imports:  
[sourcecode language="Python"]  
import numpy as np  
from scipy import linalg  
[/sourcecode]

Orthogonal matching pursuit is a very simple algorithm in pseudocode,
and as I stated before, it almost writes itself in Numpy. For this
reason, instead of stating the pseudocode here, I will start with how
naively implemented OMP looks like in Python:

[sourcecode language="Python"]  
def orthogonal\_mp(X, y, n\_nonzero\_coefs, eps=None):  
residual = y  
idx = []  
if eps == None:  
stopping\_condition = lambda: len(idx) == n\_nonzero\_coefs  
else:  
stopping\_condition = lambda: np.inner(residual, residual) &lt;= eps  
while not stopping\_condition():  
lam = np.abs(np.dot(residual, X)).argmax()  
idx.append(lam)  
gamma, \_, \_, \_ = linalg.lstsq(X[:, idx], y)  
residual = y - np.dot(X[:, idx], gamma)  
return gamma, idx  
[/sourcecode]

Using lambda expressions as stopping conditions never looked like a
brilliant idea, but it seems to me like the most elegant way to specify
such a variable stopping condition. However, the biggest slowdown in
this is the need for solving a least squares problem at each iteration,
while least-angle regression is known to produce the entire
regularization path for the cost of a single least squares problem. We
will also see that this implementation is more vulnerable to numerical
stability issues.

In [[2][]], Rubinstein et al. described the Cholesky-OMP algorithm, an
implementation of OMP that avoids solving a new least squares problem at
each iteration by keeping a Cholesky decomposition [latex] LL'[/latex]
of the Gram matrix [latex] G =
X\_{\\text{idx}}'X\_{\\text{idx}}[/latex]. Because [latex]
X\_{\\text{idx}}[/latex] grows by exactly one column at each iteration,
[latex] L[/latex] can be updated according to the following rule: Given
[latex] A = \\begin{pmatrix} \\tilde{A} & \\mathbf{v}' \\\\ \\mathbf{v}
& c \\end{pmatrix}[/latex], and knowing the decomposition of [latex]
\\tilde{A} = \\tilde{L}\\tilde{L}'[/latex], the Cholesky decomposition
[latex] A = LL'[/latex] is given by \$\$ L = \\begin{pmatrix}\\tilde{L}
& \\mathbf{0} \\\\ \\mathbf{w}' & \\sqrt{c - \\mathbf{w}'\\mathbf{w}}
\\end{pmatrix}, \\text{ where } \\tilde{L}\\mathbf{w} = \\mathbf{v}\$\$

Even if you are unfamiliar with the mathematical properties of the
Cholesky decomposition, you can see from the construction detailed above
that [latex] L[/latex] is always going to be a lower triangular matrix
(it will only have null elements above the main diagonal). Actually, the
letter L stands for lower. We have therefore replaced the step where we
needed to solve the least-squares problem [latex]
X\_{\\text{idx}}\\gamma = y[/latex] with two much simpler computations:
solving [latex] \\tilde{L}\\mathbf{w} = \\mathbf{v}[/latex] and solving
[latex] LL'\\gamma = X\_{\\text{idx}}'y[/latex]. Due to the [latex]
L[/latex]'s structure, these are much quicker operations than a least
squares projection.  
Here is the initial way I implemented this:

[sourcecode language="Python"]

def cholesky\_omp(X, y, n\_nonzero\_coefs, eps=None):  
if eps == None:  
stopping\_condition = lambda: it == n\_nonzero\_coefs  
else:  
stopping\_condition = lambda: np.inner(residual, residual) \<= eps

alpha = np.dot(X.T, y)  
residual = y  
idx = []  
L = np.ones((1,1))

while not stopping\_condition():  
lam = np.abs(np.dot(residual, X)).argmax()  
if len(idx) &gt; 0:  
w = linalg.solve\_triangular(L, np.dot(X[:, idx].T, X[:, lam]),  
lower=True)  
L = np.r\_[np.c\_[L, np.zeros(len(L))],  
np.atleast\_2d(np.append(w, np.sqrt(1 - np.dot(w.T, w))))]  
idx.append(lam)  
\# solve LL'x = y in two steps:  
Ltx = linalg.solve\_triangular(L, alpha[idx], lower=True)  
gamma = linalg.solve\_triangular(L, Ltx, trans=1, lower=True)  
residual = y - np.dot(X[:, idx], gamma)

return gamma, idx  
[/sourcecode]

Note that a lot of the code remained unchanged, this is the same
algorithm as before, only the Cholesky trick is used to improve
performance. According to the plot in [[3][]], we can see that the naive
implementation has oscillations of the reconstruction error due to
numerical instability, while this Cholesky implementation is
well-behaved.

Along with this I also implemented the Gram-based version of this
algorithm, which only needs [latex] X'X[/latex] and [latex] X'y[/latex]
(and [latex] {\\big|\\big|}y{\\big|\\big|}\_2\^2[/latex], in case the
epsilon-parametrization is desired). This is called **Batch OMP** in
[[2][]], because it offers speed gains when many signals need to be
sparse coded against the same dictionary [latex] X[/latex]. A lot of
speed is gained because two large matrix multiplications are avoided at
each iteration, but for many datasets, the cost of the precomputations
dominates the procedure. I will not insist on Gram OMP in this post, it
can be found in the `scikits.learn` repository [[4][]].

Now, the problems with this are a bit more subtle. At this point, I
moved on to code other things, since OMP was passing tests and the
signal recovery example was working. The following issues popped up
during review:

​1. The lambda stopping condition does not pickle.  
2. For well-constructed signals and data matrices, assuming normal
atoms, [latex] \\mathbf{w}[/latex] on line 14 will never have norm
greater than or equal to zero, unless the chosen feature happens to be
dependent of the already chosen set. In theory, this cannot happen,
since we do an orthogonal projection at each step. However, if the
matrix [latex] X[/latex] is not well-behaved (for example, if it has two
identical columns, and [latex] y[/latex] is built using non-zero
coefficients for those columns), then we end up with the square root of
a negative value on line 17.  
3. It was orders of magnitude slower than least-angle regression, given
the same number of nonzero coefficients.

1 was an easy fix. 2 was a bit tricky since it was a little hidden: the
first time I encountered such an error, I wrongfully assumed that given
that the diagonal of [latex] X\_\\text{idx}'X\_\\text{idx}[/latex] was
unit, then [latex] L[/latex] should also have a unit diagonal, so I
passed the parameter `unit_diagonal=True` to `linalg.solve_triangular`,
and the plethora of NaN's along the diagonal were simply ignored. Let
this show what happens when you don't pay attention when coding.

When I realized my mistake, I first did something I saw in `lars_path`
from the scikit: take the absolute value of the argument of `sqrt`, and
also ensure it is practically larger than zero. However, tests started
failing randomly. Confusion ensued until the nature of the issue,
discussed above, was discovered. It's just not right to take the `abs`:
if that argument ends up less than zero, OMP simply cannot proceed and
must stop due to malformed data. The reference implementation from the
website of the authors of [[2][]] includes explicit *early stopping*
conditions for this, along with some other cases.

At the same time, I started to try a couple of optimizations. The most
obvious thing was the way I was building the matrix [latex] L[/latex]
was clearly suboptimal, reallocating it at each iteration.

This leads to the following code:

[sourcecode language="Python"]

def cholesky\_omp(X, y, n\_nonzero\_coefs, eps=None):  
min\_float = np.finfo(X.dtype).eps  
alpha = np.dot(X.T, y)  
residual = y  
n\_active = 0  
idx = []

max\_features = X.shape[1] if eps is not None else n\_nonzero\_coefs  
L = np.empty((max\_features, max\_features), dtype=X.dtype)  
L[0, 0] = 1.

while 1:  
lam = np.abs(np.dot(X.T, residual)).argmax()  
if lam \< n\_active or alpha[lam] \*\* 2 \> min\_float:  
\# atom already selected or inner product too small  
warn(&quot;Stopping early&quot;)  
break  
if n\_active &gt; 0:  
\# Updates the Cholesky decomposition of X' X  
w = linalg.solve\_triangular(L[:n\_active, :n\_active],  
np.dot(X[:, idx].T, X[:, lam]),  
lower=True)  
L[n\_active, :n\_active] = w  
d = np.dot(w.T, w)  
if 1 - d &lt;= min\_float: \# selected atoms are dependent  
warn("Stopping early")  
break  
L[n\_active, n\_active] = np.sqrt(1 - d)  
idx.append(lam)  
\# solve LL'x = y in two steps:  
Ltx = linalg.solve\_triangular(L[:n\_active, :n\_active], alpha[idx],
lower=True)  
gamma = linalg.solve\_triangular(L[:n\_active, :n\_active], Ltx,
trans=1, lower=True)  
residual = y - np.dot(X[:, idx], gamma)  
if eps is not None and np.dot(residual.T, residual) &lt;= eps:  
break  
elif n\_active == max\_features:  
break  
return gamma, idx  
[/sourcecode]

What should be noted here, apart from the obvious fix for \#1, are the
early stopping conditions. It is natural to stop if the same feature
gets picked twice: the residual is always orthogonalized with respect to
the chosen basis, so the only way this could happen is if there would be
no more unused independent regressors. This would either lead to this,
or to the stopping criterion on line 25, depending on which equally
insignificant vector gets picked. The other criterion for early stopping
is if the chosen atom is orthogonal to y, which would make it
uninformative and would again mean that there are no better ones left,
so we might as well quit looking.

Also, we now make sure that [latex] L[/latex] is preallocated. Note that
`np.empty` is marginally faster than `np.zeros` because it does not
initialize the array to zero after allocating, so the untouched parts of
the array will contain whatever happened to be in memory before. In our
case, this means only the values above the main diagonal: everything on
and beneath is initialized before access. Luckily, the
`linalg.solve_triangular` function ignores what it doesn't need.

This is a robust implementation, but still a couple of times slower than
least-angle regression. In the next part of the article we will see how
we can make it beat LARS.

<span id="footnote-1">[1]</span> I always wanted to use this word in a
serious context :P  
<span id="footnote-2">[2]</span> Rubinstein, R., Zibulevsky, M. and
Elad, M., [Efficient Implementation of the K-SVD Algorithm using Batch
Orthogonal Matching Pursuit][] Technical Report - CS Technion, April
2008.  
<span id="footnote-3">[3]</span> [First thoughts on Orthogonal
Matching Pursuit][] on this blog.  
<span id="footnote-4">[4]</span> [omp.py][] on github.

  [1]: #footnote-1
  [2]: #footnote-2
  [3]: #footnote-3
  [4]: #footnote-4
  [Efficient Implementation of the K-SVD Algorithm using Batch
  Orthogonal Matching Pursuit]: http://www.cs.technion.ac.il/~ronrubin/Publications/KSVD-OMP-v2.pdf
  [First thoughts on Orthogonal Matching Pursuit]: http://venefrombucharest.wordpress.com/2011/05/30/first-thoughts-on-orthogonal-matching-pursuit/
    "First thoughts on Orthogonal Matching Pursuit"
  [omp.py]: https://github.com/scikit-learn/scikit-learn/blob/master/scikits/learn/linear_model/omp.py
