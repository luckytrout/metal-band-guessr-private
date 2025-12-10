# data_loader.py
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent / "datasets" / "metal_bands.csv"
DISCOGRAPHY_PATH = Path(__file__).parent / "datasets" / "all_bands_discography.csv"

def load_metal_bands() -> pd.DataFrame:
    """
    Load the datasets/metal_bands.csv dataset into a pandas DataFrame.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Could not find dataset at: {DATA_PATH} (expected file: datasets/metal_bands.csv)")

    # Try default utf-8 first, fall back to latin-1 if file contains non-UTF-8 bytes
    try:
        df = pd.read_csv(DATA_PATH)
    except UnicodeDecodeError:
        # Some CSVs (especially with special characters) may be latin-1 encoded
        df = pd.read_csv(DATA_PATH, encoding="latin-1")

    return df


def load_discography() -> pd.DataFrame:
    """
    Load the datasets/all_bands_discography.csv dataset into a pandas DataFrame.
    
    Returns a DataFrame with columns: Album Name, Type, Year, Reviews, Band ID
    """
    if not DISCOGRAPHY_PATH.exists():
        raise FileNotFoundError(f"Could not find dataset at: {DISCOGRAPHY_PATH} (expected file: datasets/all_bands_discography.csv)")

    try:
        df = pd.read_csv(DISCOGRAPHY_PATH, low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(DISCOGRAPHY_PATH, encoding="latin-1", low_memory=False)

    return df

if __name__ == "__main__":
    # Quick manual test
    df = load_metal_bands()
    print("Loaded datasets/metal_bands.csv")
    print("Shape:", df.shape)
    print(df.head())
