Title: A look at Romanian verbs with scikits-learn
Date: 2011-04-14 01:40
Author: vene
Category: nlp, scikit-learn
Tags: alternations, computational linguistics, infinitives, pca, principal components analysis
Slug: a-look-at-romanian-verbs-with-scikits-learn

One of the problems we tackled here at my university is one as old as
the modern Romanian language. It is a problem for linguists, as well as
for foreigners trying to learn the language. We call it the root
alternations problem.

Similar to French and other languages, Romanian verbs are split into
four groups with different conjugation patterns. Except for the
irregular verbs, this categorization is performed based on the suffix of
the infinitive. However, the conjugation is not straightforward even
within these classes, because many verbs exhibit alternations in their
root. For example, the verb *a purta* (to wear) becomes *eu port* (I
wear) but *el poartă* (he wears). It can be seen that the letter *o* in
the root changes to *oa* during conjugation. This makes learning the
language quite difficult, because we have no rules to describe when
these changes occur.

Attempts to formalize such rules from a computer scientific point of
view date back to G. C. Moisil in 1960. Such (incomplete) rules can be
formulated as context-sensitive grammars, since the alternations are
determined by the context in which certain characters appear.

This leads to the idea of analyzing the verbs from a machine learning
point of view: what can we find out by looking at n-gram representation
of the infinitives?

This is easy to do within scikits.learn. The `feature_extraction.text`
package contains all the necessary tools: the `CharNGramExtractor`,
which builds all the n-grams of a string, for n in an interval. Then, a
`CountVectorizer` is built on top of the extractor. Its purpose is to
extract the features out of a list of documents and transform them into
a matrix representation of token counts. By postprocessing this matrix
we can obtain a binary representation, indicating only whether a token
occurs in a document or not, instead of the count.

In this case, documents are Romanian infinitives. This means we are
limited to using short n-grams, because the documents are themselves
short. There is also the question whether anything relevant can be found
out of such a representation which does not encode a lot of information.

After building the data matrix from the list of verbs, I plotted a 2D
PCA projection and here are the results. I am only posting a teaser for
now, but the results are encouraging:

[![Romanian infinitives as 2D projection][]][]

From the image it is clear that n-gram representations of the
infinitives induce clusters. Further results suggest that for certain
subclasses of the dataset, such a representation (or even a simpler one)
is enough to clearly answer whether a verb does not exhibit
alternations. This encourages further exploration of this path,
especially supervised and semi-supervised approaches.

  [Romanian infinitives as 2D projection]: http://localhost:8001/wp-content/uploads/2011/04/infinitives_pca.png
    "infinitives_pca"
  [![Romanian infinitives as 2D projection][]]: http://localhost:8001/wp-content/uploads/2011/04/infinitives_pca.png
