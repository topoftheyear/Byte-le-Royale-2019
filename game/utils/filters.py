from game.common.enums import ObjectType, LegalStanding


def AND(*args):
    def pred(e):
        return sum(p(e) for p in args) == len(args)
    return pred


def OR(*args):
    def pred(e):
        for p in args:
            if p(e):
                return True
        return False
    return pred


def alive():
    def pred(e):
        return e.is_alive()
    return pred


def pirate():
    def pred(e):
        return e.notoriety >= LegalStanding.pirate
    return pred


def in_radius(source, radius, accessor, target_accessor=None, verify_instance=True):
    """
    Params:
    - source: the source object that you want to search a radius around
    - target: the target object you wish to see if it lies in a radius around the source
    - radius: either an integer, float or accessor function that takes the source and the target and returns an integer or float.
    - accessor: an accessor method used to get the position of the source. If target_accessor == None, this will also be applied to the target.
    - target_accessor: an accessor method used to get the position of the target. Default: None.
    - verify_instance: Verify that source and target do not have the same id.
    """
    def pred(e):
        from game.utils.helpers import in_radius as _in_radius
        return _in_radius(source, e, radius, accessor, target_accessor, verify_instance)

    return pred


def equals(obj):
    def pred(e):
        return obj == e
    return pred


def less_than(obj, accessor=None):
    def pred(e):
        if accessor:
            e = accessor(e)
        return e < obj
    return pred


def greater_than(obj, accessor=None):
    def pred(e):
        if accessor:
            e = accessor(e)
        return e > obj
    return pred

def NOT(outer_pred):
    def pred(e):
        return not outer_pred(e)
    return pred

GT = greater_than
LT = less_than
equal = equals
EQ = equals

