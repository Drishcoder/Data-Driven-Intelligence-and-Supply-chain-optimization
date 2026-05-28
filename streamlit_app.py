import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main { padding-top: 2rem; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   padding: 20px; border-radius: 10px; color: white; }
    .stTabs [data-baseweb="tab-list"] button { font-size: 16px; font-weight: bold; }
    h1 { text-align: center; color: #2c3e50; margin-bottom: 1rem; }
    h2 { color: #34495e; margin-top: 2rem; }
    .insight-box { background-color: #ecf0f1; padding: 15px; border-radius: 8px; 
                   border-left: 4px solid #3498db; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Customer Segmentation & Supply Chain Dashboard")

# Load and process data
@st.cache_data
def load_and_process_data():
    # Load the dataset
    df = pd.read_csv('online_retail.csv')
    df_copy = df.copy()

    # Data Cleaning
    df_copy = df_copy.dropna(subset=['CustomerID'])
    df_copy = df_copy.dropna(subset=['Description'])
    df_copy = df_copy[df_copy['Quantity'] > 0]
    df_copy = df_copy[df_copy['UnitPrice'] > 0]
    df_copy = df_copy[df_copy['InvoiceNo'].str.startswith('C') == False]
    df_copy['TotalPrice'] = df_copy['Quantity'] * df_copy['UnitPrice']

    # Datetime conversion
    df_copy['InvoiceDate'] = pd.to_datetime(df_copy['InvoiceDate'])
    snapshot_date = df_copy['InvoiceDate'].max() + dt.timedelta(days=1)

    # RFM Analysis
    rfm = df_copy.groupby("CustomerID").agg({
        'InvoiceDate': (lambda x:(snapshot_date - x.max()).days),
        'InvoiceNo': 'count',
        'TotalPrice': 'sum'
    })

    rfm.rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency',
        'TotalPrice': 'Monetary',
    }, inplace=True)

    # Scaling and Log Transformation
    rfm_log = np.log(rfm + 1)
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_log)
    rfm_scaled_df = pd.DataFrame(rfm_scaled, index=rfm.index, columns=rfm.columns)

    # K-means clustering
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=50, init='k-means++')
    rfm_scaled_df['Cluster'] = kmeans.fit_predict(rfm_scaled_df)
    rfm['Cluster'] = kmeans.labels_

    # Segment naming
    segment_names = {
        0: "Champions",
        1: "At Risk Customers",
        2: "Potential Loyalists",
        3: "Hibernating Customers"
    }
    rfm['Segment'] = rfm['Cluster'].map(segment_names)

    return rfm, rfm_scaled_df, df_copy

# Load data
rfm, rfm_scaled_df, df_copy = load_and_process_data()

# Sidebar filters
st.sidebar.header("🎛️ Dashboard Controls")
selected_segments = st.sidebar.multiselect(
    "Select Segments to Display:",
    options=rfm['Segment'].unique(),
    default=rfm['Segment'].unique(),
    help="Choose which customer segments to analyze"
)

# Filter data based on selection
filtered_rfm = rfm[rfm['Segment'].isin(selected_segments)]

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 RFM Analysis", "🛒 Supply Chain", "💡 Insights"])

