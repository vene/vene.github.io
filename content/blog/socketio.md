Title: Flask-SocketIO on OpenShift: fallback on another port
Date: 2015-06-07
Author: vene
Category: flask
Tags: flask-socketio, flask, socketio, openshift
Slug: flask-socketio-openshift-fallback-xhr-polling

## TL; DR

I hacked the [SocketIO client
0.9.16](https://gist.github.com/vene/c0657d854ae74a4511d2) to support
specifying a special port (`wsport`) to use only for the WebSocket protocol,
while keeping all other traffic on the default port. This is required by setups
such as OpenShift which require WebSocket traffic to come over a different port
(say `8000` rather than `80`).

## The current state of affairs

I've been trying to host an interactive web app with WebSockets on
[OpenShift](https://www.openshift.com/). Since I'm a poor student and this
is a research app, I wanted a reasonably powerful free hosting option.

[OpenShift added WebSockets support over 2 years
ago.](https://blog.openshift.com/paas-websockets/) But because of some
internal limitations, the WebSocket traffic needs to go over different ports
than usual (`8000` for unsecured and `8443` for secured connections).

[SocketIO](http://socket.io/) is a cool library that allows event-driven
bidirectional traffic in web apps.  It tries to use WebSockets if available,
and falls back to other transport protocols (such as [XHR Long
Polling](https://en.wikipedia.org/wiki/Push_technology#Long_polling))
otherwise.

Oh and to make matters worse, I'm using Flask for this web app, and currently
the best way to use SocketIO from Flask is with the [Flask-SocketIO](https://flask-socketio.readthedocs.org/en/latest/) +
[gevent-socketio](http://gevent-socketio.readthedocs.org/) combo, which is,
alas, incompatible with recent versions of SocketIO. According to the
community, the most stable release is SocketIO 0.9.16.

## The problem in a nutshell

When debugging my app locally, I'd connect with something like

```
var socket = io.connect(
    'http://' + document.domain + ':' + location.port + '/chat'
);
```

When deploying on OpenShift, the `location.port` is now different from the
WebSocket port, so I used a Flask config that determines server-side where it's
running from:

```
var wsport = '{{ config['WEBSOCKET_PORT'] }}';
```

The app now runs great both when debugging locally or on OpenShift, except if
for some reason the WebSocket connection fails (either if the browser is old
or because of strict firewalls).  This happens because long polling uses normal
HTTP requests and should be done over the default port, rather than the
OpenShift-specific one.

## Making things work

My first thought was to work around it by [manually implementing the fallback
client-side](http://stackoverflow.com/questions/8588689/node-js-socket-io-client-connect-failed-event).  This, surprisingly, failed: it turns out that
SocketIO 0.9.16 first attempts a handshake to find out what transports the
server supports. If the initial connection is on port `8000`, then the
handshake will be attempted also on port `8000`, so the `connect_failed` event
won't even be triggered.  The second cleanest solution I could think of was to
add another parameter to the SocketIO options, `wsport`, allowing the user to
specify a different port over which to do WebSocket connections, while keeping
all other traffic over the default port.  This works like a charm!

[My updated SocketIO client is available as a
gist](https://gist.github.com/vene/c0657d854ae74a4511d2), and the client-side
connection code looks like this:

```
var socket = io.connect(
    'http://' + document.domain + '/chat',
    {
        port: location.port,
        wsport: wsport || location.port,
        "connect timeout": 5000
    }
);
```

I had to reduce the connection timeout, for a better user experience.  I'm way
out of my comfort zone here, so in case I missed a better solution, do let me
know!
