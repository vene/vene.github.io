Title: More on memory benchmarking
Date: 2012-07-02 11:27
Author: vene
Category: benchmarking, python
Tags: IPython, magic, memit, memory, memory_profiler, mprun
Slug: more-on-memory-benchmarking

Following up on my task to make it easier to benchmark memory usage in
Python, I updated Fabian's [memory\_profiler][] to include a couple of
useful IPython magics. While in my [last post][], I used the new IPython
0.13 syntax for defining magics, this time I used the
backwards-compatible one from the previous version.

You can find this work-in-progress as a [pull request on
memory\_profiler][] from where you can trace it to my GitHub repo.
Here's what you can do with it:

%mprun
------

Copying the spirit of `%lprun`, since imitation is the most sincere form
of flattery, you can use %mprun to easily view line-by-line memory usage
reports, without having to go in and add the `@profile` decorator.

For example:

[sourcecode lang="python"]

In [1]: import numpy as np

In [2]: from sklearn.linear\_model import ridge\_regression

In [3]: X, y = np.array([[1, 2], [3, 4], [5, 6]]), np.array([2, 4, 6])

In [4]: %mprun -f ridge\_regression ridge\_regression(X, y, 1.0)

(...)

109 41.6406 MB 0.0000 MB if n\_features \> n\_samples or \\  
110 41.6406 MB 0.0000 MB isinstance(sample\_weight, np.ndarray) or \\  
111 41.6406 MB 0.0000 MB sample\_weight != 1.0:  
112  
113 \# kernel ridge  
114 \# w = X.T \* inv(X X\^t + alpha\*Id) y  
115 A = np.dot(X, X.T)  
116 A.flat[::n\_samples + 1] += alpha \* sample\_weight  
117 coef = np.dot(X.T, \_solve(A, y, solver, tol))  
118 else:  
119 \# ridge  
120 \# w = inv(X\^t X + alpha\*Id) \* X.T y  
121 41.6484 MB 0.0078 MB A = np.dot(X.T, X)  
122 41.6875 MB 0.0391 MB A.flat[::n\_features + 1] += alpha  
123 41.7344 MB 0.0469 MB coef = \_solve(A, np.dot(X.T, y), solver,
tol)  
124  
125 41.7344 MB 0.0000 MB return coef.T

[/sourcecode]

%memit
------

As described in my previous post, this is a `%timeit`-like magic for
quickly seeing how much memory a Python command uses.  
Unlike %timeit, however, the command needs to be executed in a fresh
process. I have to dig in some more to debug this, but if the command is
run in the current process, very often the difference in memory usage
will be insignificant, I assume because preallocated memory is used. The
problem is that when running in a new process, some functions that I
tried to bench crash with `SIGSEGV`. For a lot of stuff, though,
`%memit` is currently usable:

[sourcecode lang="python"]  
In [1]: import numpy as np

In [2]: X = np.ones((1000, 1000))

In [3]: %memit X.T  
worst of 3: 0.242188 MB per loop

In [4]: %memit np.asfortranarray(X)  
worst of 3: 15.687500 MB per loop

In [5]: Y = X.copy('F')

In [6]: %memit np.asfortranarray(Y)  
worst of 3: 0.324219 MB per loop  
[/sourcecode]

It is very easy, using this small tool, to see what forces memory
copying and what does not.

Installation instructions
-------------------------

First, you have to get the source code of this version of
memory\_profiler. Then, it depends on your version of IPython. If you
have 0.10, you have to edit `~/.ipython/ipy_user_conf.py` like this:
(once again, instructions *borrowed* from [line\_profiler][])

[sourcecode lang="python"]  
\# These two lines are standard and probably already there.  
import IPython.ipapi  
ip = IPython.ipapi.get()

\# These two are the important ones.  
import memory\_profiler  
ip.expose\_magic('mprun', memory\_profiler.magic\_mprun)  
ip.expose\_magic('memit', memory\_profiler.magic\_memit)  
[/sourcecode]

If you're using IPython 0.11 or newer, the steps are different. First
create a configuration profile:  
[sourcecode lang="bash"]  
\$ ipython profile create  
[/sourcecode]  
Then create a file named `~/.ipython/extensions/memory_profiler_ext.py`
with the following content:

[sourcecode lang="python"]  
import memory\_profiler

def load\_ipython\_extension(ip):  
ip.define\_magic('mprun', memory\_profiler.magic\_mprun)  
ip.define\_magic('memit', memory\_profiler.magic\_memit)  
[/sourcecode]

Then register it in `~/.ipython/profile_default/ipython_config.py`, like
this. Of course, if you already have other extensions such as
`line_profiler_ext`, just add the new one to the list.

[sourcecode lang="python"]  
c.TerminalIPythonApp.extensions = [  
'memory\_profiler\_ext',  
]  
c.InteractiveShellApp.extensions = [  
'memory\_profiler\_ext',  
]  
[/sourcecode]

Now launch IPython and you can use the new magics like in the examples
above.

  [memory\_profiler]: http://fseoane.net/blog/2012/line-by-line-report-of-memory-usage/
  [last post]: http://localhost:8001/2012/06/30/quick-memory-usage-benchmarking-in-ipython/
    "Quick memory usage benchmarking in IPython"
  [pull request on memory\_profiler]: https://github.com/fabianp/memory_profiler/pull/13
  [line\_profiler]: http://packages.python.org/line_profiler/
