import copy
import numpy as np

from ._utils import sort

PRECISION = 1e-7

class FeatureSplitter(object):
    def __init__(self, 
                 criterion, 
                 num_samples, 
                 num_features, 
                 num_outputs, 
                 num_classes,
                 max_num_features,
                 max_num_thresholds, 
                 class_weight):
        
        self.criterion = criterion
        self.num_samples = num_samples
        self.num_features = num_features
        self.num_outputs = num_outputs
        self.num_classes = num_classes
        self.max_num_features = max_num_features
        self.max_num_thresholds = max_num_thresholds
        self.class_weight = class_weight

        self.samples = np.zeros((num_samples))

    # Initialize node and calculate weighted histograms for all outputs and impurity for the node.
    def init_node(self, y, start, end):
        self.start = start
        self.end = end

        self.criterion._compute_node_histogram(y, self.samples, self.start, self.end)
        self.criterion._compute_node_impurity()


    def _best_split_feature(self, 
                           X, y, 
                           samples, 
                           feature_indice,  
                           threshold, 
                           partition_indice, 
                           improvement, 
                           missing_value):
        
        # y is not constant (impurity > 0)
        # has been checked by impurity stop criteria in build()
        # moving on we can assume at least 2 samples

        # Copy f_X=X[samples[start:end],f] training data X for the current node.
        num_samples = self.end - self.start
        f_x = np.zeros(num_samples)
        for i in range(num_samples):
            f_x[i] = X[samples[i] * self.num_features + feature_indice]

        # Detect samples with missing values and 
        # move them to the beginning of the samples vector
        missing_value_indice = 0
        for i in range(num_samples):
            if np.isnan(f_x[i]):
                f_x[i], f_x[missing_value_indice] = f_x[missing_value_indice], f_x[i]
                samples[i], samples[missing_value_indice] = f_x[missing_value_indice], f_x[i]
                missing_value_indice += 1
        
        # Can not split feature when all values are NA
        if missing_value_indice == num_samples:
            return 
        
        if missing_value_indice > 0:
            print("NO IMPLEMENTATION")

        # Split based on threshold
        f_max = f_min = f_x[0]
        for i in range(missing_value_indice+1, num_samples):
            if f_x[i] > f_max:
                f_max = f_x[i]
            elif f_x[i] < f_min:
                f_min = f_x[i]
        

        if f_min + PRECISION < f_max:

            if missing_value_indice == 0:
                self.criterion._init_threshold_histogram()
            elif missing_value_indice > 0:
                print("NO IMPLEMENTATION")
            
            # Loop: all thresholds
            f_x, samples = sort(f_x, samples, missing_value_indice, num_samples)

            # Find threshold with maximum impurity improvement
            
            
