from pathlib import Path
import pandas as pd

# locate dataset relative to repo root
CSV_PATH = Path(__file__).parent.parent / "datasets" / "metal_bands.csv"

if not CSV_PATH.exists():
    raise SystemExit(f"Dataset not found at: {CSV_PATH}")

# read with low_memory=False to avoid dtype warnings
df = pd.read_csv(CSV_PATH, low_memory=False)

# candidate columns that may contain country/origin
candidates = ["Country", "country", "Origin", "origin"]
cols = [c for c in candidates if c in df.columns]

if not cols:
    print("No country/origin column found. Available columns:\n", ", ".join(df.columns))
else:
    vals = set()
    for c in cols:
        # convert to string, dropna, strip whitespace
        series = df[c].dropna().astype(str).str.strip()
        vals.update(series[series != ""].unique().tolist())

    vals = sorted(vals)
    print(f"Found {len(vals)} unique country/origin values (from columns: {', '.join(cols)}):\n")
    for v in vals:
        print(v)
