Building a simple MULTICAST PYGAME NETWORKING MODULE. 
This has been done purely using sockets.
So far only multicasting and discovering players over lan is complete.
Each player is identified by his UUID.
The users join the game and later  broadcast their uuid and player number so that they get authenticated.

The users have to Subscribe to channel in the Multicast.
Players Multicast their uuid along with the channel they want to subscribe.

Advantages:
	Since its purely peer to peer there is no need to connect to the server. 
	Multicasting is a new way of broadcasting,therefore a simple module to support small games (say bomberman,snakes).
	Shows all the players connected to the game displayed on the pygame screen.
	Used mesgpack to serialize data : Faster than marshall and pickle.
 
Disadvantages:
	it hasnt been tested.
	Program stalls when the game finishes.
	Manually enter IP address
	
Functions to add :
	
	1.Use "netifaces" or else More configurations required (like manually entering ip...).	
	
	