# ==================== TAB 1: OVERVIEW ====================
with tab1:
    st.markdown("### Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Customers", len(rfm), delta="100%")
    
    with col2:
        st.metric("🎯 Active Segments", len(selected_segments), delta=f"{len(selected_segments)}/4")
    
    with col3:
        avg_monetary = rfm['Monetary'].mean()
        st.metric("💰 Avg. Customer Value", f"${avg_monetary:,.0f}")
    
    with col4:
        total_revenue = rfm['Monetary'].sum()
        st.metric("💎 Total Revenue", f"${total_revenue:,.0f}")
    
    st.markdown("---")
    
    # Segment Distribution with better layout
    col1, col2 = st.columns(2)
    
    with col1:
        segment_counts = filtered_rfm['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        fig_pie = px.pie(
            segment_counts,
            values='Count',
            names='Segment',
            title="Customer Distribution by Segment",
            color_discrete_map={
                "Champions": "#2ecc71",
                "At Risk Customers": "#e74c3c",
                "Potential Loyalists": "#3498db",
                "Hibernating Customers": "#95a5a6"
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        segment_revenue = filtered_rfm.groupby('Segment')['Monetary'].sum().reset_index()
        segment_revenue.columns = ['Segment', 'Revenue']
        segment_revenue = segment_revenue.sort_values('Revenue', ascending=True)
        
        fig_bar = px.bar(
            segment_revenue,
            x='Revenue',
            y='Segment',
            orientation='h',
            title="Revenue by Segment",
            color='Segment',
            color_discrete_map={
                "Champions": "#2ecc71",
                "At Risk Customers": "#e74c3c",
                "Potential Loyalists": "#3498db",
                "Hibernating Customers": "#95a5a6"
            },
            labels={'Revenue': 'Total Revenue ($)', 'Segment': ''}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ==================== TAB 2: RFM ANALYSIS ====================
with tab2:
    st.markdown("### 3D Customer Segments Visualization")
    
    fig_3d = px.scatter_3d(
        filtered_rfm,
        x='Recency',
        y='Frequency',
        z='Monetary',
        color='Segment',
        hover_name=filtered_rfm.index,
        title='Interactive 3D Customer Segments',
        category_orders={'Segment': ["Champions", "At Risk Customers", "Potential Loyalists", "Hibernating Customers"]},
        color_discrete_map={
            "Champions": "#2ecc71",
            "At Risk Customers": "#e74c3c",
            "Potential Loyalists": "#3498db",
            "Hibernating Customers": "#95a5a6"
        }
    )
    fig_3d.update_layout(
        scene=dict(
            xaxis_title='Recency (days)',
            yaxis_title='Frequency',
            zaxis_title='Monetary Value ($)'
        ),
        height=700
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Segment Fingerprint (Snake Plot)")
    
    rfm_scaled_df["Segment"] = rfm["Segment"]
    melted_df = pd.melt(
        rfm_scaled_df,
        id_vars=["Segment"],
        value_vars=["Recency", "Frequency", "Monetary"],
        var_name="Metric",
        value_name="Value"
    )
    
    df_snake = melted_df.groupby(["Segment", "Metric"])["Value"].mean().reset_index()
    
    fig_snake = px.line(
        df_snake,
        x="Metric",
        y="Value",
        color="Segment",
        markers=True,
        title="Segment Characteristics Comparison",
        category_orders={'Segment': ["Champions", "At Risk Customers", "Potential Loyalists", "Hibernating Customers"]},
        color_discrete_map={
            "Champions": "#2ecc71",
            "At Risk Customers": "#e74c3c",
            "Potential Loyalists": "#3498db",
            "Hibernating Customers": "#95a5a6"
        }
    )
    fig_snake.update_layout(height=500)
    st.plotly_chart(fig_snake, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Detailed RFM Statistics")
    
    segment_stats = filtered_rfm.groupby('Segment').agg({
        'Recency': ['mean', 'min', 'max'],
        'Frequency': ['mean', 'min', 'max'],
        'Monetary': ['mean', 'min', 'max', 'sum', 'count']
    }).round(2)
    
    st.dataframe(segment_stats, use_container_width=True)

# ==================== TAB 3: SUPPLY CHAIN ====================
with tab3:
    st.markdown("### 🛒 Supply Chain Optimization - Top Products by Segment")
    
    # Merge to get products by segment
    supply_chain_df = df_copy.merge(rfm[["Segment"]], on="CustomerID", how="inner")
    
    # Select number of top products to display
    num_products = st.slider("Number of Top Products to Display:", 5, 20, 10)
    
    # Create columns for each segment
    segments_list = list(selected_segments)
    
    for i in range(0, len(segments_list), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            if i + j < len(segments_list):
                segment = segments_list[i + j]
                
                with col:
                    segment_products = supply_chain_df[supply_chain_df["Segment"] == segment]
                    top_products = segment_products.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(num_products)
                    
                    st.markdown(f"#### {segment}")
                    
                    # Bar chart
                    fig_products = px.bar(
                        x=top_products.values,
                        y=top_products.index,
                        orientation='h',
                        title=f"Top {num_products} Products",
                        labels={'x': 'Total Quantity', 'y': 'Product'},
                        color=top_products.values,
                        color_continuous_scale='Viridis'
                    )
                    fig_products.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig_products, use_container_width=True)
                    
                    # Table view
                    with st.expander("📋 View as Table"):
                        df_display = top_products.reset_index()
                        df_display.columns = ['Product', 'Quantity']
                        st.dataframe(df_display, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Cross-Segment Product Analysis")
    
    # Show all segments comparison
    product_by_segment = supply_chain_df.groupby(["Description", "Segment"])["Quantity"].sum().reset_index()
    top_overall_products = supply_chain_df.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(10).index
    
    comparison_df = product_by_segment[product_by_segment["Description"].isin(top_overall_products)]
    
    fig_comparison = px.bar(
        comparison_df,
        x="Description",
        y="Quantity",
        color="Segment",
        title="Top 10 Products - Segment Comparison",
        color_discrete_map={
            "Champions": "#2ecc71",
            "At Risk Customers": "#e74c3c",
            "Potential Loyalists": "#3498db",
            "Hibernating Customers": "#95a5a6"
        },
        barmode='group'
    )
    fig_comparison.update_xaxes(tickangle=-45)
    fig_comparison.update_layout(height=500)
    st.plotly_chart(fig_comparison, use_container_width=True)

# ==================== TAB 4: INSIGHTS ====================
with tab4:
    st.markdown("### 💡 Strategic Insights & Recommendations")
    
    insights = {
        "Champions": {
            "emoji": "🌟",
            "description": "Your best customers with high recency, frequency, and monetary value.",
            "actions": [
                "✓ Focus on retention strategies",
                "✓ Offer exclusive loyalty programs",
                "✓ Provide VIP support and early access to new products",
                "✓ Personalize recommendations based on purchase history"
            ]
        },
        "At Risk Customers": {
            "emoji": "⚠️",
            "description": "Previously valuable customers with declining engagement.",
            "actions": [
                "✓ Launch immediate re-engagement campaigns",
                "✓ Offer special discounts or promotions",
                "✓ Send personalized win-back messages",
                "✓ Survey to understand reasons for decreased activity"
            ]
        },
        "Potential Loyalists": {
            "emoji": "🎯",
            "description": "New or recently active customers with good spending habits.",
            "actions": [
                "✓ Nurture to become champions",
                "✓ Send valuable content and education",
                "✓ Encourage repeat purchases with incentives",
                "✓ Build strong relationships through personalization"
            ]
        },
        "Hibernating Customers": {
            "emoji": "😴",
            "description": "Inactive customers with low engagement.",
            "actions": [
                "✓ Deploy targeted win-back campaigns",
                "✓ Offer significant discounts or incentives",
                "✓ Ask for feedback on their inactivity",
                "✓ Consider segmenting for focused re-activation efforts"
            ]
        }
    }
    
    for segment in selected_segments:
        if segment in insights:
            insight_data = insights[segment]
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"<h1 style='font-size: 40px;'>{insight_data['emoji']}</h1>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"### {segment}")
                    st.markdown(f"_{insight_data['description']}_")
                
                st.markdown("#### Recommended Actions:")
                for action in insight_data['actions']:
                    st.markdown(action)
                
                # Get segment statistics
                seg_data = filtered_rfm[filtered_rfm['Segment'] == segment]
                seg_col1, seg_col2, seg_col3 = st.columns(3)
                with seg_col1:
                    st.metric("Customers", len(seg_data))
                with seg_col2:
                    st.metric("Avg. Value", f"${seg_data['Monetary'].mean():,.0f}")
                with seg_col3:
                    st.metric("Total Revenue", f"${seg_data['Monetary'].sum():,.0f}")
                
                st.markdown("---")
