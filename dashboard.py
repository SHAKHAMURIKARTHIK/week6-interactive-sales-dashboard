from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Interactive Sales Dashboard", page_icon="📊", layout="wide")
st.title("📊 Interactive Sales Dashboard")
st.caption("Explore sales trends, customer activity, product performance and regional results.")

@st.cache_data
def load_data():
    candidates = [Path("sales_data.csv"), Path("data/sales_data.csv"), Path(__file__).parent / "sales_data.csv"]
    for p in candidates:
        if p.exists():
            data = pd.read_csv(p)
            data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
            data = data.dropna(subset=["Date", "Product", "Region", "Total_Sales"])
            data["Month"] = data["Date"].dt.to_period("M").astype(str)
            return data
    raise FileNotFoundError("Place sales_data.csv beside dashboard.py or in the data/ folder.")

try:
    df = load_data()
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

st.sidebar.header("Dashboard filters")
min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
products = st.sidebar.multiselect("Product", sorted(df["Product"].unique()), default=sorted(df["Product"].unique()))
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[filtered["Date"].between(start, end + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))]
filtered = filtered[filtered["Product"].isin(products) & filtered["Region"].isin(regions)]

if filtered.empty:
    st.warning("No records match the selected filters. Adjust the filters to see results.")
    st.stop()

revenue = filtered["Total_Sales"].sum()
orders = len(filtered)
units = filtered["Quantity"].sum()
customers = filtered["Customer_ID"].nunique()
a,b,c,d = st.columns(4)
a.metric("Total revenue", f"{revenue:,.0f}")
b.metric("Transactions", f"{orders:,}")
c.metric("Units sold", f"{units:,}")
d.metric("Unique customers", f"{customers:,}")

monthly = filtered.groupby("Month", as_index=False)["Total_Sales"].sum()
product = filtered.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales", ascending=False)
region = filtered.groupby("Region", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales", ascending=False)

left, right = st.columns(2)
with left:
    st.subheader("Sales trend")
    fig = px.line(monthly, x="Month", y="Total_Sales", markers=True, title="Monthly revenue")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Product performance")
    fig = px.bar(product, x="Product", y="Total_Sales", color="Product", title="Revenue by product")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Regional performance")
    fig = px.pie(region, names="Region", values="Total_Sales", hole=0.45, title="Revenue share by region")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Order value distribution")
    fig = px.violin(filtered, x="Region", y="Total_Sales", color="Region", box=True, points="all",
                    title="Transaction sales distribution by region")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Price distribution")
    fig = px.box(filtered, x="Product", y="Price", color="Product", points="outliers",
                 title="Unit price by product")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Quantity vs sales")
    fig = px.scatter(filtered, x="Quantity", y="Total_Sales", color="Product",
                     size="Price", hover_data=["Date", "Customer_ID", "Region"],
                     title="Transaction-level relationship")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Correlation heatmap")
corr = filtered[["Quantity", "Price", "Total_Sales"]].corr()
heat = go.Figure(data=go.Heatmap(z=corr.values, x=corr.columns, y=corr.index,
                                  zmin=-1, zmax=1, colorscale="RdBu", text=corr.round(2).values,
                                  texttemplate="%{text}"))
st.plotly_chart(heat, use_container_width=True)

st.subheader("Filtered transaction data")
st.dataframe(filtered.sort_values("Date", ascending=False), use_container_width=True)
st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_sales_data.csv", mime="text/csv")
