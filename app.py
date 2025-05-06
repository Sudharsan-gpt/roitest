# Filename: app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Maritime App ROI Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom CSS for futuristic UI -------------------
custom_css = """
<style>
    /* Main Background and Text */
    [data-testid="stAppViewContainer"] {
        background-color: #ebeced;
        color: #4A4A4A;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        padding-top: 1rem;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #212529;
        font-family: 'Arial', sans-serif;
        font-weight: 600;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stMetricLabel"] {
        color: #6C757D;
        font-size: 1rem !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #212529;
        font-size: 1.5rem !important;
        font-weight: bold;
    }

    /* Cards */
    .css-1r6slb0 {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Checkbox color */
    [data-testid="stCheckbox"] {
        color: #00C897;
    }

    /* Chart backgrounds */
    .js-plotly-plot {
        background-color: #FFFFFF;
        border-radius: 8px;
    }

    /* Button styling */
    button[kind="primary"] {
        background-color: #00B2FF;
        border-radius: 4px;
    }

    /* Divider lines */
    hr {
        border-color: #DEE2E6;
    }
    
    /* Card container */
    .card-container {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Application selection panel */
    .app-selection-panel {
        background-color: #F1F3F5;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
        border-left: 3px solid #00B2FF;
    }
    
    /* Slider color */
    .stSlider > div > div > div {
        background-color: #00B2FF !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ----------------- Title and Subtitle -------------------
col_title_left, col_title_right = st.columns([3, 1])
with col_title_left:
    st.markdown("<h1 style='font-size:32px;'>🌊 Maritime Applications ROI Calculator</h1>", unsafe_allow_html=True)
with col_title_right:
    view_3_years = st.checkbox("View 3-Year ROI", value=False)

# ----------------- Sidebar Inputs -------------------
st.sidebar.markdown("<h3 style='color:#212529;'>🛠️ Input Parameters</h3>", unsafe_allow_html=True)

fleet_size = st.sidebar.number_input("Fleet Size", min_value=1, value=10, step=1)
fuel_price = st.sidebar.number_input("Fuel Price ($/MT)", min_value=1.0, value=550.0)
daily_consumption = st.sidebar.number_input("Daily Avg Fuel Consumption per Vessel (MT)", min_value=1.0, value=50.0)
operating_days = st.sidebar.number_input("Operating Days", min_value=1, value=330, step=1)

# ----------------- Customizable Applications -------------------
st.sidebar.markdown("<h3 style='color:#212529;'>📋 Application Settings</h3>", unsafe_allow_html=True)

# Define applications with their respective ranges and default values
applications = {
    "Hull Maintainance App": {"min": 0.0, "max": 8.0, "default": 3.0, "icon": "🛥️", "default_license": 150},
    "Voyage Optimization App": {"min": 0.0, "max": 6.0, "default": 1.0, "icon": "🧭", "default_license": 200},
    "Emission App": {"min": 0.0, "max": 5.0, "default": 0.5, "icon": "🌿", "default_license": 75},
    "Performance App": {"min": 0.0, "max": 8.0, "default": 0.5, "icon": "📊", "default_license": 75},
    "Vessel Scorecard": {"min": 0.0, "max": 5.0, "default": 0.5, "icon": "☁️", "default_license": 50},
    "Propulsion Pro": {"min": 0.0, "max": 5.0, "default": 0.2, "icon": "⛽", "default_license": 50}
}

# Store selected applications, their saving percentages, and license costs
selected_apps = {}
app_savings = {}
app_license_costs = {}

# Create three columns for application selection, saving percentages, and license costs
app_col1, app_col2, app_col3 = st.columns([1, 1, 1])

with app_col1:
    st.markdown("""
    <div class="app-selection-panel">
        <h3 style='font-size:18px;'>Select Applications</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create checkboxes for applications
    for app_name, app_info in applications.items():
        selected = st.checkbox(f"{app_info['icon']} {app_name}", value=(app_info['default'] > 0))
        selected_apps[app_name] = selected

