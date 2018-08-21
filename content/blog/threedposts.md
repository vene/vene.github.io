Title: Rendering 3-d surface plots for social media 
Date: 2018-08-21
Author: vene
Category: presentation 
Slug: rendering-3d-surface-plot-social-media
Status: published
Summary: It's 2018, and your favorite meme pages on facebook constantly come up with quality 3d-post content. How can we mere researchers even begin to compete in terms of social media presence? What chance do we have at going viral? In this post, I show you how to generate 3-d renders of your or your friends' cool machine learning research.

It's 2018, and your favorite meme pages on facebook constantly come up
with quality content like this. (If you're on mobile, you will need to
open the below in the Facebook app for the full immersive experience, sadly.)

<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Ftheytheytheytheythey%2Fposts%2F1927754023930143&width=350&show_text=true&height=471" width="350" height="471" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowTransparency="true" allow="encrypted-media"></iframe>

How can we mere researchers even begin to compete in terms of social media
presence? What chance do we have at going viral? In this post, I show you how
to generate 3-d renders of your or your friends' cool machine learning research.

<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fvlad.niculae%2Fposts%2F2040964392582536&width=350&show_text=true&height=574" width="350" height="574" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowTransparency="true" allow="encrypted-media"></iframe>

Without further ado, let's make some data-driven surface plots.<label for="sn-getcode" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-getcode" class="margin-toggle"/><span class="sidenote">*[Get code for this post.](https://github.com/vene/threedposts)*</span>


# three.js

