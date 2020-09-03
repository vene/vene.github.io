Title: Optimizing with constraints:<br>reparametrization and geometry.
Date: 2020-08-01
Author: vene
Category: presentation 
Slug: mirror-descent
Status: draft
Summary: test

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


When training machine learning models, and deep networks in particular,
we typically use gradient-based methods. But if we require the weights to
satisfy some constraints, things quickly get more complicated.

I've recently learned that a few ways for handling constraints are deeply connected.
In this post, we will explore these connections and demonstrate them in PyTorch on a friendly example. 

# Why constraints are challenging 

In many machine learning models, we fit a model to data by minimizing some
error-like objective,

$$\min_{x \in \mathcal{X}} f(x). \tag{OPT}$$

Here, $x$ denote the neural network weights, the parameters to be learned. They
typically take values in $\mathcal{X}=\reals$, and we train networks by
by choosing an initial configuration $x^{(0)}$ and successively applying
updates of the form:

$$
x^{(t+1)} \leftarrow x^{(t)} - \alpha^{(t)} g(x^{(t)}).
$$

If $f$ is convex and differentiable and $g = Df$ is the gradient of $f$, this is
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
  <svg id="onedimplot" width=550 height=150></svg> <br />
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
which will become the main focus of the rest of this post.

$$ \min_{x \in \mathcal{X}} 
f(x) \coloneqq \frac{1}{2}~(x - x_0)^\top Q (x - x_0) \tag{QP} $$

taking $\mathcal{X} = [0,1] \times [0,1] \subset \reals^2$,
$x_0 = (1.5, .1)$, and 
$Q = \left(\begin{smallmatrix}3 & 2 \\\\ 2 & 3 \end{smallmatrix}\right)$.

Here is what the contours of this function look like. You can see below that the
constrained minimum $x^\star$ is not the same as the unconstrained minimum
clipped to the box.[ref]
There is an important special case where (QP) can be solved exactly: the
case $Q = I$. In this case, the problem becomes
$\arg\min_{x \in \mathcal{X}} \| x - x_0 \|^2_2,$
which is known as the *euclidean projection* of $x_0$ onto $\mathcal{X}$.
If $\mathcal{X}$ are box constraints, the projection decomposes into a series of
independent 1-d projections, which we've seen can be solved by
clipping.[/ref]
This means that, in general, we cannot simply ignore the constraints and apply
them at the end, but we need to bake them into our optimization strategy.

<img alt="quadratic landscape" src="/images/mirror_quad_landscape.png"></img>

## Ways to deal with constraints.

When faced with a box-constrained optimization problem, these are the ideas that
most practitioners would turn to.[ref]This turns out to be a handy personality
quiz to see if somebody resonates more with neural networks or with convex
optimization.[/ref]

 1. *Reparamtrization (REP).* Instead of using constrained variables $x$, replace them
    with unconstrained $u$ such that $x = \sigma(u)$, where $\sigma$ is a
    ``squishing'' nonlinearity from $\reals$ to $\mathcal{X}$. If
    $\mathcal{X}=[0,1]^d$, we may use the logistic function

    $$ [\sigma(u)]_i = \frac{1}{1 - \exp(-u_i)}. $$

 2. *Projected gradient (PG).* Perform unconstrained gradient updates, then
    project back onto the domain after each update:

    $$
    x^{(t+1)} \leftarrow \operatorname{Proj}_\mathcal{X}\big(x^{(t)} - \alpha^{(t)} g(x^{(t)})\big).
    $$

REP is convenient when working with neural network libraries like PyTorch,
because it can be implemented just by changing our model, without requiring
modifications to the optimization code. However, the resulting problem (after
reparametrization) is no longer convex in $u$, even if the original problem was
convex in $x$. PG directly solves the convex optimization problem (QP), but.[ref]come up with a downside[/ref]
