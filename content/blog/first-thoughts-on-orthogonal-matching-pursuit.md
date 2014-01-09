Title: First thoughts on Orthogonal Matching Pursuit
Date: 2011-05-30 13:02
Author: vene
Category: Uncategorized
Slug: first-thoughts-on-orthogonal-matching-pursuit

I am working on implementing the Orthogonal Matching Pursuit (OMP)
algorithm for the scikit. It is an elegant algorithm (that almost writes
itself in Numpy!) to compute a greedy approximation to the solution of a
sparse coding problem:

\$\$ \\text{argmin} \\big|\\big|\\gamma\\big|\\big|\_0 \\text{ subject
to }\\big|\\big|x-D\\gamma\\big|\\big|\_2\^2 \\leq \\epsilon\$\$

or (in a different parametrization)

\$\$ \\text{argmin} \\big|\\big|x - D\\gamma\\big|\\big|\_2\^2\\text{
subject to }\\big|\\big|\\gamma\\big|\\big|\_0 \\leq m\$\$

The second formulation is interesting in that it gives one of the few
algorithms for sparse coding that can control the actual number of
non-zero entries in the solution. Some dictionary learning methods need
this (I'm thinking of K-SVD).

Both problems are solved by the same algorithm, with a different
stopping condition. The gist of it is to include at each iteration, the
atom with the highest correlation to the current residual. However, as
opposed to regular Matching Pursuit, here, after choosing the atom, the
input signal is orthogonally projected to the space spanned by the
chosen atoms. This involves the solution of a least squares problem at
each step. However, because the problem is almost the same at each
iteration, only with one more column added to the matrix, this can be
easily solved by maintaining a QR or Cholesky decomposition of the
dictionary matrix that is updated at each step.

Rubinstein et al. [1] came up with a clever method to optimize the
calculations, based on the fact that usually in practice we never have
to find a sparse coding for a single signal, but usually for a batch.
They called this method Batch OMP, and it is based on a straightforward
modification of the Cholesky update algorithm, taking advantage of
precomputing the Gram matrix [latex] G=D'D[/latex].

Based on my experiments, their batch update is the fastest, even though
it lags behind if invoked with too small a batch. As soon as I make sure
the implementation is robust and ready for use, I will make some
benchmarks.

Update: Here's a little proof that it works!  
[![Stem plot for sparse signals recovered by OMP][]][]

Update 2: Here's a little benchmark:  
[![Orthogonal Matching Pursuit benchmark][]][]  
[1]
http://www.cs.technion.ac.il/\~ronrubin/Publications/KSVD-OMP-v2.pdf

  [Stem plot for sparse signals recovered by OMP]: http://localhost:8001/wp-content/uploads/2011/06/omp.png
    "Orthogonal Matching Pursuit sparse signal recovery"
  [![Stem plot for sparse signals recovered by OMP][]]: http://localhost:8001/wp-content/uploads/2011/06/omp.png
  [Orthogonal Matching Pursuit benchmark]: http://localhost:8001/wp-content/uploads/2011/06/omp_bench.png
    "OMP benchmark, time and error"
  [![Orthogonal Matching Pursuit benchmark][]]: http://localhost:8001/wp-content/uploads/2011/06/omp_bench.png
