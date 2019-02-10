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
3. Use `br_launcher.pyz run` to run the client and server. Alternatively you can run them in separate windows by running `br_launcher.pyz server` in one prompt followed by `br_launcher.pyz client` in another.
    - When the client and server are running, watch the 2 prompts for potential output.
4. Once the run has completed, run `br_launcher.pyz visualizer` to watch the match.

Note: You can run `br_launcher.pyz run --game-length 5000` to set the length of the game.

## Visualizer

`br_launcher.pyz visualizer`
Once the client has finished, the visualizer can be run. The visualizer takes the log of the game session
and presents it in a visual format. This is useful for seeing where the AI's weaknesses and strengths are.

## Scrimmage UI

`br_launcher.pyz scrim ui`
This is how to access the Scrimmage Server. A separate terminal will open with the following commands available:
* `announcements`: Displays the recent announcements from the server. This updates automatically.
* `registration`: This will display a form for team registration. If you have already registered your team, you will be warned
that your team is already registered and to send your teammates the registration code you receive. ONLY SEND THIS TO YOUR TEAMMATES
* `leaderboard`: Displays the leaderboard from the server. This also updates automatically.
* `submit`: This is where you submit your client to the server.
* `results`: View the results of submitted clients. While in the results panel, press the backtick key to toggle between the results panel and input prompt,
 and use `up`, `down`, `page_up`, and `page_down` to navigate the results panel.
* `help`: Displays the help page.

When you are finished, press `Control` and `C` to exit the scrimmage UI.

## Related Links

* [Running the Game](running_the_game.html)
