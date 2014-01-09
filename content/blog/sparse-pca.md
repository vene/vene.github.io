Title: Sparse PCA
Date: 2011-05-23 15:19
Author: vene
Category: scikit-learn
Tags: dictionary learning, pca, sparse pca, SparsePCA, spca, scikit-learn
Slug: sparse-pca

I have been working on the integration into the scikits.learn codebase
of a sparse principal components analysis (SparsePCA) algorithm coded by
Gaël and Alexandre and based on [[1]][]. Because the name "sparse PCA"
has some inherent ambiguity, I will describe in greater depth what
problem we are actually solving, and what it can be used for.

The problem
===========

Mathematically, this implementation of Sparse PCA solves:

\$latex (U\^\*,
V\^\*)=\\underset{U,V}{\\mathrm{argmin\\,}}\\frac{1}{2}||X-UV||\_2\^2+\\alpha||V||\_1\$

with \$latex || U\_k ||\_2 = 1\$ for all \$latex 0 \\leq k \<
n\_{atoms}\$

This looks really abstract so let's try to interpret it. We are looking
for a matrix factorization \$latex UV\$ of \$latex X \\in
\\mathbf{R}\^{n\_{samples}\\times n\_{features}}\$, just like in
ordinary PCA. The interpretation is that the \$latex n\_{atoms}\$ lines
of \$latex V\$ are the extracted components, while the lines of \$latex
U\$ are the coordinates of the samples in this projection.

The most important difference between this and PCA is that we enforce
sparsity on the *components*. In other words, we look for a
representation of the data as a linear combination of sparse signals.

Another difference is that, unlike in PCA, here we don't constrain U to
be orthogonal, just to consist of normalized column vectors. There are
different approaches where this constraint appears too, and they are on
the list for this summer, but I digress.

The approach
============

As usual, such optimization problems are solved by alternatively
minimizing one of the variables while keeping the other fixed, until
convergence is reached.

The update of \$latex V\$ (the dictionary) is computed as the solution
of a Lasso least squares problem.  We allow the user to choose between
the least angle regression method (LARS) or stochastic gradient descent
as algorithms to solve the Lasso problem.

The update of \$latex U\$ is block coordinate descent with warm restart.
This is a batch adaptation of an online algorithm proposed by Mairal et
al. in [[1]][].

Sparse PCA as a transformer
===========================

Of course, in order to be of practical use, the code needs to be
refactored into a scikits.learn transformer object, just like
`scikits.learn.decomposition.pca`. This means that the optimization
problem described above corresponds to the fitting stage. The post-fit
state of the transformer is given by the learned components (the matrix
\$latex V\$ above).

In order to transform new data according to the learned sparse PCA model
(for example, prior to classification of the test data), we simply need
to do a least squares projection of the new data on the sparse
components.

What is it good for?
====================

For applications such as text and image processing, its great advantage
is interpretability. When running a regular PCA on a set of documents in
bag of words format, we can find an interesting visualisation on a
couple of components, and it can show discrimination or clusters. The
biggest problem is that the maximum variance components found by PCA
have very dense expressions as linear combinations of the initial
features. In practice, sometimes interpretation is made by simply
marking the \$latex k\$ variables with the highest coefficients in this
representation, and basically interpreting as if the rest are truncated
to 0 (this has been taught to me in a class on PCA interpretation).

Such an approximation can be highly misleading, and now we offer you the
sparse PCA code that can extract components with only few non-zero
coefficients, and therefore easy to interpret.

For image data, sparse PCA should extract local components such as,
famously, parts of the face in the case of face recognition.

Personally I can't wait to have it ready for the scikit so that I can
play with it in some of my projects. I have two tasks where I can't wait
to see the results: one is related to [Romanian infinitives][], where
PCA revealed structure, and I would love to see how it looks with sparse
n-gram components. The other task is to plug it in as feature extractor
for handwritten digit classification, for my undergraduate thesis.

<span id="footnote_1">[1] <http://www.di.ens.fr/sierra/pdfs/icml09.pdf></span>

  [[1]]: #footnote_1
  [Romanian infinitives]: http://venefrombucharest.wordpress.com/2011/04/14/a-look-at-romanian-verbs-with-scikits-learn/
    "A look at Romanian verbs with scikits-learn"
