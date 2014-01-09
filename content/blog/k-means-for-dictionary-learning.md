Title: K-Means for dictionary learning
Date: 2011-07-10 14:27
Author: vene
Category: dictionary learning, scikit-learn, Uncategorized
Tags: dictionary learning, k-means, scikit-learn, vq
Slug: k-means-for-dictionary-learning

[![Dictionary learned with K-Means on the LFW dataset with whitening
PCA][]][][![Dictionary learned with K-Means on the LFW dataset without
whitening PCA][]][]

One of the simplest, and yet most heavily constrained form of matrix
factorization, is vector quantization (VQ). Heavily used in image/video
compression, the VQ problem is a factorization [latex] X=WH[/latex]
where [latex] H[/latex] (our dictionary) is called the codebook and is
designed to cover the cloud of data points effectively, and each line of
[latex] W[/latex] is a unit vector.

This means that each each data point [latex] x\_i[/latex] is
approximated as [latex] x\_i \\approx h\_{k} = \\sum\_{j=1}\^{r}
\\delta\_{kj}h\_{j}[/latex]. In other words, the closest row vector
(codeword/dictionary atom) [latex] h\_k[/latex] of [latex] H[/latex] is
chosen as an approximation, and this is encoded as a unit vector [latex]
(\\delta\_{k1}, ..., \\delta\_{kr})[/latex]. The data representation
[latex] W[/latex] is composed of such vectors.

There is a variation called gain-shape VQ where instead of approximating
each point as one of the codewords, we allow a scalar multiplication
invariance: [latex] x\_i \\approx \\alpha\_ih\_k[/latex]. This model
requires considerably more storage (each data point needs a floating
point number and an unsigned index, as opposed to just the index), but
it leads to a much better approximation.  
Gain-shape VQ can equivalently be accomplished by normalizing each data
vector prior to fitting the codebook.

In order to fit a codebook [latex] H[/latex] for efficient VQ use, the
K-Means Clustering [[1][]] algorithm is a natural thought. K-means is an
iterative algorithm that incrementally improves the dispersion of k
cluster centers in the data space until convergence. The cluster centers
are initialized in a random or procedural fashion, then, at each
iteration, the data points are assigned to the closest cluster center,
which is subsequently moved to the center of the points assigned to it.

The `scikits.learn.decomposition.KMeansCoder` object from our
work-in-progress dictionary learning toolkit can learn a dictionary from
image patches using the K-Means algorithm, with optional local contrast
normalization and a PCA whitening transform. Using a trained object to
transform data points with orthogonal matching pursuit, with the
parameter `n_atoms=1` is equivalent to gain-shape VQ. Of course you are
free to use any method of sparse coding such as LARS. The code used to
produce the example images on top of this post can be found in [[2][]].

Using K-Means for learning the dictionary does not optimize over linear
combinations of dictionary atoms, like standard dictionary learning
methods do. However, it's considerably faster, and Adam Coates and
Andrew Ng suggest in [[3][]] that as long as the dictionary is filled
with a large enough number of atoms and it covers well enough the cloud
of data (and of future test data) points, then K-Means, or even random
sampling of image patches, can perform remarkably well for some tasks.

<div id="footnote-1">
[1] [Wikipedia article on K-Means clustering][]

</div>
<div id="footnote-2">
[2] [K-Means Coder example][]

</div>
<div id="footnote-3">
[3] [**The importance of encoding versus training with sparse coding and
vector quantization**, Adam Coates and Andrew Y. Ng. In Proceedings of
the Twenty-Eighth International Conference on Machine Learning, 2011.][]

</div>

  [Dictionary learned with K-Means on the LFW dataset with whitening
  PCA]: http://localhost:8001/wp-content/uploads/2011/07/kmeans_w.png?w=250
    "K-Means dictionary with whitening PCA"
  [![Dictionary learned with K-Means on the LFW dataset with whitening
  PCA][]]: http://localhost:8001/wp-content/uploads/2011/07/kmeans_w.png
  [Dictionary learned with K-Means on the LFW dataset without whitening
  PCA]: http://localhost:8001/wp-content/uploads/2011/07/kmeans_no_w.png?w=250
    "K-Means dictionary without whitening PCA"
  [![Dictionary learned with K-Means on the LFW dataset without
  whitening PCA][]]: http://localhost:8001/wp-content/uploads/2011/07/kmeans_no_w.png
  [1]: #footnote-1
  [2]: #footnote-2
  [3]: #footnote-3
  [Wikipedia article on K-Means clustering]: http://en.wikipedia.org/wiki/K-means_clustering
    "K-means clustering"
  [K-Means Coder example]: https://github.com/vene/scikit-learn/blob/453bb5ef440c3bc030b14848ab4a3091fb4295c7/examples/decomposition/kmeans_coder.py
  [**The importance of encoding versus training with sparse coding and
  vector quantization**, Adam Coates and Andrew Y. Ng. In Proceedings of
  the Twenty-Eighth International Conference on Machine Learning,
  2011.]: http://ai.stanford.edu/~ang/papers/icml11-EncodingVsTraining.pdf
