import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Fashion Retail Analytics",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {padding: 0rem 1rem;}
    .metric-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        text-align: center;
    }
    .metric-label {font-size: 14px; color: #aaa;}
    .metric-value {font-size: 24px; color: white; font-weight: bold;}
    h1 {color: #1f77b4;}
    h2 {color: #2ca02c;}
    h3 {color: #ff7f0e;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base = Path(__file__).resolve().parent
    data_dir = base / "data"
    if not data_dir.exists():
        st.error("Data folder not found.")
        st.stop()

    customers = pd.read_csv(data_dir / "customers_clean.csv", low_memory=False)
    transactions = pd.read_csv(data_dir / "transactions_clean.csv")
    products = pd.read_csv(data_dir / "products_clean.csv")

    try:
        churn = pd.read_csv(data_dir / "HIGH_RISK_CUSTOMERS.csv")
        customers = customers.merge(churn[['Customer_ID', 'total_spent', 'days_as_customer', 'churn_probability']], 
                                    on='Customer_ID', how='left')
    except:
        pass

    transactions['Date'] = pd.to_datetime(transactions['Date'], errors='coerce')
    transactions['Line_Total'] = pd.to_numeric(transactions['Line_Total'], errors='coerce')
    transactions['is_return'] = (transactions['Line_Total'] < 0).astype(int)

    return customers, transactions, products

customers, transactions, products = load_data()

# Sidebar
st.sidebar.title("🎛️ Controls")
page = st.sidebar.radio("View", ["📊 Business Overview", "🎯 Churn Analysis", "🔍 Customer Deep Dive"])

countries = ['All'] + sorted(customers['Country'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Country", countries)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(transactions['Date'].min().date(), transactions['Date'].max().date())
)

# Filtering
filtered_trans = transactions[
    (transactions['Date'] >= pd.Timestamp(date_range[0])) &
    (transactions['Date'] <= pd.Timestamp(date_range[1]))
].copy()

filtered_cust = customers.copy()
if selected_country != 'All':
    filtered_cust = filtered_cust[filtered_cust['Country'] == selected_country]
    filtered_trans = filtered_trans[filtered_trans['Customer_ID'].isin(filtered_cust['Customer_ID'])]

# Business Overview (same as before)
if page == "📊 Business Overview":
    st.title("📊 Business Intelligence")

    gross = filtered_trans[filtered_trans['is_return'] == 0]['Line_Total'].sum()
    returns = abs(filtered_trans[filtered_trans['is_return'] == 1]['Line_Total'].sum())
    net = filtered_trans['Line_Total'].sum()
    customers_n = filtered_trans['Customer_ID'].nunique()
    orders_n = filtered_trans.get('Invoice_ID', pd.Series()).nunique()
    return_rate = (returns / gross * 100) if gross > 0 else 0
    aov = gross / orders_n if orders_n > 0 else 0

    cols = st.columns(5)
    metrics = [
        ("Net Revenue", f"${net/1e6:.1f}M"),
        ("Customers", f"{customers_n:,}"),
        ("Orders", f"{orders_n:,}"),
        ("Return Rate", f"{return_rate:.1f}%"),
        ("Avg Order Value", f"${aov:.0f}")
    ]
    for col, (label, value) in zip(cols, metrics):
        col.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Category")
        if 'Product_ID' in filtered_trans.columns and 'Category' in products.columns:
            cat_rev = filtered_trans.merge(products[['Product_ID', 'Category']], on='Product_ID')
            cat_rev = cat_rev.groupby('Category')['Line_Total'].sum().reset_index()
            fig = px.pie(cat_rev, values='Line_Total', names='Category', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Category data not available")

    with col2:
        st.subheader("Return Rate by Country")
        if 'Country' in filtered_cust.columns:
            trans_c = filtered_trans.merge(filtered_cust[['Customer_ID', 'Country']], on='Customer_ID')
            country_stats = trans_c.groupby('Country').agg(
                gross=('Line_Total', lambda x: x[x>0].sum()),
                returns=('Line_Total', lambda x: abs(x[x<0].sum()))
            )
            country_stats['return_rate'] = (country_stats['returns'] / country_stats['gross'] * 100).round(1)
            top = country_stats.sort_values('return_rate', ascending=False).head(10).reset_index()
            fig = px.bar(top, x='Country', y='return_rate', color='return_rate', color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Monthly Revenue Trend")
    monthly = filtered_trans.copy()
    monthly['Month'] = monthly['Date'].dt.to_period('M').dt.to_timestamp()
    monthly_rev = monthly.groupby('Month')['Line_Total'].sum().reset_index()
    fig = go.Figure(go.Scatter(x=monthly_rev['Month'], y=monthly_rev['Line_Total'], mode='lines+markers', fill='tozeroy', line_color='#1f77b4'))
    st.plotly_chart(fig, use_container_width=True)

# Churn Analysis (same as before)
elif page == "🎯 Churn Analysis":
    st.title("🎯 Churn Risk Analysis")

    if 'churn_probability' not in filtered_cust.columns:
        st.warning("Churn predictions not loaded.")
        st.stop()

    filtered_cust['risk_tier'] = pd.cut(filtered_cust['churn_probability'], bins=[0,0.4,0.7,1], labels=['Low Risk','Medium Risk','High Risk'])
    high = filtered_cust[filtered_cust['risk_tier'] == 'High Risk']
    med = filtered_cust[filtered_cust['risk_tier'] == 'Medium Risk']
    low = filtered_cust[filtered_cust['risk_tier'] == 'Low Risk']

    rev_at_risk = high['total_spent'].sum() / 1e6 if 'total_spent' in high.columns else 0

    cols = st.columns(4)
    cols[0].markdown(f"<div class='metric-card'><div class='metric-label'>High Risk</div><div class='metric-value'>{len(high):,}</div></div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div class='metric-card'><div class='metric-label'>Revenue at Risk</div><div class='metric-value'>${rev_at_risk:.1f}M</div></div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div class='metric-card'><div class='metric-label'>Medium Risk</div><div class='metric-value'>{len(med):,}</div></div>", unsafe_allow_html=True)
    cols[3].markdown(f"<div class='metric-card'><div class='metric-label'>Low Risk</div><div class='metric-value'>{len(low):,}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(values=[len(high), len(med), len(low)], names=['High','Medium','Low'], hole=0.4,
                     color_discrete_map={'High':'#e74c3c','Medium':'#f39c12','Low':'#2ecc71'})
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.histogram(filtered_cust, x='churn_probability', nbins=50)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Top 20 High-Risk Customers")
    display = high.nlargest(20, 'total_spent' if 'total_spent' in high.columns else 'churn_probability')
    cols_show = ['Customer_ID', 'churn_probability', 'days_as_customer']
    if 'total_spent' in display.columns:
        cols_show.insert(1, 'total_spent')
    display = display[cols_show].copy()
    display['churn_probability'] = (display['churn_probability'] * 100).round(1).astype(str) + "%"
    if 'total_spent' in display.columns:
        display['total_spent'] = display['total_spent'].map("${:,.0f}".format)
    st.dataframe(display, use_container_width=True, hide_index=True)

# Customer Deep Dive - Now with Segmentation
elif page == "🔍 Customer Deep Dive":
    st.title("🔍 Customer Segmentation Analysis")

    # Calculate RFM
    snapshot_date = filtered_trans['Date'].max() + pd.Timedelta(days=1)
    rfm = filtered_trans.groupby('Customer_ID').agg({
        'Date': lambda x: (snapshot_date - x.max()).days,
        'Invoice_ID': 'nunique',
        'Line_Total': lambda x: x[x > 0].sum()  # only sales
    }).reset_index()
    rfm.columns = ['Customer_ID', 'Recency', 'Frequency', 'Monetary']

    # Quantile-based scoring
    quantiles = rfm[['Recency', 'Frequency', 'Monetary']].quantile([0.25, 0.5, 0.75])
    def r_score(x): return 4 if x <= quantiles.loc[0.25, 'Recency'] else (3 if x <= quantiles.loc[0.5, 'Recency'] else (2 if x <= quantiles.loc[0.75, 'Recency'] else 1))
    def fm_score(x, col): return 1 if x <= quantiles.loc[0.25, col] else (2 if x <= quantiles.loc[0.5, col] else (3 if x <= quantiles.loc[0.75, col] else 4))

    rfm['R'] = rfm['Recency'].apply(r_score)
    rfm['F'] = rfm['Frequency'].apply(lambda x: fm_score(x, 'Frequency'))
    rfm['M'] = rfm['Monetary'].apply(lambda x: fm_score(x, 'Monetary'))
    rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

    # Value segments
    rfm['Value_Segment'] = pd.qcut(rfm['Monetary'], q=4, labels=['Low Value', 'Medium Value', 'High Value', 'VIP'])

    # Merge country if available
    if 'Country' in filtered_cust.columns:
        rfm = rfm.merge(filtered_cust[['Customer_ID', 'Country']], on='Customer_ID', how='left')

    st.markdown("### Customer Value Segments")
    col1, col2 = st.columns(2)
    with col1:
        seg_counts = rfm['Value_Segment'].value_counts()
        fig = px.pie(values=seg_counts.values, names=seg_counts.index, hole=0.4,
                     color_discrete_sequence=['#95a5a6', '#f39c12', '#3498db', '#2ecc71'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        seg_stats = rfm.groupby('Value_Segment').agg({
            'Customer_ID': 'count',
            'Monetary': ['sum', 'mean'],
            'Frequency': 'mean',
            'Recency': 'mean'
        }).round(0)
        seg_stats.columns = ['Customers', 'Total Revenue', 'Avg CLV', 'Avg Orders', 'Avg Recency (days)']
        st.dataframe(seg_stats.style.format({
            'Customers': '{:,}',
            'Total Revenue': '${:,.0f}',
            'Avg CLV': '${:,.0f}',
            'Avg Orders': '{:.1f}',
            'Avg Recency (days)': '{:.0f}'
        }), use_container_width=True)

    st.markdown("---")
    st.subheader("Revenue Contribution by Segment")
    rev_seg = rfm.groupby('Value_Segment')['Monetary'].sum().reset_index()
    fig = px.bar(rev_seg, x='Value_Segment', y='Monetary', color='Value_Segment',
                 color_discrete_sequence=['#95a5a6', '#f39c12', '#3498db', '#2ecc71'])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Top Customers by CLV")
    top_clv = rfm.nlargest(20, 'Monetary')[['Customer_ID', 'Monetary', 'Frequency', 'Recency', 'Value_Segment']]
    top_clv['Monetary'] = top_clv['Monetary'].map("${:,.0f}".format)
    st.dataframe(top_clv, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'><p>Built with Streamlit & Plotly | 2025</p></div>", unsafe_allow_html=True)