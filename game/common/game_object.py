from game.common.game_serializable import Serializable
from uuid import uuid4

class GameObject(Serializable):

    def init(self, object_type):

        if not issubclass(self, GameObject):
            raise Exception("Method must be called from subclass")

        self.object_type = object_type
        self.id = str(uuid4())

    def from_dict(self, d):

        if not issubclass(self, GameObject):
            raise Exception("Method must be called from subclass")

        self.object_type = d["object_type"]
        self.id = d["id"]

    def to_dict(self):

        if not issubclass(self, GameObject):
            raise Exception("Method must be called from subclass")

        return { "object_type": self.object_type, "id": self.id }









