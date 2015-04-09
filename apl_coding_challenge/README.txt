PROJECT COMMENTARY:


INPUT LOGFILE CONTENTS:

server1 Bob
server2 Bob
server3 Alice
server4 Nick
server3 Nick
server3 Alice

INPUT LOGFILE COMMENTARY:
Note that Alice is listed at server3 twice, but should only be messaged once.



SCRIPT OUTPUT:

The following servers were found online:
  server2
  server3
  server4
  server5
  server6

Message sent to user 'bob' at server 'server2'.
Message sent to user 'alice' at server 'server3'.
Message sent to user 'nick' at server 'server4'.
Message sent to user 'nick' at server 'server3'.

Adding server 'server5' to output logfile...
Adding server 'server6' to output logfile...

Done.



SCRIPT OUTPUT COMMENTARY:
- server1 is not online, so no messages set there.
- Alice only messaged once



OUTPUT LOGFILE CONTENTS:

server1 bob
server2 bob messaged
server3 alice messaged
server4 nick messaged
server3 nick messaged
server3 alice messaged
server5
server6

OUTPUT LOGFILE COMMENTARY:
- output logfile has 'messaged' appened to each entry that was messaged
- servers 5 & 6 were appended to the end of the output logfile, as they
  were online at runtime, but not in the input logfile.
