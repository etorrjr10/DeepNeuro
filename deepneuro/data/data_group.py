import numpy as np

from deepneuro.utilities.conversion import read_image_files


class DataGroup(object):

    def __init__(self, label):

        """ Inconsistent behavior when reading from HDF5 or filepaths in DataGroups.
        """ 

        self.label = label
        self.augmentations = []
        self.data = {}
        self.cases = []
        self.case_num = 0

        # HDF5 variables
        self.source = None
        self.data_casenames = None
        self.data_affines = None

        # TODO: More distinctive naming for "base" and "current" cases.
        self.preprocessed_case = None
        self.preprocessed_affine = None
        self.base_case = None
        self.base_affine = None

        self.augmentation_cases = [None]
        self.augmentation_strings = ['']
        self.preprocessing_data = []

        self.data_storage = None
        self.casename_storage = None
        self.affine_storage = None

        self.output_shape = None
        self.base_shape = None

    def add_case(self, case_name, item):
        self.data[case_name] = item
        self.cases.append(case_name)

    def get_shape(self):

        # TODO: Add support for non-nifti files.
        # Also this is not good. Perhaps specify shape in input?

        if self.output_shape is None:
            if self.data == {}:
                print('No Data!')
                return (0,)
            elif self.base_shape is None:
                if self.source == 'hdf5':
                    self.base_shape = self.data[0].shape
                else:
                    self.base_shape = read_image_files(list(self.data.values())[0]).shape
                self.output_shape = self.base_shape
            else:
                return None
        
        return self.output_shape

    # @profile
    def get_data(self, index=None, return_affine=False):

        """ Wonky behavior reading from hdf5 here.
        """

        if self.source == 'hdf5':
            if return_affine:
                return self.data[index][:][np.newaxis], self.data_affines[index]
            else:
                return self.data[index][:][np.newaxis]
        else:
            self.preprocessed_case, affine = read_image_files(self.preprocessed_case, return_affine=True)
            if affine is not None:
                self.preprocessed_affine = affine
            if return_affine:
                return self.preprocessed_case, self.preprocessed_affine
            else:
                return self.preprocessed_case

        return None

    def get_affine(self, index):

        if self.source == 'directories':
            if self.preprocessed_affine is None:
                self.preprocessed_case, self.preprocessed_affine = read_image_files(self.preprocessed_case, return_affine=True)
            return self.preprocessed_affine
        # A little unsure of the practical implication of the storage code below.
        elif self.source == 'hdf5':
            if self.data_affines.shape[0] == 0:
                affine = None
            else:
                affine = self.data_affines[index]
            return affine

        return None

    def convert_to_array_data(self):

        self.preprocessed_case, affine = read_image_files(self.preprocessed_case, return_affine=True)

        if affine is not None:
            self.preprocessed_affine = affine

    # @profile
    def write_to_storage(self):

        if len(self.augmentation_cases) == 1:
            self.data_storage.append(self.base_case)
        else:
            self.data_storage.append(self.augmentation_cases[-1])

        self.casename_storage.append(np.array(bytes(self.base_casename, 'utf-8'))[np.newaxis][np.newaxis])

        if self.base_affine is not None:
            self.affine_storage.append(self.base_affine[:][np.newaxis])
