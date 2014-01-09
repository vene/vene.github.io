Title: Image denoising with dictionary learning
Date: 2011-07-07 20:00
Author: vene
Category: dictionary learning, scikit-learn
Tags: denoising, dictionary learning
Slug: image-denoising-with-dictionary-learning

I am presenting an image denoising example that fully runs under my
local scikits-learn fork. Coming soon near you!

The 400 square pixels area covering Lena's face was distorted by
additive gaussian noise with a standard deviation of 50 (pixel values
are ranged 0-256.)

[![Lena image denoising using dictionary learning][]][]

The dictionary contains 100 atoms of shape 4x4 and was trained using
10000 random patches extracted from the undistorted image. Then, each
one of the four 100 square pixel areas was reconstructed using the
dictionary learning model and a different transform method.

-   OMP-1 reconstructs each patch as the closest dictionary atom,
    multiplied by a variable coefficient. This is similar to the idea of
    gain-shape vector quantization.
-   OMP-2 is like OMP-1, but it considers 2 atoms instead of just one.
    This takes advantage of the fact that the natural dictionary atoms
    are of such nature to efficiently represent random image patches
    when combined.
-   LARS finds a reconstruction of each image patch as a solution to a
    Lasso problem, solved using least angle regression.
-   Thresholding is a simple and quick non-linearity that (as it is
    currently implemented, based on [[1][]], where it is not intended
    for reconstruction but for classification) breaks the local
    brightness of the image fragment. The bottom right fragment was
    forcefully renormalized to stretch fit into the 0-256 range, but
    brightness differences can be seen.

<div id="footnote-1">
[1] [**The importance of encoding versus training with sparse coding and
vector quantization**, Adam Coates and Andrew Y. Ng. In Proceedings of
the Twenty-Eighth International Conference on Machine Learning, 2011.][]

</div>

  [Lena image denoising using dictionary learning]: http://localhost:8001/wp-content/uploads/2011/07/denoise3.png
    "Lena denoising"
  [![Lena image denoising using dictionary learning][]]: http://localhost:8001/wp-content/uploads/2011/07/denoise3.png
  [1]: #footnote-1
  [**The importance of encoding versus training with sparse coding and
  vector quantization**, Adam Coates and Andrew Y. Ng. In Proceedings of
  the Twenty-Eighth International Conference on Machine Learning,
  2011.]: http://ai.stanford.edu/~ang/papers/icml11-EncodingVsTraining.pdf
