import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Multi-Department Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
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
    .warning-box {
        background-color: #ffebee;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================
@st.cache_data
def load_marketing_data():
    try:
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
    except:
        return None

@st.cache_data
def load_billing_data():
    try:
        df = pd.read_csv('Billing_Data_Complete_2022_2025.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return None

@st.cache_data
def load_csc_data():
    try:
        df = pd.read_csv('CSC_Complere.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return None

@st.cache_data
def load_hr_data():
    try:
        df = pd.read_csv('HR_Department_Complete.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return None

@st.cache_data
def load_nt_data():
    try:
        df = pd.read_csv('NT_Department_Complete.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return None

@st.cache_data
def load_resource_data():
    try:
        df = pd.read_csv('Resource_Check_Department.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return None

@st.cache_data
def load_sales_data():
    try:
        df = pd.read_csv('Sales_Data_Complete_2022_2025.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return None

@st.cache_data
def load_cloud_data():
    try:
        df = pd.read_csv('Cloud_Department_Complete.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return None

# ============================================================================
# LOAD ALL DATA
# ============================================================================
marketing_data = load_marketing_data()
billing_data = load_billing_data()
csc_data = load_csc_data()
hr_data = load_hr_data()
nt_data = load_nt_data()
resource_data = load_resource_data()
sales_data = load_sales_data()
cloud_data = load_cloud_data()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.title("🏢 Enterprise Dashboard")
page = st.sidebar.radio(
    "Select Department",
    [
        "🏠 Home",
        "📊 Marketing",
        "💰 Billing",
        "🌐 Customer Service",
        "👥 HR",
        "🌐 Network Team",
        "🔍 Resource Check",
        "💼 Sales",
        "☁️ Cloud"
    ]
)

# ============================================================================
# HOME PAGE
# ============================================================================
if page == "🏠 Home":
    st.title("📊 Multi-Department Enterprise Dashboard")
    st.markdown("Executive Overview - All Departments at a Glance")
    
    # Summary Cards
    st.header("📈 Department Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Marketing Summary
    if marketing_data is not None:
        mql_total = marketing_data[marketing_data['Metric'] == 'MQL']['Value'].sum()
        with col1:
            st.metric("📊 Marketing Total MQL", f"{int(mql_total):,}")
    
    # Billing Summary
    if billing_data is not None:
        billing_total = billing_data['Value'].sum()
        with col2:
            st.metric("💰 Billing Total", f"{int(billing_total):,}")
    
    # HR Summary
    if hr_data is not None:
        final_staff = hr_data[hr_data['Parameter'] == 'Final staff 期末人数​, including 3 employess of Le food (乐肴)']['Value'].iloc[-1]
        with col3:
            st.metric("👥 Current Headcount", f"{int(final_staff)}")
    
    # CSC Summary
    if csc_data is not None:
        fault_cases = csc_data[csc_data['Parameter'] == 'Fault cases']['Value'].sum()
        with col4:
            st.metric("🌐 CSC Fault Cases", f"{int(fault_cases)}")
    
    st.divider()
    
    # Timeline Comparison
    st.header("📅 Department Trends Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Marketing MQL Trend
        if marketing_data is not None:
            mql_trend = marketing_data[marketing_data['Metric'] == 'MQL'].sort_values('Date')
            if len(mql_trend) > 0:
                fig_marketing = px.line(
                    mql_trend,
                    x='Date',
                    y='Value',
                    title='Marketing: MQL Trend',
                    labels={'Value': 'MQL Count'},
                    height=400
                )
                st.plotly_chart(fig_marketing, use_container_width=True)
    
    with col2:
        # Billing Trend
        if billing_data is not None:
            billing_trend = billing_data.groupby('Date')['Value'].sum().reset_index()
            fig_billing = px.line(
                billing_trend,
                x='Date',
                y='Value',
                title='Billing: Total Revenue Trend',
                labels={'Value': 'Total Value'},
                height=400
            )
            st.plotly_chart(fig_billing, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # HR Headcount Trend
        if hr_data is not None:
            hr_trend = hr_data[hr_data['Parameter'] == 'Final staff 期末人数​, including 3 employess of Le food (乐肴)'].sort_values('Date')
            if len(hr_trend) > 0:
                fig_hr = px.line(
                    hr_trend,
                    x='Date',
                    y='Value',
                    title='HR: Headcount Trend',
                    labels={'Value': 'Headcount'},
                    height=400
                )
                st.plotly_chart(fig_hr, use_container_width=True)
    
    with col4:
        # Cloud Active POC Trend
        if cloud_data is not None:
            cloud_trend = cloud_data[cloud_data['Parameter'] == 'Active POC'].sort_values('Date')
            if len(cloud_trend) > 0:
                fig_cloud = px.line(
                    cloud_trend,
                    x='Date',
                    y='Value',
                    title='Cloud: Active POC Trend',
                    labels={'Value': 'Active Count'},
                    height=400
                )
                st.plotly_chart(fig_cloud, use_container_width=True)
    
    st.divider()
    
    # Key Insights
    st.header("💡 Cross-Department Insights")
    
    st.markdown("""
    <div class="insight-box">
    <h4>🎯 Dashboard Highlights</h4>
    <ul>
        <li><strong>8 Departments Tracked:</strong> Marketing, Billing, Customer Service, HR, Network, Resource Check, Sales, and Cloud</li>
        <li><strong>Data Period:</strong> July 2022 to Present</li>
        <li><strong>Real-time Analysis:</strong> All visualizations update automatically from your data files</li>
        <li><strong>Navigation:</strong> Use the left sidebar to explore each department in detail</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="recommendation-box">
    <h4>📌 Getting Started</h4>
    <p>Click on any department in the left sidebar to:</p>
    <ul>
        <li>View detailed KPIs and metrics</li>
        <li>Analyze trends and patterns</li>
        <li>Explore correlations between metrics</li>
        <li>Get actionable recommendations</li>
        <li>Download insights as CSV</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MARKETING PAGE
# ============================================================================
elif page == "📊 Marketing":
    st.title("📊 Marketing Analytics")
    
    if marketing_data is not None:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(marketing_data['Date'].min().date(), marketing_data['Date'].max().date()),
            min_value=marketing_data['Date'].min().date(),
            max_value=marketing_data['Date'].max().date()
        )
        
        df_filtered = marketing_data[(marketing_data['Date'].dt.date >= date_range[0]) & 
                                     (marketing_data['Date'].dt.date <= date_range[1])]
        
        df_pivot = df_filtered.pivot_table(index='Date', columns='Metric', values='Value', aggfunc='sum')
        
        # Key Metrics
        st.header("📈 Key Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        if 'Marketing Events' in df_pivot.columns:
            total_events = int(df_pivot['Marketing Events'].sum())
            col1.metric("Marketing Events", f"{total_events}", delta=f"Avg: {total_events/len(df_pivot):.1f}/month")
        
        if 'MQL' in df_pivot.columns:
            total_mql = int(df_pivot['MQL'].sum())
            avg_mql = total_mql / len(df_pivot)
            col2.metric("Total MQLs", f"{total_mql:,}", delta=f"Avg: {avg_mql:.0f}/month")
        
        if 'Press Releases' in df_pivot.columns:
            total_pr = int(df_pivot['Press Releases'].sum())
            col3.metric("Press Releases", f"{total_pr}", delta=f"Avg: {total_pr/len(df_pivot):.1f}/month")
        
        if 'Social Media Posts' in df_pivot.columns:
            total_posts = int(df_pivot['Social Media Posts'].sum())
            col4.metric("Social Media Posts", f"{total_posts}", delta=f"Avg: {total_posts/len(df_pivot):.1f}/month")
        
        st.divider()
        
        # Timeline
        st.header("📅 Marketing Trends Over Time")
        
        fig_timeline = go.Figure()
        for metric in df_pivot.columns:
            metric_data = df_filtered[df_filtered['Metric'] == metric].sort_values('Date')
            if metric == 'MQL':
                fig_timeline.add_trace(go.Scatter(
                    x=metric_data['Date'], y=metric_data['Value'], name=metric,
                    mode='lines+markers', line=dict(color='#d62728', width=3), yaxis='y2'
                ))
            else:
                fig_timeline.add_trace(go.Scatter(
                    x=metric_data['Date'], y=metric_data['Value'], name=metric, mode='lines+markers'
                ))
        
        fig_timeline.update_layout(
            title="Marketing Metrics Timeline",
            xaxis_title="Date", yaxis_title="Count", height=450, template='plotly_white',
            yaxis2=dict(title="MQL Count", overlaying='y', side='right'), hovermode='x unified'
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        st.divider()
        
        # Correlation & Insights
        st.header("🔗 Correlation Analysis")
        if 'MQL' in df_pivot.columns:
            correlation_matrix = df_pivot.corr()
            mql_corr = correlation_matrix['MQL'].sort_values(ascending=False)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.subheader("MQL Correlations")
                for metric, corr in mql_corr.items():
                    if metric != 'MQL':
                        color = '🟢' if corr > 0 else '🔴'
                        st.write(f"{color} **{metric}**: {corr:.3f}")
            
            with col2:
                fig_corr = px.imshow(correlation_matrix, text_auto='.2f', color_continuous_scale='RdBu_r')
                st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.error("Marketing data not found. Please ensure Marketing_Data_Cleaned.csv is uploaded.")

# ============================================================================
# BILLING PAGE
# ============================================================================
elif page == "💰 Billing":
    st.title("💰 Billing Analytics")
    
    if billing_data is not None:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(billing_data['Date'].min().date(), billing_data['Date'].max().date()),
            min_value=billing_data['Date'].min().date(),
            max_value=billing_data['Date'].max().date()
        )
        
        df_filtered = billing_data[(billing_data['Date'].dt.date >= date_range[0]) & 
                                   (billing_data['Date'].dt.date <= date_range[1])]
        
        # Key Metrics
        st.header("📈 Billing Overview")
        col1, col2, col3 = st.columns(3)
        
        total_billing = df_filtered['Value'].sum()
        avg_billing = df_filtered.groupby('Date')['Value'].sum().mean()
        max_month = df_filtered.groupby('Date')['Value'].sum().idxmax()
        
        col1.metric("Total Billing", f"{int(total_billing):,}")
        col2.metric("Monthly Average", f"{int(avg_billing):,}")
        col3.metric("Peak Month", max_month.strftime('%B %Y'))
        
        st.divider()
        
        # Billing by Entity
        st.header("🏢 Billing by Entity")
        entity_billing = df_filtered.groupby('Parameter')['Value'].sum().sort_values(ascending=False)
        
        fig_entity = px.bar(
            x=entity_billing.values, y=entity_billing.index,
            orientation='h', title='Total Billing by Entity',
            labels={'x': 'Billing Amount', 'y': 'Entity'}
        )
        st.plotly_chart(fig_entity, use_container_width=True)
        
        st.divider()
        
        # Timeline
        st.header("📅 Billing Trend Over Time")
        billing_trend = df_filtered.groupby('Date')['Value'].sum().reset_index()
        
        fig_trend = px.line(
            billing_trend, x='Date', y='Value',
            title='Billing Trend', labels={'Value': 'Billing Amount'},
            height=400
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.error("Billing data not found. Please ensure Billing_Data_Complete_2022_2025.csv is uploaded.")

# ============================================================================
# CSC PAGE
# ============================================================================
elif page == "🌐 Customer Service":
    st.title("🌐 Customer Service Center Analytics")
    
    if csc_data is not None:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(csc_data['Date'].min().date(), csc_data['Date'].max().date()),
            min_value=csc_data['Date'].min().date(),
            max_value=csc_data['Date'].max().date()
        )
        
        df_filtered = csc_data[(csc_data['Date'].dt.date >= date_range[0]) & 
                               (csc_data['Date'].dt.date <= date_range[1])]
        
        # Key Metrics
        st.header("📈 CSC Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        if 'Fault cases' in df_filtered['Parameter'].values:
            fault_cases = df_filtered[df_filtered['Parameter'] == 'Fault cases']['Value'].sum()
            col1.metric("Fault Cases", f"{int(fault_cases):,}")
        
        if 'Major incidents' in df_filtered['Parameter'].values:
            major_incidents = df_filtered[df_filtered['Parameter'] == 'Major incidents']['Value'].sum()
            col2.metric("Major Incidents", f"{int(major_incidents)}")
        
        if 'MTTR - Internet (hour)' in df_filtered['Parameter'].values:
            avg_mttr = df_filtered[df_filtered['Parameter'] == 'MTTR - Internet (hour)']['Value'].mean()
            col3.metric("Avg MTTR (Internet)", f"{avg_mttr:.2f} hrs")
        
        if 'Order dispatched' in df_filtered['Parameter'].values:
            orders = df_filtered[df_filtered['Parameter'] == 'Order dispatched']['Value'].sum()
            col4.metric("Orders Dispatched", f"{int(orders)}")
        
        st.divider()
        
        # Fault Cases Trend
        st.header("📊 Performance Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Fault cases' in df_filtered['Parameter'].values:
                fault_trend = df_filtered[df_filtered['Parameter'] == 'Fault cases'].sort_values('Date')
                fig_fault = px.line(fault_trend, x='Date', y='Value', title='Fault Cases Trend', height=400)
                st.plotly_chart(fig_fault, use_container_width=True)
        
        with col2:
            if 'Cloud' in df_filtered['Parameter'].values:
                cloud_trend = df_filtered[df_filtered['Parameter'] == 'Cloud'].sort_values('Date')
                fig_cloud = px.line(cloud_trend, x='Date', y='Value', title='Cloud Metrics Trend', height=400)
                st.plotly_chart(fig_cloud, use_container_width=True)
    else:
        st.error("CSC data not found. Please ensure CSC_Complere.csv is uploaded.")

# ============================================================================
# HR PAGE
# ============================================================================
elif page == "👥 HR":
    st.title("👥 HR Department Analytics")
    
    if hr_data is not None:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(hr_data['Date'].min().date(), hr_data['Date'].max().date()),
            min_value=hr_data['Date'].min().date(),
            max_value=hr_data['Date'].max().date()
        )
        
        df_filtered = hr_data[(hr_data['Date'].dt.date >= date_range[0]) & 
                              (hr_data['Date'].dt.date <= date_range[1])]
        
        # Key Metrics
        st.header("📈 HR Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        latest_data = df_filtered.sort_values('Date').iloc[-1]
        
        if 'Final staff 期末人数​, including 3 employess of Le food (乐肴)' in df_filtered['Parameter'].values:
            final_staff = df_filtered[df_filtered['Parameter'] == 'Final staff 期末人数​, including 3 employess of Le food (乐肴)']['Value'].iloc[-1]
            col1.metric("Current Headcount", f"{int(final_staff)}")
        
        if 'Turnover of staff  离职率' in df_filtered['Parameter'].values:
            avg_turnover = df_filtered[df_filtered['Parameter'] == 'Turnover of staff  离职率']['Value'].mean()
            col2.metric("Avg Turnover Rate", f"{avg_turnover:.2%}")
        
        if 'Vacancy 空缺人数​' in df_filtered['Parameter'].values:
            vacancies = df_filtered[df_filtered['Parameter'] == 'Vacancy 空缺人数​']['Value'].iloc[-1]
            col3.metric("Current Vacancies", f"{int(vacancies)}")
        
        if 'People Managers 有下属的经理' in df_filtered['Parameter'].values:
            managers = df_filtered[df_filtered['Parameter'] == 'People Managers 有下属的经理']['Value'].iloc[-1]
            col4.metric("People Managers", f"{int(managers)}")
        
        st.divider()
        
        # Headcount Trend
        st.header("📊 HR Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Final staff 期末人数​, including 3 employess of Le food (乐肴)' in df_filtered['Parameter'].values:
                staff_trend = df_filtered[df_filtered['Parameter'] == 'Final staff 期末人数​, including 3 employess of Le food (乐肴)'].sort_values('Date')
                fig_staff = px.line(staff_trend, x='Date', y='Value', title='Headcount Trend', height=400)
                st.plotly_chart(fig_staff, use_container_width=True)
        
        with col2:
            if 'Turnover of staff  离职率' in df_filtered['Parameter'].values:
                turnover_trend = df_filtered[df_filtered['Parameter'] == 'Turnover of staff  离职率'].sort_values('Date')
                fig_turnover = px.line(turnover_trend, x='Date', y='Value', title='Turnover Rate Trend', height=400)
                st.plotly_chart(fig_turnover, use_container_width=True)
    else:
        st.error("HR data not found. Please ensure HR_Department_Complete.csv is uploaded.")

# ============================================================================
# NETWORK TEAM PAGE
# ============================================================================
elif page == "🌐 Network Team":
    st.title("🌐 Network Team Analytics")
    
    if nt_data is not None:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(nt_data['Date'].min().date(), nt_data['Date'].max().date()),
            min_value=nt_data['Date'].min().date(),
            max_value=nt_data['Date'].max().date()
        )
        
        df_filtered = nt_data[(nt_data['Date'].dt.date >= date_range[0]) & 
                              (nt_data['Date'].dt.date <= date_range[1])]
        
        # Key Metrics
        st.header("📈 Network Team Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        if 'New DIA order installed' in df_filtered['Parameter'].values:
            dia_installed = df_filtered[df_filtered['Parameter'] == 'New DIA order installed']['Value'].sum()
            col1.metric("DIA Orders Installed", f"{int(dia_installed)}")
        
        if 'New MPLS VPN order installed' in df_filtered['Parameter'].values:
            mpls_installed = df_filtered[df_filtered['Parameter'] == 'New MPLS VPN order installed']['Value'].sum()
            col2.metric("MPLS VPN Installed", f"{int(mpls_installed)}")
        
        if 'New PLC order installed' in df_filtered['Parameter'].values:
            plc_installed = df_filtered[df_filtered['Parameter'] == 'New PLC order installed']['Value'].sum()
            col3.metric("PLC Orders Installed", f"{int(plc_installed)}")
        
        if 'DIA order disconnected' in df_filtered['Parameter'].values:
            dia_disconnected = df_filtered[df_filtered['Parameter'] == 'DIA order disconnected']['Value'].sum()
            col4.metric("DIA Disconnected", f"{int(dia_disconnected)}")
        
        st.divider()
        
        # Order Trends
        st.header("📊 Network Order Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'New DIA order installed' in df_filtered['Parameter'].values:
                dia_trend = df_filtered[df_filtered['Parameter'] == 'New DIA order installed'].sort_values('Date')
                fig_dia = px.line(dia_trend, x='Date', y='Value', title='DIA Orders Installed', height=400)
                st.plotly_chart(fig_dia, use_container_width=True)
        
        with col2:
            if 'New MPLS VPN order installed' in df_filtered['Parameter'].values:
                mpls_trend = df_filtered[df_filtered['Parameter'] == 'New MPLS VPN order installed'].sort_values('Date')
                fig_mpls = px.line(mpls_trend, x='Date', y='Value', title='MPLS VPN Installed', height=400)
                st.plotly_chart(fig_mpls, use_container_width=True)
    else:
        st.error("Network Team data not found. Please ensure NT_Department_Complete.csv is uploaded.")

# ============================================================================
# RESOURCE CHECK PAGE
# ============================================================================
elif page == "🔍 Resource Check":
    st.title("🔍 Resource Check Department Analytics")
    
    if resource_data is not None:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(resource_data['Date'].min().date(), resource_data['Date'].max().date()),
            min_value=resource_data['Date'].min().date(),
            max_value=resource_data['Date'].max().date()
        )
        
        df_filtered = resource_data[(resource_data['Date'].dt.date >= date_range[0]) & 
                                    (resource_data['Date'].dt.date <= date_range[1])]
        
        # Key Metrics
        st.header("�� Resource Check Overview")
        col1, col2, col3 = st.columns(3)
        
        if 'Checking through BOSS' in df_filtered['Parameter'].values:
            boss_checks = df_filtered[df_filtered['Parameter'] == 'Checking through BOSS']['Value'].sum()
            col1.metric("BOSS Checks", f"{int(boss_checks):,}")
        
        if 'Checking through email' in df_filtered['Parameter'].values:
            email_checks = df_filtered[df_filtered['Parameter'] == 'Checking through email']['Value'].sum()
            col2.metric("Email Checks", f"{int(email_checks):,}")
        
        if 'checking through excel' in df_filtered['Parameter'].values:
            excel_checks = df_filtered[df_filtered['Parameter'] == 'checking through excel']['Value'].sum()
            col3.metric("Excel Checks", f"{int(excel_checks):,}")
        
        st.divider()
        
        # Check Methods Trend
        st.header("📊 Resource Check Methods Trend")
        
        fig_resource = go.Figure()
        for method in ['Checking through BOSS', 'Checking through email', 'checking through excel']:
            if method in df_filtered['Parameter'].values:
                method_data = df_filtered[df_filtered['Parameter'] == method].sort_values('Date')
                fig_resource.add_trace(go.Scatter(
                    x=method_data['Date'], y=method_data['Value'], name=method, mode='lines+markers'
                ))
        
        fig_resource.update_layout(title="Resource Check Methods Over Time", height=400, template='plotly_white')
        st.plotly_chart(fig_resource, use_container_width=True)
    else:
        st.error("Resource Check data not found. Please ensure Resource_Check_Department.csv is uploaded.")

# ============================================================================
# SALES PAGE
# ============================================================================
elif page == "💼 Sales":
    st.title("💼 Sales Analytics")
    
    if sales_data is not None:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(sales_data['Date'].min().date(), sales_data['Date'].max().date()),
            min_value=sales_data['Date'].min().date(),
            max_value=sales_data['Date'].max().date()
        )
        
        df_filtered = sales_data[(sales_data['Date'].dt.date >= date_range[0]) & 
                                 (sales_data['Date'].dt.date <= date_range[1])]
        
        # Key Metrics
        st.header("📈 Sales Overview")
        
        billed_revenue = df_filtered[df_filtered['Metric'] == 'Billed Revenue']['Value'].sum()
        monthly_win = df_filtered[df_filtered['Metric'] == 'Monthly WIN - MRC']['Value'].sum()
        tcv = df_filtered[df_filtered['Metric'] == 'Monthly WIN - TCV']['Value'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Billed Revenue", f"${int(billed_revenue):,}")
        col2.metric("Total Monthly WIN (MRC)", f"${int(monthly_win):,}")
        col3.metric("Total TCV", f"${int(tcv):,}")
        
        st.divider()
        
        # Sales by Channel
        st.header("🏢 Sales by Channel")
        channel_sales = df_filtered[df_filtered['Metric'] == 'Billed Revenue'].groupby('Function')['Value'].sum().sort_values(ascending=False)
        
        fig_channels = px.pie(
            values=channel_sales.values, names=channel_sales.index,
            title='Billed Revenue by Sales Channel',
            height=400
        )
        st.plotly_chart(fig_channels, use_container_width=True)
        
        st.divider()
        
        # Revenue Trend
        st.header("📅 Revenue Trend")
        revenue_trend = df_filtered[df_filtered['Metric'] == 'Billed Revenue'].groupby('Date')['Value'].sum().reset_index()
        
        fig_revenue = px.line(revenue_trend, x='Date', y='Value', title='Billed Revenue Trend', height=400)
        st.plotly_chart(fig_revenue, use_container_width=True)
    else:
        st.error("Sales data not found. Please ensure Sales_Data_Complete_2022_2025.csv is uploaded.")

# ============================================================================
# CLOUD PAGE
# ============================================================================
elif page == "☁️ Cloud":
    st.title("☁️ Cloud Department Analytics")
    
    if cloud_data is not None:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(cloud_data['Date'].min().date(), cloud_data['Date'].max().date()),
            min_value=cloud_data['Date'].min().date(),
            max_value=cloud_data['Date'].max().date()
        )
        
        df_filtered = cloud_data[(cloud_data['Date'].dt.date >= date_range[0]) & 
                                 (cloud_data['Date'].dt.date <= date_range[1])]
        
        # Key Metrics
        st.header("📈 Cloud Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        if 'Active POC' in df_filtered['Parameter'].values:
            active_poc = df_filtered[df_filtered['Parameter'] == 'Active POC']['Value'].iloc[-1]
            col1.metric("Active POC", f"{int(active_poc)}")
        
        if 'uCPE for billed customers' in df_filtered['Parameter'].values:
            ucpe = df_filtered[df_filtered['Parameter'] == 'uCPE for billed customers']['Value'].iloc[-1]
            col2.metric("uCPE Billed Customers", f"{int(ucpe)}")
        
        if 'ECR for billed customers' in df_filtered['Parameter'].values:
            ecr = df_filtered[df_filtered['Parameter'] == 'ECR for billed customers']['Value'].iloc[-1]
            col3.metric("ECR Billed Customers", f"{int(ecr)}")
        
        if 'Fault cases reported by CS' in df_filtered['Parameter'].values:
            fault_cases = df_filtered[df_filtered['Parameter'] == 'Fault cases reported by CS']['Value'].sum()
            col4.metric("Fault Cases", f"{int(fault_cases)}")
        
        st.divider()
        
        # Cloud Trends
        st.header("📊 Cloud Metrics Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Active POC' in df_filtered['Parameter'].values:
                poc_trend = df_filtered[df_filtered['Parameter'] == 'Active POC'].sort_values('Date')
                fig_poc = px.line(poc_trend, x='Date', y='Value', title='Active POC Trend', height=400)
                st.plotly_chart(fig_poc, use_container_width=True)
        
        with col2:
            if 'uCPE for billed customers' in df_filtered['Parameter'].values:
                ucpe_trend = df_filtered[df_filtered['Parameter'] == 'uCPE for billed customers'].sort_values('Date')
                fig_ucpe = px.line(ucpe_trend, x='Date', y='Value', title='uCPE for Billed Customers', height=400)
                st.plotly_chart(fig_ucpe, use_container_width=True)
    else:
        st.error("Cloud data not found. Please ensure Cloud_Department_Complete.csv is uploaded.")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown(f"""
<p style='text-align: center; color: gray;'>
    <strong>Multi-Department Enterprise Dashboard v2.0</strong><br>
    Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}
</p>
""", unsafe_allow_html=True)
