from game.common.enums import *

def get_material_name(material_type):

    if material_type == MaterialType.iron:
        return "Iron"
    elif material_type == MaterialType.circuitry:
        return "Circuitry"
    elif material_type == MaterialType.computers:
        return "Computers"
    elif material_type == MaterialType.copper:
        return "Copper"
    elif material_type == MaterialType.cuprite:
        return "Cuprite"
    elif material_type == MaterialType.drones:
        return "Drones"
    elif material_type == MaterialType.goethite:
        return "Goethite"
    elif material_type == MaterialType.gold:
        return "Gold"
    elif material_type == MaterialType.machinery:
        return "Machinery"
    elif material_type == MaterialType.pylons:
        return "Pylons"
    elif material_type == MaterialType.steel:
        return "Steel"
    elif material_type == MaterialType.weaponry:
        return "Weaponry"
    elif material_type == MaterialType.wire:
        return "Wire"
    else:
        return f"N/A ({material_type})"



