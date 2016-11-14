class Array(object):
    def __init__(self):
        """Set dimensions and create compartments"""
        # Require a list of compartment types. Arrays may comprise
        # different types of compartment with diffrerent initial
        # collective parameter or reactions.
        #
        # Should edge_width default to zero or one? Do rows and cols
        # include the edge compartments or are these added extra?
        # Should we instead create a subclass?
