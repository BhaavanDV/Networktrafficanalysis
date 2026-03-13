import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Demo dataset loader
def load_demo_dataset():
    # Create a demo dataset
    demo_rows = 10
    feature_count = 70
    df = pd.DataFrame(np.random.rand(demo_rows, feature_count),
                      columns=[f"f{i}" for i in range(feature_count)])
    # Inject some attacks
    df.iloc[0, 0] = 9999
    df.iloc[3, 5] = 8888
    df.iloc[7, 2] = 7777
    df['label'] = ['Attack' if i in [0,3,7] else 'Normal' for i in range(demo_rows)]
    logger.info("Demo dataset loaded successfully.")
    return df

# Dummy prediction function
def predict_attack(row):
    return "Attack" if row.max() > 100 else "Normal"