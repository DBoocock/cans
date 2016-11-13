class Model(object):
    def __init__(self, filename):
        # May want to generate a parameter list before setting
        # parameters to know order. Just parse the file here.
        pass

    def _parse(self, filename):
        """Parse a model.txt file"""
        pass

    def generate(self, array, params, outfile=""):
        """Generate SBML and the RoadRunner model

        Generate SMBL for array from params with an option to save to
        outfile. From the SBML, create a RoadRunner instance and store
        as an attribute of self.
        """
        pass

    def set_params(self, params):
        """Set RoadRunner parameters values

        self must have a RoadRunner instance.
        """
        self.rr.model.setGlobalParameterValues(params)


    def solve(self, times):
        """Solve the model and return values

        Simulates between timepoints the RoadRunner instance belonging
        to self.
        """
        pass


    def get_param_names(self):
        """Return paramter names in order"""
        pass
