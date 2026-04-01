import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
from scipy import stats

# Page configuration
st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .highlight {
        color: #1f77b4;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Marketing_Data_Cleaned.csv')
    
    # Clean metric names for easier reference
    metric_mapping = {
        'Marketing event incl Speaking engagement 包括演讲在内的市场营销活动': 'Marketing Events',
        'Marketing qualified Lead (MQL) \n市场部确认的商机(MQL)': 'MQL',
        'Press Release 新闻通稿': 'Press Releases',
        'Social Media Posting \n社交媒体发帖量': 'Social Media Posts'
    }
    
    df['Metric'] = df['Metric'].replace(metric_mapping)
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date'].min().date(), df['Date'].max().date()),
    min_value=df['Date'].min().date(),
    max_value=df['Date'].max().date()
)

# Filter data by date range
df_filtered = df[(df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])]

# Metric filter
selected_metrics = st.sidebar.multiselect(
    "Select Metrics",
    options=df['Metric'].unique(),
    default=df['Metric'].unique()
)

df_filtered = df_filtered[df_filtered['Metric'].isin(selected_metrics)]

# Main dashboard title
st.title("📊 Marketing Analytics Dashboard")
st.markdown("Monitor marketing activities and their correlation with sales leads (MQL)")

# Pivot data for easier analysis
df_pivot = df_filtered.pivot_table(index='Date', columns='Metric', values='Value', aggfunc='sum')

# ============================================================================
# KEY METRICS SECTION
# ============================================================================
st.header("📈 Key Performance Metrics")

col1, col2, col3, col4 = st.columns(4)

if 'Marketing Events' in df_pivot.columns:
    total_events = int(df_pivot['Marketing Events'].sum())
    col1.metric(
        "Total Marketing Events",
        f"{total_events}",
        delta=f"Avg: {total_events/len(df_pivot):.1f}/month"
    )

if 'MQL' in df_pivot.columns:
    total_mql = int(df_pivot['MQL'].sum())
    avg_mql = total_mql / len(df_pivot)
    col2.metric(
        "Total MQLs Generated",
        f"{total_mql:,}",
        delta=f"Avg: {avg_mql:.0f}/month"
    )

if 'Press Releases' in df_pivot.columns:
    total_pr = int(df_pivot['Press Releases'].sum())
    col3.metric(
        "Press Releases",
        f"{total_pr}",
        delta=f"Avg: {total_pr/len(df_pivot):.1f}/month"
    )

if 'Social Media Posts' in df_pivot.columns:
    total_posts = int(df_pivot['Social Media Posts'].sum())
    col4.metric(
        "Social Media Posts",
        f"{total_posts}",
        delta=f"Avg: {total_posts/len(df_pivot):.1f}/month"
    )

st.divider()

# ============================================================================
# TIMELINE VIEW - All Metrics Over Time
# ============================================================================
st.header("📅 Timeline: Marketing Activities vs MQL Generation")

fig_timeline = go.Figure()

# Add traces for each metric
for metric in selected_metrics:
    metric_data = df_filtered[df_filtered['Metric'] == metric].sort_values('Date')
    
    if metric == 'MQL':
        fig_timeline.add_trace(go.Scatter(
            x=metric_data['Date'],
            y=metric_data['Value'],
            name=metric,
            mode='lines+markers',
            line=dict(color='#d62728', width=3),
            yaxis='y2',
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>MQL: %{y:,.0f}<extra></extra>'
        ))
    else:
        fig_timeline.add_trace(go.Scatter(
            x=metric_data['Date'],
            y=metric_data['Value'],
            name=metric,
            mode='lines+markers',
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>%{fullData.name}: %{y:,.0f}<extra></extra>'
        ))

fig_timeline.update_layout(
    title="Marketing Activities & MQL Trends Over Time",
    xaxis_title="Date",
    yaxis_title="Count (Events, Posts, Releases)",
    yaxis2=dict(
        title="MQL Count",
        overlaying='y',
        side='right'
    ),
    hovermode='x unified',
    height=500,
    template='plotly_white'
)

