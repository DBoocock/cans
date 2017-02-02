"""Tests for the cans parsing module"""
import os

from unittest import TestCase
from mock import patch, mock_open
from textwrap import dedent

import cans.parser
import cans.parser2

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class TestIrreversibleCompModelParsing(TestCase):

    # A mock data file representation of the irreversible competition
    # model
    IR_COMP_MODEL = dedent("""
        # Reaction equation representation of the qfa competition model

        # The "#" character is reserved for comments (Python style).
        # Species names may contain alpha-numeric and underscore characters only.

        # If specified here (i.e. given numberic values rather than None),
        # initial amounts and array-level parameters cannot be changed in the
        # resulting roadrunner object. If these are to be inferred then leave
        # the values as None.

        # All species must by specified an initial numeric value or None. Using
        # None creates a global parameter for which it is later possible to
        # change the value.
        @init_amounts
        N: None
        C: None

        @array_lvl_params
        k: None

        # The order of listing of compartment level parameters will dictate the
        # order in which they appear in the global parameter list of the SBML model.
        # No values can be set for these parameters.
        @compartment_lvl_params
        b

        @reaction
        name: Growth
        # Does the reaction apply to internal and/or edge cultures
        internal: True
        edge: True
        # Use SBML Level 3 compatible math in rete (e.g. ^ not **)
        C + N -> 2C: b*C*N    # Rate equation follows a colon

        # Diffusion from a compartment to a nearest neighbour
        @reaction
        name: Diffusion
        internal: True
        edge: True
        # Species in a neighbouring compartment have a perceding underscore after a
        # possible stoichiometry (e.g. _N or 2_H20).
        N -> _N: k*N    # -> indicates irreversibility
    """)

    # @patch("__main__.open", mock_open(read_data=IR_COMP_MODEL))
    # def test_open(self):
    #     with open("any_filename", "r") as f:
    #         result = f.read()
    #     open.assert_called_once_with("any_filename", "r")
    #     self.assertEqual(self.IR_COMP_MODEL, result)

    # We want the parser to have the following __dict__ after parsing
    # IR_COMP_MODEL
    DESIRED_ATTRS = {
        "species": ["C", "N"],
        "init_amounts": {
            # Use None to specify that parameters are to become global
            # parameters of the SBML model. This is required if they
            # are to be infered.
            "C": None,
            "N": None,
        },
        "params": {
            "global": {
                "k": None
            },
            "local": ["b"]
        },
        "reactions": [
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
        }


    def setUp(cls):
        MODEL_PATH = THIS_DIR + "/models/irreversible_competition_model.txt"
        cls.parser = cans.parser.Parser(MODEL_PATH)

    # Highest level testing of parsed dict followed by separate tests
    # of individual fields
    # def test_parsing_irreversible_comp_model(cls):
    #     assert(cls.parser.__dict__ == cls.DESIRED_ATTRS)

    # def test_parsing_irreversible_comp_model_species(cls):
    #     assert(cls.parser.species == cls.DESIRED_ATTRS["species"])

    # def test_parsing_irreversible_comp_model_init_amounts(cls):
    #     assert(cls.parser.init_amounts == cls.DESIRED_ATTRS["init_amounts"])

    # def test_parsing_irreversible_comp_model_params(cls):
    #     assert(cls.parser.params == cls.DESIRED_ATTRS["params"])

    # def test_parsing_irreversible_comp_model_reactions(cls):
    #     assert(cls.parser.reactions == cls.DESIRED_ATTRS["reactions"])

class TestLowLevelParsing(TestCase):

    def setUp(self):
        self.parser = cans.parser.Parser()

    def test_group_data(self):
        DATA = dedent("""
            # Some spiel
            @field1
            @field2
            N : None # hello
            @reaction_field
            N + C -> E
            @reaction_field
            A + B -> 2B
        """)
        RESULT = [
            ["@field1"],
            ["@field2", "N:None"],
            ["@reaction_field", "N+C->E"],
            ["@reaction_field", "A+B->2B"]
            ]
        self.assertListEqual(self.parser.group_data(DATA), RESULT)

    def test_parse_init_amounts(self):
        DATA = ["C:None", "N:3e-5", "S_2:0.003"]
        RESULT = {
            "species": ["C", "N", "S_2"],
            "init_amounts": {
                "C": None,
                "N": float(3e-5),
                "S_2": float(0.003)
                }
            }
        self.assertDictEqual(self.parser.parse_init_amounts(DATA), RESULT)

    def test_parse_init_amounts_bad_amounts(self):
        DATA = ["C:NONE", "N:some_chat", "S_2:"]
        RESULT = {
            "species": ["C", "N", "S_2"],
            "init_amounts": {
                "C": None,
                "N": None,
                "S_2": None
                }
            }
        self.assertDictEqual(self.parser.parse_init_amounts(DATA), RESULT)


class TestIrreversibleCompModelParsing2(TestCase):

    # A mock data file representation of the irreversible competition
    # model
    IR_COMP_MODEL = dedent("""
        # Reaction equation representation of the qfa competition model

        # The "#" character is reserved for comments (Python style).
        # Species names may contain alpha-numeric and underscore characters only.

        # If specified here (i.e. given numberic values rather than None),
        # initial amounts and array-level parameters cannot be changed in the
        # resulting roadrunner object. If these are to be inferred then leave
        # the values as None.

        # All species must by specified an initial numeric value or None. Using
        # None creates a global parameter for which it is later possible to
        # change the value.
        @init_amounts
        N: None
        C: None

        @array_lvl_params
        k: None

        # The order of listing of compartment level parameters will dictate the
        # order in which they appear in the global parameter list of the SBML model.
        # No values can be set for these parameters.
        @compartment_lvl_params
        b

        @reaction
        name: Growth
        # Does the reaction apply to internal and/or edge cultures
        internal: True
        edge: True
        # Use SBML Level 3 compatible math in rete (e.g. ^ not **)
        C + N -> 2C: b*C*N    # Rate equation follows a colon

        # Diffusion from a compartment to a nearest neighbour
        @reaction
        name: Diffusion
        internal: True
        edge: True
        # Species in a neighbouring compartment have a perceding underscore after a
        # possible stoichiometry (e.g. _N or 2_H20).
        N -> _N: k*N    # -> indicates irreversibility
    """)

    # @patch("__main__.open", mock_open(read_data=IR_COMP_MODEL))
    # def test_open(self):
    #     with open("any_filename", "r") as f:
    #         result = f.read()
    #     open.assert_called_once_with("any_filename", "r")
    #     self.assertEqual(self.IR_COMP_MODEL, result)

    # We want the parser to have the following __dict__ after parsing
    # IR_COMP_MODEL
    DESIRED_ATTRS = {
        "species": ["C", "N"],
        "init_amounts": {
            # Use None to specify that parameters are to become global
            # parameters of the SBML model. This is required if they
            # are to be infered.
            "C": None,
            "N": None,
        },
        "params": {
            "global": {
                "k": None
            },
            "local": ["b"]
        },
        "reactions": [
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
        }


    def setUp(cls):
        MODEL_PATH = THIS_DIR + "/models/irreversible_competition_model.txt"
        cls.parser = cans.parser2.Parser(MODEL_PATH)

    # Highest level testing of parsed dict followed by separate tests
    # of individual fields
    # def test_parsing_irreversible_comp_model(cls):
    #     assert(cls.parser.__dict__ == cls.DESIRED_ATTRS)

    # def test_parsing_irreversible_comp_model_species(cls):
    #     assert(cls.parser.species == cls.DESIRED_ATTRS["species"])

    # def test_parsing_irreversible_comp_model_init_amounts(cls):
    #     assert(cls.parser.init_amounts == cls.DESIRED_ATTRS["init_amounts"])

    # def test_parsing_irreversible_comp_model_params(cls):
    #     assert(cls.parser.params == cls.DESIRED_ATTRS["params"])

    # def test_parsing_irreversible_comp_model_reactions(cls):
    #     assert(cls.parser.reactions == cls.DESIRED_ATTRS["reactions"])

class TestLowLevelParsing2(TestCase):

    def setUp(self):
        self.parser = cans.parser2.Parser()

    def test_group_data(self):
        DATA = dedent("""
            # Some spiel
            @field1
            @field2
            N : None # hello
            @reaction_field
            N + C -> E
            @reaction_field
            A + B -> 2B
        """)
        RESULT = [
            ["@field1"],
            ["@field2", "N:None"],
            ["@reaction_field", "N+C->E"],
            ["@reaction_field", "A+B->2B"]
            ]
        self.assertListEqual(self.parser.group_data(DATA), RESULT)

    def test_parse_init_amounts(self):
        DATA = ["C:None", "N:3e-5", "S_2:0.003"]
        RESULT = {
            "species": ["C", "N", "S_2"],
            "init_amounts": {
                "C": None,
                "N": float(3e-5),
                "S_2": float(0.003)
                }
            }
        self.assertDictEqual(self.parser.parse_init_amounts(DATA), RESULT)

    def test_parse_bad_init_amount_raises_syntax_error(self):
        BAD_DATA = [
            "C:e-1", "N:with space", "S_2:",    # Bad amounts
            "&%%:1.0", "with space:1.0", ":1.0"    # Bad species
        ]
        self.parser.raw_lines = BAD_DATA
        self.parser.clean_lines = BAD_DATA
        for data in BAD_DATA:
            with self.assertRaises(SyntaxError) as cm:
                self.parser.parse_init_amounts([data])

if __name__ == "__main__":
    import unittest
    unittest.main()
