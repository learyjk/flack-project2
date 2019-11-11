# Project 2 - FLACK

Web Programming with Python and JavaScript

Project Spec:
https://docs.cs50.net/ocw/web/projects/2/project2.html

YouTube project demo:
https://youtu.be/OqApYS_mo7o

Flack is a chat app for cs50 Web Dev class with objectives to improve my abilities with JavaScript, web UI, and Socket.IO.  This repository hosts my code to accomplish this app.

Some issues that I experienced while working on this program:

1. cs50 Project spec says to run the program using 'flask run', but that throws a warning.  Some googling later and the creator of flask_socketio (Miguel) gives some pretty good instructions on using gevent or eventlet and running via 'python3 application.py'.
2. Even with Bootstrap, UIs are hard and time-consuming.  I definitely found myself spending 30-45 minutes figuring out how to get a div on the right side of the page or whatever.
3. Still cannot get automatic scroll to work.  I spent a lot of time on this and foind some good code on Stack Overflow, but I still couldn't figure it out.  When I inspect my '#message_box' div that I want to scroll on, its scrollHeight property is null (as is scrollTop).  This occurs even when I actively am scrolling that div, and when i try to access different divs.  I'm giving up on this one for now, but I left the code in index.html just because.
4. websockets was incredibly mystifying at first.  It wasn't until I went through a number of tutorials that it started to make sense.  Mixing sockets with flask routes was incredibly confusing at first.  Thanks to the tutorial authors below for their incredible write-ups and/or instructional videos.  My code matured through time, but I didn't bother to go back and update 'old' code.  As a result, some of the websocket events may appear a bit different.  Some tutorials seem to publish events and callbacks for each action, but I settled on passing most of the events to 'message_update'.  I think Sandeep Sudhakaran does a great job of implementing the send() function, which is not discussed in cs50 lecture.  I wish I had found his videos sooner!


Helpful Tutorials I couldn't have survived without:
1. flack-socketio documentation: https://flask-socketio.readthedocs.io/en/latest/
2. Sandeep Sudhakaran: https://www.youtube.com/watch?v=zQDzNNt6xd4
3. nobaa36: https://github.com/nobaa36/CS50-s-Web---project-2-Flack
4. Pretty Printed: https://www.youtube.com/watch?v=mX7hPZidPPY


Issues to fix / Program Quirks:

1. Auto scroll to bottom of #message_box div.
2. joinRoom() is a bit too verbose when I open multiple local chat boxes to test.  In deployed environment this wouldn't really occur assuming 1 user on 1 client.
3. My personal touch was to implement private messaging.  I didn't really build my interface with this in mine, so I settled on printing the allowed_users[] list to the left column and using the names as 'clickable' send buttons.  The private message appears as a javascript alert to the recipient.  Again, not a great UI, but I was focused more on function over form for this feature.
4. Login is ugly.
5. There are currently only 3 users allowed: Keegan, foo, and bar.  Again - functionality over form here.
