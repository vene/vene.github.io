Title: An overview of dictionary learning: Terminology
Date: 2011-04-15 14:10
Author: vene
Category: dictionary learning
Tags: dictionary learning, scikit-learn, Uncategorized
Slug: an-overview-of-dictionary-learning-terminology

My GSoC proposal is titled "Dictionary learning in scikits.learn" and in
the project, I plan to implement methods used in state of the art
research and industry applications in signal and image processing. In
this post, I want to clarify the terminology used.

Usually the terms *dictionary learning* and *sparse coding* are used
interchangably. Also my proposal contains methods such as Sparse PCA
which are technically not *sparse coding* but closely related problems.

The basic idea is the approximation of a signal vector [latex] x \\in
\\mathbb{R}\^d[/latex] by a linear combination of components, as good as
possible, under certain constraints. This can be formulated as a basic
(unconstrained) loss function measuring the quality of the
approximation: [latex] \\mathcal{L}(x, D, \\alpha) = \\big|\\big|x -
D\\alpha\\big|\\big|\^2\_2, D \\in \\mathbb{R}\^{d \\times r}, \\alpha
\\in \\mathbb{R}\^r[/latex], where [latex] r[/latex] is the dimension of
the dictionary (the number of *components)*.

When working with a dataset of more signal vectors, the overall basic
loss for such an approximation is [latex] \\mathcal{L}(X, D, A) =
\\sum\_{i = 1}\^N \\mathcal{L}(x\_i, D, \\alpha\_i) = \\big|\\big|X -
DA\\big|\\big|\^2\_F[/latex]. Minimizing such a loss function amounts to
finding the closest (in the Frobenius sense) matrix factorization
[latex] DA[/latex] that approximates the data matrix [latex] X[/latex]

This generic problem is called a **matrix factorization problem**. Many
classical problems are matrix factorization problems with additional
constraints. For example, PCA is a matrix factorization that constrains
[latex] D[/latex] to be orthogonal. NMF constrains both [latex]
D[/latex] and [latex] A[/latex] to have no negative elements. Sparse
variants of these two decompositions are useful for getting local
components, such as parts of faces. These are obtained by adding an
aditional constraint on the dictionary columns.

It can  be sometimes useful to consider the dictionary fixed. The signal
processing community has introduced over the years many such
dictionaries, for examples wavelets. These are used, for example, in the
JPEG2000 compression standard.

A very useful represenation is when the dictionary is *overcomplete*
([latex] r \> d[/latex]). The wavelets are an example of this. Given
such a dictionary, we are interested in an efficient encoding of a
vector [latex] x[/latex], in the sense of sparseness: we want to use as
few dictionary components as possible in our representation. Such a
solution is the vector [latex]\\alpha[/latex] minimizing [latex]
\\mathcal{L}(x, D, \\alpha) +
\\lambda\\big|\\big|\\alpha\\big|\\big|\_1[/latex] but other
sparsity-inducing constraints can be used. Such a vector is a **sparse
coding** of [latex] x[/latex] and it can be solved using algorithms such
as least-angle regression and orthogonal matching pursuit.

However, we are not limited to using precomputed dictionaries. The term
**dictionary learning** refers to methods of inferring, given [latex]
X[/latex], a (usually overcomplete) dictionary that will perform good at
sparsely encoding the data in [latex] X[/latex]. Such methods are more
expensive than using precomputed dictionaries, but they perform better,
since the dictionary is optimized for the current dataset.

Because usually such loss functions are non-convex in [latex] D[/latex]
and [latex] A[/latex] simultaneously, dictionary learning algorithms
alternate between minimizing each while keeping the other fixed. The
step that minimizes [latex] D[/latex] is sometimes called the
**dictionary update** step, and the one minimizing [latex] A[/latex] is
(similarily to the case where the dictionary is always fixed) the
**sparse coding** step. Dictionary learning algorithms differ in the
method used for each of this step.

To resume, many problems can be posed as matrix factorization problems.
Depending on the constraints imposed, the problem becomes interesting
for different applications. Dictionary learning is very good for image
reconstruction. Matrix decompositions with sparse undercomplete
dictionaries such as Sparse PCA can be used to find local features that
constitute the dataset, for example parts of faces, for a dataset of
facial images. NMF can be used in both under and overcomplete settings
and it offers a good model for additive data such as text or images. We
are interested in these variants and they are planned for implementation
in my GSoC proposal.

Julien Mairal's presentation of his work in this domain, available
[here][], shows the theoretical background of such methods, along with
examples showing state of the art results in image processing.

  [here]: http://videolectures.net/icml09_mairal_odlsc/
    "Mairal dictionary learning"
