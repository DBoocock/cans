"""Parse reaction equations"""
#import pkgutil
import re


class Parser(object):

    _SBML_math_characters = r"\w\(\)"

    def __init__(self, filename):
        with open(filename) as f:
            lines = f.readlines()
        self.model = self.parse(lines)


    def parse(self, lines):
        # Call all the functions (but when to SBML it?)
        lines = self._strip_list(self._remove_comments(lines))


    def _remove_comments(self, lines):
        return [line.split("#")[0] for line in lines]

    def _strip_list(self, lines):
        return [line.strip() for line in lines if line.strip()]

    def get_global_params(self):
        pass

    # Need to call before matching reactions with a regex in
    # get_reactions
    def _remove_whitespace(self, lines):
        return ["".join(line.split()) for line in lines]

    def get_reactions(self, lines):
        irreversible_reg = re.compile(r'(?P<reactants>(?:\w+)*(?:\+\w+)*)[-]+>'
                                      r'(?P<products>(?:\w+)*(?:\+\w+)*):'
                                      r'(?P<rate>.+)')
        # reversible_reg = re.compile(r'(?P<reactants>(?:\w+)*(?:\+\w+)*)<[-]+>'
        #                             r'(?P<products>(?:\w+)*(?:\+\w+)*):'
        #                             r'(?P<rate>.+)')
        matches = [irrerversible.match(line) for line in
                   self._remove_whitespace(lines)]
        [self.set_reaction for match in matches]


    def check_if_reversible_reaction(self):
        pass

    def check_if_irreversible_reaction(self):
        pass

    def set_reaction(self, match):
        pass

    def set_reactants(self):
        # Including stochiometries
        pass

    def set_products(self):
        # including stochiometries
        pass

    def set_rates(self):
        # Rates must be expressed in SBML Level 3 format see the
        # function libsbml.parseL3Formula in the libSBML package
        pass

    def parse_rate_expression(self, rate_expr):
        try:
            assert isinstance(libsbml.parseL3Formula(rate_expr),
                              libsbml.ASTNode)
        except AssertionError:
            raise libsbml.getLastParseL3Error()


    def add_species(self):
        pass
