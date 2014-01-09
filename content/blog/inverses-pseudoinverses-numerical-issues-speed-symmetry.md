Title: Inverses and pseudoinverses. Numerical issues, speed, symmetry.
Date: 2012-08-18 19:41
Author: vene
Category: benchmarking
Tags: inv, matrix inverse, numerical analysis, numerical methods, pinv, pinvh, positive semidefinite, pseudoinverse, symmetric, benchmarking, python
Slug: inverses-pseudoinverses-numerical-issues-speed-symmetry

The matrix inverse is a cornerstone of linear algebra, taught, along
with its applications, since high school. The inverse of a matrix
\$latex A\$, if it exists, is the matrix \$latex A\^{-1}\$ such that
\$latex AA\^{-1} = A\^{-1}A = I\_n\$. Based on the requirement that the
left and right multiplications should be equal, it follows that it only
makes sense to speak of inverting square matrices. But just the square
shape is not enough: for a matrix \$latex A\$ to have an inverse,
\$latex A\$ must be full rank.

The inverse provides an elegant (on paper) method of finding solutions
to systems of \$latex n\$ equations with \$latex n\$ unknowns, which
correspond to solving \$latex Ax = b\$ for \$latex x\$. If we're lucky
and \$latex A\^{-1}\$ exists, then we can find \$latex x = A\^{-1}b\$.
For this to work, it must be the case that:

-   We have exactly as many unknowns as equations
-   No equation is redundant, i.e. can be expressed as a linear
    combination of the others

In this setting, there is a unique solution for \$latex x\$.

The Moore-Penrose pseudoinverse
-------------------------------

What if we have more equations than unknowns? It is most likely the case
that we cannot satisfy all the equations perfectly, so let's settle for
a solution that best fits the constraints, in the sense of minimising
the sum of squared errors. We solve \$latex \\operatorname{arg\\,min}\_x
||b - Ax||\$.

And how about the other extreme, where we have a lot of unknowns, but
just a few equations constraining them. We will probably have an
infinity of solutions, how can we choose one? A popular choice is to
take the one of least \$latex \\ell\_2\$ norm: \$latex
\\operatorname{arg\\,min}\_x ||x|| \\operatorname{s.t.} Ax = b\$. Is
there a way to generalize the idea of a matrix inverse for this setting?

The pseudoinverse of an arbitrary-shaped matrix \$latex A\$, written
\$latex A\^{+}\$, has the same shape as \$latex A\^{T}\$ and solves our
problem: the answer to both optimization methods above is given by
\$latex x = A\^{+}y\$.

The theoretical definition of the pseudoinverse is given by the
following conditions. The intuitive way to read them is as properties of
\$latex AA\^+\$ or \$latex A\^+A\$:

-   \$latex AA\^+A = A\$
-   \$latex A\^+AA\^+ = A\^+\$
-   \$latex (AA\^+)\^T = AA\^+\$
-   \$latex (A\^+A)\^T = A\^+A\$

These conditions do not however give us a way to get our hands on a
pseudoinverse, so we need something else.

How to compute the pseudoinverse on paper
-----------------------------------------

The first time I ran into the pseudoinverse, I didn't even know its
definition, only the expression of the closed-form solution of such a
problem, and given as:

\$latex A\^+ = (A\^T A)\^{-1}A\^T\$

What can we see from this expression:

-   It gives us a way to compute the pseudoinverse, and hence to solve
    the problem
-   If \$latex A\$ is actually invertible, it means \$latex A\^T\$ is
    invertible, so we have \$latex A\^+ = A\^{-1}(A\^T)\^{-1}A\^T =
    A\^{-1}\$
-   Something bad happens if \$latex A\^TA\$ is not invertible.

The pseudoinverse is still defined, and unique, when \$latex A\^TA\$ is
not invertible, but we cannot use the expression above to compute it.

Numerical issues
----------------

Before going on, we should clarify and demystify some of the urban
legends about numerical computation of least squares problems. You might
have heard the following unwritten rules:

1.  Never compute \$latex A\^{-1}\$, solve the system directly
2.  If you really need \$latex A\^{-1}\$, use `pinv` and not `inv`

The first of these rules is based on some misguided beliefs, but is
still good advice. If your goal is a one-shot answer to a system,
there's no use in explicitly computing a possibly large inverse, when
all you need is \$latex x\$. But [this paper][] shows that computing the
inverse is not necessarily a bad thing. The key to this is conditional
accuracy, and as long as the `inv` function used has good conditional
bounds, you will get as good results as with a least squares solver.

