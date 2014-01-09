Title: Customizing scikits.learn for a specific text analysis task
Date: 2011-04-29 14:33
Author: vene
Category: nlp, scikit-learn
Slug: customizing-scikits-learn-for-a-specific-text-analysis-task

Scikits.learn is a great general library, but machine learning has so
many different application, that it is often very helpful to be able to
extend its API to better integrate with your code. With scikits.learn,
this is extremely easy to do using inheritance and using the pipeline
module.

The problem
-----------

While continuing the [morphophonetic analysis of Romanian verbal
forms][], I found the need to streamline my workflow to allow for more
complex models. There were a lot of free model parameters and it would
have been painful to interactively tweak everything in order to find a
good combination

In my case, I needed to read a file containing infinitives and labels
corresponding to conjugation groups, and run a linear support vector
classifier on this data. The SVC has its C parameter that needs to be
tweaked, but I also had some ideas that arose from the images in my old
post. There, I compared the way the data looked when represented as
differently sized n-gram features. Furthermore, I compared the count
features (ie. features indicating the number of times an n-gram occurs
in a string) with binary features (ie. indicating only whether the
n-gram occurs in the string or not). It looked to me like, for such a
low-level text analysis task, using counts only adds noise.

For this reason, the `feature_extraction.text.CountVectorizer` was not
enough for me. It only returns count features. There was also another
thing that needed to be adjusted: by default, its analyzer uses a
preprocessor that strips accented characters, and I had strong reasons
to believe that Romanian diacritics are very relevant for the learning
task. So, I needed to extend the vectorizer.

The solution
------------

The code I came up with is [here][]. I tried to build a class that would
be as specific to my needs as possible. It is important to retain the
full API, however. Note the `y=None` parameter in the fit functions. Its
necessity will become clear in a moment.

Another tricky part was exposing the `max_n` parameter from the inner
analyzer. This was not really natural, but it simplified the
constructions later on.

My `InfinitivesExtractor` class builds a data matrix from a list of
strings. After using it, the data needs to be passed to the classifier,
an instance of `svm.LinearSVC`. The `pipeline `module in scikits.learn
allows us to plug components into eachother in order to build a more
complex object. In this case, we would like a classifier that receives a
string as input, and directly outputs its label. We wouldn't want the
user to have to manually use the feature extractor prior to
classification.

The pipeline is very easy to build:  

` pipeline = Pipeline([('extr', InfinitivesExtractor()), ('svc', LinearSVC(multi_class=True))])`  
The pipeline object now works exactly as expected: we can call fit and
predict on it. It also exposes the parameters of its constituents, by
prefixing them with the name of that component. For example, the support
vector machine's C parameter can be accessed as pipeline.svc\_\_C.

All that is left now is to see whether this is a good model, and what
combination of parameters makes it work the best. Scikits.learn provides
a great tool for choosing the parameters: the `grid_search` module. When
working with models like support vector machines, model parameters (such
as the radial basis kernel width) usually need to be chosen by cross
validation, because intuition doesn't help much when dealing with high
dimensional data.

Grid search allows the definition of a discrete range of values for
multiple parameters. Then, for each combination of parameters, it fits
and evaluates a model using cross-validation, and the model with the
best score is the winner. Because we combined the components into a
pipeline, it is very easy to run grid search on the combined model, and
to simultaneously tweak the settings both for the extractor and for the
classifier.

After running the grid search using the code [here][1], I found that
indeed, using binary features instead of occurence counts improves
performance. I also found that the optimal n-gram length is 5, but the
gain is not that big when compared to a length of 3, which generates a
lot less features.

Conclusions
-----------

I hope that I managed to show the strength of a well-designed API.
Because of it, it would be very easy to add, for example, an extra layer
for dimensionality reduction before classification. It would only
require an extra item in the pipeline constructor. A call from a
web-based frontend, for example, would be very short and simple. Because
of the consistency in the scikits.learn classes, we can write cleaner
and better code, and therefore work with greater efficiency.

  [morphophonetic analysis of Romanian verbal forms]: http://venefrombucharest.wordpress.com/2011/04/14/a-look-at-romanian-verbs-with-scikits-learn/
    "A look at Romanian verbs with scikits-learn"
  [here]: https://github.com/vene/misc-nlp/blob/master/conjugation/grid_search_example/preprocess.py
  [1]: https://github.com/vene/misc-nlp/blob/master/conjugation/grid_search_example/gridsearch.py
