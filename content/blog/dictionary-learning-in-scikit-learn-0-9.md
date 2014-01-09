Title: Dictionary learning in scikit-learn 0.9
Date: 2011-09-19 19:15
Author: vene
Category: scikit-learn
Tags: dictionary learning, scikit-learn
Slug: dictionary-learning-in-scikit-learn-0-9

Thanks to Olivier, Gaël and Alex, who reviewed the code heavily the last
couple of days, and with apologies for my lack of activity during a
sequence of conferences, Dictionary learning has officially been merged
into scikit-learn master, and just in time for the new scikit-learn 0.9
release. Here are some glimpses of the examples you can run for
yourself:

[![Dictionary learned from Lena patches][]][]

[![Noisy image for denoising][]][]

[![Image denoising with Dictionary learning and Orthogonal matching
pursuit][]][]

The stars of this new release are: the manifold learning module by Jake
Vanderplas and Fabian Pedregosa, the Dirichlet process gaussian mixture
model by Alexandre Passos, and many others, as you can see from the
[development changelog][] (as soon as the release is made, I will update
this post with permanent links).

The release is due tomorrow. I will also be in charge with building the
Windows installers for this release, let's hope I do a good job and you
can think of me and smile when installing!

  [Dictionary learned from Lena patches]: http://localhost:8001/wp-content/uploads/2011/09/plot_image_denoising_1.png
    "plot_image_denoising_1"
  [![Dictionary learned from Lena patches][]]: http://localhost:8001/wp-content/uploads/2011/09/plot_image_denoising_1.png
  [Noisy image for denoising]: http://localhost:8001/wp-content/uploads/2011/09/plot_image_denoising_24.png
    "plot_image_denoising_24"
  [![Noisy image for denoising][]]: http://localhost:8001/wp-content/uploads/2011/09/plot_image_denoising_24.png
  [Image denoising with Dictionary learning and Orthogonal matching
  pursuit]: http://localhost:8001/wp-content/uploads/2011/09/plot_image_denoising_44.png
    "Image denoising with Dictionary learning and Orthogonal matching pursuit"
  [![Image denoising with Dictionary learning and Orthogonal matching
  pursuit][]]: http://localhost:8001/wp-content/uploads/2011/09/plot_image_denoising_44.png
  [development changelog]: http://scikit-learn.sourceforge.net/dev/whats_new.html
    "scikit-learn development changelog"
