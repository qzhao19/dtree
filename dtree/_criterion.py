import numpy as np

class Gini(object):
    def __init__(self, 
                 num_outputs, 
                 num_classes, 
                 num_samples, 
                 class_weight):
        self.num_outputs = num_outputs
        self.num_classes = num_classes
        self.num_samples = num_samples
        self.class_weight = class_weight

        self.node_position_threshold = 0

    def compute_node_histogram(self, y, samples, start, end):
        self.node_weighted_histogram = np.zeros((self.num_outputs, self.num_classes))
        self.node_weighted_num_samples = np.zeros((self.num_outputs))
        for o in range(self.num_outputs):
            histogram = {}
            for i in range(start, end):
                histogram[y[samples[i] * self.num_outputs + o]] += 1

            for c in range(self.num_classes):
                weighted_count = self.class_weight[o * self.num_classes + c] * histogram[c]
                self.node_weighted_histogram[o][c] =     weighted_count
                self.node_weighted_num_samples[o] += weighted_count

    
    def _compute_impurity(self, histogram):
        sum_count = 0
        sum_count_squared = 0

        for c in histogram:
            sum_count += histogram[c]
            sum_count_squared += histogram[c] * histogram[c]
        
        impurity = (1.0 - sum_count_squared / (sum_count*sum_count)) if (sum_count > 0.0) else 0.0
        return impurity
    

    def compute_node_impurity(self):
        self.node_impurity = np.zeros(self.num_outputs)
        for o in range(self.num_outputs):
            self.node_impurity[o] = self._compute_impurity(self.node_weighted_histogram[o])
    

    def init_threshold_histogram(self):
        self.node_weighted_histogram_threshold_left = np.zeros((self.num_outputs, self.num_classes))
        self.node_weighted_histogram_threshold_right = np.zeros((self.num_outputs, self.num_classes))

        self.node_weighted_num_samples_threshold_left = np.zeros((self.num_outputs))
        self.node_weighted_num_samples_threshold_right = np.zeros((self.num_outputs))

        for o in range(self.num_outputs):
            for c in range(self.num_classes):
                self.node_weighted_histogram_threshold_left[o][c] = 0
                self.node_weighted_histogram_threshold_right[o][c] = self.node_weighted_histogram[o][c]
            
            self.node_weighted_num_samples_threshold_left[o] = 0
            self.node_weighted_num_samples_threshold_right[o] = self.node_weighted_num_samples[o]

        self.node_position_threshold = 0


    def update_threshold_histograms(self, y, samples, curr_position):
        for o in range(self.num_outputs):
            histogram = np.zeros(self.num_classes)

            # Calculate class histogram for samples[pos:new_pos]
            for i in range(self.node_position_threshold, curr_position):
                histogram[y[samples[i] * self.num_outputs + o]] += 1
            
            weighted_count = 0.0
            for c in range(self.num_classes):
                weighted_count = self.class_weight[o * self.num_classes_max + c] * histogram[c]
                self.node_weighted_histogram[o][c] = weighted_count
                self.node_weighted_n_samples[o] += weighted_count


    def get_node_impurity(self):
        return np.sum(self.node_impurity) / self.num_outputs