with app_col2:
    st.markdown("""
    <div class="app-selection-panel">
        <h3 style='font-size:18px;'>Savings Potential (%)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create sliders for saving percentages (only shown for selected applications)
    for app_name, app_info in applications.items():
        if selected_apps[app_name]:
            app_savings[app_name] = st.slider(
                f"{app_info['icon']} {app_name} Saving %", 
                app_info['min'], 
                app_info['max'], 
                app_info['default']
            )
        else:
            app_savings[app_name] = 0.0

with app_col3:
    st.markdown("""
    <div class="app-selection-panel">
        <h3 style='font-size:18px;'>License Cost ($/vessel/month)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create number inputs for license costs (only shown for selected applications)
    for app_name, app_info in applications.items():
        if selected_apps[app_name]:
            app_license_costs[app_name] = st.number_input(
                f"{app_info['icon']} {app_name} License",
                min_value=0.0,
                value=float(app_info['default_license']),
                step=10.0,
                format="%.0f"
            )
        else:
            app_license_costs[app_name] = 0.0

# Calculate total license cost per vessel per month
license_cost_per_vessel_per_month = sum(app_license_costs.values())

# ----------------- Core Calculations -------------------
license_cost_annual = fleet_size * license_cost_per_vessel_per_month * 12
baseline_fuel_cost = fleet_size * daily_consumption * operating_days * fuel_price

# Calculate savings for each application
app_saving_amounts = {}
total_savings = 0

for app_name in applications.keys():
    saving_percentage = app_savings[app_name]
    saving_amount = baseline_fuel_cost * saving_percentage / 100
    app_saving_amounts[app_name] = saving_amount
    total_savings += saving_amount

# Calculate ROI metrics
payback_years = license_cost_annual / total_savings if total_savings else np.nan
payback_months = payback_years * 12 if payback_years else np.nan
roi_percent = ((total_savings - license_cost_annual) / license_cost_annual) * 100 if license_cost_annual else np.nan

# Calculate environmental impact
fuel_saved = sum(app_saving_amounts.values()) / fuel_price
emissions_reduced = fuel_saved * 3.114  # Tons of CO2 saved

# For 3-year view
if view_3_years:
    license_cost_total = license_cost_annual * 3
    total_savings_3yr = total_savings * 3
    roi_percent_3yr = ((total_savings_3yr - license_cost_total) / license_cost_total) * 100 if license_cost_total else np.nan
    fuel_saved_3yr = fuel_saved * 3
    emissions_reduced_3yr = emissions_reduced * 3
    
    # Create year-by-year data for chart
    years = [1, 2, 3]
    yearly_savings = [total_savings] * 3
    yearly_roi = [roi_percent, ((total_savings * 2 - license_cost_annual * 2) / (license_cost_annual * 2)) * 100, roi_percent_3yr]
    yearly_fuel_saved = [fuel_saved] * 3
    cumulative_savings = [total_savings, total_savings * 2, total_savings * 3]

# ----------------- UI Display -------------------
st.markdown("<hr>", unsafe_allow_html=True)

# Display total license cost per vessel per month
st.markdown(f"""
<div class="card-container">
    <h3 style='font-size:20px;'>💼 Total License Cost Per Vessel: ${license_cost_per_vessel_per_month:.0f}/month</h3>
</div>
""", unsafe_allow_html=True)

# --- Display key metrics in two rows ---
st.markdown("""
<div class="card-container">
    <h3 style='font-size:20px;'>📈 Key Performance Metrics</h3>
</div>
""", unsafe_allow_html=True)

# First row of metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Baseline Fuel Cost",
        value=f"${baseline_fuel_cost:,.0f}"
    )

with col2:
    annual_or_total = "Total 3-Year" if view_3_years else "Annual"
    savings_value = total_savings_3yr if view_3_years else total_savings
    st.metric(
        label=f"{annual_or_total} Savings",
        value=f"${savings_value:,.0f}"
    )

with col3:
    license_cost_value = license_cost_total if view_3_years else license_cost_annual
    period = "3 Years" if view_3_years else "Year"
    st.metric(
        label=f"License Cost (${period})",
        value=f"${license_cost_value:,.0f}"
    )

# Second row of metrics
col4, col5, col6 = st.columns(3)

with col4:
    roi_value = roi_percent_3yr if view_3_years else roi_percent
    st.metric(
        label="Return on Investment",
        value=f"{roi_value:.1f}%"
    )

with col5:
    st.metric(
        label="Payback Period",
        value=f"{payback_months:.1f} Months"
    )

with col6:
    emissions_value = emissions_reduced_3yr if view_3_years else emissions_reduced
    st.metric(
        label="Emissions Reduced",
        value=f"{emissions_value:,.0f} tCO₂"
    )

# Create two columns for visualizations
viz_col1, viz_col2 = st.columns(2)

