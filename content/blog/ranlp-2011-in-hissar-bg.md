Title: RANLP 2011 in Hissar, BG
Date: 2011-09-20 14:17
Author: vene
Category: conferences
Tags: conferences, nlp
Slug: ranlp-2011-in-hissar-bg

Last week was marked by the international RANLP (Recent Advances in
Natural Language Processing) conference, taking place in a nice spa in
Hissar, Bulgaria. The excellent folks from the [computational
linguistics group][] at the University of Wolverhampton were behind it,
together with the [Institute of Information and Communication
Technologies][] from the Bulgarian Academy of Sciences.  
[caption id="attachment\_247" align="alignleft" width="225" caption="
"][![][]][]

A fountain with warm mineral spring water in Hissarya.   
<small>Picture by [Miranda][]</small>

[/caption]  
I must begin by thanking them: the organization was impeccable! I'm not
sure, but I think that at one point Ivelina was even running around
buying routers to improve wifi coverage (which is already spectacular in
Bulgaria -- I've received reports from [Miranda][] that you can get wifi
in the mountains!)

The schedule was busy, with three tracks going in parallel, in order to
cover a wide range of topics in computational linguistics. The student
workshop should also be noted for the excellent quality of the works
there.

Of course it would be infeasible to write about all the great people I
met and their high quality work. And if I were to write about all the
fun we had, it would probably make this post look unprofessional :).
This doesn't mean I forgot about any of you, and as soon as I get the
chance to work on something related, I will most certainly write about
it, and you.

So, if I would have to summarize the trends and the ideas stated during
the conference and especially during the keynotes, I would say:

-   When talking about word sense disambiguation, it's wrong to speak
    about the different meanings of a word, but rather about the
    potential a word has for bringing a certain meaning in a certain
    context. See [Patrick Hanks][]' [Corpus Pattern Analysis][]. Without
    something like this, to have good WSD you need to heavily adjust the
    overlapping meanings from a Wordnet-style ontology.
-   Certain relations, such as temporal and spacial ones, can naturally
    be modeled by complex domain-specific logics (see [Inderjeet
    Mani][]'s new book, Interpreting Motion: Grounded Representations
    for Spatial Language, that is due for publishing). But these only
    appear in a small subset of human communication. The attempt to map
    human language to a complete logic in which to do general-purpose
    inference seems futile: [Ido Dagan][] suggests textual entailment:
    reasoning directly in natural language, and only abstracting away to
    a formal logic system when need arises.
-   If you have a large enough sample of n-gram frequency data, you can
    eventually beat the performance you can get with a limited amount of
    labeled data, and most importantly: it generalizes much better when
    going out of the domain you trained on. Apparently the best tool for
    this at the moment is the [Google n-gram data][], which has some
    limitations. In time, we can easily extend this data by huge amounts
    by mining n-grams from Wikipedia (which allegedly has a higher count
    of distinct n-grams than the Google dataset), and more importantly,
    by aligning multi-language data, making use of transliterations and
    cognate identification.

Please note that I may be (or most probably, am) ignorant of older
instances of similar ideas, and I may have misunderstood certain claims.
Please feel free to discuss in the comments whether you think I forgot
about something important, or whether I am plain wrong about something.
In particular, I seem to have been completely ignorant of the existence
of the Google n-gram data, which has been around for quite a while, so I
must have missed other important things as well.

Take care, kind readers, and express your opinion!  
V

  [computational linguistics group]: http://clg.wlv.ac.uk/
  [Institute of Information and Communication Technologies]: http://www.iict.bas.bg/EN/index.html
  []: http://localhost:8001/wp-content/uploads/2011/09/319030_10150303323328171_677848170_8151131_1046590975_n1.jpg?w=225
    "Warm spring in Hissar"
  [![][]]: http://localhost:8001/wp-content/uploads/2011/09/319030_10150303323328171_677848170_8151131_1046590975_n1.jpg
  [Miranda]: http://pers-www.wlv.ac.uk/~ex0233/ "Miranda Chong"
  [Patrick Hanks]: http://www.patrickhanks.com/
  [Corpus Pattern Analysis]: http://nlp.fi.muni.cz/projects/cpa/
  [Inderjeet Mani]: http://sites.google.com/site/inderjeetmani/
  [Ido Dagan]: http://u.cs.biu.ac.il/~dagan/
  [Google n-gram data]: http://ngrams.googlelabs.com/datasets
