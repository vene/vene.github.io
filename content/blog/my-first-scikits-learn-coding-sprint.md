Title: My first scikits.learn coding sprint
Date: 2011-04-02 20:12
Author: vene
Category: scikit-learn
Tags: coding sprint, scikit-learn
Slug: my-first-scikits-learn-coding-sprint

The fifth [scikits.learn][] coding sprint took place Friday, April 1st
2011. For anyone who is not familiar with it, scikits.learn is a fast
and easy to use machine learning toolkit for the pylab environment
(Python, NumPy, SciPy, Matplotlib.)

This was a good opportunity for me to get code reviews by the developers
in order to bring my NMF code up to standards, so that it can be merged.
Though I live far from every nucleus of scikits-learn developers, I
efficiently participated via IRC. This way, I also got the chance to
help out a bit on Mathieu Blondel's Kernel PCA code, which will also be
merged into main soon.

How it felt like
----------------

Short answer: awesome!

Slightly longer answer: Everybody was very encouraging  and helpful.
They gave me a lot of feedback from which I learned a lot, and they
manifested the intention to merge soon. It is a pleasure to work on
projects that you like and use, especially when the projects leaders and
collaborators are so good to work with.

But the main reason why it makes me feel so good is that I'm proud to
able to contribute on a project that I consider very significant and the
best in the field from many points of view.

What I got done
---------------

Most of my work was on the non-negative matrix factorization module that
I began some while back, but only intermitently worked on. It is now a
solid module with high test coverage, documentation, and a cool simple
example showing a sparse set of features for the digits dataset in
scikits.learn.  Apart from all the minor fixes in overall code quality
and cleanliness, probably what is the most relevant is the improvement
and the study of the initialization methods. I will look into this
further and document it on this blog, the point is that the choice of
initialization method greatly influences the speed of convergence, and
in the case of a high-tolerance setting, also the error obtained. Some
initializations are more fit for sparsity settings, while others are
more fit for dense settings.

I have a theory that I plan to test out, regarding the use of different
initialization methods for components and for data in a sparse setting.

What I learned
--------------

I think my greatest improvement was in terms of workflow and efficiency.
While my code was under review, I was receiving frequent comments on my
git pull request, and eventually I ended up responding to some comments
even before they were posted :). I sent small fixes as pull requests to
help other developers as much as I could. Before scikits.learn I had
never worked on a project with so many developers, and I think I handled
it well, even though I asked once or twice on the IRC channel for pieces
of git-fu.

I learned that it's difficult to tweak matplotlib subplots! I'm still
staring at Alexandre Gramfort's tweak in my example and I have no idea
what he did to make it look so good. But I'll figure it out soon, I'm
sure.

I also learned a lot more about the intricacies of the scikits.learn
APIs, the philosophy of ease of use, and the project tree in general.

In short, the coding sprint has been a great and rewarding experience,
for which I thank all of you guys there!

  [scikits.learn]: http://scikit-learn.sourceforge.net/ "scikits.learn"
