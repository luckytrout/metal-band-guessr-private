from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from geo import resolve_origin

CSV_PATH = Path(__file__).parent.parent / "datasets" / "metal_bands.csv"
if not CSV_PATH.exists():
    raise SystemExit(f"Dataset not found: {CSV_PATH}")

df = pd.read_csv(CSV_PATH, low_memory=False)
# pick candidate columns
candidates = [c for c in ("Country","country","Origin","origin") if c in df.columns]
if not candidates:
    print("No country column found")
    raise SystemExit(1)

vals = set()
for c in candidates:
    vals.update(df[c].dropna().astype(str).str.strip().unique().tolist())

vals = sorted(v for v in vals if v.strip() != "")

resolvable = []
unresolvable = []
for v in vals:
    key, coords = resolve_origin(v)
    if key and coords:
        resolvable.append((v, key, coords))
    else:
        unresolvable.append(v)

print(f"Total unique country/origin values: {len(vals)}")
print(f"Resolvable: {len(resolvable)}")
print(f"Unresolvable: {len(unresolvable)}")

if unresolvable:
    print("\nUnresolvable values:")
    for u in unresolvable:
        print(u)

# Optionally print a few resolved examples
print("\nSample resolved (first 10):")
for r in resolvable[:10]:
    print(r)