# --- Bar Chart for Savings by Application ---
with viz_col1:
    st.markdown("""
    <div class="card-container">
        <h3 style='font-size:18px;'>💰 Savings by Application</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter out applications with zero savings
    filtered_app_savings = {app: amount for app, amount in app_saving_amounts.items() if amount > 0}
    
    if filtered_app_savings:
        saving_data = pd.DataFrame({
            "Application": list(filtered_app_savings.keys()),
            "Annual Savings ($)": list(filtered_app_savings.values())
        })
        
        # Add application icons to labels
        saving_data["App with Icon"] = saving_data["Application"].apply(
            lambda x: f"{applications[x]['icon']} {x}"
        )
        
        fig = px.bar(
            saving_data,
            x="App with Icon",
            y="Annual Savings ($)",
            text_auto=".2s",
            color="Application",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        
        fig.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(color="#212529"),
            xaxis=dict(title="", tickangle=-45),
            margin=dict(l=20, r=20, t=20, b=20),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No applications selected with savings. Please select at least one application.")

# --- Pie Chart for Savings Distribution ---
with viz_col2:
    st.markdown("""
    <div class="card-container">
        <h3 style='font-size:18px;'>📊 Savings Distribution</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if filtered_app_savings:
        fig2 = px.pie(
            saving_data,
            values="Annual Savings ($)",
            names="App with Icon",
            template="plotly_dark",
            hole=0.4,
            color="Application",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        
        fig2.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(color="#212529"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=20, b=20),
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No applications selected with savings. Please select at least one application.")

# --- License Cost Breakdown Chart ---
st.markdown("""
<div class="card-container">
    <h3 style='font-size:18px;'>💵 Monthly License Cost Breakdown</h3>
</div>
""", unsafe_allow_html=True)

# Filter out applications with zero license cost
filtered_app_licenses = {app: cost for app, cost in app_license_costs.items() if cost > 0 and selected_apps[app]}

if filtered_app_licenses:
    license_data = pd.DataFrame({
        "Application": list(filtered_app_licenses.keys()),
        "Monthly License Cost ($)": list(filtered_app_licenses.values())
    })
    
    # Add application icons to labels
    license_data["App with Icon"] = license_data["Application"].apply(
        lambda x: f"{applications[x]['icon']} {x}"
    )
    
    fig_license = px.bar(
        license_data,
        x="App with Icon",
        y="Monthly License Cost ($)",
        text_auto=True,
        color="Application",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Pastel1
    )
    
    fig_license.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#212529"),
        xaxis=dict(title="", tickangle=-45),
        margin=dict(l=20, r=20, t=20, b=20),
        height=300
    )
    
    st.plotly_chart(fig_license, use_container_width=True)
else:
    st.info("No applications selected with license costs. Please select at least one application.")

# --- Year-on-Year ROI Chart (only when 3-Year ROI is selected) ---
if view_3_years:
    st.markdown("""
    <div class="card-container">
        <h3 style='font-size:18px;'>📈 3-Year Performance Metrics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create subplot with dual y-axis
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add cumulative savings bars
    fig3.add_trace(
        go.Bar(
            x=years,
            y=cumulative_savings,
            name="Cumulative Savings ($)",
            marker_color="#00B2FF",
            opacity=0.7
        ),
        secondary_y=False
    )
    
    # Add ROI line
    fig3.add_trace(
        go.Scatter(
            x=years,
            y=yearly_roi,
            name="ROI (%)",
            marker_color="#FF5733",
            mode="lines+markers",
            line=dict(width=3)
        ),
        secondary_y=True
    )
    
    # Add fuel saved markers
    fig3.add_trace(
        go.Scatter(
            x=years,
            y=[y/1000 for y in yearly_fuel_saved],  # Convert to thousands for better scale
            name="Fuel Saved (K MT)",
            marker_color="#33FF57",
            mode="markers",
            marker=dict(size=12, symbol="diamond")
        ),
        secondary_y=True
    )
    
    # Update layout
    fig3.update_layout(
        title="Year-on-Year Performance",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#212529"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=50, b=50),
        height=450,
        barmode="group",
        xaxis=dict(
            title="Year",
            tickvals=[1, 2, 3]
        )
    )
    
    # Set y-axes titles
    fig3.update_yaxes(title_text="Cumulative Savings ($)", secondary_y=False, color="#00B2FF")
    fig3.update_yaxes(title_text="ROI (%) / Fuel Saved (K MT)", secondary_y=True, color="#FF5733")
    
    st.plotly_chart(fig3, use_container_width=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #7A8999; font-size: 0.8rem;">
    ⚓ Built for Maritime Digitalization | Futuristic Dashboard v2.0
</div>
""", unsafe_allow_html=True)
