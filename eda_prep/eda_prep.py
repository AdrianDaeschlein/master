import pandas as pd
import os


def merge_geophone_falls(folder_path):
    """
    Merges all 'fall' data from CSV files in the given geophone folder.

    Parameters:
    - folder_path (str): Path to the geophone folder containing CSV files.

    Returns:
    - pd.DataFrame: Merged DataFrame with labeled columns.
    """
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            parts = filename.split("_")

            if len(parts) < 5:
                print(f"Skipping file with unexpected format: {filename}")
                continue  # Skip files that don't match expected format

            fall_type = parts[0]  # First part of the filename
            fall_binary = parts[1]  # Check for fall keyword
            distance = parts[2]  # Third part of the filename
            person = parts[3]  # AW, AD, or 0
            # Last part without ".csv"
            floor_type = parts[-1].replace(".csv", "")

            # Load CSV
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path, header=None)

            # Take only the first 500 values
            # values = df.iloc[0, :500].tolist() if df.shape[1] >= 500 else df.iloc[0, :].tolist() + [None] * (500 - df.shape[1])
            for _, row in df.iterrows():
                # Ensure only 500 values are added
                values = row[:500].tolist() if len(
                    row) >= 500 else row.tolist() + [None] * (500 - len(row))
                all_data.append(
                    [fall_type, fall_binary, distance, person, floor_type] + values)

    # Create DataFrame
    column_names = ["activity", "fall_binary", "distance_m",
                    "person_binary", "floor"] + [f"value_{i}" for i in range(1, 501)]
    merged_df = pd.DataFrame(all_data, columns=column_names)

    return merged_df


def get_features(df: pd.DataFrame, groupby_col: str = 'activity'):
    """
    Extracts features from the given DataFrame.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - groupby_col (str): Column to group by.

    Returns:
    - pd.DataFrame: DataFrame with extracted features.
    """
    return_df = pd.DataFrame()
    # Extract features
    return_df["mean"] = df.iloc[:, 6:].mean(axis=1)
    return_df["std"] = df.iloc[:, 6:].std(axis=1)
    return_df["min"] = df.iloc[:, 6:].min(axis=1)
    return_df["max"] = df.iloc[:, 6:].max(axis=1)
    return_df["median"] = df.iloc[:, 6:].median(axis=1)
    return_df["range"] = return_df["max"] - return_df["min"]

    return return_df
