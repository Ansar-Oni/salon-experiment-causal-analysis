# ==========================================
# SALON EXPERIMENT - SYNTHETIC DATA GENERATOR
# ==========================================

import numpy as np
import pandas as pd
from pathlib import Path

# Reproducibility: same random data every time
np.random.seed(42)

# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

# Create data folder if it does not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Basic project settings
NUM_OUTLETS = 22
NUM_CUSTOMERS = 10000

print("Salon synthetic data generator initialized.")
print(f"Number of outlets: {NUM_OUTLETS}")
print(f"Number of customers: {NUM_CUSTOMERS}")
print(f"Data folder: {DATA_DIR}")
# ==========================================
# PART 2: GENERATE OUTLETS AND CUSTOMERS
# ==========================================

# Generate 22 salon outlets
outlets = pd.DataFrame({
    "outlet_id": [f"OUT_{i:02d}" for i in range(1, NUM_OUTLETS + 1)],
    "city": ["Coimbatore"] * NUM_OUTLETS
})

# Generate 10,000 customers
customers = pd.DataFrame({
    "customer_id": [f"CUST_{i:05d}" for i in range(1, NUM_CUSTOMERS + 1)],
    "outlet_id": np.random.choice(
        outlets["outlet_id"],
        size=NUM_CUSTOMERS
    ),
    "baseline_visits": np.random.poisson(
        lam=3,
        size=NUM_CUSTOMERS
    )
})

# Create customer frequency segments
customers["frequency_band"] = np.where(
    customers["baseline_visits"] >= 4,
    "High",
    "Low"
)

# ==========================================
# RANDOMIZE CUSTOMERS INTO TWO GROUPS
# ==========================================

customers["experiment_group"] = ""

# Stratified randomization:
# Randomize separately within each outlet and frequency group
for _, group in customers.groupby(["outlet_id", "frequency_band"]):

    customer_indices = group.index.to_numpy().copy()

    np.random.shuffle(customer_indices)

    split_point = len(customer_indices) // 2

    treatment_indices = customer_indices[:split_point]
    control_indices = customer_indices[split_point:]

    customers.loc[treatment_indices, "experiment_group"] = "Treatment"
    customers.loc[control_indices, "experiment_group"] = "Control"

# Display results
print("\nOutlets generated:", len(outlets))
print("Customers generated:", len(customers))

print("\nExperiment group distribution:")
print(customers["experiment_group"].value_counts())

print("\nCustomer frequency distribution:")
print(customers["frequency_band"].value_counts())

print("\nFirst 5 customer records:")
print(customers.head())
# ==========================================
# PART 3: GENERATE APPOINTMENT DATA
# ==========================================

# Service categories and their prices
services = {
    "Haircut": 300,
    "Hair Coloring": 1200,
    "Facial": 800,
    "Manicure": 500,
    "Pedicure": 600,
    "Spa": 1500
}

service_names = list(services.keys())

# Generate baseline appointments
baseline_counts = customers["baseline_visits"].to_numpy()

baseline_customer_ids = np.repeat(
    customers["customer_id"].to_numpy(),
    baseline_counts
)

baseline_appointments = pd.DataFrame({
    "customer_id": baseline_customer_ids
})

baseline_appointments["appointment_date"] = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2025-01-01").value // 10**9,
        pd.Timestamp("2025-06-30").value // 10**9,
        size=len(baseline_appointments)
    ),
    unit="s"
)

# Generate index appointments for all customers
index_appointments = pd.DataFrame({
    "customer_id": customers["customer_id"],
    "appointment_date": pd.Timestamp("2025-07-01")
})

# Generate 90-day follow-up retention outcome
retention_probability = np.where(
    customers["experiment_group"] == "Treatment",
    0.35,
    0.30
)

customers["retained_90d"] = (
    np.random.random(NUM_CUSTOMERS) < retention_probability
).astype(int)

# Create one repeat appointment for retained customers
repeat_customers = customers.loc[
    customers["retained_90d"] == 1,
    "customer_id"
]

repeat_appointments = pd.DataFrame({
    "customer_id": repeat_customers.to_numpy()
})

repeat_appointments["appointment_date"] = (
    pd.Timestamp("2025-07-02")
    + pd.to_timedelta(
        np.random.randint(1, 90, size=len(repeat_appointments)),
        unit="D"
    )
)

# Combine all appointment records
appointments = pd.concat(
    [
        baseline_appointments,
        index_appointments,
        repeat_appointments
    ],
    ignore_index=True
)

# Add outlet information
appointments = appointments.merge(
    customers[["customer_id", "outlet_id"]],
    on="customer_id",
    how="left"
)

# Assign services and prices
appointments["service"] = np.random.choice(
    service_names,
    size=len(appointments)
)

appointments["revenue"] = appointments["service"].map(services)

# Assign appointment status
appointments["status"] = np.random.choice(
    ["Completed", "Cancelled", "No-show"],
    size=len(appointments),
    p=[0.80, 0.12, 0.08]
)

# Display appointment summary
print("\nTotal appointments:", len(appointments))

print("\nAppointment status:")
print(appointments["status"].value_counts())

print("\nService distribution:")
print(appointments["service"].value_counts())

print("\nFirst 5 appointments:")
print(appointments.head())
# ==========================================
# PART 4: FINAL VALIDATION AND CSV EXPORT
# ==========================================

# Ensure repeat appointments are completed
followup_mask = appointments["appointment_date"] > pd.Timestamp("2025-07-01")
appointments.loc[followup_mask, "status"] = "Completed"

# Check missing values
print("\nMissing values in appointments:")
print(appointments.isnull().sum())

# Check duplicate appointment records
print("\nDuplicate appointment rows:", appointments.duplicated().sum())

# Check customer and outlet counts
print("\nUnique customers:", customers["customer_id"].nunique())
print("Unique outlets:", outlets["outlet_id"].nunique())

# Save datasets as CSV files
outlets.to_csv(DATA_DIR / "outlets.csv", index=False)

customers.to_csv(DATA_DIR / "customers.csv", index=False)

appointments.to_csv(DATA_DIR / "appointments.csv", index=False)

# Save experiment assignment separately
assignment = customers[
    ["customer_id", "outlet_id", "frequency_band", "experiment_group"]
]

assignment.to_csv(
    DATA_DIR / "experiment_assignment.csv",
    index=False
)

# Save retention outcome separately
outcomes = customers[
    ["customer_id", "retained_90d"]
]

outcomes.to_csv(
    DATA_DIR / "customer_outcomes.csv",
    index=False
)

print("\n================================")
print("SYNTHETIC DATA GENERATION DONE!")
print("================================")

print("\nFiles saved:")
for file in DATA_DIR.glob("*.csv"):
    print(file.name)