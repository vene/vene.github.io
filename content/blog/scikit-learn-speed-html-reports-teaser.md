Title: Scikit-learn-speed HTML reports teaser
Date: 2012-07-20 14:40
Author: vene
Category: scikit-learn
Tags: gsoc, scikit-learn-speed, vbench, benchmarking, python, scikit-learn
Slug: scikit-learn-speed-html-reports-teaser

EDIT: I made the plots a little more readable, check it out!

Last time, I teased you with a screenshot of local output. Now, I will
tease you with the benchmarks run on a couple of recent commits, along
with some from earlier this year.

After some effort and bugfixes, the project now reliably runs on
different machines, so the next step to host it on a remote server and
invoke it daily is getting closer. In the mean time, you can have a look
at [the sample output][].

Note that just last time, the plots look jagged but the differences are
mostly minor and significant conclusions cannot be drawn yet, but as the
suite will start running daily, the plots will become much more
meaningful. I could waste time running the suite on more previous
commits, but the results wouldn't be comparable with the ones from the
deployed system, because of hardware differences.

Playing around with this makes me want a couple of features in vbench.
One is the possibility to overlay related benchmarks on the same plot
(for example, different parameters for the same algorithm and data):
this could be useful to spot patterns. A second one is some query /
sorting support: see what are the most expensive benchmarks, see what
benchmarks show the biggest jump in performance (but this could become a
historical wall of fame or shame).

  [the sample output]: http://vene.github.com/scikit-learn-speed/
    "scikit-learn-speed"
