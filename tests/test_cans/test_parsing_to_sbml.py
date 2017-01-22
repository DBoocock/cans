# from cans import model
from cans import parser


# This is to be the result of parsing from the file. This should
# probably be a Parser rather than Model object. This is only the
# information, other than the size of the array, required to create an
# SBML model. Instead, Model can contain the rr object and only any
# other information it might need for solving (e.g. b_index).
class ExampleParser(parser.Parser):

    def __init__(self):
        self.species = ["C", "N"]
        self.init_amounts = {
            # Use None to specify that parameters are to become global
            # parameters of the SBML model. This is required if they
            # are to be infered.
            "C": None,
            "N": None,
            }
        self.params = {
            "global": {
                "k": None
                }
            "local": ["b"]
            }
        self.reactions = [
            {
                "name": "Growth_{0}",
                "rate": "b{0} * C{0} * N{0}",
                "reactants": [(1, "N{0}"), (1, "C{0}")],
                "products": [(2, "C{0}")],
                "reversible": False,
                "x_compartment": False,
                # Does reaction apply to internal and/or edge
                # compartments?
                "internals": True,
                "edges": True,
            },
            {
                "name": "Diff_{0}_{1}",
                "rate": "kn * N{0}",
                "reactants": [(1, "N{0}")],
                "products": [(1, "N{1}")],
                "reversible": False,
                "neighs": True,
                "internals": True,
                "edges": True,
            }
        ]
