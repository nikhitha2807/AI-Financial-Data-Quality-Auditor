import pandas as pd
import numpy as np

def calculate_quality_score(df: pd.DataFrame, issues: list):
    """
    Calculate an overall quality score from 0 to 100.
    """
    # 1. Completeness (Missing values)
    total_cells = df.size
    total_missing = df.isnull().sum().sum()
    completeness_score = ((total_cells - total_missing) / total_cells) * 100 if total_cells > 0 else 100
    
    # 2. Uniqueness (Duplicates)
    total_rows = len(df)
    duplicates = df.duplicated().sum()
    uniqueness_score = ((total_rows - duplicates) / total_rows) * 100 if total_rows > 0 else 100
    
    # 3. Validity & Consistency (Based on issue counts)
    # Penalize based on the number of non-completeness/uniqueness issues
    other_issues_count = len([i for i in issues if i['type'] not in ['Missing Values', 'Duplicate Records']])
    validity_score = max(0, 100 - (other_issues_count * 5)) # Simple penalty
    
    # Overall Weighted Score
    # We can weigh them differently
    weights = {
        "completeness": 0.4,
        "uniqueness": 0.3,
        "validity": 0.3
    }
    
    overall_score = (
        (completeness_score * weights["completeness"]) +
        (uniqueness_score * weights["uniqueness"]) +
        (validity_score * weights["validity"])
    )
    
    return {
        "overall_score": round(float(overall_score), 2),
        "dimensions": {
            "Completeness": round(float(completeness_score), 2),
            "Uniqueness": round(float(uniqueness_score), 2),
            "Validity & Consistency": round(float(validity_score), 2)
        }
    }
