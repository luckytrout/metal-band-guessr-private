"""Quick test runner to verify data_loader and Streamlit import correctly."""
from data_loader import load_metal_bands

def run():
    df = load_metal_bands()
    print("Loaded MetalBands.csv -> shape:", df.shape)
    print(df.head(3).to_string(index=False))

if __name__ == "__main__":
    run()
