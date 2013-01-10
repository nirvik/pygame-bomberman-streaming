Building a simple MULTICAST PYGAME NETWORKING MODULE. 
This has been done purely using sockets.
So far only multicasting and discovering players over lan is complete.
Each player is identified by his UUID.
The users join the game and later  broadcast their uuid and player number so that they get authenticated.

Advantages:
	Since its purely peer to peer there is no need to connect to the server. 
	Multicasting is a new way of broadcasting,therefore a simple module to support small games (say bomberman,snakes).
	Shows all the players connected to the game displayed on the pygame screen.
	
 
Functions to add :
	1.Serialising the events using mesgpack instead of using pickle and marshall.
	2.Use "netifaces" or else More configurations required (like manually entering ip...).	
	3.A function to stream the pygame events ! 	 
	4.have to bind EDsend.py properly.
	
	
