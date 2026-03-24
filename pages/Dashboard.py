import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Textile_sales_data.csv")

df['DATE'] = pd.to_datetime(df['DATE'], format='mixed', dayfirst=True)
df['month'] = df['DATE'].dt.month

st.title("📊 Live Analytics Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

pfco = st.sidebar.multiselect(
    "Select PFco_Code",
    df['PFco_Code'].unique(),
    default=df['PFco_Code'].unique()[:5]
)

month_range = st.sidebar.slider("Select Month", 1, 12, (1, 12))

# Apply filters
filtered = df[
    (df['PFco_Code'].isin(pfco)) &
    (df['month'] >= month_range[0]) &
    (df['month'] <= month_range[1])
]

# KPI
col1, col2, col3 = st.columns(3)

col1.metric("Total Demand", round(filtered['QUANTITIES_Kgs'].sum(),2))
col2.metric("Avg Demand", round(filtered['QUANTITIES_Kgs'].mean(),2))
col3.metric("Max Demand", round(filtered['QUANTITIES_Kgs'].max(),2))

# Charts
col1, col2 = st.columns(2)

with col1:
    st.write("### Monthly Trend")
    monthly = filtered.groupby('month')['QUANTITIES_Kgs'].mean()

    fig, ax = plt.subplots()
    ax.plot(monthly.index, monthly.values, marker='o')
    st.pyplot(fig)

with col2:
    st.write("### Top PFco_Code")
    top = filtered.groupby('PFco_Code')['QUANTITIES_Kgs'].sum().nlargest(5)

    fig2, ax2 = plt.subplots()
    ax2.bar(top.index.astype(str), top.values)
    st.pyplot(fig2)