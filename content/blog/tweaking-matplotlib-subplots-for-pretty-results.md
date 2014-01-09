Title: Tweaking matplotlib subplots for pretty results
Date: 2011-04-04 20:53
Author: vene
Category: python
Tags: matplotlib, python
Slug: tweaking-matplotlib-subplots-for-pretty-results

When plotting multiple subplots using matplotlib, the axes rarely look
pretty with the default configuration. Since matplotlib figures are
abstract objects, designed for consistency in print as well as on
screen, tweaking their layout can get tricky.

### An example

The following code is taken from the [face recognition example][] in
scikits.learn:  
`pl.figure(figsize=(1.8 * n_col, 2.4 * n_row))`

This is very confusing at first, for somebody used to work on screen:
the quantities in there are actually inches! These are converted
implicitly to pixels through the dpi parameter, which is left as default
(80 dpi) in this example.

Then, it gets even worse: In order to tweak the positioning of the
subplots, this is what is done:  

`pl.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)`  
Now, all of these are percents of the image height/width. The margins
are sort of like CSS-style margins, only relative to the bottom left
corner. In other words, `right=.99` means that the right margin is 1%
away from the right edge.

The parameters `hspace` and `wspace` control the spacing between the
subplots. However these are kind of hard to get right, because,
obviously, there are more settings than there are degrees of freedom.

### My tip

On my system, the default matplotlib backend is TkAgg. The matplotlib
backend controls the graphical environment that builds the plot windows,
as well as the rendering engine used. TkAgg has a "configure subplots"
button that opens a popup window with sliders to visually adjust the
parameters above. The problem is that the sliders are unlabeled, so I
needed to do an heuristic by first setting the parameters by hand and
then exploring the direction in which they need to be changed.

When I tried different backends, I found that WXAgg has labeled sliders.
This means you can adjust your subplots visually and you will have the
parameter values to use in the call to `subplots_adjust` in one go!

You can set your backend to WXAgg by adding the line `backend: WXAgg` in
your [matplotlibrc file][].

  [face recognition example]: http://scikit-learn.sourceforge.net/auto_examples/applications/plot_face_recognition.html
    "face recognition example"
  [matplotlibrc file]: http://matplotlib.sourceforge.net/users/customizing.html#the-matplotlibrc-file
    "Customizing matplotlib"
