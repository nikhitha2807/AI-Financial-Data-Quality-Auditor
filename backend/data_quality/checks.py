import pandas as pd
import numpy as np

def run_quality_checks(df: pd.DataFrame):
    """
    Detect missing values, duplicates, outliers, etc.
    """
    issues = []
    
    # 1. Missing Values
    missing_info = df.isnull().sum()
    for col, count in missing_info.items():
        if count > 0:
            percentage = (count / len(df)) * 100
            issues.append({
                "type": "Missing Values",
                "column": col,
                "count": int(count),
                "severity": "High" if percentage > 20 else "Medium",
                "description": f"{count} missing values ({percentage:.2f}%)"
            })
            
    # 2. Duplicate Records
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append({
            "type": "Duplicate Records",
            "column": "Dataset Level",
            "count": int(duplicates),
            "severity": "Medium",
            "description": f"{duplicates} duplicate rows found"
        })
        
    # 3. Outliers (for numeric columns)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col].count()
        if outliers > 0:
            issues.append({
                "type": "Outliers",
                "column": col,
                "count": int(outliers),
                "severity": "Low",
                "description": f"{outliers} potential outliers detected using IQR method"
            })
            
    # 4. Data Type Consistency
    # (Simplified: check if strings look like numbers but are objects)
    for col in df.select_dtypes(include=['object']).columns:
        try:
            pd.to_numeric(df[col].dropna())
            issues.append({
                "type": "Type Inconsistency",
                "column": col,
                "count": 0,
                "severity": "Low",
                "description": f"Column '{col}' is typed as Object but seems to contain numeric data"
            })
        except:
            pass

    return issues
