from game.common.game_serializable import Serializable
from uuid import uuid4

class GameObject(Serializable):

    def __str__(self):
        x = '<{}: {}>'.format(self.__class__.__name__, self.id)
        return x

    def __repr__(self):
        x = '<{}: {}>'.format(self.__class__.__name__, self.id)
        return x

    def init(self, object_type):

        if not issubclass(type(self), GameObject):
            raise Exception("Method must be called from subclass")

        self.object_type = object_type
        self.id = str(uuid4())
        self.inited = True

    def from_dict(self, d):

        if not issubclass(type(self), GameObject):
            raise Exception("Method must be called from subclass")

        self.object_type = d["object_type"]
        self.id = d["id"]
        self.inited = d["inited"]

    def to_dict(self):

        if not issubclass(type(self), GameObject):
            raise Exception("Method must be called from subclass")

        return {
            "object_type": self.object_type,
            "id": self.id,
            "inited": self.inited
        }









