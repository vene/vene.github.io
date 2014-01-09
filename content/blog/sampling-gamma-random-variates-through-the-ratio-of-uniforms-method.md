Title: Sampling Gamma random variates through the ratio-of-uniforms method
Date: 2011-10-09 15:40
Author: vene
Category: python
Tags: monte carlo, numpy, random sampling, ratio-of-uniforms, scipy, python
Slug: sampling-gamma-random-variates-through-the-ratio-of-uniforms-method

One year ago I had the chance to take a class on Monte Carlo simulation
with prof. Ion Văduva, and my assignment for the class was to implement
exactly what it says in the title of the blog post. I am going to walk
you through the idea behind this.

### General formulation

The ratio-of-uniforms is a method that can be applied to many density
functions. Essentially, given a density function over [latex]
\\mathbb{R}\^m[/latex], [latex] f(x) = \\frac{h(x)}{H}[/latex] where
[latex]H[/latex] is a normalization constant (ie. [latex] h(x) \\geq
0[/latex], [latex] H = \\int h(x)dX[/latex]). Given a parameter [latex]
c \> 0 [/latex] and a parametrization [latex]\\phi[/latex] from [latex]
\\mathbb{R}\^{m+1}[/latex] to [latex] \\mathbb{R}\^{m}[/latex] expressed
as: \$\$ \\phi(v\_0, v\_1, ..., v\_m) = \\left ( \\frac{v\_1}{v\_0\^c},
\\frac{v\_2}{v\_0\^c}, ..., \\frac{v\_m}{v\_0\^c} \\right )\$\$  
Define the set [latex] \\mathcal{C} = \\{\\mathbf{v} \\big |
\\gamma(\\mathbf{v}) \\leq 0, v\_0 \> 0\\} \\in
\\mathbb{R}\^{m+1}[/latex] where  
\$\$\\gamma(\\mathbf{v}) = \\log v\_0 - \\frac{\\log h(\\phi(v\_0,
v\_1, ..., v\_m))}{mc + 1}\$\$ If [latex] \\mathcal{C}[/latex] is
bounded and we sample a uniform vector [latex] \\mathbf{V} \\sim
\\text{Uniform}(\\mathcal{C})[/latex] then [latex] \\phi(\\mathbf{V})
\\sim f(x)[/latex]. Also note that the measure (volume) of the set
[latex] \\mathcal{C}[/latex] is [latex] \\frac{H}{mc + 1}[/latex]. I do
not have any references for the proof, except for a book in Romanian,
but if you are interested, just leave me a comment and I'll do a
follow-up post with the proofs.

### Univariate scenario

For the univariate case, all the above simplifies to \$\$ \\mathcal{C} =
\\left \\{(u, v) \\Big | 0 \< u \< \\sqrt  
{h\\left (\\frac{v}{u\^c}\\right )} \\right \\} \$\$. We generate
[latex] (U, V) \\sim \\text{Uniform}(\\mathcal{C})[/latex] and take
[latex] \\frac{V}{U\^c} \\sim f(x)[/latex].  
Since we are looking at the (univariate) Gamma distribution, described
by: \$\$ f(x; \\nu, \\theta) = \\frac{x\^{\\mu - 1}
\\exp(\\frac{-x}{\\theta})}{\\theta\^k\\Gamma(k)}\$\$ [latex]
\\nu[/latex] is the shape parameter and [latex] \\theta[/latex] is the
scale parameter.  
But because of the property that if [latex] X \\sim \\text{Gamma}(\\nu,
\\theta)[/latex], then for any [latex] k \> 0[/latex], [latex] kX \\sim
\\text{Gamma}(\\nu, k\\theta)[/latex], we conclude that we can fix
[latex] \\theta[/latex] to 1 without loss of generality. Replacing in
the style of the definition in the previous section, we have [latex]
h(x; \\nu) = x\^{\\nu-1}e\^{-x}[/latex] and [latex] H\_\\nu =
\\Gamma(\\nu)[/latex].  
This allows us to compute the equation of the boundary of the set
[latex] \\mathcal{C}[/latex] which ends up being described by
[latex]\\gamma(u, v) = \\log{u} - \\frac{\\nu - 1}{c + 1}
\\log{\\left(\\frac{v}{u\^c}\\right)} + \\frac{1}{c+1}
\\frac{v}{u\^c}[/latex]. For visualisation purposes, here is how it
would look like for [latex] \\nu=6, c=1[/latex] (plotted using [Wolfram
Alpha][]):[![][]][]

### Sampling algorithm

In order to uniformly sample from this set, we can apply basic rejection
sampling: just uniformly sample from a rectangular region surrounding
the set, and reject the points that do not satisfy the condition. In
order to do this as efficiently as possible, we need to compute the
minimal bounding box, which can be done by solving a couple of
optimization problems using Lagrange multipliers and the KKT conditions.
Also by looking closely at the image, you can see that the lower left
corner is exactly the origin: this turns out not to be a coincidence. I
won't go into detail here, but here are the bounds I derived:  
\$\$ 0 \< u \< (\\nu - 1)\^\\frac{\\nu - 1}{c + 1} e \^ {-\\frac{\\nu -
1}{c + 1}} \\text{ and } 0\< v \< \\left(\\frac{c\\nu +
1}{c}\\right)\^{\\frac{c\\nu + 1}{c + 1}} e \^ {- \\frac {c\\nu +
1}{c+1}}\$\$

