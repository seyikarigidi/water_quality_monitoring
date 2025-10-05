import pandas as pd


def clean_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()


    # Fix sensor_id format
    df['sensor_id'] = df['sensor_id'].astype(str).str.upper().str.replace(r'[^0-9]', '', regex=True)
    df['sensor_id'] = df['sensor_id'].apply(lambda x: f"SENSOR_{int(x):03d}" if x.isdigit() else None)


    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')


    # Convert numeric columns safely
    for col in ['ph', 'turbidity', 'dissolved_oxygen', 'temperature']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')


    # Handle invalid values
    df.loc[(df["ph"] < 0) | (df["ph"] > 14), "ph"] = None
    df.loc[(df["turbidity"] < 0) | (df["turbidity"] > 50), "turbidity"] = None
    df.loc[(df["dissolved_oxygen"] < 0) | (df["dissolved_oxygen"] > 20), "dissolved_oxygen"] = None
    df.loc[(df["temperature"] < 0) | (df["temperature"] > 100), "temperature"] = None




    df = df.dropna()


    # Remove duplicate sensor-timestamp pairs
    df = df.drop_duplicates(subset=['sensor_id', 'timestamp'])


    # Reset index
    df.reset_index(drop=True, inplace=True)


    return df