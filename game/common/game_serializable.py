from uuid import uuid4

class Serializable:


    def __repr__(self):
        return "<{0}.{1} at {2}>".format(
                self.__class__.__module__,
                self.__class__.__name__,
                hex(id(self)) )


    __str__ = __repr__

    def init(self):
        """Manually initialize object"""
        raise Exception("{0} missing implementation of init()".format(self.__class__.__name__))

    def from_dict(self, d):
        """ Load object data from dict that has been deserialized from json """
        raise Exception("{0} missing implementation of from_dict()".format(self.__class__.__name__))


    def to_dict(self):
        """ Dump object data to a dict to prepare it for json serialization. """
        raise Exception("{0} missing implementation of to_dict()".format(self.__class__.__name__))

