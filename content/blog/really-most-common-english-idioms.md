Title: Really the most common english idioms?
Date: 2013-02-11 16:50
Author: vene
Category: nlp
Tags: bnc, british national corpus, corpus, fixed expression, fixed phrase, idioms, oec, oxford english corpus, corpus linguistics, nlp
Slug: really-most-common-english-idioms

A while back I ran into [this blog post][] and it made me wonder. I'm
not a native speaker but the idiomatic phrases that they note as common
don't strike me as such. I don't think I have ever encountered them very
often in real dialogue.

The blog post lists the 10 most common idioms in English. **Idioms**,
also known less ambiguously as **fixed expressions**, are units of
language that span at least two words. Their meaning, relatively to the
individual meaning of the parts of the phrase, are figurative. Despite
this, fixed expressions don't classify as creative language, or
exploitations. By definition most speakers will unequivocally be
familiar with them.

For example, they cite *piece of cake* as the most common idiomatic
expression. This refers to using the phrase to mean that something is
easy, that it isn't challenging. An example of literal use, however,
would be when ordering *a piece of cake* for desert in a restaurant.

Everyone knows that language is a perpetually changing thing, so to
begin with it's even slightly misleading to discuss of the commonness of
a phrase, without giving more context. The blog post doesn't justify the
ranking with any numbers anyway, so let's take them one by one and find
out how common they really are!

Corpus Linguistics
------------------

The approach we are taking here is known as corpus linguistics. The best
way to argue that a certain phrase is common, that something is used
with a specific meaning or that some constructions are normal is, under
corpus linguistics, not to make up examples that seem reasonable, but to
look at **representative collections of text** (corpora) and trying to
find the examples there. The conclusions you get this way are backed by
real-world language use.

An argument often brought against generative linguistics is that it
focuses on the (hard) border between grammatical and not grammatical,
and the border is usually defined by made-up examples. This is
inappropriate for studying how the norms are exploited in real language
use, for example. I refer the interested to the work of [Patrick
Hanks][] [[1][], [2][]].

Corpus linguistics is sensitive to the corpus used. For this example
let's use two British English corpora: the [British National Corpus][]
and the [Oxford English Corpus][]. Measuring by number of words, the
latter is around 20 times bigger. The strong point of the BNC is the
attention given to the mixing proportions of various domains. The OEC,
on the other hand, is larger and more recent. I have a feeling (but I
cannot strongly affirm) that the differences in the following results
arise from the inclusion in the OEC of blogs dating from the mid-2000s.

Cognitive salience vs. social salience
--------------------------------------

One of the key ideas that motivate corpus approaches is the mismatch
between these. The cognitive salience of something is the ease with
which we can recall it. An example often used in language is the fixed
expression *kicking the bucket*. It is one of the standard examples of
fixed expressions that people give very often when asked. It is supposed
to mean *dying*.

However, big surprise: the BNC has only 18 instances of this phrase, out
of which only 3 are idiomatic, the rest being either literal or
metalinguistic. This is a nice example of the salience contrast, but we
mustn't hurry to conclusions. The OEC has 193 examples (still few,
relative to its size) but a lot more of them are idiomatic uses. To save
the time I didn't look at all the examples, but took a random sample of
size 18, to compare the relative frequencies to BNC. Here, 15 out of 18
instances are idiomatic and none are meta. Quite a difference!

This goes to show the importance of context when we draw conclusions
about language use. Now let's tackle the list with a similar analysis.

The idioms
----------

1.  **Piece of cake**

    In BNC, this phrase occurs 51 times. 29 of these occurrences,
    however, the meaning is literal. In OEC we find 601 occurrences. In
    a random sample of size 51 we find 12 literal uses.

2.  **Costing an arm and a leg**

    For flexibility we search for the phrase *an arm and a leg*. In BNC
    it can be found 29 times: one literal, four with the verb *to pay*,
    and 16 with *to cost*. In OEC it appears 228 times. We take, again,
    a sample of size 29 and find no literal uses, 16 with *to cost*,
    four with *to pay*, three with *to charge* and a few different uses.
    The figurative meaning is the same in all cases: a lot of money.

3.  **Break a leg**
    <p>
    BNC: 16, 13 of which are literal. OEC: 70 hits, 10/16 literal.
4.  **Hitting the books**

    BNC: 1 occurrence of *hit the record books*, which has a different
    meaning. The idiom is never used. OEC: 135, one of which literal.

5.  **Letting the cat out of the bag**

    We just looked for cooccurrences of *cat* in the context of the
    phrase *out of the bag*.  
    BNC: 19, out of which 3 metalinguistic/literal. OEC: 298, and out
    of a sample of 19, all were idiomatic.

6.  **Hitting the nail on the head**

    BNC: 12 instances, all idiomatic. OEC: 484, and out of a sample of
    12 all were idiomatic.

7.  **When pigs fly**
    <p>
    We looked for the lemma *fly* before the word *pigs* therefore
    catching multiple variations.  
    BNC: 17 hits, OEC: 240.
8.  **Judging a book by its cover**

    We looked for the fixed phrase *book by its cover*, because the
    leading verb might vary.  
    In the BNC, 11 instances (1 of them with tell instead of judge). In
    OEC, 195 instances. Sampling 11, all were idiomatic.

