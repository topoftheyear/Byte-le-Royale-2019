# Overview

1. Start API Server and mongodb
2. Start runner
3. Start visualizer server
4. Register team with API server
5. team uploads client
6. Ever N minutes, runner pulls the latest submissions and runs them
7. When done running, the runner zips the game_log directory and  scp's it to the visualizer server
8. The runner posts results to the API server
9. The visualizer server polls the API server, listening for the runner to post results. Once results are posted, the 
visualizer unzips the game_logs that have been scp'd to it and begins running the visualizer.
10. visualization ends, visualiser server begins polling API server for results to update.