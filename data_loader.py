# data_loader.py
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent / "MetalBands.csv"

def load_metal_bands() -> pd.DataFrame:
    """
    Load the MetalBands.csv dataset into a pandas DataFrame.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Could not find dataset at: {DATA_PATH}")

    # Try default utf-8 first, fall back to latin-1 if file contains non-UTF-8 bytes
    try:
        df = pd.read_csv(DATA_PATH)
    except UnicodeDecodeError:
        # Some CSVs (especially with special characters) may be latin-1 encoded
        df = pd.read_csv(DATA_PATH, encoding="latin-1")

    return df

if __name__ == "__main__":
    # Quick manual test
    df = load_metal_bands()
    print("Loaded MetalBands.csv")
    print("Shape:", df.shape)
    print(df.head())
