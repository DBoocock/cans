# Do not subclass Array or store rows and cols
# Store model type by ename or other id
#
# Store observed data if given. Times are the same for all
# Compartments and should instead be an attribute of Array.
#
# Store dimensions x, y, z or not? More natural to store here but
# Array might summarise it better using fewer variables, e.g., width,
# edge_width, and height.
class Compartment(object):
    def __init__(self):
        pass

    def set_data(self):
        pass
