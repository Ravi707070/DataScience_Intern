import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")

# ----------------------- Sidebar Year Selection ----------------------- #
st.sidebar.title("🗂️ Year Selector")
year = st.sidebar.selectbox("Select Sales Year", ["2023", "2024", "2025"])

# File map
file_map = {
    "2023": "Sales_Overview_2023/customer_segments_SALES_2023.csv",
    "2024": "Sales_Overview/customer_segments_output.csv",
    "2025": "Sales_Overview_2025/customer_segments_SALES_2025.csv"
}

# ----------------------- Load Data ----------------------- #
try:
    df = pd.read_csv(file_map[year])
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# ----------------------- Title and Overview ----------------------- #
st.title(f"📊 Customer Segmentation Dashboard - {year}")
st.markdown("Explore customer segments across multiple sales years with filtering, KPIs, and downloads.")

# ----------------------- Metrics ----------------------- #
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(df))
col2.metric("VIP Customers", df[df['Segment'].str.contains("VIP")].shape[0])
col3.metric("Unique Cities", df['City'].nunique())

# ----------------------- Segment Distribution ----------------------- #
st.subheader("📈 Segment Distribution")
segment_counts = df['Segment'].value_counts()
fig1, ax1 = plt.subplots()
segment_counts.plot(kind='bar', color='teal', ax=ax1)
ax1.set_ylabel("No. of Customers")
ax1.set_title("Segment Count")
st.pyplot(fig1)

# Optional Plotly version
fig2 = px.pie(df, names='Segment', title='Customer Segment Pie Chart')
st.plotly_chart(fig2)

# ----------------------- Filter Options ----------------------- #
st.sidebar.subheader("🔍 Filters")
segment_filter = st.sidebar.multiselect("Select Segment", options=df['Segment'].unique(), default=list(df['Segment'].unique()))
city_filter = st.sidebar.multiselect("Select City", options=sorted(df['City'].unique()), default=sorted(df['City'].unique()))

# Apply filters
filtered_df = df[df['Segment'].isin(segment_filter) & df['City'].isin(city_filter)]

# ----------------------- Data Table ----------------------- #
st.subheader("🧾 Filtered Customer Details")
st.dataframe(filtered_df[['CustomerName', 'City', 'Segment']].sort_values(by='Segment'), use_container_width=True)

# ----------------------- Advanced Cluster Summary (Optional) ----------------------- #
if {'Frequency', 'TotalSpend', 'Recency', 'TimeBetweenPurchases'}.issubset(df.columns):
    st.subheader("🧬 Cluster Summary Stats")
    cluster_stats = df.groupby('Segment')[['Frequency', 'TotalSpend', 'Recency', 'TimeBetweenPurchases']].mean().round(2)
    st.dataframe(cluster_stats, use_container_width=True)

# ----------------------- Download Button ----------------------- #
st.subheader("📥 Download Segments")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"filtered_customer_segments_{year}.csv",
    mime='text/csv'
)