st.plotly_chart(fig_timeline, use_container_width=True)

st.divider()

# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================
st.header("🔗 Correlation Analysis: Activities → MQL Generation")

# Create correlation matrix
if 'MQL' in df_pivot.columns:
    correlation_data = df_pivot.copy()
    correlation_matrix = correlation_data.corr()
    
    # Display correlation with MQL
    mql_correlations = correlation_matrix['MQL'].sort_values(ascending=False)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Correlation Coefficients with MQL")
        for metric, corr in mql_correlations.items():
            if metric != 'MQL':
                color = '🟢' if corr > 0 else '🔴'
                st.write(f"{color} **{metric}**: {corr:.3f}")
    
    with col2:
        # Heatmap
        fig_corr = px.imshow(
            correlation_matrix,
            text_auto='.2f',
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            title="Correlation Matrix - All Metrics"
        )
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown("""
    **Interpretation Guide:**
    - **+1.0 to +0.5**: Strong positive correlation (activity increases → MQL increases)
    - **+0.5 to 0**: Weak positive correlation
    - **-0.5 to 0**: Weak negative correlation
    - **-1.0 to -0.5**: Strong negative correlation
    """)

st.divider()

# ============================================================================
# ACTIVITY IMPACT ANALYSIS
# ============================================================================
st.header("💡 Activity Impact on MQL Generation")

if 'MQL' in df_pivot.columns:
    col1, col2 = st.columns(2)
    
    # Marketing Events Impact
    if 'Marketing Events' in df_pivot.columns:
        with col1:
            st.subheader("Marketing Events Impact")
            # Categorize months by event count
            df_pivot['Event_Category'] = pd.cut(
                df_pivot['Marketing Events'],
                bins=[-0.1, 0, 2, 6],
                labels=['No Events', '1-2 Events', '3+ Events']
            )
            impact = df_pivot.groupby('Event_Category')['MQL'].agg(['mean', 'count', 'min', 'max'])
            
            for cat in ['No Events', '1-2 Events', '3+ Events']:
                if cat in impact.index:
                    mean_mql = impact.loc[cat, 'mean']
                    count = int(impact.loc[cat, 'count'])
                    st.write(f"**{cat}** ({count} months): Avg MQL = {mean_mql:.0f}")
    
    # Social Media Posts Impact
    if 'Social Media Posts' in df_pivot.columns:
        with col2:
            st.subheader("Social Media Posts Impact")
            df_pivot['Social_Category'] = pd.cut(
                df_pivot['Social Media Posts'],
                bins=[0, 5, 10, 20],
                labels=['Low (1-5)', 'Medium (6-10)', 'High (11+)']
            )
            impact_social = df_pivot.groupby('Social_Category')['MQL'].agg(['mean', 'count', 'min', 'max'])
            
            for cat in ['Low (1-5)', 'Medium (6-10)', 'High (11+)']:
                if cat in impact_social.index:
                    mean_mql = impact_social.loc[cat, 'mean']
                    count = int(impact_social.loc[cat, 'count'])
                    st.write(f"**{cat}** ({count} months): Avg MQL = {mean_mql:.0f}")

st.divider()

# ============================================================================
# COMBINED ACTIVITY ANALYSIS
# ============================================================================
st.header("🎯 Combined Activity Strategy Analysis")

