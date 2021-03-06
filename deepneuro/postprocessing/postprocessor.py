from deepneuro.utilities.util import add_parameter


class Postprocessor(object):

    def __init__(self, **kwargs):

        # Default Variables
        add_parameter(self, kwargs, 'verbose', False)
        add_parameter(self, kwargs, 'raw_data', None)
        add_parameter(self, kwargs, 'ground_truth', 'ground_truth')

        # Naming Variables
        add_parameter(self, kwargs, 'name', 'Postprocesser')
        add_parameter(self, kwargs, 'postprocessor_string', '_postprocess')

        self.load(kwargs)

    def load(self, kwargs):

        return

    def execute(self, output, raw_data):

        postprocessed_objects = []

        # TODO: Return object syntax is broken / not implemented
        for return_object in output.return_objects:

            if self.verbose:
                print(('Postprocessing with...', self.name))

            # Hacky.
            if self.ground_truth in list(output.data_collection.data_groups.keys()):
                casename = output.data_collection.data_groups[self.ground_truth].base_casename
            else:
                casename = None

            postprocessed_objects += [self.postprocess(return_object, raw_data=raw_data, casename=casename)]

        output.return_objects = postprocessed_objects

    def postprocess(self, input_data, raw_data=None, casename=None):

        return input_data

    def clear_outputs(self):

        return

    def close(self):

        return