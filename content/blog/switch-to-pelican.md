Title: Site move
Date: 2014-01-10 12:00
Category: meta
Tags: pelican, blog


I finally got around to moving my entire website, including the blog,
to [Pelican](http://getpelican.com).  I probably would have gotten away with it
too if it weren't for those meddling kids who hacked my friend's server and
convinced me that it's worth the effort to go static.

**It only took 5 hours!** I am more and more convinced that static websites
allow for a better streamlined workflow that does wonders for productivity.

The static part of my old website was made with Jekyll before, so I kept it
almost identical, except for fixing some childish CSS bugs.  The same self-hate
that comes with reading code that you wrote yourself years ago also comes from
markup, apparently.

The blog, however, was migrated thanks to Pelican's Wordpress importer.  This
means that the images are missing, the comments are missing (though I think
they can be imported somehow) and the plugin-specific syntax such as Latex
and source code is poorly rendered.  Luckily the images are there in the
database dump, but I will need to go through the posts one by one to fix
everything.  For now, my priority was to get it up and running and keep as many
of the old links as possible.

Unfortunately [GitHub Pages](http://pages.github.com) doesn't allow URL
rewriting, but I use [CloudFlare](https://cloudflare.com) for DNS and their
free plan gives me the right to use three forwarding rules.  With just 3 rules
I couldn't save all of the old URLs, so I had to prioritize something.  I
decided to rescue the links pointing directly to articles, which needed two
rules, for links with and without trailing slashes, because the CloudFlare
syntax has no way of specifying optional characters.  I used the third wish
that the genie granted me to simply redirect the subdomain
<code>blog.vene.ro</code> to the appropriate subfolder,
<code>vene.ro/blog</code>.

Best part about this is that I will now be able to migrate my [personal list of
papers](/papers.html) to
[pelican-bibtex](https://github.com/vene/pelican-bibtex).
