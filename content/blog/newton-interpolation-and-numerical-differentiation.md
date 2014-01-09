Title: Newton interpolation and numerical differentiation
Date: 2011-04-15 13:34
Author: vene
Category: python
Tags: differentiation, interpolation, matplotlib, newton, numerical, numpy
Slug: newton-interpolation-and-numerical-differentiation

I am sharing some Python code code that I wrote as a school assignment.
This computes the Newton form of the interpolation polynomial of a given
set of points, and allows for the evaluation of both the polynomial and
its derivative, at a given point. This is an accurate way of estimating
the derivative of a complicated function.

Initially it plots the function, the interpolating polynomial and its
derivative. When clicking on the plot, the tangent to the interpolating
polynomial at the horizontal position of the mouse cursor is plotted.

It can be found here: <https://gist.github.com/921554>