9.  **Biting off more than one can chew**

    BNC: 16 occurences, one of which with "to take" instead of "to
    bite". OEC: 231, all idiomatic after sampling 16.

10. **Scratching one's back**

    BNC: 23, out of which only 5 idiomatic. OEC: 756, 5/23 idiomatic.

Recalculating the rank
----------------------

<p>
We now have enough data to reorder the expressions and compare. The
result will be more approximate for the OEC because of our use of small
subsamples to estimate the frequencies, but hopefully it will still be
interesting. The way we are estimating the counts for the OEC is as
follows: take, for instance, *break a leg*. It was found 70 times, and
out of a sample of 16, 10 were literal. The expected number of idiomatic
uses is therefore:  

<center>
[latex]n = \\left ( 1 - \\frac{10}{16} \\right ) \\cdot 70 =
26.25[/latex]

</center>
  
Repeating this computation and skipping a ton of steps leads to the
following rankings:

</p>
<div style="float: left; margin-left: 5em;">
**In the British National Corpus:**

</p>
1.  Costing an arm and a leg
2.  Piece of cake
3.  When pigs fly
4.  Letting the cat out of the bag
5.  Biting off more than one can chew
6.  Hitting the nail on the head
7.  Judging a book by its cover
8.  Scratching one’s back
9.  Break a leg
10. Hitting the books

</div>
<div style="float: right; margin-right: 5em;">
**In the Oxford English Corpus:**

</p>
1.  Hitting the nail on the head
2.  Piece of cake
3.  Letting the cat out of the bag
4.  When pigs fly
5.  Biting off more than one can chew
6.  Costing an arm and a leg
7.  Judging a book by its cover
8.  Scratching one’s back
9.  Hitting the books
10. Break a leg

</div>
  
  
We can see that apart from the apparent switching of *hitting the nail
on the head* with *costing an arm and a leg*, the rankings are not too
different. We can quantify this by using the **Rank Distance**, a metric
introduced by Liviu P. Dinu [[3][], [4][]]. Here, all our 3 rankings are
over the same domain: we are not looking for the most frequent idioms in
the corpora, this would be very hard. We are just reordering the
proposed rank according to the occurrences in BNC and OEC. In this
simple case, Rank Distance reduces to [latex]\\ell\_1[/latex] distance
over rank position vectors. The weighted Rank Distance, bounded on
[latex][0, 1][/latex] is in this case given by a scaling factor of
[latex]0.5k\^2[/latex] where *k* is the length of the rankings (10 in
our case).

The computed distance between the original ranking and the BNC
reordering is 0.52. Between the original and the OEC reordering, it is
0.68. Our two reorderings are much closer: the distance is 0.28. This is
mostly because that the permutations between the two reorderings affect
the top position, and are therefore weighted more.

It's also interesting to look at the ratio of the counts. Interestingly,
they approximately differ by a constant factor not far from the relative
size difference of the two corpora, as would be expected.

We have to throw away *hitting the books* because its BNC zero count
leads to divisions by zero. After this step, the average of the relative
counts of the idioms is 19.5, with a standard deviation of 10.1, while
OED is supposed to have around 20 times more words than the BNC.

Conclusions
-----------

Well, it seems people don't say *break a leg* and *let's hit the books*
as often as the original author claims. The popularity of most of the
cited idioms seems supported by the data, but we have no easy way to
find other idioms that might turn out to be much more frequent. Corpus
linguistics is a reliable way to measure the social salience of language
patterns It should always be used to verify and back empty claims of the
form *X is correct*, *Y is frequent* or *Nobody says Z*.

[<span id="f1">1</span>] Patrick Hanks, [How people use words to make
meanings][].  
[<span id="f2">2</span>] Patrick Hanks, [Lexical Analysis: Norms and
Exploitations][]. The MIT Press (January 25, 2013)  
[<span id="f3">3</span>] Liviu P. Dinu, Florin Manea. [An efficient
approach for the rank aggregation problem][]. In: Theoretical Computer
Science, Volume 359 Issue 1, 14 August 2006. Pages 455 - 461.  
[<span id="f4">4</span>] Liviu P. Dinu, [On the Classification and
Aggregation of Hierarchies with Different Constitutive Elements][].
Fundam. Inform. 55(1): 39-50 (2003)

  [this blog post]: http://voxy.com/blog/index.php/2012/02/top-10-most-common-idioms-in-english/
  [Patrick Hanks]: http://www.patrickhanks.com/
  [1]: #f1
  [2]: #f2
  [British National Corpus]: http://www.natcorp.ox.ac.uk/
  [Oxford English Corpus]: http://oxforddictionaries.com/words/the-oxford-english-corpus
  [3]: #f3
  [4]: #f4
  [How people use words to make meanings]: http://www.patrickhanks.com/uploads/5/1/4/9/5149363/howpeopleusewordstomakemeanings.pdf
  [Lexical Analysis: Norms and Exploitations]: http://www.amazon.com/Lexical-Analysis-Exploitations-Patrick-Hanks/dp/0262018578
  [An efficient approach for the rank aggregation problem]: http://dl.acm.org/citation.cfm?id=1167105
  [On the Classification and Aggregation of Hierarchies with Different
  Constitutive Elements]: http://dl.acm.org/citation.cfm?id=937465
