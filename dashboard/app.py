import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

DATAPATH = "data/canadalens.db"
st.set_page_config(page_title="CanadaLens", layout="wide")
st.title("CanadaLens")
st.caption("Canadian tech job market - powered by Job Bank open data")

# Cache the result so the database isn't queried on every rerender — without this the app queries the DB hundreds of times per minute
@st.cache_data
def load_postings():
    conn = sqlite3.connect(DATAPATH)
    df = pd.read_sql("SELECT * FROM postings", conn)
    conn.close()
    return df

df = load_postings()

# Sidebar filter that lets the user pick a province - All plus the four provinces
provinces = ["All", "Ontario", "British Columbia", "Alberta", "Québec"]
selected = st.sidebar.selectbox("province", provinces)

# "All" is not a real province — passing it to the filter would return zero rows
if selected == "All":
    filtered = df
else:
    filtered = df[df["province"] == selected]


col1, col2, col3, col4 = st.columns(4)
col1.metric("Total postings", len(filtered))
col2.metric("Unique cities", filtered["city"].nunique())
col3.metric("With salary", filtered[filtered["has_salary"] == 1].shape[0])
col4.metric("Fast expiring", filtered[filtered["expired_fast"] == 1].shape[0])


top_cities = filtered["city"].value_counts().head(10)

fig1, ax1 = plt.subplots(figsize=(10, 5))
# Reverse the order of top_cities to show the highest bar at the top
ax1.barh(top_cities.index[::-1], top_cities.values[::-1])
ax1.set_xlabel("Number of Postings")
ax1.set_title("Top 10 cities by posting count")
st.pyplot(fig1)

# Filter to show only jobs that have a salary
salary_df = filtered[filtered["has_salary"] == 1]
average_salary = salary_df.groupby("province")["salary_maximum"].mean().round(2)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.barh(average_salary.index, average_salary.values)
ax2.set_xlabel("Average salary Maximum")
ax2.set_title("Average Salary by Province only")
st.pyplot(fig2)

st.divider()

st.dataframe(filtered)

