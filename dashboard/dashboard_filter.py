import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Sales Dashboard with Search and Filters")

# Absolute path for deployment reliability
BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / "data" / "sales.csv"

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv(data_path, parse_dates=["date"])

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

# Region filter
region = st.sidebar.selectbox(
    "Select Region",
    options=["All"] + sorted(df["region"].unique())
)

if region != "All":
    df = df[df["region"] == region]

# Product filter
product = st.sidebar.selectbox(
    "Select Product",
    options=["All"] + sorted(df["product"].unique())
)

if product != "All":
    df = df[df["product"] == product]

# Units sold filter
if not df.empty:

    min_units = int(df["units_sold"].min())
    max_units = int(df["units_sold"].max())

    # Handle edge case where min == max
    if min_units == max_units:

        st.sidebar.info(
            f"Only one units_sold value available: {min_units}"
        )

        units_range = (min_units, max_units)

    else:

        units_range = st.sidebar.slider(
            "Units Sold",
            min_units,
            max_units,
            value=(min_units, max_units)
        )

    # Apply units filter
    df = df[
        (df["units_sold"] >= units_range[0]) &
        (df["units_sold"] <= units_range[1])
    ]

# Search functionality
search_term = st.sidebar.text_input("Search Product Name")

if search_term:
    df = df[
        df["product"].str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

# Display filtered data
st.subheader("Filtered Results")

if not df.empty:
    st.dataframe(df)
else:
    st.warning("No data available for the selected filters.")

# Revenue visualization
st.subheader("Revenue Over Time")

if not df.empty:

    revenue_by_date = (
        df.groupby("date")["revenue"]
        .sum()
        .reset_index()
    )

    st.line_chart(
        revenue_by_date
        .rename(columns={"date": "index"})
        .set_index("index")
    )

else:
    st.info("No chart available because the filtered dataset is empty.")
