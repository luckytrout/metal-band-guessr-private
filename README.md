# Metal Band Guessr — minimal runner

This repo contains a small dataset and a minimal Streamlit app to preview it.

Quick steps to run locally (Windows PowerShell):

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the Streamlit app:

```powershell
streamlit run app.py
```

Alternatively run the quick test to verify `data_loader`:

```powershell
python test_load.py
```

## Data source and credits

This project uses a dataset derived from the Kaggle collection "Every Metal Archives Band" (November 2024) by Henrique Guimarães. The canonical source is:

- "Every Metal Archives Band November 2024" — Henrique Guimarães
- Kaggle dataset: https://www.kaggle.com/datasets/guimacrlh/every-metal-archives-band-october-2024/data

The file included in this repository is `datasets/metal_bands.csv`. Please consult the original Kaggle dataset page for license details, citation preferences, and any restrictions on redistribution.
