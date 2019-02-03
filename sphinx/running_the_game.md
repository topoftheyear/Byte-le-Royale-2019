# Running The Game

Basic flow of how a game works:
1. A game map is generated.
2. Start a server.
3. Start a client. Your client will connect to the server. 
4. The server then orchestrates the game based on the ```game_data.json``` file and responses from the client. The server also generates a ```game_log/``` directory which contains the game log which is used by the visualizer to visualize the game after it has finished running.
5. Wait for the client and server to finish running.
6. [Run the visualizer](using_the_visualizer.html) to visualize how the game played out.

## Related Links
[Writing Your AI](writing_your_ai.html)