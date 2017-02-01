"""Parse reaction equations"""
#import pkgutil
import re


class Parser(object):

    def __init__(self, path):
        self.path = path
        self.parse(path)

    def parse(self, path):
        with open(path, 'r') as f:
            data = f.read()
        groups = self.group_data(data)
        self.process_groups(groups)

    def _remove_comments(self, lines):
        return [line.split("#")[0] for line in lines]

    def _remove_whitespace(self, lines):
        return ["".join(line.split()) for line in lines if line]

    def clean_lines(self, lines):
        return self._remove_whitespace(self._remove_comments(lines))

    def group_data(self, data):
        """Group data into fields with comments and whitespace removed

        returns a list of lists
        """
        groups = re.findall(r'@[^@]+', data)
        groups = [re.split(r'\n', group) for group in groups]
        groups = [self.clean_lines(group) for group in groups]
        return groups

    def process_groups(self, groups):
        """Call the relevent function to process each group"""
        PROCESSES = {
            "@init_amounts": self.set_init_amounts,
            "@array_lvl_params": self.set_array_lvl_params,
            "@compartement_lvl_params": self.set_compartment_lvl_params,
            "@reaction": self.set_reaction
            }
        [PROCESSES[group[0]](group[1:]) for group in groups]

    def set_init_amounts(self, lines):
        """Set species and initial amounts"""
        pattern = re.compile(r"(\w+):(NONE|\w+)")

    def set_array_lvl_params(self, lines):
        pass

    def set_compartment_lvl_params(self, lines):
        pass

    def set_reaction(self, lines):
        pass



    # def _strip_list(self, lines):
    #     return [line.strip() for line in lines if line.strip()]

    # def read_lines(self, path):
    #     with open(path, 'r') as f:
    #         lines = f.readlines()
    #     return lines


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
        # Could also test whether fun()'s are builtin SBML. I.e. if
        # we do not want to support custom functions.

    def add_species(self):
        pass
