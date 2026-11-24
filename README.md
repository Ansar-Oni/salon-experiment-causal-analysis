# Salon Experiment & Causal Analysis

**A/B Testing | Causal Inference | Difference-in-Differences | CUPED | Business Analytics**

A reproducible Python data science project evaluating the impact of personalised rebooking reminders on customer retention and business performance for a fictional salon and spa chain in Coimbatore, India.

**Project Status:** Analysis completed using a simulated dataset.

> **Data transparency:** All data used in this project are synthetically generated for educational and portfolio purposes. The results do not represent actual salon business performance or a real-world experiment.

## 1. Business Problem

The business wants to understand whether personalised rebooking reminders can improve customer retention and commercial performance.

The central question:

Can personalised reminders increase the probability of customers returning within 90 days compared with standard communication?

## 2. Project Objectives

- Design and evaluate a client-level 1:1 randomised A/B experiment.
- Measure 90-day customer retention.
- Compare treatment and control group performance.
- Evaluate revenue and appointment outcomes.
- Perform Difference-in-Differences (DiD) analysis.
- Apply CUPED adjustment using pre-treatment customer behaviour.
- Validate randomisation through Sample Ratio Mismatch (SRM).
- Analyse customer segments and outlet-level performance.
- Develop data-driven business recommendations.

## 3. Dataset Overview

The project uses a custom-generated synthetic dataset.

| Dataset | Description |
|---|---|
| Outlets | 22 fictional salon outlets |
| Customers | 10,000 synthetic customers |
| Appointments | Synthetic appointment records |
| Experiment Assignment | Treatment and control allocation |
| Customer Outcomes | Customer-level retention outcomes |

### Experiment Design

- Randomisation unit: Customer.
- Allocation: Approximately 50% Treatment and 50% Control.
- Treatment: Personalised rebooking reminder.
- Control: Standard communication.
- Primary metric: 90-day repeat-visit retention.
- Secondary metrics: Revenue, cancellations and no-shows.

## 4. Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Jupyter Notebook
- Git and GitHub

## 5. Repository Structure

```text
salon-experiment-causal-analysis/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── outlets.csv
│   ├── customers.csv
│   ├── appointments.csv
│   ├── experiment_assignment.csv
│   ├── customer_outcomes.csv
│   ├── data_dictionary_template.csv
│   └── service_mapping_template.csv
│
├── docs/
│   └── 01_experiment_design_v2.docx
│
├── notebooks/
│   └── 02_analysis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── data_quality.py
│   ├── experiment.py
│   ├── did.py
│   └── cuped.py
│
└── reports/
```

## 6. Analysis Workflow

1. Synthetic data generation.
2. Data loading and quality validation.
3. Customer retention analysis.
4. Statistical significance testing.
5. Outlet-wise retention analysis.
6. Revenue analysis.
7. Cancellation and no-show analysis.
8. Customer segmentation.
9. Difference-in-Differences analysis.
10. CUPED adjustment.
11. Randomization and baseline balance checks.
12. Data visualization.
13. Business insights and recommendations.

## 7. Key Analytical Results

### A/B Testing Results

| Metric | Treatment | Control |
|---|---:|---:|
| Customers | 4,988 | 5,012 |
| Retention Rate | 35.49% | 30.69% |

**Observed retention improvement: +4.80 percentage points.**

### Difference-in-Differences

| Metric | Result |
|---|---:|
| Treatment group change | -55.35 pp |
| Control group change | -60.51 pp |
| DiD effect | +5.16 pp |

### CUPED Analysis

| Metric | Result |
|---|---:|
| CUPED theta | 0.0043 |
| Original treatment effect | +4.80 pp |
| CUPED-adjusted effect | +4.80 pp |

### Randomization Checks

| Check | Result |
|---|---:|
| SRM p-value | 0.8103 |
| Baseline visits SMD | 0.0033 |

No significant sample ratio mismatch was detected, and baseline visits were well-balanced between the two groups.

### Revenue Analysis

| Metric | Result |
|---|---:|
| Treatment average revenue | ₹2,914.21 |
| Control average revenue | ₹2,866.76 |
| Difference | +₹47.45 |

### Customer Segment Analysis

| Segment | Treatment Retention | Control Retention | Treatment Lift |
|---|---:|---:|---:|
| High Frequency | 38% | 30% | +7.31 pp |
| Low Frequency | 34% | 31% | +3.45 pp |

*All results above are from the simulated dataset and should be interpreted as illustrative findings.*

## 8. Business Recommendations

Based on the simulated analysis:

- Personalised reminders show a positive customer-retention signal.
- The high-frequency customer segment shows a larger observed retention lift.
- Outlet-level performance should be monitored before implementation.
- Revenue impact should be validated using a clearly defined post-treatment revenue window.
- A longer real-world experiment should be conducted before a full business rollout.

## 9. Important Limitations

- The dataset is synthetic and does not represent actual salon customers.
- The treatment effects are simulated, not measured real-world effects.
- CUPED produced negligible adjustment because the baseline covariate had a weak relationship with the simulated retention outcome.
- The DiD estimate is exploratory; its assumptions, particularly parallel trends, cannot be established from this simple pre/post setup.
- The results should not be treated as proof of actual business impact.
- Further validation with real operational data is necessary.

## 10. How to Run the Project

### Clone the repository

```bash
git clone https://github.com/Ansar-Oni/salon-experiment-causal-analysis
cd salon-experiment-causal-analysis
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate on Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Generate the synthetic dataset

```bash
python src/generate_data.py
```

### Run the analysis

Open:

```text
notebooks/02_analysis.ipynb
```

Select the project virtual environment as the Jupyter kernel and execute the notebook cells in sequence.

## 11. Project Deliverables

- Synthetic data generation script.
- Experiment design documentation.
- Data quality and validation workflow.
- A/B test and retention analysis.
- DiD and CUPED analysis.
- Randomization checks.
- Business-focused visualizations.
- Business insights and recommendations.

## 12. Conclusion

This project demonstrates an end-to-end data science workflow combining experimental design, statistical analysis, causal inference, customer segmentation and business decision-making.

It highlights how Python-based analytics can help evaluate customer engagement strategies and translate analytical findings into business recommendations.

**Project developed for educational and data science portfolio purposes.**

**Author:** Ansar Malik