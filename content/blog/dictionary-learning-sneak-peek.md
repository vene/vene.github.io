Title: Dictionary learning sneak peek
Date: 2011-06-24 12:06
Author: vene
Category: Uncategorized
Slug: dictionary-learning-sneak-peek

Closing in on the goal of integrating J. Mairal's dictionary learning in
the scikit, I stitched together a couple of examples.

The code is not yet integrated according to our standards, but here is
the kind of results you can expect.

Here is how a dictionary obtained from 8x8 patches of Lena looks like.
Pretty much it looks as expected: gabor-like wavelets with different
rotations and shifts, which means things are working!

[![Dictionary learned from lena patches][]][]

And here is how it works for denoising Lena. On the left is the noisy
image and on the right is the reconstruction from a learned dictionary.
The sparse code code producing the result on the right is found using
orthogonal matching pursuit.

This is by no means a good denoising example, I have no idea at the
moment how to tweak the patch sizes and the model parameters to obtain a
better result. This is just a sneak peek and pretty soon you will see
better stuff!

[![Denoising Lena with dictionary learning and OMP][]][]

  [Dictionary learned from lena patches]: http://localhost:8001/wp-content/uploads/2011/06/image.png
    "Dictionary learned from lena patches"
  [![Dictionary learned from lena patches][]]: http://localhost:8001/wp-content/uploads/2011/06/image.png
  [Denoising Lena with dictionary learning and OMP]: http://localhost:8001/wp-content/uploads/2011/06/denoise.png
    "Denoising Lena"
  [![Denoising Lena with dictionary learning and OMP][]]: http://localhost:8001/wp-content/uploads/2011/06/denoise.png
