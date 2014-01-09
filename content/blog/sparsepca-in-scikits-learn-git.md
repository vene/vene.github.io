Title: SparsePCA in scikits.learn-git
Date: 2011-07-19 12:01
Author: vene
Category: scikit-learn
Tags: pca, principal components analysis, scikit-learn, sparse pca, SparsePCA, spca
Slug: sparsepca-in-scikits-learn-git

I am happy to announce that the Sparse PCA code has been reviewed and
merged into the main `scikits.learn` repository.

You can use it if you install the bleeding edge `scikits.learn` git
version, by first downloading the source code as explained in the
[user's guide][], and then running `python setup.py install`.  
[caption id="" align="aligncenter" width="400" caption="Sparse PCA on
images of the digit 3"][![][]][][/caption]  
To see what code is needed to produce an image such as the one above,
using `scikits.learn`. check out this cool [decomposition example][]
that compares the results of most matrix decomposition models
implemented at the moment.

There are other new cool things that have been recently merged by other
contributors, such as support for sparse matrices in [minibatch
K-means][], and the [variational infinite gaussian mixture model][], so
I invite you to take a look!

  [user's guide]: http://scikit-learn.sourceforge.net/stable/developers/index.html#git-repo
    "installation user's guide"
  []: http://scikit-learn.sourceforge.net/dev/_images/plot_digits_decomposition_4.png
    "Sparse PCA on images of the digit 3"
  [![][]]: http://scikit-learn.sourceforge.net/dev/_images/plot_digits_decomposition_4.png
  [decomposition example]: http://scikit-learn.sourceforge.net/dev/auto_examples/decomposition/plot_digits_decomposition.html
    "decomposition example"
  [minibatch K-means]: http://scikit-learn.sourceforge.net/dev/modules/clustering.html#mini-batch-k-means
    "minibatch K-means"
  [variational infinite gaussian mixture model]: http://scikit-learn.sourceforge.net/dev/modules/mixture.html#infinite-gaussian-mixtures-dpgmm-classifier
    "variational infinite gaussian mixture model"
