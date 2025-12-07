import numpy as np

class KNNClassifier:
    def __init__(self, k=3):
        self.k = k
        self.train_graphs = []
        self.train_labels = {}

    def fit(self, graphs, labels_dict):
        """
        Store training data.
        labels_dict: {'molid123': 'active', ...}
        """
        # TODO: Role D Implementation
        pass

    def predict(self, test_graph, distance_function):
        """
        Predict label for a single graph using the distance_function (from Role C).
        """
        # TODO: Role D Implementation
        # 1. Compute distance to all train_graphs
        # 2. Find k nearest neighbors
        # 3. Vote for class (active/inactive)
        return 'inactive'