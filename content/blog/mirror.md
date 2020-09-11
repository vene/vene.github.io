Title: Optimizing with constraints: <br>reparametrization and geometry.
Date: 2020-08-01
Author: vene
Category: presentation 
Slug: mirror-descent
Status: draft
Summary: test

When training machine learning models, and deep networks in particular,
we typically use gradient-based methods. But if we require the weights to
satisfy some constraints, things quickly get more complicated.

I've recently learned that a few ways for handling constraints are deeply connected.
In this post, we will explore these connections and demonstrate them in PyTorch on a friendly example. 

**Outline.** 

[TOC]

<script src="https://unpkg.com/d3@3/d3.min.js"></script>
<style type="text/css">

#plotdiv {text-align: center;}

.rules line, .rules path {
  shape-rendering: crispEdges;
  stroke: #00000;
}

.series path {
  fill: none;
  stroke: #348;
}

.labels {
    font-family: sans-serif;
    font-size: .7em;
}

.thick {
  stroke-width: 4px;
}

.dashed {
    stroke-width: 1px;
}

.unconstr{ fill: gray };
.constr{ fill: black };
</style>


$$
\newcommand\pfrac[2]{\frac{\partial #1}{\partial #2}}
\newcommand\DP[2]{{#1}^\top#2}
$$


# Why are constraints challenging? 

In machine learning, we fit models to data by minimizing an objective,

$$\min_{x \in \mathcal{X}} f(x). \tag{OPT}$$

Here, $x$ denotes the parameters to be learned, for instance, the neural network weights.
They typically take values in $\mathcal{X}=\reals$, and we train networks by
choosing an initial configuration $x^{(0)}$ and successively applying
updates of the form:

$$
x^{(t+1)} \leftarrow x^{(t)} - \alpha^{(t)} g(x^{(t)}).
$$

If $f$ is convex and differentiable and $g(x) = \nabla f(x)$ is the gradient of $f,$ this is
the acclaimed *gradient descent* method. In deep learning, we typically get
stochastic, non-descent methods that nonetheless perform well and are efficient.
Here, we will focus on a "nice", differentiable $f$, and we will see that even
so, constraints quickly complicate things.

For modeling reasons, we might want to impose **constraints** on some of the weights
$x$.  Perhaps one of the parameter corresponds to the variance of a
distribution, and thus it cannot be negative. Or perhaps a parameter denotes
some sort of ``gate'', or mixture between two alternatives $xa_1 + (1-x)a_2$. 
In this case, we would need to constrain $x \in [0, 1]$. This is often called a
*box constraint* and it is one of the most friendly types of inequality
constraint we might deal with.

For one-dimensional convex problems, *i.e.,* $\mathcal{X} = [a, b] \subset
\reals$, box constraints do not complicate the problem: we can solve the
unconstrained problem $x_{\text{unc}}^* = \arg\min_{x\in\reals} f(x)$.  If the
answer satisfies the constraint, then it must be the solution of the constrained
problem as well. If not, the answer can be found by *clipping* to the interval:

$$ x^\star = \operatorname{clip}_{[a,b]}(x_\text{unc}^\star)
\coloneqq \min(a, \max(b, x_\text{unc}^\star)).
$$

??? note "Proof"

    We add non-negative dual variables $\mu_a$ and $\mu_b$ to handle the inequality
    constraints $x \geq a$ and $x \leq b$, and write the lagrangian,

    $$\mathcal{L}(x) = f(x) + \mu_a (a-x) + \mu_b(x-b).$$

    An optimal $x^\star$ must satisfiy the original constraints $(a \leq x^\star \leq b)$
    and be a stationary point of the lagrangian:

    $$ 
    D_x \mathcal{L}(x^\star) = 0 \iff f'(x^\star) = \mu_a - \mu_b.
    \tag{F}
    $$ 

    The dual variables must be non-negative and satisfy
    complementary slackness:

    $$
    \mu_a (a - x^\star) = 0, \quad\text{and}\quad \mu_b (x^\star - b) = 0.
    $$

    Let $x^\star_\text{unc}$ be the solution of the unconstrained problem,
    satisfying  $f'(x^\star_\text{unc})=0$. If 
    $a \leq x^\star_\text{unc} \leq b$, then $x^\star=x^\star_\text{unc}$, and
    choosing $\mu_a=\mu_b=0$ satisfies all conditions.
    
    Otherwise, $x^\star_\text{unc}$ is either too small or too large.
    Assume $x^\star_\text{unc} > a$ and take $x^\star = a$. Then we have $\mu_b=0$,
    and from (F) we must have $\mu_a = f'(a)$. Is this a valid value for the
    dual variable? We must check that $f'(a) \geq 0$. Convex $f$ satisfies
    $ f(a) - f(x) \leq f'(a)(a-x) $
    for any $x$, including the minimizer $x=x^\star_\text{unc}$.
    By assumption, $a-x^\star_\text{unc} > 0$, so we may divide by it yielding

    $$ \mu_a = f'(a) \geq \frac{f(a)-f(x^\star_\text{unc})}{a-x^\star_\text{unc}} \geq 0. $$

    The case $ x^\star_\text{unc} > b $ follows similarly.

The following animation might convince you that this is true:

  <div id="plotdiv">
  <svg id="onedimplot" preserveAspectRatio="xMinYMin meet" viewBox="0 0 550 150"></svg> <br />
	<input type="range" min="-1" max="2" step=".001" oninput="plot(this.value)" onchange="plot(this.value)">
  </div>


<script>
var w = 500;
var h = 100;

var x = d3.scale.linear().domain([-2, 3]).range([0, w]);
var xint = d3.scale.linear().domain([0, 1]);
var y = d3.scale.linear().domain([ 0, 1]).range([h, 0]);

//  var svg = d3.select("body").append("svg")
//  .attr("width", w + 50)
//  .attr("height", h + 50);
var svg = d3.select("#onedimplot");
    var vis = svg.append("svg:g").attr("transform", "translate(25,25)")
    make_rules();

    plot(0.5);


    function plot(x0) {
        var quadratic = make_quadratic(x0);
        chart_line(quadratic, x0);
    }

    function make_quadratic(x0) {
            return (function(t) {
                    return 0.5 * (t - x0) * (t - x0) + 0.2;
            });
    }

function chart_line(func, x0) {
            vis.selectAll('.dots').remove();
            vis.selectAll('.series').remove();
    var g = vis.append("svg:g").classed("series", true)

    g.append("svg:path")
        .classed("dashed", true)
        .attr("d", function(d) { return d3.svg.line()(
          x.ticks(100).map(function(t) {
            return [ x(t), y(func(t)) ]
          })
         )})

    g.append("svg:path")
        .classed("thick", true)
        .attr("d", function(d) { return d3.svg.line()(
          xint.ticks(100).map(function(t) {
            return [ x(t), y(func(t)) ]
          })
                    )})

        
            vis.append('circle')
                .classed("dots", true)
                .classed("unconstr", true)
                .attr("r", 5)
                .attr("cx", function(d) { return x(x0); })
                .attr("cy", function(d) { return y(func(x0)); })

          var xstar = Math.min(Math.max(x0, 0), 1);

            vis.append('circle')
                .classed("dots", true)
                .classed("constr", true)
                .attr("r", 5)
                .attr("cx", function(d) { return x(xstar); })
                .attr("cy", function(d) { return y(func(xstar)); })
}

function make_rules() {
    var rules = vis.append("svg:g").classed("rules", true)

    function make_x_axis() {
        return d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .ticks(10)
    }


    rules.append("svg:g").classed("grid x_grid", true)
            .attr("transform", "translate(0,"+h+")")
            .call(make_x_axis()
                .tickSize(0,0,0)
                .tickFormat("")
            )

    rules.append("svg:g").classed("labels x_labels", true)
            .attr("transform", "translate(0,"+h+")")
            .call(make_x_axis()
                .tickSize(1)
            )
}
</script>


However, in dimension two or more, clipping no longer works, because of
interactions between the variables. We demonstate this on a quadratic problem
which will become the main focus of the rest of this post,

$$ \min_{x \in \mathcal{X}} 
f(x) \coloneqq \frac{1}{2}~(x - x_0)^\top Q (x - x_0).\tag{QP} $$

Let us visualize this problem for the specific case of
the unit square $\mathcal{X} = [0,1] \times [0,1] \subset \reals^2$,
with $x_0 = (1.5, .1)$, and 
$Q = \left(\begin{smallmatrix}3 & 2 \\\\ 2 & 3 \end{smallmatrix}\right)$.
If not for the constraints, since $Q$ is positive definite, the minimum
would be $x^\star_\text{unc} = x_0$.[ref]Because $f(x_0)=0,$ and positive
definiteness guarantess $f(x) > 0$ for any $x \neq x_0$.[/ref]
But a contour plot shows that the constrained minimum $x^\star$ is not the same as the
result of clipping the unconstrained minimum to the box.

<img alt="quadratic landscape" src="/images/mirror_quad_landscape.png"></img>

This means that, in general, we cannot simply ignore the constraints and apply
them at the end, but we need to bake them into our optimization strategy.[ref]
There is an important special case where (QP) can be solved exactly: the
case $Q = I$. In this case, the problem becomes
$\arg\min_{x \in \mathcal{X}} \| x - x_0 \|^2_2,$
which is known as the *euclidean projection* of $x_0$ onto $\mathcal{X}$.
If $\mathcal{X}$ are box constraints, the projection decomposes into a series of
independent 1-d projections, which we've seen can be solved by
clipping.[/ref]


# Ways to deal with constraints.

When faced with a box-constrained optimization problem, these are the ideas that
most practitioners would turn to.[ref]This turns out to be a handy personality
quiz to see if somebody resonates more with neural networks or with convex
optimization.[/ref]

 1. *Reparamtrization (REP).* Circumvent the constraints on $x$, 
    by expressing the function in terms of unconstrained variables $u$
    such that $x_i = \sigma(u_i)$, where $\sigma : \reals \to \mathcal{X}$ is a
    ``squishing'' nonlinearity.
    We can then perform unconstrained minimiziation on $f \circ \sigma$.
    For $\mathcal{X}=[0,1]^d$, we may use the logistic
    function[ref]General intervals $[a,b]$ are obtained by affinely
    transforming $[0,1]$.[/ref]

    $$ \sigma(u) = \frac{1}{1 + \exp(-u)}.$$

 2. *Projected gradient (PG).* Perform unconstrained gradient updates, then
    project back onto the domain after each update:

    $$
    \begin{aligned}
    x^{(t+0.5)} &\leftarrow x^{(t)} - \alpha^{(t)} g(x^{(t)}) \\
    x^{(t+1)} &\leftarrow \operatorname{Proj}_\mathcal{X}\big(x^{(t+0.5)}\big)
    \\
    \end{aligned}
    $$

REP is convenient when working with neural network libraries like PyTorch,
because it can be implemented just by changing our model, without requiring
modifications to the optimization code. However, the resulting problem (after
reparametrization) is no longer convex in $u$, even if the original problem was
convex in $x$. PG directly solves the convex optimization problem (QP), but
the intermediate iterates $x^{(t+0.5)}$ can leave $\mathcal{X}$,
leading to a possibly less stable or too aggressive trajectory.

In this post, we will explore the connection between the two by studying *mirror
descent* and its information-geometric interpretation as natural gradient
in a dual space. But first, let's explore our two initial ideas.

### Reparametrization.

Instead of optimizing w.r.t. the constrained variables $x$, we introduce an
underlying variable $u$, such that $x_i = \sigma(u_i)$.[ref]This seems to be the
more common method among neural network practitioners; one
place where it shows up often is *neural variational inference*, where we would
constrain the variance of a learned distribution using a *softplus*
function.[/ref]
In our case, we use a logistic sigmoid reparametrization to get the
unconstrained non-convex problem

$$ \min_{u \in \reals^2} f(\sigma(u)), $$

where $\sigma$ is applied element-wise.  Let's first implement our function
$f(x) = \frac{1}{2} (x - x_0)^\top Q (x - x_0)$:

```python

def f(x):
    z = x - x_star
    Qz = z @ Q
    return .5 * torch.einsum("ij,ij,i", Qz, z)
```

When reparametrizing, $x$ is no longer a learned parameter, but a function of
the learned parameter $u$. The chain rule gives

<!--%$$ D_u f(\sigma(u)) = {D_x}f(\sigma(u)) \cdot D_u\sigma(u),$$-->

$$ \pfrac{}{u} f(\sigma(u)) = \pfrac{f(x)}{x}\biggr\rvert_{x=\sigma(u)} \pfrac{\sigma(u)}{u} $$

<!--
$$ \pfrac{}{u} f(\sigma(u)) = \pfrac{f(\sigma(u))}{x} \pfrac{\sigma(u)}{u} $$

$$ \nabla_{u} f(\sigma(u)) = \nabla_x f(\sigma(u))  \pfrac{\sigma(u)}{u} $$

$$ \nabla_{u} f(\sigma(u)) = \nabla_x f(\sigma(u))  J_\sigma(u) $$
-->

but PyTorch autodiff does this automatically for us.
We may now write a minimalist gradient-based optimization loop:

```python

def optim_reparam(u_init, lr, max_iter=100000):
    u = u_init.clone()
    for i in range(max_iter):
        u_ = u.clone().requires_grad_()
        f(torch.sigmoid(u_)).backward()  # compute grad wrt u_
        u -= lr * grad  # take gradient step
    return u
```

With a very small learning rate, we get a glimpse into the dynamics of this
method. For comparison, we include the unconstrained trajectory.

<img alt="quadratic landscape" src="/images/mirror_quad_lr0.010_reparam.png"></img>

In practice, we would use a much larger learning rate to accelerate
optimization:

<img alt="quadratic landscape" src="/images/mirror_quad_lr0.200_reparam.png"></img>

We can see that even with a large learning rate, the reparametrization method
takes much smaller steps, especially as it gets closer to the boundary of the
domain. At any point $u$, recall the reparametrized gradient:

$$ \pfrac{}{u} f(\sigma(u)) = \pfrac{f(x)}{x}\biggr\rvert_{x=\sigma(u)} \pfrac{\sigma(u)}{u}. $$

This is the unconstrained gradient at $x=\sigma(u)$, rescaled by the Jacobian of $\sigma$.
Since $\sigma$ acts elementwise, its Jacobian is a diagonal matrix, with
$\pfrac{\sigma(u)_i}{u_i}  = \sigma(u_i)(1 - \sigma(u_i)) = x_i (1 - x_i).$ We can thus see
that as $x_i$ approaches $0$ or $1$, the reparametrization rescales the
gradient **severely**, bringing the effective step size toward 0. Remember, this
happens *automatically* via the chain rule! But, although slowly, and along a
slightly winding trajectory, our method finds the right answer.

### Projected gradient.

The projected gradient method is particularly well suited to handling ``simple'' constraints
like the box case, but, unlike reparametrization, requires a different kind of
expertise to get running in the case of complicated constraints.
[ref]PG is very popular in convex optimization, useful both for theory and for
practice. However, it does not seem to be so widely used in the pure neural
network world, perhaps mostly because it is not directly supported by the
built-in optimizers in major frameworks.[/ref]
For box constraints, the projection can be computed efficiently, since
$\big[\!\operatorname{Proj}_{[0,1]^d}(x)\big]_i = \operatorname{clip}_{[0,1]}(x_i).$
The implementation follows:

```python

def optim_pg(x_init, lr, max_iter=100000):
    x = x_init.clone()
    for i in range(max_iter):
        x_ = x.clone().requires_grad_()
        f(x_).backward()  # compute grad wrt x_
        x -= lr * grad  # take gradient step
        x = torch.clamp(x, min=0, max=1)  # project
    return x
```

<img alt="quadratic landscape" src="/images/mirror_quad_lr0.010_pg.png"></img>

It looks like the projected gradient method tends to follow the unconstrained
trajectory while sticking to the boundary of the domain. Of course, with larger
steps, the differences become more pronounced.

<img alt="quadratic landscape" src="/images/mirror_quad_lr0.200_pg.png"></img>

In this instance, PG is the clear winner: look how fast it makes progress. With
less well-behaved and non-convex functions this need not be the case. So we are
motivated to delve deeper and explore how PG and REP relate, despite seeming so
different. 

# Generalizing the projected gradient method with divergences.
In the projected gradient method, we take unconstrained steps, which might take
us outside of $\mathcal{X}$, and then move the solution back to $\mathcal{X}$ by
projection:

$$ x^{(t+1)} \leftarrow \operatorname{Proj}_\mathcal{X}\big(x^{(t+0.5)}\big). $$

Projection finds the point $x \in \mathcal{X}$ closest to $x^{(t+0.5)}$, i.e.,

$$ \operatorname{Proj}_\mathcal{X}\big(x^{(t+0.5)}\big) = \argmin_{x \in \mathcal{X}} \| x - x^{(t+0.5)} \|. $$

This update can be interpreted as approximately minimizing a regularized linearization of
$f,$

$$ x^{(t+1)} \leftarrow \arg\min_{x \in \mathcal{X}}  \DP{\nabla f(x^{(t)})}{x} + \frac{1}{2\alpha_t}\|x - x^{(t)}\|^2. \tag{GD}
$$

??? note "Explanation"

    Why does this update make sense, and where does it come from? We are trying to
    minimize a function $f(x)$, but we don't know what it looks like globally: we only
    have access to its value $f(x)$ and its gradient $\nabla f(x)$ at points $x$
    that we may query one at a time. At any point $x_0$,
    the first-order Taylor expansion is:

    $$ f(x_0 + \delta) = f(x_0) + \DP{\nabla f(x_0)}{\delta} + o(\|\delta\|). $$

    To get a linear approximation of $f$ we can plug in $\delta = x - x_0$:

    $$ f(x) =  f(x_0) + \DP{\nabla f(x_0)}{x - x_0} + o(\|x - x_0\|). $$

    So as long as $x$ is not too far from $x_0$, we have 

    $$f(x) \approx \tilde{f}_{x_0}(x) \coloneqq f(x_0) + \DP{\nabla f(x_0)}{x - x_0}.$$

    This affine approximation is much easier to
    minimize, but it is only accurate locally, therefore, we use it iteratively,
    taking a small step, then updating the approximation:

    $$ 
    x^{(t+1)} \leftarrow \arg\min_{x \in \mathcal{X}} \tilde f_{x^{(t)}}(x) + \frac{1}{2\alpha_t}\|x - x^{(t)}\|^2. 
    $$

    where the term on the right keeps us close to $x^{(t)}$ to ensure the
    approximation is not too bad. Clearing up the constant terms from inside the
    $\arg\min$ yields the desired expression.

If $\mathcal{X}=\reals$, the problem (GD) can be solved by setting the gradient
to 0, which recovers the gradient descent update. Otherwise, we get exactly the
projected gradient update.

??? note "Derivation"
    
    $$
    \begin{aligned}
     & \arg\min_{x \in \mathcal{X}} \DP{x}{\nabla f(x^{(t)})} + \frac{1}{2\alpha_t} \|x-x^{(t)}\|^2 \\
    =& \arg\min_{x \in \mathcal{X}} \DP{x}{\nabla f(x^{(t)})} + \frac{1}{2\alpha_t} \|x\|^2 - \frac{1}{\alpha_t} \DP{x}{x^{(t)}} \\
    =& \arg\min_{x \in \mathcal{X}} \alpha_t \DP{x}{\nabla f(x^{(t)})} + \frac{1}{2} \|x\|^2 - \DP{x}{x^{(t)}} \\
    =& \arg\min_{x \in \mathcal{X}} \DP{x}{\underbrace{\alpha_t \nabla f(x^{(t)}) - x^{(t)}}_{-x^{(t+0.5)}}} + \frac{1}{2} \|x\|^2 \\
    =& \arg\min_{x \in \mathcal{X}} \frac{1}{2} \| x - x^{(t+0.5)} \|^2 \textcolor{gray}{ - \frac{1}{2} \|x^{(t+0.5)}\|} \\
    =& \operatorname{Proj}_{\mathcal{X}} (x^{(t+0.5)}).
    \end{aligned}
    $$


The function $D(x, y) = \| x - y \|^2 = \sum_i (x_i - y_i)^2$ is the *squared Euclidean distance*.
Here, geometry starts to come into play!  Euclidean geometry is
convenient and comfortable for thinking about spaces like $\reals^d,$ but
it is not always the best model.
<!--all quantities are well characterized by it.
Our case of variables constrained
on $[0, 1]$ provide a good example: the difference between .50 and .51 seems
like should not be the same as the difference between .98 and .99.-->
The **Bregman divergence** provides a convenient generalization of the squared
euclidean distance: given strictly convex, twice-differentiable $\Psi$,

$$ D_\Psi(x, y) \coloneqq \Psi(x) - \Psi(y) - \DP{\nabla \Psi(y)}{x - y}. $$

For $\Psi = \frac{1}{2} \| \cdot \|^2$, this recovers the squared euclidean
distance. Replacing $\frac{1}{2}\|\cdot\|^2$ by $D_\Psi$ in the projected
gradient algorithm leads to a generalization known as **mirror descent**,

$$
x^{(t+1)} \leftarrow \arg\min_{x \in \mathcal{X}}  \DP{\nabla f(x^{(t)})}{x} + \frac{1}{\alpha_t}D_\psi(x, x^{(t)}). \tag{MD}
$$

Since $\Psi$ is twice differentiable and strongly convex, it has a gradient
$\psi = \nabla\Psi$ which is invertible. Solving (MD) gives the update in the
form of a so-called Bregman projection,[ref]Not technically a projection, 
since iterating it twice need not give the same
result, but the term emphasizes the parallel to the euclidean case.[/ref]

$$
\begin{aligned}
u^{(t+0.5)} &\leftarrow \psi(x^{(t)}) - \alpha_t \nabla f(x^{(t)}) \\ 
x^{(t+1)} &\leftarrow 
\argmin_{x \in \mathcal{X}} D_\Psi\big(x,  \psi^{-1}(u^{(t+0.5)})\big). \\
\end{aligned}
$$

If $\Psi$ is carefully chosen such that $\psi^{-1}(u) \in \mathcal{X}$ for all
$u \in \mathcal{U}$, then the Bregman projection step is trivial, yielding

$$ x^{(t+1)} \leftarrow \psi^{-1}\big(
\psi(x^{(t)}) - \alpha_t \nabla f(x^{(t)})
\big). $$

Let's make this more concrete.

The choice of $\Psi$ will define the *geometry* of our space.
Values in $[0,1]$ may be interpreted as *coin flip* probabilities:
the higher, the more likely an event is to happen. An important property of a
binary random variable is its entropy. If $x_i \in [0, 1]$ denotes the
probability associated with coin $i$, the entropy is

$$H(x_i) = -x_i \log x_i - (1 - x_i) \log (1 - x_i).$$

We may extend this additively to vectors as $H(x) = \sum_i H(x_i)$.
On $\mathcal{X}=[0, 1]$, entropy is continuously differentiable and strictly
**concave**, maximized at $x=0.5$ and minimized at $x=0$ and $x=1$.[ref]$H(0.5) =
\log 2,$<br>$H(0)=H(1)=0$.[/ref] 

Let us thus take $\Psi = -H$. Its gradient is $\psi : \mathcal{X} \rightarrow \mathcal{U}$,

$$ \psi(x) \coloneqq -\nabla H(x) = \log(x) - \log(1-x), $$

with inverse $\phi : \mathcal{U} \rightarrow \mathcal{X}$,

$$ \phi(u) \coloneqq \psi^{-1}(u) = \frac{1}{1 + \exp(-u)} = \sigma(u). $$

<!--
The entropy induces a Bregman divergence $D_{-H}$, which after some manipulation
can be written as

$$D_{-H}(x, y) = x \log \frac{x}{y} - (1-x) \log \frac{1-x}{1-y}. $$
-->

o, written in terms of the familiar sigmoid, the mirror descent update induced by the negative entropy takes the (remarkable!) form

$$ x^{(t+1)} = \sigma(\sigma^{-1}(x^{(t)}) - \alpha_t \nabla f(x^{(t)})). $$

Things are beginning to clear up! We can think of the pair of inverse functions
$(\psi, \phi)$ as maps between $\mathcal{X}$ and $\mathcal{U}$.  We will call these
the **primal** and **dual** spaces, respectively. Mirror descent thus
first moves into dual (unconstrained) space, performs an update there, and then moves
back. Reparametrization rewrites the problem in dual coordinates and performs
gradient descent: this is not the same, and the trajectories are quite
different!

<img alt="quadratic landscape" src="/images/mirror_quad_lr0.010_md.png"></img>

With a larger step size, we see that mirror descent takes much larger steps than
reparametrization does.

<img alt="quadratic landscape" src="/images/mirror_quad_lr0.200_md.png"></img>

Now that we figured out that we may think about the problem in primal or dual
coordinates, we may also visualize the optimization trajectory in dual coordinates.

<img alt="quadratic landscape" src="/images/quad_lr0.010_md.png"></img>

Yet, the way that mirror descent leans on moving from $\mathcal{X}$ to
$\mathcal{U}$ is very familiar to the reparametrization strategy. Is there a
deeper connection between the two? We illuminate it next.

# Duality between mirror descent <br/>and natural gradient.

The main result.

# Acknowledgements.

Anima Anandkumar's talk and paper, Caio.


