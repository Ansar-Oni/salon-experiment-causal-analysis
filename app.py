
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Salon Experiment | Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>
.main {
    background-color: #f7f8fc;
}
.block-container {
    padding-top: 2rem;
}
[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    appointments = pd.read_csv(DATA / "appointments.csv")
    customers = pd.read_csv(DATA / "customers.csv")
    outlets = pd.read_csv(DATA / "outlets.csv")

    appointments["appointment_date"] = pd.to_datetime(
        appointments["appointment_date"], errors="coerce"
    )

    return appointments, customers, outlets


try:
    appointments, customers, outlets = load_data()
except Exception as e:
    st.error(f"Unable to load project data: {e}")
    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📊 Salon Analytics")
st.sidebar.caption("Experiment & Causal Analysis")

page = st.sidebar.radio(
    "Navigation",
    [
        "Project Overview",
        "Experiment Results",
        "Retention Analysis",
        "Revenue Analysis",
        "Customer Segmentation",
        "Data Explorer",
        "Methodology & Limitations"
    ]
)

st.sidebar.divider()
st.sidebar.info("Academic project using synthetic data.")

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.subheader("Dashboard Filters")

outlet_options = sorted(customers["outlet_id"].dropna().unique())
selected_outlets = st.sidebar.multiselect(
    "Select Outlets",
    outlet_options,
    default=outlet_options
)

frequency_options = sorted(customers["frequency_band"].dropna().unique())
selected_frequency = st.sidebar.multiselect(
    "Customer Frequency",
    frequency_options,
    default=frequency_options
)

filtered_customers = customers[
    customers["outlet_id"].isin(selected_outlets)
    & customers["frequency_band"].isin(selected_frequency)
].copy()

filtered_appointments = appointments[
    appointments["customer_id"].isin(filtered_customers["customer_id"])
].copy()

if filtered_customers.empty:
    st.warning("No records match the selected filters. Please change your filters.")
    st.stop()

# --------------------------------------------------
# COMMON CALCULATIONS
# --------------------------------------------------

retention = (
    filtered_customers.groupby("experiment_group")["retained_90d"]
    .mean()
    .mul(100)
    .reset_index(name="Retention Rate")
)

group_counts = filtered_customers["experiment_group"].value_counts()

treatment_rate = (
    filtered_customers.loc[
        filtered_customers["experiment_group"] == "Treatment",
        "retained_90d"
    ].mean() * 100
)

control_rate = (
    filtered_customers.loc[
        filtered_customers["experiment_group"] == "Control",
        "retained_90d"
    ].mean() * 100
)

retention_lift = treatment_rate - control_rate

revenue_data = (
    filtered_appointments[
        filtered_appointments["status"].astype(str).str.lower() == "completed"
    ]
    .groupby("customer_id")["revenue"]
    .sum()
    .reset_index(name="Total Revenue")
)

customer_revenue = filtered_customers[
    ["customer_id", "experiment_group"]
].merge(revenue_data, on="customer_id", how="left")

customer_revenue["Total Revenue"] = customer_revenue["Total Revenue"].fillna(0)

average_revenue = (
    customer_revenue.groupby("experiment_group")["Total Revenue"]
    .mean()
    .reset_index()
)

# --------------------------------------------------
# PROJECT OVERVIEW
# --------------------------------------------------

if page == "Project Overview":

    st.title("Salon Experiment & Causal Analysis")
    st.markdown(
        "### An interactive analytics dashboard for customer retention "
        "and personalised rebooking experiments."
    )

    st.warning(
        "Research disclaimer: This project uses synthetic data generated "
        "for academic and analytical demonstration. Results do not represent "
        "actual salon business performance."
    )

    st.subheader("Project Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", f"{len(filtered_customers):,}")
    col2.metric("Appointments", f"{len(filtered_appointments):,}")
    col3.metric("Treatment Customers",
                f"{(filtered_customers['experiment_group'] == 'Treatment').sum():,}")
    col4.metric("Retention Lift", f"{retention_lift:+.2f} pp")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Experiment Group Distribution")
        group_chart = (
            filtered_customers["experiment_group"]
            .value_counts()
            .reset_index()
        )
        group_chart.columns = ["Experiment Group", "Customers"]

        fig = px.pie(
            group_chart,
            names="Experiment Group",
            values="Customers",
            hole=0.55
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Customer Retention")
        fig = px.bar(
            retention,
            x="experiment_group",
            y="Retention Rate",
            color="experiment_group",
            text_auto=".2f",
            labels={
                "experiment_group": "Experiment Group",
                "Retention Rate": "Retention (%)"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Project Objectives")
    st.markdown("""
    - Evaluate personalised rebooking reminders.
    - Compare treatment and control group retention.
    - Analyse customer revenue patterns.
    - Identify differences across customer segments.
    - Demonstrate statistical and causal analysis techniques.
    """)

# --------------------------------------------------
# EXPERIMENT RESULTS
# --------------------------------------------------

elif page == "Experiment Results":

    st.title("Experiment Results")
    st.caption("Comparison of personalised reminders and standard communication.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Treatment Retention", f"{treatment_rate:.2f}%")
    col2.metric("Control Retention", f"{control_rate:.2f}%")
    col3.metric("Retention Difference", f"{retention_lift:+.2f} pp")

    st.divider()

    fig = px.bar(
        retention,
        x="experiment_group",
        y="Retention Rate",
        color="experiment_group",
        text_auto=".2f",
        title="Treatment vs Control Retention",
        labels={
            "experiment_group": "Experiment Group",
            "Retention Rate": "Retention (%)"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Experiment Group Sample Size")
    st.dataframe(
        filtered_customers["experiment_group"]
        .value_counts()
        .rename_axis("Experiment Group")
        .reset_index(name="Customer Count"),
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "The full project analysis reported a retention difference of "
        "+4.80 percentage points and a Difference-in-Differences estimate "
        "of +5.16 percentage points. These are synthetic-data findings."
    )

# --------------------------------------------------
# RETENTION ANALYSIS
# --------------------------------------------------

elif page == "Retention Analysis":

    st.title("Customer Retention Analysis")

    retention_table = (
        filtered_customers.groupby("experiment_group")
        .agg(
            Customers=("customer_id", "count"),
            Retained_Customers=("retained_90d", "sum"),
            Retention_Rate=("retained_90d", "mean")
        )
        .reset_index()
    )

    retention_table["Retention_Rate"] *= 100

    st.subheader("Retention by Experiment Group")

    fig = px.bar(
        retention_table,
        x="experiment_group",
        y="Retention_Rate",
        color="experiment_group",
        text_auto=".2f",
        labels={
            "experiment_group": "Experiment Group",
            "Retention_Rate": "Retention (%)"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Outlet-wise Retention")

    outlet_retention = (
        filtered_customers.groupby("outlet_id")["retained_90d"]
        .mean()
        .mul(100)
        .reset_index(name="Retention Rate")
    )

    fig = px.bar(
        outlet_retention,
        x="outlet_id",
        y="Retention Rate",
        labels={
            "outlet_id": "Outlet",
            "Retention Rate": "Retention (%)"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        retention_table,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# REVENUE ANALYSIS
# --------------------------------------------------

elif page == "Revenue Analysis":

    st.title("Revenue Analysis")

    st.caption("Revenue is calculated using completed appointments only.")

    col1, col2 = st.columns(2)

    treatment_revenue = customer_revenue.loc[
        customer_revenue["experiment_group"] == "Treatment",
        "Total Revenue"
    ].mean()

    control_revenue = customer_revenue.loc[
        customer_revenue["experiment_group"] == "Control",
        "Total Revenue"
    ].mean()

    col1.metric("Treatment Revenue / Customer", f"₹{treatment_revenue:,.2f}")
    col2.metric("Control Revenue / Customer", f"₹{control_revenue:,.2f}")

    fig = px.bar(
        average_revenue,
        x="experiment_group",
        y="Total Revenue",
        color="experiment_group",
        text_auto=".2f",
        title="Average Revenue per Customer",
        labels={
            "experiment_group": "Experiment Group",
            "Total Revenue": "Revenue (₹)"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Appointment Status Distribution")

    status_data = (
        filtered_appointments["status"]
        .value_counts()
        .reset_index()
    )
    status_data.columns = ["Appointment Status", "Count"]

    fig = px.pie(
        status_data,
        names="Appointment Status",
        values="Count",
        hole=0.45
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# CUSTOMER SEGMENTATION
# --------------------------------------------------

elif page == "Customer Segmentation":

    st.title("Customer Segmentation")

    segment_data = (
        filtered_customers.groupby(
            ["frequency_band", "experiment_group"]
        )["retained_90d"]
        .mean()
        .mul(100)
        .reset_index(name="Retention Rate")
    )

    fig = px.bar(
        segment_data,
        x="frequency_band",
        y="Retention Rate",
        color="experiment_group",
        barmode="group",
        text_auto=".2f",
        title="Retention by Customer Frequency",
        labels={
            "frequency_band": "Customer Frequency",
            "Retention Rate": "Retention (%)",
            "experiment_group": "Experiment Group"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Segment Summary")
    st.dataframe(segment_data, use_container_width=True, hide_index=True)

    st.info(
        "The original full-dataset analysis reported a +7.31 percentage-point "
        "retention difference for high-frequency customers and +3.45 points "
        "for low-frequency customers. Current filters may change the results."
    )

# --------------------------------------------------
# DATA EXPLORER
# --------------------------------------------------

elif page == "Data Explorer":

    st.title("Data Explorer")
    st.caption("Explore the underlying synthetic project datasets.")

    dataset_name = st.selectbox(
        "Choose Dataset",
        ["Customers", "Appointments", "Outlets"]
    )

    if dataset_name == "Customers":
        selected_data = filtered_customers
    elif dataset_name == "Appointments":
        selected_data = filtered_appointments
    else:
        selected_data = outlets[
            outlets["outlet_id"].isin(selected_outlets)
        ]

    st.write(f"Total records: {len(selected_data):,}")

    st.dataframe(
        selected_data.head(1000),
        use_container_width=True,
        hide_index=True
    )

    csv = selected_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Filtered CSV",
        data=csv,
        file_name=f"{dataset_name.lower()}_data.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# METHODOLOGY AND LIMITATIONS
# --------------------------------------------------

elif page == "Methodology & Limitations":

    st.title("Methodology & Limitations")

    st.subheader("Research Design")
    st.markdown("""
    This project evaluates personalised rebooking reminders against
    standard customer communication using a simulated experiment.

    **Analysis techniques include:**
    - A/B testing
    - Retention rate comparison
    - Difference-in-Differences (DiD)
    - CUPED adjustment
    - Sample Ratio Mismatch (SRM) testing
    - Customer segmentation
    - Revenue analysis
    """)

    st.subheader("Research Workflow")
    st.markdown("""
    1. Data collection and preparation
    2. Data cleaning and validation
    3. Exploratory data analysis
    4. Experiment group comparison
    5. Statistical analysis
    6. Interpretation and reporting
    """)

    st.subheader("Important Limitations")
    st.markdown("""
    - The dataset is synthetic and does not represent real customers.
    - The findings are illustrative, not verified commercial outcomes.
    - The Difference-in-Differences analysis uses only one pre-period.
    - Parallel trends cannot be empirically tested with one pre-period.
    - Results should not be interpreted as definitive real-world causal evidence.
    """)

    st.success("Dashboard generated from the project's local datasets.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "Salon Experiment & Causal Analysis | Academic Data Science Project | "
    "Synthetic Data"
)
