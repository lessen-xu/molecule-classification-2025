import os
import pandas as pd
from src.parser import parse_gxl
from src.ged import compute_ged
from src.classifier import KNNClassifier

def main():
    print("=== Molecule Classification (Exercise 5) ===")
    
    # 1. Setup
    DATA_DIR = 'data/gxl'
    TRAIN_FILE = 'data/train.tsv'
    VAL_FILE = 'data/validation.tsv'
    
    # TODO: Integrate Role A (Load Data)
    # train_graphs = ...
    
    # TODO: Integrate Role D (Train Classifier)
    # clf = KNNClassifier(k=3)
    # clf.fit(...)
    
    # TODO: Validation Loop (Using Role C's GED)
    print("Pipeline not yet implemented.")

if __name__ == "__main__":
    main()