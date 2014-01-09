Title: The nasty bug crawling in my Orthogonal Matching Pursuit code
Date: 2011-11-18 20:51
Author: vene
Category: scikit-learn
Tags: bug, omp, orthogonal matching pursuit, dictionary learning, scikit-learn
Slug: the-nasty-bug-crawling-in-my-orthogonal-matching-pursuit-code

A while back, Bob L. Sturm blogged about a [similar implementation of
OMP][] to the one in scikit-learn. Instead of using the Cholesky
decomposition like we did, his Matlab code uses the QR decomposition, to
a similar (or maybe even identical) outcome, in theory. So lucky that
Alejandro pointed out to him the existence of the scikit-learn
implementation, and that Bob's code [exposed a bug][] that all the test
coverage didn't catch! This plot should increase, certainly not
decrease! Something is clearly wrong here.  
[![OMP buggy phase transition, decreasing instead of
increasing][]][exposed a bug]  
Luckily we were able to find it and [fix it][] very quickly. I have
updated the old entries I wrote on the OMP optimizations, so they no
longer include the bug. But I take this opportunity to explain what
exactly went wrong.

A key part of the optimization was that slicing out arbitrary columns
out of an array is slow when they are passed to BLAS functions like
matrix multiplication. In order to make the most out of your code, the
data should have a contiguous layout. We achieved this by swapping
active dictionary atoms (columns) to the beginning of the array.

Something that can happen, but won't happen very often, is that after an
atom is selected as active, the atom that takes its place after swapping
needs to be selected. This is rare because dictionaries have many
columns, out of which only very very few will be active. But when it
happens, because the code didn't keep track of swapped indices, the
corresponding coefficient of the solution would get updated twice,
leading to more zero entries than we should have. A keen eye could have
noticed that the first \`n\_nonzero\_coefs\` entries in OMP solution
vectors were never non-zero. But alas, my eye was not a keen one at all.

In other words, the following test (that was written after the bug was
found, unfortunately) was failing:  
[sourcecode lang="Python"]  
def test\_swapped\_regressors():  
gamma = np.zeros(n\_features)  
\# X[:, 21] should be selected first, then X[:, 0] selected second,  
\# which will take X[:, 21]'s place in case the algorithm does  
\# column swapping for optimization (which is the case at the moment)  
gamma[21] = 1.0  
gamma[0] = 0.5  
new\_y = np.dot(X, gamma)  
new\_Xy = np.dot(X.T, new\_y)  
gamma\_hat = orthogonal\_mp(X, new\_y, 2)  
gamma\_hat\_gram = orthogonal\_mp\_gram(G, new\_Xy, 2)  
\# active indices should be [0, 21], but prior to the bugfix  
\# the algorithm would update only [21] but twice  
assert\_equal(np.flatnonzero(gamma\_hat), [0, 21])  
assert\_equal(np.flatnonzero(gamma\_hat\_gram), [0, 21])  
[/sourcecode]

Note that this bug has been fixed for a while, but I didn't get the free
time to write this post until now. Good news is: we fixed it, and did so
very quickly after the report. So you can still trust me, I guess!

  [similar implementation of OMP]: http://media.aau.dk/null_space_pursuits/2011/10/efficient-omp.html
  [exposed a bug]: http://media.aau.dk/null_space_pursuits/2011/10/omp-in-python-strange-results.html
  [OMP buggy phase transition, decreasing instead of increasing]: http://media.aau.dk/null_space_pursuits/2011/10/17/OMPscikit.png
    "OMP buggy phase transition"
  [fix it]: http://media.aau.dk/null_space_pursuits/2011/10/to-the-rescue.html
