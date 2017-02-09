"""Parse reaction equations"""
#import pkgutil
import re
import copy


class Line(object):
    def __init__(self, raw, num):
        self.raw = raw
        self.num = num
        self.clean = self.clean_line(self.raw)

    def clean_line(self, raw):
        """Remove comments and whitespace"""
        return None

class Section(object):
    """A section of the file e.g. the specifier @reaction and its content"""
    def __init__(self, lines):
        self.head = lines[0]
        self.body = lines[1:]    # No need to worry about index error
                                 # as empty list is returned rather
                                 # than an error if length < 1.
        # The following are just for reaction type sections and should
        # perhaps go somewhere else
        self.name = self.get_name(self.body)
        self.internal = None
        self.edge = None

    def get_name(self, body):
        pattern = re.compile(r'name:(\w)+')
        matches = [re.match(pattern, line.clean) for line in body]
        matches = [(i, m) for i, m in enumerate(matches) if m is not None]
        if not matches:
            return None
        elif len(matches) == 1:
            return matches[0][-1].group(1)
        else:
            conflicting_lines = [self.body[i] for i, m in matches]
            self.handle_multi_def_error(conflicting_lines)

    def handle_multi_def_error(self, lines):
        """Handle the error of repeated fields in a section"""
        msg = "Some message".format()
        raise ParserError(msg)    # Could subclass an error to get ParserError


class Parser(object):

    def __init__(self, path=""):
        self.path = path
        if path:
            self.parse(path)

    def _clean_lines(self, lines):
    """Remove comments and whitespace"""
        lines = [line.split("#")[0] for line in lines]
        lines = ["".join(line.split()) for line in lines if line]
        return lines

    def _raise_parsing_error(self, line, expected):
        line_no = self.clean_lines.index(line)
        raw_line = self.raw_lines[line_no]
        msg = ("Error in line {0}: '{1}'. "
               "Expected {2}. "
               "Examples: '{3}'.")
        msg = msg.format(line_no + 1, raw_line,
                         expected["expected"],
                         "', '".join(expected["examples"]))
        raise SyntaxError("Warning: " + msg)

    def group_data(self, data):
        """Group data into fields with comments and whitespace removed"""
        groups = re.findall(r'@[^@]+', data)
        groups = [re.split(r'\n', group) for group in groups]
        groups = [self._clean_lines(group) for group in groups]
        return groups

    def process_groups(self, groups):
        """Call the relevent function to process each group"""
        PROCESSES = {
            "@init_amounts": self.parse_init_amounts,
            "@array_lvl_params": self.parse_array_lvl_params,
            "@compartement_lvl_params": self.parse_compartment_lvl_params,
            "@reaction": self.parse_reaction
            }
        [PROCESSES[group[0]](group[1:]) for group in groups]

    def parse(self, path):
        with open(path, 'r') as f:
            self.raw_lines = f.readlines()
        self.clean_lines = self._clean_lines(copy.copy(self.raw_lines))
        # Group data into sections (e.g. @reaction, @init_amounts)
        groups = self.group_data("\n".join(self.raw_lines))
        self.process_groups(groups)


    def match_line(self, pattern, line, error_msg):
        try:
            return re.match(pattern, line).groups()
        except AttributeError:
            self._raise_parsing_error(line, error_msg)


    def _parse_amount(self, species, amount):
        try:
            return float(amount)
        except ValueError:
            try:
                assert(amount == "None")
                return None
            except AssertionError:
                msg = ("Warning: amount '{0}' for species '{1}' is not valid. "
                       "Amount should be either a string representation of "
                       "a number or 'None'. Returning None.")
                print(msg.format(amount, species))
                return None

    def parse_init_amounts(self, lines):
        error_msg = {
            "expected": ("'species:amount' where 'species' may contain "
                         "alphanumeric characters and underscores, and "
                         "'amount' must be either 'None' or "
                         "convertable to float."),
            "examples": ["N:None", "S_2:0.33", "H20:1e-5"]
            }
        pattern = re.compile(r'(\w+):([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?|None)')
        matches = [self.match_line(pattern, line, error_msg) for line in lines]
        dct = {}
        dct["species"] = [s for s, a in matches]
        dct["init_amounts"] = {s: self._parse_amount(s, a) for s, a in matches}
        return dct

    def parse_array_lvl_params(self, lines):
        pass

    def parse_compartment_lvl_params(self, lines):
        pass

    def parse_reaction(self, lines):
        pass

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
