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

# Custom CSS for better styling
st.markdown("""
<style>
    .insight-box {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
    .recommendation-box {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #ff9800;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Marketing_Data_Cleaned.csv')
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
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date'].min().date(), df['Date'].max().date()),
    min_value=df['Date'].min().date(),
    max_value=df['Date'].max().date()
)

df_filtered = df[(df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])]

selected_metrics = st.sidebar.multiselect(
    "Select Metrics",
    options=df['Metric'].unique(),
    default=df['Metric'].unique()
)

df_filtered = df_filtered[df_filtered['Metric'].isin(selected_metrics)]

# Main dashboard
st.title("📊 Marketing Analytics Dashboard")
st.markdown("Monitor marketing activities and their correlation with sales leads (MQL)")

df_pivot = df_filtered.pivot_table(index='Date', columns='Metric', values='Value', aggfunc='sum')

# KEY METRICS
st.header("📈 Key Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

if 'Marketing Events' in df_pivot.columns:
    total_events = int(df_pivot['Marketing Events'].sum())
    col1.metric("Total Marketing Events", f"{total_events}", delta=f"Avg: {total_events/len(df_pivot):.1f}/month")

if 'MQL' in df_pivot.columns:
    total_mql = int(df_pivot['MQL'].sum())
    avg_mql = total_mql / len(df_pivot)
    col2.metric("Total MQLs Generated", f"{total_mql:,}", delta=f"Avg: {avg_mql:.0f}/month")

if 'Press Releases' in df_pivot.columns:
    total_pr = int(df_pivot['Press Releases'].sum())
    col3.metric("Press Releases", f"{total_pr}", delta=f"Avg: {total_pr/len(df_pivot):.1f}/month")

if 'Social Media Posts' in df_pivot.columns:
    total_posts = int(df_pivot['Social Media Posts'].sum())
    col4.metric("Social Media Posts", f"{total_posts}", delta=f"Avg: {total_posts/len(df_pivot):.1f}/month")

st.divider()

# TIMELINE
st.header("📅 Timeline: Marketing Activities vs MQL Generation")
fig_timeline = go.Figure()

for metric in selected_metrics:
    metric_data = df_filtered[df_filtered['Metric'] == metric].sort_values('Date')
    if metric == 'MQL':
        fig_timeline.add_trace(go.Scatter(
            x=metric_data['Date'],
            y=metric_data['Value'],
            name=metric,
            mode='lines+markers',
            line=dict(color='#d62728', width=3),
            yaxis='y2'
        ))
    else:
        fig_timeline.add_trace(go.Scatter(
            x=metric_data['Date'],
            y=metric_data['Value'],
            name=metric,
            mode='lines+markers'
        ))

fig_timeline.update_layout(
    title="Marketing Activities & MQL Trends Over Time",
    xaxis_title="Date",
    yaxis_title="Count (Events, Posts, Releases)",
    yaxis2=dict(title="MQL Count", overlaying='y', side='right'),
    hovermode='x unified',
    height=500,
    template='plotly_white'
)

st.plotly_chart(fig_timeline, use_container_width=True)
st.divider()

# CORRELATION ANALYSIS
st.header("🔗 Correlation Analysis: Activities → MQL Generation")

if 'MQL' in df_pivot.columns:
    correlation_matrix = df_pivot.corr()
    mql_corr = correlation_matrix['MQL'].sort_values(ascending=False)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Correlation with MQL")
        for metric, corr in mql_corr.items():
            if metric != 'MQL':
                color = '🟢' if corr > 0 else '🔴'
                st.write(f"{color} **{metric}**: {corr:.3f}")
    
    with col2:
        fig_corr = px.imshow(correlation_matrix, text_auto='.2f', color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
        st.plotly_chart(fig_corr, use_container_width=True)

st.divider()

# ACTIVITY IMPACT
st.header("💡 Activity Impact on MQL Generation")

if 'MQL' in df_pivot.columns:
    col1, col2 = st.columns(2)
    
    if 'Marketing Events' in df_pivot.columns:
        with col1:
            st.subheader("📍 Marketing Events Impact")
            df_pivot['Event_Category'] = pd.cut(df_pivot['Marketing Events'], bins=[-0.1, 0, 2, 6], labels=['No Events', '1-2 Events', '3+ Events'])
            impact = df_pivot.groupby('Event_Category')['MQL'].agg(['mean', 'count'])
            
            fig_events = px.bar(x=impact.index, y=impact['mean'], text=impact['mean'].apply(lambda x: f'{int(x)} MQL'), 
                               title='Average MQL by Event Level', color=impact['mean'], color_continuous_scale=['#ff9800', '#ffc107', '#4caf50'])
            fig_events.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_events, use_container_width=True)
    
    if 'Social Media Posts' in df_pivot.columns:
        with col2:
            st.subheader("📱 Social Media Posts Impact")
            df_pivot['Social_Category'] = pd.cut(df_pivot['Social Media Posts'], bins=[0, 5, 10, 20], labels=['Low (1-5)', 'Medium (6-10)', 'High (11+)'])
            impact_social = df_pivot.groupby('Social_Category')['MQL'].agg(['mean', 'count'])
            
            fig_social = px.bar(x=impact_social.index, y=impact_social['mean'], text=impact_social['mean'].apply(lambda x: f'{int(x)} MQL'),
                               title='Average MQL by Social Media Activity', color=impact_social['mean'], color_continuous_scale=['#ff9800', '#ffc107', '#4caf50'])
            fig_social.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_social, use_container_width=True)

st.divider()

# SIMPLIFIED COMBINED ANALYSIS
st.header("🎯 Combined Marketing Strategy - Simple Analysis")

if all(col in df_pivot.columns for col in ['Marketing Events', 'MQL', 'Social Media Posts']):
    
    df_pivot['Overall_Activity'] = 'Low Activity'
    df_pivot.loc[(df_pivot['Marketing Events'] >= 3) | (df_pivot['Social Media Posts'] >= 11), 'Overall_Activity'] = 'High Activity'
    df_pivot.loc[((df_pivot['Marketing Events'] >= 1) & (df_pivot['Marketing Events'] < 3)) | ((df_pivot['Social Media Posts'] >= 6) & (df_pivot['Social Media Posts'] < 11)), 'Overall_Activity'] = 'Medium Activity'
    
    activity_analysis = df_pivot.groupby('Overall_Activity')['MQL'].agg(['count', 'mean', 'min', 'max'])
    
    fig_activity = px.bar(x=activity_analysis.index, y=activity_analysis['mean'], 
                          text=activity_analysis['mean'].apply(lambda x: f'{int(x)}<br>Avg MQL'),
                          title='📊 Average MQL by Marketing Activity Level',
                          color_discrete_sequence=['#ff6b6b', '#ffd93d', '#6bcf7f'])
    fig_activity.update_layout(height=400, showlegend=False, template='plotly_white')
    st.plotly_chart(fig_activity, use_container_width=True)
    
    st.divider()
    
    # KEY INSIGHTS
    st.subheader("✨ Key Insights")
    
    low_activity_mql = activity_analysis.loc['Low Activity', 'mean'] if 'Low Activity' in activity_analysis.index else 0
    high_activity_mql = activity_analysis.loc['High Activity', 'mean'] if 'High Activity' in activity_analysis.index else 0
    
    if high_activity_mql > 0 and low_activity_mql > 0:
        uplift = ((high_activity_mql / low_activity_mql) - 1) * 100
        st.markdown(f"""
        <div class="insight-box">
        <h4>💡 Main Finding</h4>
        <p><strong>When you increase marketing activities, you generate {uplift:.0f}% MORE leads!</strong></p>
        <ul>
            <li><strong>Low Activity Months:</strong> Average {low_activity_mql:.0f} MQL</li>
            <li><strong>High Activity Months:</strong> Average {high_activity_mql:.0f} MQL</li>
            <li><strong>Difference:</strong> +{high_activity_mql - low_activity_mql:.0f} additional leads per month</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # BEST MONTH
    best_month_idx = df_pivot['MQL'].idxmax()
    best_month_data = df_pivot.loc[best_month_idx]
    
    st.markdown(f"""
    <div class="insight-box">
    <h4>🏆 Your Best Month: {best_month_idx.strftime('%B %Y')}</h4>
    <p><strong>{int(best_month_data['MQL'])} MQL Generated</strong></p>
    <ul>
        <li>📍 Marketing Events: {int(best_month_data['Marketing Events'])}</li>
        <li>📱 Social Media Posts: {int(best_month_data['Social Media Posts'])}</li>
        <li>📰 Press Releases: {int(best_month_data['Press Releases'])}</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # RECOMMENDATIONS
    st.subheader("🎯 Recommendations for Your Team")
    
    recent_months = df_pivot.tail(3)
    avg_recent_events = recent_months['Marketing Events'].mean()
    avg_recent_social = recent_months['Social Media Posts'].mean()
    avg_recent_pr = recent_months['Press Releases'].mean()
    
    best_events = df_pivot['Marketing Events'].quantile(0.75)
    best_social = df_pivot['Social Media Posts'].quantile(0.75)
    best_pr = df_pivot['Press Releases'].quantile(0.75)
    
    st.markdown(f"""
    <div class="recommendation-box">
    <h4>📌 Action Items (Based on Your Data)</h4>
    
    <h5>1. Marketing Events</h5>
    <p><strong>Current:</strong> {avg_recent_events:.1f} events/month | <strong>Target:</strong> {best_events:.1f} events/month</p>
    
    <h5>2. Social Media Posts</h5>
    <p><strong>Current:</strong> {avg_recent_social:.1f} posts/month | <strong>Target:</strong> {best_social:.1f} posts/month</p>
    
    <h5>3. Press Releases</h5>
    <p><strong>Current:</strong> {avg_recent_pr:.1f} releases/month | <strong>Target:</strong> {best_pr:.1f} releases/month</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ANOMALY DETECTION
st.header("🚨 Anomaly Detection")

if 'MQL' in df_pivot.columns:
    mql_data = df_pivot['MQL'].copy()
    z_scores = np.abs(stats.zscore(mql_data))
    anomalies = df_pivot[z_scores > 2].copy()
    
    if len(anomalies) > 0:
        st.write(f"Found **{len(anomalies)} unusual months**:")
        for date, row in anomalies.iterrows():
            st.write(f"**{date.strftime('%B %Y')}**: {int(row['MQL'])} MQL")
    else:
        st.info("No significant anomalies detected.")

st.divider()

# DATA TABLE
st.header("📋 Detailed Data View")

with st.expander("View Full Dataset"):
    df_display = df_filtered.pivot_table(index='Date', columns='Metric', values='Value', aggfunc='sum').reset_index()
    st.dataframe(df_display, use_container_width=True)
    csv = df_display.to_csv(index=False)
    st.download_button(label="📥 Download as CSV", data=csv, file_name=f"marketing_data_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

st.divider()
st.markdown(f"**Dashboard Version:** 2.0 | **Last Updated:** {datetime.now().strftime('%B %d, %Y')}")
