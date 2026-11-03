import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Supply Chain Intelligence", page_icon="📦", layout="wide")
st.markdown("""
<style>
.stApp {background: #f5f7fb;}
[data-testid="stMetric"] {background: white; border: 1px solid #e7ebf2; padding: 16px; border-radius: 12px;}
.block-container {padding-top: 1.6rem;}
h1,h2,h3 {color:#172b4d;}
</style>
""", unsafe_allow_html=True)

st.title("📦 Supply Chain Intelligence Dashboard")
st.caption("A data-driven view of procurement, inventory, supplier performance and delivery reliability.")

@st.cache_data
def load_data():
    path = Path(__file__).parent / "data" / "supply_chain_data.csv"
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df

df = load_data()
with st.sidebar:
    st.header("Dashboard filters")
    min_date, max_date = df.order_date.min().date(), df.order_date.max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    regions = st.multiselect("Region", sorted(df.region.unique()), default=sorted(df.region.unique()))
    categories = st.multiselect("Product category", sorted(df.category.unique()), default=sorted(df.category.unique()))
    if len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = df[(df.order_date >= start) & (df.order_date <= end)]
    else:
        filtered = df.copy()
    filtered = filtered[filtered.region.isin(regions) & filtered.category.isin(categories)]

if filtered.empty:
    st.warning("No records match the selected filters. Please broaden your selection.")
    st.stop()

total_revenue = filtered.revenue.sum()
total_orders = filtered.order_id.nunique()
on_time = (filtered.delivery_status == "On Time").mean() * 100
avg_lead = filtered.lead_time_days.mean()
low_stock = filtered[filtered.inventory_units < filtered.reorder_level].shape[0]

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total revenue", f"₹{total_revenue/1e6:.2f}M")
c2.metric("Orders", f"{total_orders:,}")
c3.metric("On-time delivery", f"{on_time:.1f}%")
c4.metric("Avg. lead time", f"{avg_lead:.1f} days")
c5.metric("Low-stock records", f"{low_stock:,}")

st.divider()
left,right = st.columns((1.55,1))
with left:
    st.subheader("Revenue trend")
    trend = filtered.assign(month=filtered.order_date.dt.to_period("M").dt.to_timestamp()).groupby("month", as_index=False).revenue.sum()
    fig = px.area(trend, x="month", y="revenue", markers=True, color_discrete_sequence=["#2563eb"])
    fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), plot_bgcolor="white", paper_bgcolor="white", yaxis_title="Revenue (₹)", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Orders by delivery status")
    delivery = filtered.delivery_status.value_counts().rename_axis("status").reset_index(name="orders")
    fig = px.pie(delivery, names="status", values="orders", hole=.62, color="status",
                 color_discrete_map={"On Time":"#16a34a","Delayed":"#f59e0b"})
    fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="white", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

left,right = st.columns(2)
with left:
    st.subheader("Revenue by product category")
    cat = filtered.groupby("category", as_index=False).revenue.sum().sort_values("revenue", ascending=True)
    fig = px.bar(cat, x="revenue", y="category", orientation="h", color="revenue", color_continuous_scale="Blues")
    fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), plot_bgcolor="white", paper_bgcolor="white", coloraxis_showscale=False, xaxis_title="Revenue (₹)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Supplier delivery performance")
    sup = filtered.groupby("supplier", as_index=False).agg(orders=("order_id","count"), on_time_pct=("delivery_status", lambda x:(x=="On Time").mean()*100), avg_days=("delivery_days","mean"))
    sup = sup.sort_values("on_time_pct")
    fig = px.bar(sup.tail(12), x="on_time_pct", y="supplier", orientation="h", color="on_time_pct", color_continuous_scale="Teal")
    fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), plot_bgcolor="white", paper_bgcolor="white", coloraxis_showscale=False, xaxis_title="On-time delivery (%)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Inventory risk monitor")
inventory = filtered.copy()
inventory["stock_status"] = inventory.apply(lambda r: "Reorder required" if r.inventory_units < r.reorder_level else "Healthy", axis=1)
risk = inventory.groupby(["category","stock_status"], as_index=False).size()
fig = px.bar(risk, x="category", y="size", color="stock_status", barmode="group",
             color_discrete_map={"Healthy":"#2563eb","Reorder required":"#ef4444"})
fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), plot_bgcolor="white", paper_bgcolor="white", xaxis_title="", yaxis_title="Records")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Operational data explorer")
show_cols = ["order_id","order_date","region","category","supplier","quantity","revenue","lead_time_days","delivery_days","delivery_status","inventory_units","reorder_level"]
st.dataframe(filtered[show_cols].sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered data (CSV)", csv, "filtered_supply_chain_data.csv", "text/csv")

st.caption("Portfolio demo project • Dataset is synthetic and generated for demonstration; it is not real company data.")
