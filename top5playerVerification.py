#file /Users/danlynmedou/Desktop/soccerFootballStats/top5playerVerification.py
import pandas as pd
import numpy as np
from scipy import stats

def load_data(file_path):
    return pd.read_csv(file_path)

def remove_duplicates(data):
    duplicates_removed = data.drop_duplicates()
    return duplicates_removed

def list_missing_values(data):
    missing_values = data.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    return missing_values

def detect_outliers(data):
    numerical_data = data.select_dtypes(include=['float64', 'int64'])
    z_scores = np.abs(stats.zscore(numerical_data))
    outliers = (z_scores > 3).any(axis=1)
    return data[outliers]

def clean_data(file_path):
    data = load_data(file_path)
    
    # Remove duplicates
    data_cleaned = remove_duplicates(data)
    print(f"Duplicates removed: {len(data) - len(data_cleaned)}")

    # List Missing Values
    missing_values = list_missing_values(data_cleaned)
    if not missing_values.empty:
        print("\nMissing values located at:")
        print(missing_values)
    else:
        print("\nNo missing values found.")

    # Detect Outliers
    outliers = detect_outliers(data_cleaned)
    if not outliers.empty:
        print(f"\nOutliers detected in {len(outliers)} rows:")
        print(outliers)
    else:
        print("\nNo outliers detected.")

    return data_cleaned

if __name__ == "__main__":
    file_path = 'top5-players.csv'
    cleaned_data = clean_data(file_path)
    
    # Save cleaned data to a new CSV file
    cleaned_data.to_csv('cleaned_top5-players.csv', index=False)
    print("\nCleaned data saved to 'cleaned_top5-players.csv'")
