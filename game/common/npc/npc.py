from game.client.user_client import UserClient

class NPC(UserClient):

    def team_name(self):
        return f"~AI ({self.id})"

    def move(self):

        x = 50
        y = 50
        print(f"Move to ({x}, {y})")

        return (x,y)



