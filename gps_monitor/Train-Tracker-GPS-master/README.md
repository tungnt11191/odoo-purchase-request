Open GPS-tracker
========

![Open GPS-tracker screenshot](http://i.imgur.com/nFvnm0F.png)

Open GPS-tracker is a GPS-tracking-thing written in JavaScript. It is primarily built for tracking running events, but may be modified to track anything.

It utilizes Node.js and WebSockets to communicate between the 'runners', server and viewers. MySQL is used for storage of track data.

##Structure

###Tracking app

mobile_app - the tracking app, to be run on a GPS-enabled device. Sends location data on a set interval to the Node.js-server.

###Server

The server recieves the tracking data, sends it to all connected viewers, then stores the tracking data in the database.

###Viewer

The viewer gets data from the server via WebSockets and plots it on a map (Google Maps API).

##Instructions

What you need: Node.js & Socket.io, MySQL, web server.

###Installation:
- Edit `server/server.js` with your MySQL-details.
- Create database as per `gpstracks.sql`.
- Edit `mobile_app/app.js` with your socket.io-server.
- Edit `mobile_app/index.html` with your socket.io-server.
- Edit `viewer/viewer.html` with your socket.io-server.
- Edit `viewer/viewer.js` with your socket.io-server. Take a look at line 275 for editing custom tile server.

###Tracking:
1.  Start server with `node server.js`.
2.  Send someone for a walk with the mobile_app running.
1.	Browse to `viewer.html` and hopefully you'll see the tracking goodness.