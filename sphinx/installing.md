# Installing

The installation process has been streamlined from previous years. The application
has the bonuses of update notification, an enclosed runtime environment, and a help
function to assist in starting up the components.

There are 3 components to the launcher:
- Server
- Client
- Visualizer

To initialize each component, run br_launcher.pyz in CMD with the corresponding command
/ argument. Here are the steps for setting up the server:
1. Open 2 command prompts / powershells in the folder that `br_launcher.pyz` is located in.
2. In one command prompt, run `br_launcher.pyz server` to start the server.
3. In the second instance, run `br_launcher.pyz client` to start the client.
4. When the client and server are running, watch the 2 prompts for potential output.
5. Once the client has completed, run `br_launcher.pyz visualizer` to watch the match.

## Server
`br_launcher.pyz server`
The server must be started before the client. The server will wait idle until a client
connects to the server, then runs the instance.

## Client
`br_launcher.pyz client`
The client is what you create. This stores the logic of your specific ship and is run after
the server is initialized. 

## Visualizer
`br_launcher.pyz visualizer`
Once the client has finished, the visualizer runs the log file in a visual format.