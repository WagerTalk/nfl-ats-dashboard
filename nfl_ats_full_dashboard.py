
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NFL Full Filter Dashboard", layout="wide")

# Load CSV from GitHub
csv_url = "https://raw.githubusercontent.com/WagerTalk/nfl-ats-dashboard/main/NFL_Basic.csv"
df = pd.read_csv(csv_url)

# Clean columns
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='ignore')

# Sidebar filter generation
st.sidebar.header("🔍 Filter Games")

# Filter by Team
teams = sorted(set(df["Home Team"].dropna().unique()) | set(df["Away Team"].dropna().unique()))
selected_team = st.sidebar.selectbox("Filter by Team (Home or Away)", ["All"] + teams)
if selected_team != "All":
    df = df[(df["Home Team"] == selected_team) | (df["Away Team"] == selected_team)]

# Filter by Date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
date_range = st.sidebar.date_input("Game Date Range", [df["Date"].min(), df["Date"].max()])
if isinstance(date_range, list) and len(date_range) == 2:
    df = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

# Numeric filter sliders
numeric_fields = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
for col in numeric_fields:
    min_val, max_val = float(df[col].min()), float(df[col].max())
    selected_range = st.sidebar.slider(f"{col}", min_val, max_val, (min_val, max_val))
    df = df[df[col].between(*selected_range)]

# Categorical dropdowns
categorical_fields = [col for col in df.columns if df[col].dtype == 'object' and col not in ["Home Team", "Away Team", "Date"]]
for col in categorical_fields:
    unique_vals = df[col].dropna().unique().tolist()
    if len(unique_vals) <= 50:
        selected = st.sidebar.multiselect(f"{col}", unique_vals, default=unique_vals)
        df = df[df[col].isin(selected)]

# Display results
st.title("🏈 NFL Advanced ATS Dashboard")
st.markdown("Use the filters on the left to narrow down your query. All fields are filterable.")

st.dataframe(df)

# Export
st.download_button("📥 Download Filtered CSV", df.to_csv(index=False), "filtered_nfl_results.csv", "text/csv")
