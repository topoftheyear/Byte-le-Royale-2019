# Getting Started

## Starting the Launcher

There are 3 components to the launcher:
- Server
- Client
- Visualizer

To initialize each component, run br_launcher.pyz in CMD with the corresponding command
/ argument. Here are the steps for setting up the server:
1. Open a command prompt / PowerShell / terminal in the folder that `br_launcher.pyz` is located in.
2. Run `by_launcher.pyz update` to check if any updates have occurred since last runtime and automatically update.
2. Use `br_launcher.pyz run` to run the client and server.
  - When the client and server are running, watch the 2 prompts for potential output.
3. Once the client has completed, run `br_launcher.pyz visualizer` to watch the match.

## Visualizer
`br_launcher.pyz visualizer`
Once the client has finished, the visualizer can be run. The visualizer takes the log of the game session
and presents it in a visual format. This is useful for seeing where the AI's weaknesses and strengths are.


## Related Links
* [Getting Started](getting_started.md)
* [Writing Your AI](writing_your_ai.md)
* [Using the Visualizer](using_the_visualizer.md)