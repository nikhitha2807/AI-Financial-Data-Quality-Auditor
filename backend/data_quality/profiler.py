import pandas as pd
import numpy as np

def profile_dataset(df: pd.DataFrame):
    """
    Generate basic statistics for the dataset.
    """
    profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "unique_counts": df.nunique().to_dict(),
        "dtypes": df.dtypes.apply(lambda x: str(x)).to_dict(),
        "statistics": df.describe(include='all').replace({np.nan: None}).to_dict()
    }
    return profile
