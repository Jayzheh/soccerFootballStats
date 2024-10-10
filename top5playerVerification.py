#file /Users/danlynmedou/Desktop/soccerFootballStats/top5playerVerification.py
import pandas as pd
import numpy as np
from scipy import stats

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_data(file_path):
    data = load_data(file_path)
    
    # Remove duplicates
    data_cleaned = data.drop_duplicates()
    print(f"Duplicates removed: {len(data) - len(data_cleaned)}")

    # Drop unnecessary columns
    columns_to_drop = ['Nation', 'Born', 'npxG']
    data_cleaned = data_cleaned.drop(columns=columns_to_drop)

    # Organize data by position
    data_cleaned = data_cleaned.sort_values('Pos')

    # List Missing Values
    missing_values = data_cleaned.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        print("\nMissing values located at:")
        print(missing_values)
    else:
        print("\nNo missing values found.")

    # Detect and Remove Outliers
    data_cleaned, outliers = remove_outliers(data_cleaned)
    if not outliers.empty:
        print(f"\nOutliers detected and removed in {len(outliers)} rows:")
        print(outliers[['Player', 'Pos', 'Squad']])  # Print only relevant columns
    else:
        print("\nNo outliers detected.")

    return data_cleaned

def remove_outliers(data):
    numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
    z_scores = np.abs(stats.zscore(data[numerical_columns]))
    outliers = (z_scores > 3).any(axis=1)
    return data[~outliers], data[outliers]

if __name__ == "__main__":
    file_path = 'top5-players.csv'
    cleaned_data = clean_data(file_path)
    
    # Save cleaned data to a new CSV file
    cleaned_data.to_csv('cleaned_top5-playerV2.csv', index=False)
    print("\nCleaned data saved to 'cleaned_top5-playerV2.csv'")


