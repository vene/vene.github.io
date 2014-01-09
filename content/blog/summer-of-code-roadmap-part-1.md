Title: Summer of Code roadmap, part 1
Date: 2011-06-12 14:28
Author: vene
Category: Uncategorized
Slug: summer-of-code-roadmap-part-1

After a little busy while, I have graduated and entered the summer
vacation, which means time for serious GSoC work.

[![Me on graduation day][]][]

So we had a little conference in order to discuss what will be done and
when. We gathered quite a few code snippets since the official start of
the project, but it's now time to talk about integration and pull
requests.

Here is the plan:

#### SparsePCA

First pull request due: **June 15**  
This will be the use case I blogged about [before][]. Specifically, we
want to learn a dictionary of sparse atoms, but representations of the
data will be dense.

#### SparseCoder

First pull request due: **June 25**  
This is the transpose of the SparsePCA problem. We are learning the
optimal, dense dictionary for sparse representations of the data.

#### KMeansCoder

First pull request due: **June 30**  
This method builds the dictionary out of cluster centers found by
K-means.

#### OnlineSparseCoder

First pull request due: **July 10**  
This will involve the online learning tricks suggested in Julien
Mairal's work and will allow for faster computations of both sparse PCA
and sparse coding. In the case of sparse coding, it will make use of the
scikits.learn API for online learning.

While I will try to keep the deadlines for the initial pull requests as
strictly as I can, we did not establish deadlines for merging, since
this will depend on more factors. As long as the pull requests are up,
the code review system will push it forward towards the merge. The focus
is on teamwork and on feedback cycles as short as possible, as opposed
to falling into the trap of delaying work until the night before the
deadline.

  [Me on graduation day]: http://localhost:8001/wp-content/uploads/2011/06/p1080283.jpg
    "Graduation day"
  [![Me on graduation day][]]: http://localhost:8001/wp-content/uploads/2011/06/p1080283.jpg
  [before]: http://venefrombucharest.wordpress.com/2011/05/23/sparse-pca/
    "Sparse PCA"