There seems to be a lot of 3-d modeling software out there, such as
[Blender](https://www.blender.org/), but point-and-click interfaces
don't seem well-suited for data-driven plots.
<label for="sn-blender" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-blender" class="margin-toggle"/><span class="sidenote">Blender does seem to have a Python API,
but I couldn't easily figure out if it supports all we're doing here. If you know, leave a comment!</span>

After a while I settled on [three.js](https://threejs.org/),
a JavaScript library for interactive 3-d graphics. I found
[Graphulus](http://stemkoski.github.io/Three.js/Graphulus-Function.html): a
three.js example that seems close to what we want. 
Also, three.js supports exporting to [GLTF](https://en.wikipedia.org/wiki/GlTF),
the format required to [upload 3-d posts](https://developers.facebook.com/docs/sharing/3d-posts/).

The strategy used by Graphulus uses the three.js
[ParametricGeometry](https://threejs.org/docs/index.html#api/geometries/ParametricGeometry):
a 3-d geometry defined by a function `z = f(x, y)`. This seems to be exactly
what we want! If we can implement `f` easily in JS, we are done! 

In most cases, `f` is complicated and took months to implement, using Python or
C++, so we might not be able (or willing) to rewrite it in JS. I see two
possible paths to take here:

 1. Building a web app, and implementing `f` as an API call.
 2. Finding a way to draw a three.js surface plot from precomputed values.

Five years ago I would have been eager to take approach 1 and build an
overcomplicated solution, but this time I decided 2 is lazier.

I eventually found [this
example](https://bl.ocks.org/grahampullan/b3beb793b10382c13f7a34c843156a8c)
of building a 3-d plot in three.js from a grid of points. In the rest of this
blog, I will walk through the resulting method.

# Computing the function values 

First thing to do is to compute the value of `f` on a grid of points. To keep
things simple, we will plot $\operatorname{softmax}([x, y, 0])_2$
as a function of $a$ and $b$. Recall that
$\operatorname{softmax}(\boldsymbol{\theta}) = \boldsymbol{p}$, where
$p_i = \frac{\exp(\theta_i)}{\sum_j \exp(\theta_j)}$.

We can implement `f(x, y)` easily:

```python
# generate.py

import math

def f(x, y):
    """computes p[1] where p = softmax([x, y, 0])

    (it's p[1], not p[2], because in math we index from 1
    """

    theta = np.array([x, y, 0])
    p = np.exp(theta) / np.sum(np.exp(theta))
    return p[1]
```

Now, let's define a grid of points. This is more or less the same
as for making a [3-d surface plot in
matplotlib](https://matplotlib.org/examples/mplot3d/surface3d_demo.html).

```python
# generate.py (part 2)

import numpy as np

n = 111 
m = 111 

xs = np.linspace(-3, 3, n)
ys = np.linspace(-3, 3, m)

X, Y = np.meshgrid(xs, ys)
Z = np.empty_like(X)

for i in range(n):
    for j in range(m):
        x = X[i, j]
        y = Y[i, j]
        Z[i, j] = f(x, y)

points = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
```

The easiest way to copy data between Python and JS is using json.
Indeed, we can very easily generate a valid JS file:

```python
# generate.py (part 3)
# output points to a javascript file

import json

data = {
    'x': points[:, 0].tolist(),
    'y': points[:, 1].tolist(),
    'z': points[:, 2].tolist()
}

template = f"""\
var n = {n};
var m = {m};
var data = {json.dumps(data)};
"""

with open('data.js', 'w')  as f:
    print(template, file=f)
```

Run this script to obtain a `data.js` file describing the point cloud that we
want to visualize.

# Constructing the 3-d surface

Once we have the 3-d points, it's time to use three.js to construct
the 3-d object. First, download [three.js](https://github.com/mrdoob/three.js/raw/r95/build/three.js) itself, as well the
[GLTFExporter.js](https://raw.githubusercontent.com/mrdoob/three.js/r95/examples/js/exporters/GLTFExporter.js) file.<label for="sn-threejsversion" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-threejsversion" class="margin-toggle"/><span class="sidenote">The links provided are for version r95, the version I
used. Feel free to try newer versions; new features may appear!</span>

Let's make a minimal HTML file to load the required libraries:

```html
<!-- plot-glb.html -->

<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<script src="three.js"></script>
<script src="GLTFExporter.js"></script>
<script src="data.js"></script>  <!-- generated above -->
</head>

<body>
<a id="download">Download .glb</a>
<script src="plot-glb.js"></script> <!-- we'll write this file below -->
</body>
</html>
```

Now it's time to do the heavy lifting in `plot-glb.js`.
First thing we must do is construct a three.js scene. This consists of a
*Mesh*, which in turn is described by a *Material* and a 
*Geometry* (a set of vertices and faces). The *Material* is easy to pick; the
tricky part is the *Geometry*, which we will construct manually.

```js

function makeScene() {
    var geometry = new THREE.Geometry(); 
    var color = new THREE.Color('tomato');
        
    // make a long sequence containing our 3-d points
    var nverts = n * m;
    for (var k = 0; k < nverts; ++k) {
        var newvert = new THREE.Vector3(data.x[k], data.y[k], data.z[k]);
        geometry.vertices.push(newvert);
    }
        

    // build triangular faces (top and bottom) between adjacent points
    for (var j = 0; j < m - 1; j++) {
        for (var i = 0; i < n - 1; i++) { 
            var n0 = j * n + i;
            var n1 = n0 + 1;
            var n2 = (j+1) * n + i + 1;
            var n3 = n2 - 1;
            face1 = new THREE.Face3(n0, n1, n2, undefined, color);
            face2 = new THREE.Face3(n2, n3, n0, undefined, color);
            geometry.faces.push(face1);
            geometry.faces.push(face2);
        }
    }

    // Compute normals for shading
    geometry.computeFaceNormals();
    geometry.computeVertexNormals();
        
    // Give it a pretty material
    var material = new THREE.MeshLambertMaterial( {
        side: THREE.DoubleSide,
        color: 0xffffff,
        vertexColors: THREE.FaceColors,
        emissive: 0x111111,
    });
        
    var scene = new THREE.Scene();
    scene.add( new THREE.Mesh( geometry, material ) );
    return scene;
}
```

Normally, the next step would be to add
[cameras](https://threejs.org/docs/index.html#api/cameras/PerspectiveCamera)
and [lights](https://threejs.org/docs/index.html#api/lights/SpotLight), maybe
some [axes](https://threejs.org/docs/index.html#api/helpers/ArrowHelper) and
descriptive
[text](https://threejs.org/docs/index.html#manual/introduction/Creating-text),
and render to a `<div>`. But our goal is to make a Facebook 3-d post, so we can
simply export the current scene as a binary GLB file. 

The GLTF exporter will give us a byte buffer that we need to download. We can
handle with a function that modifies our link: 

```js
// plot-glb.js (part 2)

function saveArrayBuffer( buffer, filename ) {
    var blob = new Blob( [ buffer ], { type: 'application/octet-stream' } );
    var link = document.getElementById( 'download' );
	link.href = URL.createObjectURL( blob );
	link.download = filename;
}

```

Finally, we use the `GLTFExporter` to generate a Facebook-compatible 3-d model.

```js
// plot-glb.js (part 3)

var scene = makeScene();

var exporter = new THREE.GLTFExporter();
var options = {
	trs: false,
	onlyVisible: false,
	truncateDrawRange: false,
	binary: true,
	forceIndices: true,  // for Facebook
	forcePowerOfTwoTextures: false  // for Facebook
};

exporter.parse( scene, function ( glb ) {
    saveArrayBuffer( glb, 'scene.glb' );
}, options );
```

Now, if you open `plot-glb.html` and click the Download link, you should get a
`.glb` file that can be drag-and-dropped onto a new Facebook post.

# But it shows up seen from above and looks ugly!

Indeed, there seems to be no way to specify the camera angle in a Facebook post.
[Three.js cameras](https://threejs.org/docs/index.html#api/cameras/PerspectiveCamera)
are not part of the *scene*,<label for="sn-scene" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-scene" class="margin-toggle"/><span class="sidenote">Unlike the folks below, who are definitely part of *the scene*:
<a title="By Kirsten Hartsoch [2] ([1]) [CC BY 2.0 (https://creativecommons.org/licenses/by/2.0)], via Wikimedia Commons"
 href="https://commons.wikimedia.org/wiki/File:Scene_kids2.jpg"><img width="256"
 alt="Scene kids2"
 src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Scene_kids2.jpg/256px-Scene_kids2.jpg"></a>
</span>
so I think they don't get exported in a GLTF/GLB.

But now that we know that the default camera is somewhere along the Z axis above
the plot, we can simply rotate our point cloud to get to a more aesthetically
pleasing angle! 

```python

# generate.py (part 2.5)

def rotate3d_x(points, theta):
    c = math.cos(theta)
    s = np.sin(theta)

    R = np.array([[1, 0, 0],
                  [0, c, -s],
                  [0, s, c]])
    return np.dot(points, R)


def rotate3d_z(points, theta):
    c = math.cos(theta)
    s = np.sin(theta)

    R = np.array([[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]])
    return np.dot(points, R)


points = rotate3d_z(points, np.pi / 4)
points = rotate3d_x(points, np.pi / 2.5)
```
Above, we used *rotation matrices* to rotate the point cloud around.<label for="sn-rotation" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-rotation" class="margin-toggle"/><span class="sidenote">Rotating a 3-d point is equivalent to multiplying by a
certain orthogonal matrix. [The wikipedia article](https://en.wikipedia.org/wiki/Rotation_matrix#Basic_rotations) lists formulas for
rotation matrices against the canonical axes $x$, $y$, $z$. </span>

The result should look just like the 3-d post I made below.
Of course, in `generate.py` we can do arbitrary complicated calculations in `f`,
including numerical optimization, so this approach is quite powerful. May it
bring you many likes!

<iframe
src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fvlad.niculae%2Fposts%2F2040960132582962&width=350&show_text=true&height=535"
width="350" height="535" style="border:none;overflow:hidden" scrolling="no"
frameborder="0" allowTransparency="true" allow="encrypted-media"></iframe>

*[Get code for this post.](https://github.com/vene/threedposts)*
