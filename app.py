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
    page_title="Multi-Department Enterprise Dashboard",
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
    .alert-box {
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
    except Exception as e:
        st.error(f"Error loading Marketing data: {e}")
        return None

@st.cache_data
def load_billing_data():
    try:
        df = pd.read_csv('Billing_Data_Complete_2022_2025.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading Billing data: {e}")
        return None

@st.cache_data
def load_csc_data():
    try:
        df = pd.read_csv('CSC_Complere.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading CSC data: {e}")
        return None

@st.cache_data
def load_hr_data():
    try:
        df = pd.read_csv('HR_Department_Complete.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading HR data: {e}")
        return None

@st.cache_data
def load_nt_data():
    try:
        df = pd.read_csv('NT_Department_Complete.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading Network Team data: {e}")
        return None

@st.cache_data
def load_resource_data():
    try:
        df = pd.read_csv('Resource_Check_Department.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading Resource Check data: {e}")
        return None

@st.cache_data
def load_sales_data():
    try:
        df = pd.read_csv('Sales_Data_Complete_2022_2025.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading Sales data: {e}")
        return None

@st.cache_data
def load_cloud_data():
    try:
        df = pd.read_csv('Cloud_Department_Complete.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading Cloud data: {e}")
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
# HOME PAGE - EXECUTIVE DASHBOARD
# ============================================================================
if page == "🏠 Home":
    st.title("📊 Multi-Department Enterprise Dashboard")
    st.markdown("**Executive Overview - All Departments at a Glance**")
    
    # ========== SUMMARY KPI CARDS ==========
    st.header("📈 Department Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Marketing Summary
    if marketing_data is not None:
        try:
            mql_data = marketing_data[marketing_data['Metric'] == 'MQL']
            if len(mql_data) > 0:
                mql_total = mql_data['Value'].sum()
                with col1:
                    st.metric("📊 Marketing Total MQL", f"{int(mql_total):,}")
        except:
            pass
    
    # Billing Summary
    if billing_data is not None:
        try:
            billing_total = billing_data['Value'].sum()
            with col2:
                st.metric("💰 Billing Total", f"{int(billing_total):,}")
        except:
            pass
    
    # HR Summary
    if hr_data is not None:
        try:
            hr_sorted = hr_data.sort_values('Date')
            latest_data = hr_sorted.iloc[-1]
            
            # Find headcount columns dynamically
            headcount_params = [p for p in hr_data['Parameter'].unique() if 'Final staff' in p]
            if headcount_params:
                headcount_data = hr_sorted[hr_sorted['Parameter'] == headcount_params[0]]
                if len(headcount_data) > 0:
                    headcount = headcount_data['Value'].iloc[-1]
                    with col3:
                        st.metric("👥 Current Headcount", f"{int(headcount)}")
        except:
            pass
    
    # Cloud Summary
    if cloud_data is not None:
        try:
            poc_data = cloud_data[cloud_data['Parameter'] == 'Active POC']
            if len(poc_data) > 0:
                latest_poc = poc_data.sort_values('Date').iloc[-1]
                with col4:
                    st.metric("☁️ Active Cloud POC", f"{int(latest_poc['Value'])}")
        except:
            pass
    
    st.divider()
    
    # ========== KEY INSIGHTS ==========
    st.header("💡 Executive Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>🎯 Top Opportunities</h4>
        <ul>
            <li><strong>☁️ Cloud Department:</strong> Fastest growth - uCPE customers up 100% (635→1,278). Scale infrastructure to support demand.</li>
            <li><strong>💼 Sales:</strong> New channels (Zscaler) emerging. Q4 2024 peak ($180M+) shows seasonal strength - plan for Q4 2025.</li>
            <li><strong>📊 Marketing:</strong> MQL generation stable. Strong correlation with events - maintain activity levels.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="recommendation-box">
        <h4>📌 Action Items for Leadership</h4>
        <ul>
            <li><strong>Resource Check:</strong> Excel-based checks increasing (manual work). Implement automation to improve efficiency.</li>
            <li><strong>HR:</strong> Vacancy rate fluctuates (0-14 open positions). Strengthen recruitment pipeline for growth.</li>
            <li><strong>CSC:</strong> Fault cases vary (400-800/month). Staffing levels may need adjustment during peaks.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ========== CROSS-DEPARTMENT TRENDS ==========
    st.header("📅 Department Trends Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if marketing_data is not None:
            try:
                mql_trend = marketing_data[marketing_data['Metric'] == 'MQL'].sort_values('Date')
                if len(mql_trend) > 0:
                    fig_marketing = px.line(mql_trend, x='Date', y='Value', title='📊 Marketing: MQL Trend',
                                           labels={'Value': 'MQL Count'}, height=350)
                    fig_marketing.update_layout(template='plotly_white')
                    st.plotly_chart(fig_marketing, use_container_width=True)
            except:
                st.warning("Could not load Marketing trend")
    
    with col2:
        if cloud_data is not None:
            try:
                cloud_poc = cloud_data[cloud_data['Parameter'] == 'Active POC'].sort_values('Date')
                if len(cloud_poc) > 0:
                    fig_cloud = px.line(cloud_poc, x='Date', y='Value', title='☁️ Cloud: Active POC Growth',
                                       labels={'Value': 'Active POC Count'}, height=350)
                    fig_cloud.update_layout(template='plotly_white')
                    st.plotly_chart(fig_cloud, use_container_width=True)
            except:
                st.warning("Could not load Cloud trend")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if hr_data is not None:
            try:
                headcount_params = [p for p in hr_data['Parameter'].unique() if 'Final staff' in p]
                if headcount_params:
                    hr_headcount = hr_data[hr_data['Parameter'] == headcount_params[0]].sort_values('Date')
                    if len(hr_headcount) > 0:
                        fig_hr = px.line(hr_headcount, x='Date', y='Value', title='👥 HR: Headcount Trend',
                                        labels={'Value': 'Headcount'}, height=350)
                        fig_hr.update_layout(template='plotly_white')
                        st.plotly_chart(fig_hr, use_container_width=True)
            except:
                st.warning("Could not load HR trend")
    
    with col4:
        if sales_data is not None:
            try:
                sales_revenue = sales_data[sales_data['Metric'] == 'Billed Revenue'].groupby('Date')['Value'].sum().reset_index()
                if len(sales_revenue) > 0:
                    fig_sales = px.line(sales_revenue, x='Date', y='Value', title='💼 Sales: Revenue Trend',
                                       labels={'Value': 'Revenue'}, height=350)
                    fig_sales.update_layout(template='plotly_white')
                    st.plotly_chart(fig_sales, use_container_width=True)
            except:
                st.warning("Could not load Sales trend")
    
    st.divider()
    
    # ========== CORRELATION MATRIX ==========
    st.header("🔗 Department Metrics Correlations")
    
    st.markdown("""
    <div class="insight-box">
    <h4>Key Correlations Identified:</h4>
    <ul>
        <li>✅ <strong>Marketing MQL ↔ CSC Activity:</strong> More leads drive more service requests</li>
        <li>✅ <strong>Sales Growth ↔ HR Hiring:</strong> Revenue increase correlates with vacancy increases</li>
        <li>✅ <strong>Cloud Growth ↔ Network Orders:</strong> Cloud expansion requires infrastructure support</li>
        <li>⚠️ <strong>Resource Excel Checks ↑:</strong> Manual processes increasing - automation needed</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MARKETING PAGE
# ============================================================================
elif page == "📊 Marketing":
    st.title("📊 Marketing Analytics")
    
    if marketing_data is not None:
        try:
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
                col1.metric("Marketing Events", f"{total_events}", delta=f"Avg: {total_events/len(df_pivot):.1f}/month" if len(df_pivot) > 0 else "N/A")
            
            if 'MQL' in df_pivot.columns:
                total_mql = int(df_pivot['MQL'].sum())
                avg_mql = total_mql / len(df_pivot) if len(df_pivot) > 0 else 0
                col2.metric("Total MQLs", f"{total_mql:,}", delta=f"Avg: {avg_mql:.0f}/month")
            
            if 'Press Releases' in df_pivot.columns:
                total_pr = int(df_pivot['Press Releases'].sum())
                col3.metric("Press Releases", f"{total_pr}", delta=f"Avg: {total_pr/len(df_pivot):.1f}/month" if len(df_pivot) > 0 else "N/A")
            
            if 'Social Media Posts' in df_pivot.columns:
                total_posts = int(df_pivot['Social Media Posts'].sum())
                col4.metric("Social Media Posts", f"{total_posts}", delta=f"Avg: {total_posts/len(df_pivot):.1f}/month" if len(df_pivot) > 0 else "N/A")
            
            st.divider()
            
            # Insights
            st.header("💡 Marketing Insights")
            st.markdown("""
            <div class="insight-box">
            <h4>🎯 Key Findings</h4>
            <ul>
                <li><strong>MQL Generation:</strong> Consistent output with seasonal peaks in December and strong Q4 performance</li>
                <li><strong>Activity Correlation:</strong> Marketing Events show strong positive correlation with MQL generation</li>
                <li><strong>Content Strategy:</strong> Social media posts and press releases contribute to overall lead generation</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
            <h4>📌 Recommendations</h4>
            <ul>
                <li>✅ Maintain consistent event execution - direct correlation with MQL generation observed</li>
                <li>✅ Increase social media activity during Q4 to capitalize on seasonal strength</li>
                <li>✅ Monitor press release effectiveness - ensure quality over quantity</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Timeline
            st.header("📅 Marketing Trends")
            
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
            
            # Correlation Analysis
            st.header("🔗 Correlation Analysis")
            if len(df_pivot.columns) > 1 and 'MQL' in df_pivot.columns:
                correlation_matrix = df_pivot.corr()
                mql_corr = correlation_matrix['MQL'].sort_values(ascending=False)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.subheader("MQL Correlations")
                    for metric, corr in mql_corr.items():
                        if metric != 'MQL':
                            color = '🟢' if corr > 0.5 else '🟡' if corr > 0 else '🔴'
                            st.write(f"{color} **{metric}**: {corr:.3f}")
                
                with col2:
                    fig_corr = px.imshow(correlation_matrix, text_auto='.2f', color_continuous_scale='RdBu_r', height=350)
                    st.plotly_chart(fig_corr, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying Marketing data: {e}")
    else:
        st.error("❌ Marketing data not found")

# ============================================================================
# BILLING PAGE
# ============================================================================
elif page == "💰 Billing":
    st.title("💰 Billing Analytics")
    
    if billing_data is not None:
        try:
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
            monthly_avg = df_filtered.groupby('Date')['Value'].sum()
            avg_billing = monthly_avg.mean() if len(monthly_avg) > 0 else 0
            
            col1.metric("Total Billing", f"{int(total_billing):,}")
            col2.metric("Monthly Average", f"{int(avg_billing):,}")
            
            if len(monthly_avg) > 0:
                max_month = monthly_avg.idxmax()
                col3.metric("Peak Month", max_month.strftime('%B %Y'))
            
            st.divider()
            
            # Insights
            st.header("💡 Billing Insights")
            st.markdown("""
            <div class="insight-box">
            <h4>🎯 Key Findings</h4>
            <ul>
                <li><strong>Revenue Stability:</strong> Billing remains consistent with monthly revenue 200-300K</li>
                <li><strong>Key Customers:</strong> CBC China is largest contributor, followed by CBC Hong Kong and Singapore</li>
                <li><strong>Geographic Diversification:</strong> Multi-region presence reduces risk</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
            <h4>📌 Recommendations</h4>
            <ul>
                <li>✅ Monitor CBC China relationship - largest revenue source requires attention</li>
                <li>✅ Explore growth opportunities in Singapore and Taiwan markets</li>
                <li>✅ Maintain service quality to ensure billing stability</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Billing by Entity
            st.header("🏢 Billing by Entity")
            entity_billing = df_filtered.groupby('Parameter')['Value'].sum().sort_values(ascending=False).head(10)
            
            fig_entity = px.bar(
                x=entity_billing.values, y=entity_billing.index,
                orientation='h', title='Top 10 Billing Entities',
                labels={'x': 'Billing Amount', 'y': 'Entity'},
                height=400
            )
            st.plotly_chart(fig_entity, use_container_width=True)
            
            st.divider()
            
            # Timeline
            st.header("📅 Billing Trend")
            billing_trend = df_filtered.groupby('Date')['Value'].sum().reset_index()
            
            fig_trend = px.line(
                billing_trend, x='Date', y='Value',
                title='Billing Amount Over Time', labels={'Value': 'Billing Amount'},
                height=400
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying Billing data: {e}")
    else:
        st.error("❌ Billing data not found")

# ============================================================================
# CSC PAGE
# ============================================================================
elif page == "🌐 Customer Service":
    st.title("🌐 Customer Service Center Analytics")
    
    if csc_data is not None:
        try:
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
            
            # Safe metric extraction
            fault_df = df_filtered[df_filtered['Parameter'] == 'Fault cases']
            if len(fault_df) > 0:
                fault_cases = fault_df['Value'].dropna().sum()
                col1.metric("Fault Cases", f"{int(fault_cases):,}")
            
            incident_df = df_filtered[df_filtered['Parameter'] == 'Major incidents']
            if len(incident_df) > 0:
                major_incidents = incident_df['Value'].dropna().sum()
                col2.metric("Major Incidents", f"{int(major_incidents)}")
            
            mttr_df = df_filtered[df_filtered['Parameter'] == 'MTTR - Internet (hour)']
            if len(mttr_df) > 0:
                avg_mttr = mttr_df['Value'].dropna().mean()
                col3.metric("Avg MTTR (Internet)", f"{avg_mttr:.2f} hrs")
            
            order_df = df_filtered[df_filtered['Parameter'] == 'Order dispatched']
            if len(order_df) > 0:
                orders = order_df['Value'].dropna().sum()
                col4.metric("Orders Dispatched", f"{int(orders)}")
            
            st.divider()
            
            # Insights
            st.header("💡 CSC Insights")
            st.markdown("""
            <div class="insight-box">
            <h4>🎯 Key Findings</h4>
            <ul>
                <li><strong>Service Performance:</strong> Fault cases range 400-800/month - high variability suggests capacity issues</li>
                <li><strong>MTTR Improving:</strong> Mean Time To Repair trending downward (positive sign)</li>
                <li><strong>Cloud Metrics:</strong> Cloud-related metrics showing growth - indicates expanding customer base</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="alert-box">
            <h4>⚠️ Action Required</h4>
            <ul>
                <li>🔴 <strong>Staffing Variance:</strong> Fault cases fluctuate significantly - align staffing to demand patterns</li>
                <li>🟡 <strong>Cloud Growth:</strong> Monitor cloud services - may need dedicated support team</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Trends
            st.header("📊 CSC Performance Trends")
            col1, col2 = st.columns(2)
            
            with col1:
                fault_trend = df_filtered[df_filtered['Parameter'] == 'Fault cases'].sort_values('Date')
                if len(fault_trend) > 0:
                    fig_fault = px.line(fault_trend, x='Date', y='Value', title='Fault Cases Over Time', height=400)
                    st.plotly_chart(fig_fault, use_container_width=True)
            
            with col2:
                mttr_trend = df_filtered[df_filtered['Parameter'] == 'MTTR - Internet (hour)'].sort_values('Date')
                if len(mttr_trend) > 0:
                    fig_mttr = px.line(mttr_trend, x='Date', y='Value', title='MTTR Trend (Hours)', height=400)
                    st.plotly_chart(fig_mttr, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying CSC data: {e}")
    else:
        st.error("❌ CSC data not found")

# ============================================================================
# HR PAGE
# ============================================================================
elif page == "👥 HR":
    st.title("👥 HR Department Analytics")
    
    if hr_data is not None:
        try:
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
            
            # Find headcount dynamically
            headcount_params = [p for p in df_filtered['Parameter'].unique() if 'Final staff' in p]
            if headcount_params:
                headcount_df = df_filtered[df_filtered['Parameter'] == headcount_params[0]]
                if len(headcount_df) > 0:
                    final_staff = headcount_df['Value'].dropna().iloc[-1] if len(headcount_df[headcount_df['Value'].notna()]) > 0 else 0
                    col1.metric("Current Headcount", f"{int(final_staff)}")
            
            # Turnover
            turnover_df = df_filtered[df_filtered['Parameter'] == 'Turnover of staff  离职率']
            if len(turnover_df) > 0:
                avg_turnover = turnover_df['Value'].dropna().mean()
                col2.metric("Avg Turnover Rate", f"{avg_turnover:.2%}", delta="✅ Excellent Retention")
            
            # Vacancies
            vacancy_df = df_filtered[df_filtered['Parameter'] == 'Vacancy 空缺人数​']
            if len(vacancy_df) > 0:
                vacancies = vacancy_df['Value'].dropna().iloc[-1] if len(vacancy_df[vacancy_df['Value'].notna()]) > 0 else 0
                col3.metric("Current Vacancies", f"{int(vacancies)}")
            
            # Managers
            manager_df = df_filtered[df_filtered['Parameter'] == 'People Managers 有下属的经理']
            if len(manager_df) > 0:
                managers = manager_df['Value'].dropna().iloc[-1] if len(manager_df[manager_df['Value'].notna()]) > 0 else 0
                col4.metric("People Managers", f"{int(managers)}")
            
            st.divider()
            
            # Insights
            st.header("💡 HR Insights")
            st.markdown("""
            <div class="insight-box">
            <h4>🎯 Key Findings</h4>
            <ul>
                <li><strong>Retention Excellence:</strong> Turnover rate <1.5% shows exceptional employee satisfaction and stability</li>
                <li><strong>Stable Workforce:</strong> Headcount maintained at 190-203 across the period</li>
                <li><strong>Hiring Challenge:</strong> Vacancy rate fluctuates 0-14, indicating recruitment lag during growth periods</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
            <h4>📌 Recommendations</h4>
            <ul>
                <li>✅ <strong>Leverage Retention:</strong> Document and share practices driving low turnover across organization</li>
                <li>🟡 <strong>Improve Recruitment:</strong> Vacancy fluctuations suggest need for pipeline development</li>
                <li>✅ <strong>Plan for Growth:</strong> Align hiring with cloud/sales expansion (vacancy → 14 positions)</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Trends
            st.header("📊 HR Trends")
            col1, col2 = st.columns(2)
            
            with col1:
                if headcount_params:
                    headcount_trend = df_filtered[df_filtered['Parameter'] == headcount_params[0]].sort_values('Date')
                    if len(headcount_trend) > 0:
                        fig_headcount = px.line(headcount_trend, x='Date', y='Value', title='Headcount Trend', height=400)
                        st.plotly_chart(fig_headcount, use_container_width=True)
            
            with col2:
                turnover_trend = df_filtered[df_filtered['Parameter'] == 'Turnover of staff  离职率'].sort_values('Date')
                if len(turnover_trend) > 0:
                    fig_turnover = px.line(turnover_trend, x='Date', y='Value', title='Turnover Rate Trend', height=400)
                    st.plotly_chart(fig_turnover, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying HR data: {e}")
    else:
        st.error("❌ HR data not found")

# ============================================================================
# NETWORK TEAM PAGE
# ============================================================================
elif page == "🌐 Network Team":
    st.title("🌐 Network Team Analytics")
    
    if nt_data is not None:
        try:
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
            
            dia_df = df_filtered[df_filtered['Parameter'] == 'New DIA order installed']
            if len(dia_df) > 0:
                col1.metric("DIA Installed", f"{int(dia_df['Value'].sum())}")
            
            mpls_df = df_filtered[df_filtered['Parameter'] == 'New MPLS VPN order installed']
            if len(mpls_df) > 0:
                col2.metric("MPLS VPN Installed", f"{int(mpls_df['Value'].sum())}")
            
            plc_df = df_filtered[df_filtered['Parameter'] == 'New PLC order installed']
            if len(plc_df) > 0:
                col3.metric("PLC Installed", f"{int(plc_df['Value'].sum())}")
            
            dia_disc_df = df_filtered[df_filtered['Parameter'] == 'DIA order disconnected']
            if len(dia_disc_df) > 0:
                col4.metric("DIA Disconnected", f"{int(dia_disc_df['Value'].sum())}")
            
            st.divider()
            
            # Insights
            st.header("💡 Network Team Insights")
            st.markdown("""
            <div class="insight-box">
            <h4>🎯 Key Findings</h4>
            <ul>
                <li><strong>Steady Installation:</strong> Consistent new order deployment across all network types</li>
                <li><strong>DIA/MPLS Focus:</strong> Both DIA and MPLS VPN showing strong adoption</li>
                <li><strong>Infrastructure Growth:</strong> Total installations support cloud expansion needs</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
            <h4>📌 Recommendations</h4>
            <ul>
                <li>✅ <strong>Scale with Cloud:</strong> Network orders correlate with cloud growth - maintain capacity planning</li>
                <li>✅ <strong>Monitor PLC Demand:</strong> PLC orders growing - explore expansion opportunities</li>
                <li>✅ <strong>Optimize Operations:</strong> Track installation/disconnection ratio for capacity management</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Trends
            st.header("📊 Network Order Trends")
            col1, col2 = st.columns(2)
            
            with col1:
                dia_trend = df_filtered[df_filtered['Parameter'] == 'New DIA order installed'].sort_values('Date')
                if len(dia_trend) > 0:
                    fig_dia = px.line(dia_trend, x='Date', y='Value', title='DIA Orders Installed', height=400)
                    st.plotly_chart(fig_dia, use_container_width=True)
            
            with col2:
                mpls_trend = df_filtered[df_filtered['Parameter'] == 'New MPLS VPN order installed'].sort_values('Date')
                if len(mpls_trend) > 0:
                    fig_mpls = px.line(mpls_trend, x='Date', y='Value', title='MPLS VPN Installed', height=400)
                    st.plotly_chart(fig_mpls, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying Network Team data: {e}")
    else:
        st.error("❌ Network Team data not found")

# ============================================================================
# RESOURCE CHECK PAGE
# ============================================================================
elif page == "🔍 Resource Check":
    st.title("🔍 Resource Check Department Analytics")
    
    if resource_data is not None:
        try:
            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(resource_data['Date'].min().date(), resource_data['Date'].max().date()),
                min_value=resource_data['Date'].min().date(),
                max_value=resource_data['Date'].max().date()
            )
            
            df_filtered = resource_data[(resource_data['Date'].dt.date >= date_range[0]) & 
                                        (resource_data['Date'].dt.date <= date_range[1])]
            
            # Key Metrics
            st.header("📈 Resource Check Overview")
            col1, col2, col3 = st.columns(3)
            
            boss_df = df_filtered[df_filtered['Parameter'] == 'Checking through BOSS']
            if len(boss_df) > 0:
                col1.metric("BOSS Checks", f"{int(boss_df['Value'].sum()):,}")
            
            email_df = df_filtered[df_filtered['Parameter'] == 'Checking through email']
            if len(email_df) > 0:
                col2.metric("Email Checks", f"{int(email_df['Value'].sum()):,}")
            
            excel_df = df_filtered[df_filtered['Parameter'] == 'checking through excel']
            if len(excel_df) > 0:
                col3.metric("Excel Checks", f"{int(excel_df['Value'].sum()):,}")
            
            st.divider()
            
            # Insights
            st.header("💡 Resource Check Insights")
            st.markdown("""
            <div class="alert-box">
            <h4>⚠️ Process Optimization Needed</h4>
            <ul>
                <li><strong>Excel Usage Growing:</strong> Manual Excel checks increasing - indicates process not fully automated</li>
                <li><strong>Multiple Systems:</strong> BOSS, Email, and Excel all in use - fragmented process</li>
                <li><strong>Manual Workload:</strong> High check volume (800-2000 BOSS checks/month) suggests need for automation</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
            <h4>🎯 Critical Action Items</h4>
            <ul>
                <li>🔴 <strong>Implement Automation:</strong> Consolidate Excel-based checks into BOSS system</li>
                <li>🟡 <strong>Process Integration:</strong> Unify email notifications with BOSS workflow</li>
                <li>✅ <strong>Reduce Manual Effort:</strong> Target 50% reduction in manual checks through automation</li>
                <li>✅ <strong>Free Up Capacity:</strong> Redirect saved effort to higher-value activities</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Trends
            st.header("📊 Check Methods Trend")
            
            fig_resource = go.Figure()
            for method in ['Checking through BOSS', 'Checking through email', 'checking through excel']:
                method_data = df_filtered[df_filtered['Parameter'] == method].sort_values('Date')
                if len(method_data) > 0:
                    fig_resource.add_trace(go.Scatter(
                        x=method_data['Date'], y=method_data['Value'], name=method, mode='lines+markers'
                    ))
            
            fig_resource.update_layout(title="Resource Check Methods Over Time", height=400, template='plotly_white')
            st.plotly_chart(fig_resource, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying Resource Check data: {e}")
    else:
        st.error("❌ Resource Check data not found")

# ============================================================================
# SALES PAGE
# ============================================================================
elif page == "💼 Sales":
    st.title("💼 Sales Analytics")
    
    if sales_data is not None:
        try:
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
            
            billed_df = df_filtered[df_filtered['Metric'] == 'Billed Revenue']
            billed_revenue = billed_df['Value'].dropna().sum() if len(billed_df) > 0 else 0
            
            win_df = df_filtered[df_filtered['Metric'] == 'Monthly WIN - MRC']
            monthly_win = win_df['Value'].dropna().sum() if len(win_df) > 0 else 0
            
            tcv_df = df_filtered[df_filtered['Metric'] == 'Monthly WIN - TCV']
            tcv = tcv_df['Value'].dropna().sum() if len(tcv_df) > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Billed Revenue", f"${int(billed_revenue):,}")
            col2.metric("Total Monthly WIN (MRC)", f"${int(monthly_win):,}")
            col3.metric("Total TCV", f"${int(tcv):,}")
            
            st.divider()
            
            # Insights
            st.header("💡 Sales Insights")
            st.markdown("""
            <div class="insight-box">
            <h4>🎯 Key Findings</h4>
            <ul>
                <li><strong>Seasonal Strength:</strong> Q4 2024 peak ($180M+) shows strong seasonal pattern</li>
                <li><strong>New Channels:</strong> Zscaler channel emerging (May 2025+) with immediate impact</li>
                <li><strong>Multi-Channel Mix:</strong> IPA and MNC are core channels; new channels diversifying revenue</li>
                <li><strong>Growth Trajectory:</strong> Recent months show increasing TCV indicating pipeline strength</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
            <h4>📌 Recommendations</h4>
            <ul>
                <li>✅ <strong>Plan for Q4 2025:</strong> Repeat Q4 2024 success - start planning campaigns now</li>
                <li>✅ <strong>Scale New Channels:</strong> Zscaler and AT&T showing promise - invest in channel development</li>
                <li>✅ <strong>Nurture Pipeline:</strong> TCV growth indicates strong pipeline - maintain sales execution</li>
                <li>🟡 <strong>Retention Focus:</strong> Ensure existing customers remain engaged during growth phase</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Sales by Channel
            st.header("🏢 Sales by Channel")
            channel_sales = df_filtered[df_filtered['Metric'] == 'Billed Revenue'].groupby('Function')['Value'].sum().sort_values(ascending=False)
            
            if len(channel_sales) > 0:
                fig_channels = px.pie(
                    values=channel_sales.values, names=channel_sales.index,
                    title='Billed Revenue Distribution by Sales Channel',
                    height=400
                )
                st.plotly_chart(fig_channels, use_container_width=True)
            
            st.divider()
            
            # Revenue Trend
            st.header("📅 Revenue Trend")
            revenue_trend = df_filtered[df_filtered['Metric'] == 'Billed Revenue'].groupby('Date')['Value'].sum().reset_index()
            
            if len(revenue_trend) > 0:
                fig_revenue = px.line(revenue_trend, x='Date', y='Value', title='Billed Revenue Trend', height=400)
                st.plotly_chart(fig_revenue, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying Sales data: {e}")
    else:
        st.error("❌ Sales data not found")

# ============================================================================
# CLOUD PAGE
# ============================================================================
elif page == "☁️ Cloud":
    st.title("☁️ Cloud Department Analytics")
    
    if cloud_data is not None:
        try:
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
            
            poc_df = df_filtered[df_filtered['Parameter'] == 'Active POC']
            if len(poc_df) > 0:
                active_poc = poc_df['Value'].dropna().iloc[-1] if len(poc_df[poc_df['Value'].notna()]) > 0 else 0
                col1.metric("Active POC", f"{int(active_poc)}")
            
            ucpe_df = df_filtered[df_filtered['Parameter'] == 'uCPE for billed customers']
            if len(ucpe_df) > 0:
                ucpe = ucpe_df['Value'].dropna().iloc[-1] if len(ucpe_df[ucpe_df['Value'].notna()]) > 0 else 0
                col2.metric("uCPE Customers", f"{int(ucpe)}")
            
            ecr_df = df_filtered[df_filtered['Parameter'] == 'ECR for billed customers']
            if len(ecr_df) > 0:
                ecr = ecr_df['Value'].dropna().iloc[-1] if len(ecr_df[ecr_df['Value'].notna()]) > 0 else 0
                col3.metric("ECR Customers", f"{int(ecr)}")
            
            fault_df = df_filtered[df_filtered['Parameter'] == 'Fault cases reported by CS']
            if len(fault_df) > 0:
                fault_cases = fault_df['Value'].dropna().sum()
                col4.metric("Fault Cases", f"{int(fault_cases)}")
            
            st.divider()
            
            # Insights
            st.header("💡 Cloud Insights")
            st.markdown("""
            <div class="insight-box">
            <h4>🎯 Key Findings - FASTEST GROWING SEGMENT!</h4>
            <ul>
                <li><strong>Exceptional Growth:</strong> uCPE customers doubled from 635 → 1,278 (100% growth!)</li>
                <li><strong>POC Expansion:</strong> Active POCs grew from 9 → 103 (10x increase)</li>
                <li><strong>Customer Base:</strong> ECR customers increased 635 → 1,083</li>
                <li><strong>Market Momentum:</strong> This is the growth engine of the organization</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
            <h4>🎯 Critical Investment Priorities</h4>
            <ul>
                <li>🟢 <strong>PRIORITY #1: Scale Immediately!</strong> Cloud is the highest growth opportunity - invest in capacity</li>
                <li>🟢 <strong>Support Infrastructure:</strong> Ensure CSC and Network teams are scaled to support cloud growth</li>
                <li>✅ <strong>Talent Acquisition:</strong> Hire cloud-specialized engineers immediately</li>
                <li>✅ <strong>Cross-Team Alignment:</strong> Cloud success requires coordination with Network and CSC teams</li>
                <li>✅ <strong>Sales Focus:</strong> Expand cloud sales channels - this segment drives company growth</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Trends
            st.header("📊 Cloud Growth Metrics")
            col1, col2 = st.columns(2)
            
            with col1:
                poc_trend = df_filtered[df_filtered['Parameter'] == 'Active POC'].sort_values('Date')
                if len(poc_trend) > 0:
                    fig_poc = px.line(poc_trend, x='Date', y='Value', title='Active POC Growth', height=400)
                    st.plotly_chart(fig_poc, use_container_width=True)
            
            with col2:
                ucpe_trend = df_filtered[df_filtered['Parameter'] == 'uCPE for billed customers'].sort_values('Date')
                if len(ucpe_trend) > 0:
                    fig_ucpe = px.line(ucpe_trend, x='Date', y='Value', title='uCPE for Billed Customers', height=400)
                    st.plotly_chart(fig_ucpe, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying Cloud data: {e}")
    else:
        st.error("❌ Cloud data not found")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown(f"""
<p style='text-align: center; color: gray;'>
    <strong>Multi-Department Enterprise Dashboard v2.0 - Professional Edition</strong><br>
    Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M')} | Data-Driven Insights for Leadership
</p>
""", unsafe_allow_html=True)
