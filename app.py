import streamlit as st
from data_loader import load_metal_bands

def main():
    st.set_page_config(page_title="Metal Band Guessr - Data Preview", layout="wide")
    st.title("Metal Band Guessr — Dataset Preview")

    try:
        df = load_metal_bands()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return

    st.markdown(f"**Rows:** {df.shape[0]} — **Columns:** {df.shape[1]}")
    st.dataframe(df.head(100))

    with st.expander("Show raw CSV (first 500 rows)"):
        st.text(df.head(500).to_csv(index=False))

if __name__ == "__main__":
    main()
