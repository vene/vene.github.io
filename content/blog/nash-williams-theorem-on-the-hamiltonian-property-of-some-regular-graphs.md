Title: Nash-Williams theorem on the Hamiltonian property of some regular graphs
Date: 2012-01-29 22:31
Author: vene
Category: Uncategorized
Tags: graph, graph theory, hamiltonian, nash-williams
Slug: nash-williams-theorem-on-the-hamiltonian-property-of-some-regular-graphs

I have been digging on the internet for the proof of this theorem for
the last couple of days without success. The result was published by Sir
Crispin Nash-Williams as *Valency Sequences which force graphs to have
Hamiltonian Circuits*. Interim Rep, University of Waterloo Res Rep.,
Waterloo, Ontario, 1969. However, this old paper is unavailable online
but I have a proof in some lecture notes from my class, that I want to
share here.

**Theorem.** Let [latex]G=(V, E)[/latex] be an [latex]n[/latex]-regular
graph with [latex]|V| = 2n + 1[/latex]. Then, [latex]G[/latex] is
Hamiltonian.

**Proof.** We first remark that [latex]n[/latex] must be even, since
\$\$\\sum\_{x \\in V} d(x) = n(2n + 1) = 2|E|\$\$ We might try to apply
Dirac's theorem, which would give us a Hamiltonian cycle if [latex]
\\forall x \\in V, d(x) \\geq \\frac{|V|}{2}[/latex]. But in the current
case, [latex]\\forall x \\in V, d(x) = n \< \\frac{2n+1}{2}[/latex].

So we force Dirac by adding an extra vertex [latex]w[/latex] and
connecting it to all [latex] x \\in V [/latex]. In this new graph
[latex]G'[/latex], [latex]d(x) = n + 1 \\forall x \\in V[/latex] and
[latex]d(w) = 2n + 1[/latex]. Therefore we have a Hamiltonian cycle that
passes through [latex]w[/latex] and in which, [latex]w[/latex] is
adjacent to two vertices [latex]x[/latex] and [latex]y \\in V[/latex].
Therefore this cycle induces a Hamiltonian path in [latex]G[/latex]:
\$\$P = [x = v\_0, v\_1, ..., v\_{2n-1}, v\_{2n}=y] \$\$

Suppose that [latex]G[/latex] is not Hamiltonian. It follows that if
[latex] v\_0v\_i \\in E [/latex], then [latex] v\_{i-1}v\_{2n} \\notin
E[/latex] and also that if [latex] v\_0v\_i \\notin E [/latex], then
[latex] v\_{i-1}v\_{2n} \\in E[/latex].

We have two cases. If [latex]v\_0[/latex] is adjacent to [latex]v\_1,
..., v\_n[/latex] then it follows that [latex]v\_{2n}[/latex] is
adjacent to [latex]v\_n, v\_{n+1}, ..., v\_{2n-1}[/latex], since it
cannot be adjacent to any [latex]v\_i, i \< n[/latex] without creating a
Hamiltonian cycle. But in this case, in the graph induced by the first
half [latex]G[\\{v\_0, v\_1, ... v\_n\\}][/latex], [latex]v\_n[/latex]
cannot be adjacent to all the others, since in [latex]G[/latex] it has
degree [latex]n[/latex] and it already has [latex]2[/latex] outgoing
edges. So there is at least one vertex [latex]v\_i, i \< n[/latex] that
isn't adjacent to it, which means [latex]v\_i[/latex] is adjacent to
some [latex]v\_j, j \> n[/latex], thus forming a Hamiltonian cycle.

In the second case, we have a vertex [latex]v\_i, 2 \\leq i \\leq 2n -
1[/latex] such that [latex]v\_0v\_i \\notin E[/latex] and
[latex]v\_0v\_{i+1} \\in E[/latex]. This also means that
[latex]v\_{i-1}v\_{2n} \\in E[/latex].

We therefore have a cycle of length [latex]2n[/latex] in
[latex]G[/latex] that excludes [latex]v\_i[/latex]. Let's rename this
cycle [latex]C=[y\_1, y\_2, ..., y\_{2n}, y\_1][/latex] and
[latex]v\_i=y\_0[/latex].

[latex]y\_0[/latex] cannot be adjacent to two consecutive vertices
[latex]y\_i[/latex] and [latex]y\_{i+1}[/latex] because this will give a
Hamiltonian cycle. But we know that [latex]deg(y\_0) = n[/latex]. It
follows that it's adjacent to all of the even or odd numbered vertices.
We assume the latter, without loss of generality. Let [latex]2k[/latex]
be some even index. Notice that we have [latex]\\{y\_0y\_{2k-1},
y\_0y\_{2k+1}\\} \\subset E[/latex] and we can follow the cycle
[latex]C[/latex] from [latex]y\_{2k+1}[/latex] all the way back to
[latex]y\_{2n-1}[/latex] giving us a new cycle [latex]C' = [y\_1, y\_2,
..., y\_{2n-1}, y\_0, y\_{2k+1}, ..., y\_{2n}, y\_1][/latex] also of
length [latex]2n[/latex]. So by repeating the same reasoning for every
even vertex, by placing it in the middle and building a cycle around it,
it follows that every even vertex is adjacent to all the odd vertices.
But there are [latex]n+1[/latex] even indices, so it follows that the
degree of any odd vertex is at least [latex]n+1[/latex], contradicting
the initial conditions of the theorem. [latex]\\square[/latex]
