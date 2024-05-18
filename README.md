### Working WebsocketServer

So this works but not perfectly. The webpage is served and a websocket connection is made.

However, there is often a >10s delay on the server side before more messages can be send via the websocket. When the webpage is opened in a browser, I would expect this to cause two connections to be made - one to serve the webpage and then close, and one to connect to and maintain the websocket connection. However, there is an additional connection that is serving the webpage, and I don't know why this connection is happening. The blocking happens on this third connection, and resolves itself on its own after a while.