The second rule comes from numerical stability, and will definitely bite
you if misunderstood. If \$latex A\$ is a square matrix with a row full
of zeros, it's clearly not invertible, so an algorithm attempting to
compute the inverse will fail and you will be able to catch that
failure. But what if the row is not exactly zero, but the sum of several
other rows, and a slight loss of precision is propagated at every step?

Numerical rank vs. actual rank
------------------------------

The rank of a matrix \$latex A\$ is defined as the number of linearly
independent rows (or equivalently, columns) in \$latex A\$. In other
words, the number of non-redundant equations in the system. We've seen
before that if the rank is less than the total number of rows, the
system cannot have a unique solution anymore, so the matrix \$latex A\$
is not invertible.

The rank of a matrix is a computationally tricky problem. On paper, with
small matrices, you would look at minors of decreasing size, until you
find the first non-zero one. This is unfeasible to implement on a
computer, so numerical analysis has a different approach. Enter the
singular value decomposition!

The SVD of a matrix \$latex A\$ is \$latex A = USV\^{T}\$, where \$latex
S\$ is diagonal and \$latex U, V\$ are orthogonal. The elements on the
diagonal of \$latex S\$ are called the singular values of \$latex A\$.
It can be seen that to get a row full of zeros when multiplying three
such matrices, a singular value needs to be exactly zero.

The ugly thing that could happen is that one (or usually more) singular
values are not exactly zero, but very low values, due to propagated
imprecision. Why is this a problem? By looking at the SVD and noting its
properties, it becomes clear that \$latex A\^{-1} = VS\^{-1}U\^{T}\$ and
since \$latex S\$ is diagonal, its inverse is formed by taking the
inverse of all the elements on the diagonal. But if a singular value is
very small but not quite zero, its inverse is very large and it will
blow up the whole computation of the inverse. The right thing to do here
is either to tell the user that \$latex A\$ is numerically rank
deficient, or to return a pseudoinverse instead. A pseudoinverse would
mean: give up on trying to get \$latex AA\^+\$ to be the identity
matrix, simply aim for a diagonal matrix with approximately ones and
zeroes. In other words, when singular values are very low, set them to
0.

How do you set the threshold? This is actually a delicate issue, being
discussed on [the numeric Python mailing list][].

Scipy implementations
---------------------

Scipy exposes `inv`, `pinv` and `pinv2`. `inv` secretly invokes LAPACK,
that ancient but crazy robust code that's been used since the 70s, to
first compute a pivoted LU decomposition that is then used to compute
the inverse. `pinv` also uses LAPACK, but for computing the
least-squares solution to the system \$latex AX = I\$. `pinv2` computes
the SVD and transposes everything like shown above. Both `pinv` and
`pinv2` expose `cond` and `rcond` arguments to handle the treatment of
very small singular values, but (*attention!*) they behave differently!

The different implementations also lead to different speed. Let's look
at inverting a random square matrix:

[sourcecode lang="python"]  
In [1]: import numpy as np

In [2]: from scipy import linalg

In [3]: a = np.random.randn(1000, 1000)

In [4]: timeit linalg.inv(a)  
10 loops, best of 3: 132 ms per loop

In [5]: timeit linalg.pinv(a)  
1 loops, best of 3: 18.8 s per loop

In [6]: timeit linalg.pinv2(a)  
1 loops, best of 3: 1.58 s per loop  
[/sourcecode]

Woah, huge difference! But do all three methods return the "right"
result?

[sourcecode lang="python"]  
In [7]: linalg.inv(a)[:3, :3]  
Out[7]:  
array([[ 0.03636918, 0.01641725, 0.00736503],  
[-0.04575771, 0.03578062, 0.02937733],  
[ 0.00542367, 0.01246306, 0.0122156 ]])

In [8]: linalg.pinv(a)[:3, :3]  
Out[8]:  
array([[ 0.03636918, 0.01641725, 0.00736503],  
[-0.04575771, 0.03578062, 0.02937733],  
[ 0.00542367, 0.01246306, 0.0122156 ]])

In [9]: linalg.pinv2(a)[:3, :3]  
Out[9]:  
array([[ 0.03636918, 0.01641725, 0.00736503],  
[-0.04575771, 0.03578062, 0.02937733],  
[ 0.00542367, 0.01246306, 0.0122156 ]])

In [10]: np.testing.assert\_array\_almost\_equal(linalg.inv(a),
linalg.pinv(a))

In [11]: np.testing.assert\_array\_almost\_equal(linalg.inv(a),
linalg.pinv2(a))  
[/sourcecode]

