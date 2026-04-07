import os
import sys
import pandas as pd
import pytest
from backend.data_quality.profiler import profile_dataset
from backend.data_quality.checks import run_quality_checks
from backend.data_quality.scoring import calculate_quality_score

def test_profiling():
    data = {
        'A': [1, 2, None],
        'B': ['cat', 'dog', 'cat']
    }
    df = pd.DataFrame(data)
    profile = profile_dataset(df)
    assert profile['row_count'] == 3
    assert profile['column_count'] == 2
    assert profile['missing_values']['A'] == 1

def test_quality_checks():
    data = {
        'A': [1, 2, 1], # Duplicate row possible context
        'B': [10, 20, 1000] # 1000 is an outlier? Maybe not in 3 rows, but let's check structure
    }
    df = pd.DataFrame(data)
    issues = run_quality_checks(df)
    # Check if duplicate is found
    has_duplicates = any(i['type'] == 'Duplicate Records' for i in issues)
    # In run_quality_checks, df.duplicated().sum() is used
    # [1, 10], [2, 20], [1, 1000] -> No full row duplicates.
    
    df_with_dup = pd.concat([df, df.iloc[[0]]])
    issues_with_dup = run_quality_checks(df_with_dup)
    assert any(i['type'] == 'Duplicate Records' for i in issues_with_dup)

def test_scoring():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    issues = []
    score = calculate_quality_score(df, issues)
    assert score['overall_score'] == 100.0