if all(col in df_pivot.columns for col in ['Marketing Events', 'MQL', 'Social Media Posts']):
    # Create combined activity score
    df_pivot['Combined_Score'] = (
        (df_pivot['Marketing Events'] / df_pivot['Marketing Events'].max() * 0.4) +
        (df_pivot['Social Media Posts'] / df_pivot['Social Media Posts'].max() * 0.4) +
        (df_pivot.get('Press Releases', 0) / (df_pivot.get('Press Releases', 0).max() + 0.1) * 0.2)
    )
    
    fig_combined = px.scatter(
        df_pivot.reset_index(),
        x='Combined_Score',
        y='MQL',
        size='Marketing Events',
        color='Social Media Posts',
        hover_data=['Date'],
        labels={
            'Combined_Score': 'Combined Activity Score',
            'MQL': 'MQL Generated',
            'Social Media Posts': 'Social Posts'
        },
        title="Impact of Combined Marketing Activities on MQL",
        color_continuous_scale='Viridis'
    )
    
    fig_combined.update_layout(height=450)
    st.plotly_chart(fig_combined, use_container_width=True)
    
    # Statistical summary
    st.subheader("Statistical Insights")
    if 'MQL' in df_pivot.columns:
        # Calculate efficiency metrics
        high_activity = df_pivot['Combined_Score'] >= df_pivot['Combined_Score'].quantile(0.75)
        low_activity = df_pivot['Combined_Score'] <= df_pivot['Combined_Score'].quantile(0.25)
        
        high_activity_mql = df_pivot[high_activity]['MQL'].mean()
        low_activity_mql = df_pivot[low_activity]['MQL'].mean()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "High Activity Months - Avg MQL",
                f"{high_activity_mql:.0f}",
                delta=f"{((high_activity_mql/low_activity_mql - 1) * 100):.0f}% vs Low Activity"
            )
        
        with col2:
            best_month = df_pivot['MQL'].idxmax()
            best_value = df_pivot.loc[best_month, 'MQL']
            st.metric("Best Performing Month", f"{best_month.strftime('%B %Y')}", f"{best_value:.0f} MQL")
        
        with col3:
            worst_month = df_pivot['MQL'].idxmin()
            worst_value = df_pivot.loc[worst_month, 'MQL']
            st.metric("Lowest Performing Month", f"{worst_month.strftime('%B %Y')}", f"{worst_value:.0f} MQL")

st.divider()

# ============================================================================
# ANOMALY DETECTION
# ============================================================================
st.header("🚨 Anomaly Detection - Unusual Months")

if 'MQL' in df_pivot.columns:
    # Use Z-score to identify anomalies
    mql_data = df_pivot['MQL'].copy()
    z_scores = np.abs(stats.zscore(mql_data))
    anomalies = df_pivot[z_scores > 2].copy()
    
    if len(anomalies) > 0:
        st.write(f"Found **{len(anomalies)} anomalous months** (>2 standard deviations from mean):")
        
        for date, row in anomalies.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{date.strftime('%B %Y')}**: {int(row['MQL'])} MQL generated")
                details = []
                if 'Marketing Events' in row and row['Marketing Events'] > 0:
                    details.append(f"{int(row['Marketing Events'])} events")
                if 'Social Media Posts' in row and row['Social Media Posts'] > 0:
                    details.append(f"{int(row['Social Media Posts'])} social posts")
                if 'Press Releases' in row and row['Press Releases'] > 0:
                    details.append(f"{int(row['Press Releases'])} press releases")
                if details:
                    st.caption(f"Activities: {', '.join(details)}")
    else:
        st.info("No significant anomalies detected in the data.")

st.divider()

# ============================================================================
# DATA TABLE
# ============================================================================
st.header("📋 Detailed Data View")

with st.expander("View Full Dataset"):
    # Prepare data for display
    df_display = df_filtered.pivot_table(
        index='Date',
        columns='Metric',
        values='Value',
        aggfunc='sum'
    ).reset_index()
    
    st.dataframe(df_display, use_container_width=True)
    
    # Download option
    csv = df_display.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"marketing_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
---
**Dashboard Version:** 1.0  
**Last Updated:** {}  
**Data Source:** Marketing_Data_Cleaned.csv  
**Built with:** Streamlit + Plotly
""".format(datetime.now().strftime('%B %d, %Y')))