Looks good! This is because we got lucky, though, and `a` was invertible
to start with. Let's look at its spectrum:

[sourcecode lang="python"]  
In [12]: \_, s, \_ = linalg.svd(a)

In [13]: np.min(s), np.max(s)  
Out[13]: (0.029850235603382822, 62.949785645178906)  
[/sourcecode]

This is a lovely range for the singular values of a matrix, not too
small, not too large. But what if we built the matrix in a way that
would always pose problems? Specifically, let's look at the case of
covariance matrices:

[sourcecode lang="python"]  
In [14]: a = np.random.randn(1000, 50)

In [15]: a = np.dot(a, a.T)

In [16]: \_, s, \_ = linalg.svd(a)

In [17]: s[-9:]  
Out[17]:  
array([ 7.40548924e-14, 6.48102455e-14, 5.75803505e-14,  
5.44263048e-14, 4.51528730e-14, 3.55317976e-14,  
2.46939141e-14, 1.54186776e-14, 5.08135874e-15])

[/sourcecode]

`a` has at least 9 tiny singular values. Actually it's easy to see why
there are 950 of them:

[sourcecode lang="python"]  
In [18]: np.sum(s \< 1e-10)  
Out[18]: 950  
[/sourcecode]

How do our functions behave in this case? Instead of just looking at a
corner, let's use our gift of sight:[![][]][]

The small eigenvalues are large enough that `inv` thinks the matrix is
full rank. `pinv` does better but it still fails, you can see a group of
high-amplitude noisy columns. `pinv2` is faster and it also gives us a
useful result in this case.

Wait, does this mean that `pinv2` is simply better, and `pinv` is
useless?

Not quite. Remember, we are now trying to actually invert matrices, and
degrade gracefully in case of rank deficiency. But what if we need the
pseudoinverse to solve an actual non-square, wide or tall system?

[sourcecode lang="python"]  
In [19]: a = np.random.randn(1000, 50)

In [20]: timeit linalg.pinv(a)  
10 loops, best of 3: 104 ms per loop

In [21]: timeit linalg.pinv(a.T)  
100 loops, best of 3: 7.08 ms per loop

In [22]: timeit linalg.pinv2(a)  
10 loops, best of 3: 114 ms per loop

In [23]: timeit linalg.pinv2(a.T)  
10 loops, best of 3: 126 ms per loop  
[/sourcecode]

Huge victory for `pinv` in the wide case! Hurray! With all this insight,
we can draw a line and see what we learned.

-   If you are 100% sure that your matrix is invertible, use `inv` for a
    huge speed gain. The implementation of `inv` from Scipy is based on
    LAPACK's `*getrf` + `*getri`, known to have good bounds.
-   If you are trying to solve a tall or wide system, use `pinv`.
-   If your matrix is square but might be rank deficient, use `pinv2`
    for speed and numerical gain.

Improving the symmetric case
----------------------------

But wait a second, can't we do better? \$latex AA\^T\$ is symmetric,
can't we make use of that to speed up the computation even more?
Clearly, if \$latex A\$ is symmetric, in its SVD \$latex A = USV\^T\$,
we must have \$latex U = V\$. But this is exactly the eigendecomposition
of a symmetric matrix \$latex A\$. The eigendecomposition can be
computed cheaper than the SVD using Scipy `eigh`, that uses LAPACK's
`*evr`. As part of my GSoC this year, with help from [Jake
VanderPlas][], we made a [pull request to Scipy][] containing a `pinvh`
function that is equivalent to `pinv2` but faster for symmetric
matrices.

[sourcecode lang="python"]  
In [24]: timeit linalg.pinv2(a)  
1 loops, best of 3: 1.54 s per loop

In [25]: timeit linalg.pinvh(a)  
1 loops, best of 3: 621 ms per loop

In [26]: np.testing.assert\_array\_almost\_equal(linalg.pinv2(a),
linalg.pinvh(a))  
[/sourcecode]

  [this paper]: http://arxiv.org/abs/1201.6035
  [the numeric Python mailing list]: http://thread.gmane.org/gmane.comp.python.numeric.general/50396/focus=50912
  []: http://localhost:8001/wp-content/uploads/2012/08/pseudoinverses-300x218.png
    "Pseudoinverses"
  [![][]]: http://localhost:8001/wp-content/uploads/2012/08/pseudoinverses.png
  [Jake VanderPlas]: http://jakevdp.github.com/
  [pull request to Scipy]: https://github.com/scipy/scipy/pull/289