The probability of acceptance (which can be seen as the efficiency) of
the rejection sampling method is given by the ratio of the areas of the
set [latex] \\mathcal{C}[/latex] and the bounding box. The larger this
probability, the less points we throw away and the more efficient the
algorithm is. Using the values derived above, this probability is: \$\$
p(\\nu, c) = \\frac{\\Gamma(\\nu)e\^{\\nu}}{(c+1) (\\nu -
1)\^{\\frac{\\nu - 1}{c + 1}} \\left(\\frac{c\\nu +
1}{c}\\right)\^{\\frac{c\\nu + 1}{c + 1}}}\$\$

Personally I got stumped here. The idea would be to determine the ideal
[latex] c[/latex] for a given [latex] \\nu[/latex] in order to maximize
the probability, but I didn't manage to do it (I leave it as an exercise
for the reader ;)). Anyway, this is enough to proceed with an
implementation, so I'm gonna give the Python code for it. Note that I
used the name k for the shape parameter instead of [latex] \\nu[/latex].
Also note that the case when [latex] 0 \< \\nu \< 1[/latex] needed to be
treated separately, which I did using the following property: Let
[latex] \\nu \\in (0, 1)[/latex]. If [latex] X' \\sim
\\text{Gamma}(1+\\nu, 1), U \\sim \\text{Uniform}(0, 1)[/latex] then
\$\$ X = X' \\cdot \\sqrt[\\nu]{U} \\sim \\text{Gamma}(\\nu, 1)\$\$ For
a proof of this fact, see [[1][]], which is a great article on
generating Gamma variates.

### Implementation

[sourcecode language="python"]  
from import numpy as np

def \_cond(u, v, k, c):  
"""Identity function describing the acceptance region"""  
x = v / u \*\* c  
return (c + 1) \* np.log(u) \<= (k - 1) \* np.log(x) - x

def vn\_standard\_gamma(k, c=1.0, rng=np.random):  
"""Generates a single standard gamma random variate"""  
if k \<= 0:  
raise ValueError("Gamma shape should be positive")  
elif k \< 1:  
return vn\_standard\_gamma(1 + k, c, rng) \* rng.uniform() \*\* (1 /
k)  
elif k == 1:  
return rng.standard\_exponential()  
else:  
a, b = get\_bounds(k, c)  
while True:  
u, v = rng.uniform(0, a), rng.uniform(0, b)  
if \_cond(u, v, k, c):  
break;  
return v / u \*\* c

def vn\_gamma(k, t, shape=1, c=1.0, rng=np.random):  
"""Vectorized function to generate multiple gamma variates"""  
generator = lambda x: t \* vn\_standard\_gamma(k, c, rng)  
generator = np.vectorize(generator)  
return generator(np.empty(shape))

def get\_bounds(k, c=1.0):  
"""Computes the minimal upper bounds surrounding the acceptance
region"""  
a = ((k - 1) / np.e) \*\* ((k - 1) / (c + 1))  
b = ((c \* k + 1) / (c \* np.e)) \*\* ((c \* k + 1) / (c + 1))  
return a, b

def prob\_acc(k, c=1.0):  
"""Calculates the probability of acceptance for the given
parameters"""  
from scipy.special import gamma  
a, b = get\_bounds(k, c)  
return gamma(k) / ((c + 1) \* a \* b)  
[/sourcecode]

### Results

And of course I should show you that it works. Here are some histograms
for various values of [latex] \\nu[/latex], with the theoretical density
plotted in dotted red, after sampling [latex] 10\^5[/latex] values. The
y-axis is the frequency (sorry for labeling in Romanian), and for the
red dotted line it can be interpreted as the theoretical probability.
You can clearly see the goodness of fit is excellent.

[![][2]][][![][3]][][![][4]][]

<span id="footnote-1">[1]</span>: George Marsaglia and Wai Wan Tsang.
1998. [The Monty Python method for generating random variables][]. ACM
Trans. Math. Softw. 24, 3 (September 1998), 341-350.
[DOI=10.1145/292395.292453][]

  [Wolfram Alpha]: http://www.wolframalpha.com/ "Wolfram Alpha"
  []: http://localhost:8001/wp-content/uploads/2011/10/regiunea.png
    "The accepting set C"
  [![][]]: http://localhost:8001/wp-content/uploads/2011/10/regiunea.png
  [1]: #footnote-1
  [2]: http://localhost:8001/wp-content/uploads/2011/10/hist1.png
    "Histogram for nu=6"
  [![][2]]: http://localhost:8001/wp-content/uploads/2011/10/hist1.png
  [3]: http://localhost:8001/wp-content/uploads/2011/10/hist2.png
    "Histogram for nu=100"
  [![][3]]: http://localhost:8001/wp-content/uploads/2011/10/hist2.png
  [4]: http://localhost:8001/wp-content/uploads/2011/10/hist3.png
    "Histogram for nu=0.66"
  [![][4]]: http://localhost:8001/wp-content/uploads/2011/10/hist3.png
  [The Monty Python method for generating random variables]: http://www.jstatsoft.org/v03/i03/paper
  [DOI=10.1145/292395.292453]: http://doi.acm.org/10.1145/292395.292453
