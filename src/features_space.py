# Copyright (C) 2019 Aurore Fass
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
    Building of an (AST-based + variables' name info) features space.
"""

import logging
import numpy as np
from scipy.sparse import csr_matrix

import features_extraction


def features2int(features2int_dict, feature):
    """ Convert a feature into an int (position in the vector space). """

    try:
        i = features2int_dict[feature]
        return i
    except KeyError as err:
        logging.debug('The key %s is not in the dictionary %s', str(feature), str(err))
    return None


def int2features(int2features_dict, i):
    """ Convert an int (position in the vector space) into the corresponding feature. """

    try:
        feature = int2features_dict[i]
        return feature
    except KeyError as err:
        logging.debug('The key %s is not in the dictionary', str(i), str(err))
    return None


def features_vector(input_file, nb_features, features2int_dict):
    """ Builds a vector so that the probability of occurrences of a feature is stored at the
    corresponding position in the vector space. """

    features_dict, total_features = features_extraction.get_features(input_file)
    if features_dict is not None:
        features_vect = np.zeros(nb_features + 1)
        for feature in features_dict:
            map_feature2int = features2int(features2int_dict, feature)
            if map_feature2int is not None:
                features_vect[map_feature2int] = features_dict[feature] / total_features
                # Features appear only once in "features", so done only once per feature
        csr = csr_matrix(features_vect)
        if csr.nnz == 0:  # Empty matrix, no known features
            features_vect[nb_features] = 1  # Because cannot concatenate empty CSR matrices
            csr = csr_matrix(features_vect)
        return csr
    return None
