from game.common.game_serializable import Serializable

class GameObject(Serializable):

    def init(self, object_type):

        if not issubclass(self, GameObject):
            raise Exception("Method must be called from subclass")

        self.object_type = object_type

    def from_dict(self, d):

        if not issubclass(self, GameObject):
            raise Exception("Method must be called from subclass")

        self.object_type = d["object_type"]

    def to_dict(self):

        if not issubclass(self, GameObject):
            raise Exception("Method must be called from subclass")

        return { "object_type": self.object_type }









