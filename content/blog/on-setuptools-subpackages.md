Title: On setuptools subpackages
Date: 2011-04-04 15:01
Author: vene
Category: python
Tags: python, setuptools
Slug: on-setuptools-subpackages

Today, I spent more than two hours trying to figure out why, despite
things working out fine in my development scikits.learn folder,
`python setup.py install` would completely ignore the module I
refactored into a subpackage.

I imagined that simply adding it to the parent `__init__.py __all__`
attribute would do, I kind of thought that setuptools automatically
finds the subpackages.

At first I thought of looking in `setup.py`, but I only examined the one
in the topmost directory, which, in the case of scikits.learn, is two
degrees of separation away from the actual setup.py that takes care of
subpackages (ie. I was looking at `/setup.py` instead of
`/scikits/learn/setup.py`).  This had me fooled for a while.

The steps to add a working and installable module to a python
setuptools-based project are as follows:

1.  Add a `__init__.py` file in the folder (ie.
    `/scikits/learn/decomposition/__init__.py`)
2.  If the module requires compiling or any special attention, add an
    appropriate  `__setup__.py` file in the folder.
3.  Update the `__init__.py __all__` attribute in the parent folder (ie.
    `/scikits/learn/__init__.py`)
4.  Update the `setup.py` in the parent folder (ie.
    `/scikits/learn/setup.py`) by adding something like:  
    `config.add_subpackage('decomposition')`

Don't forget to do the same for the tests subfolder!

Conclusions
-----------

While wasting so much time due to a simple beginner's mistake is not
very pleasant, I am not frustrated with setuptools. On the contrary, now
that I understand it better I can appreciate its flexibility and
clarity, when compared to, for example, MSBuild and Visual Studio
project files. Just one more reason to love Python!
