# Salon Experiment & Causal Analysis

**A/B Test Design · Experiment Evaluation · Difference-in-Differences · CUPED**

A reproducible Python analytics project for a fictional salon and spa chain in Coimbatore, India. The case covers 22 outlets and approximately 300,000 appointment, service, stylist and product-sales records, plus anonymous walk-ins.

> **Project status:** Repository scaffold and analysis blueprint. No real experiment or historical dataset has been supplied yet, so this repository does not claim any measured treatment effect or business result.

## Business question

Did the salon chain's initiative genuinely improve customer retention and commercial performance, or can the apparent improvement be explained by seasonality, customer mix, outlet differences or other concurrent changes?

## Project objectives

1. Design a client-level, 1:1 randomised A/B test for a personalised rebooking reminder.
2. Use 90-day client retention as the primary outcome; revenue per visit and no-show rate are secondary outcomes.
3. Audit assignment quality using sample-ratio mismatch (SRM) and pre-treatment balance checks.
4. Estimate intention-to-treat effects with confidence intervals, t-tests and client-level bootstrap.
5. Estimate the historical initiative's effect using Difference-in-Differences (DiD), event-study diagnostics and sensitivity checks.
6. Explore pre-specified segments and apply CUPED / regression adjustment.
7. Produce a pre-defined GO / NO-GO / EXTEND decision memo.

## Key design choices

- **Randomisation unit:** client ID, assigned once and frozen for the experiment.
- **Allocation:** 1:1, stratified by outlet and baseline visit-frequency band, with enrolment-week blocking.
- **Primary metric:** 90-day repeat-visit retention.
- **Illustrative power assumptions:** 30% baseline retention, +5 percentage-point MDE, two-sided alpha 0.05 and 80% power.
- **Illustrative sample:** 1,378 clients per arm before the 15% operational buffer; 1,585 per arm after the buffer.
- **Illustrative calendar duration:** 19.2 weeks including buffered enrolment, 90-day outcome maturation and one-week data lag.
- **Decision threshold:** the lower bound of the 95% CI must exceed +2.0 percentage points for GO, subject to guardrails and data-quality checks.

All illustrative assumptions must be replaced with measured business baselines before pre-registration. See the full design document in `docs/`.

## Repository structure

```text
salon-experiment-causal-analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   └── 01_experiment_design_v2.docx
├── data/
│   ├── raw/                 # Keep private source data out of Git
│   ├── processed/           # Generated analysis tables; normally not committed
│   ├── data_dictionary_template.csv
│   └── service_mapping_template.csv
├── notebooks/
│   └── 02_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_quality.py
│   ├── experiment.py
│   ├── did.py
│   └── cuped.py
├── reports/
│   └── figures/
└── outputs/                 # Generated tables and memo inputs
```

## Data required

The final analysis needs the experiment assignment file and operational records, plus at least 12 months of pre-period outlet-month outcomes and the post period for the historical DiD.

Expected source areas:

- Appointments: appointment/client/outlet identifiers, booking and slot timestamps, status and cancellation timestamp.
- Services: raw service name, category, duration, list price and discount.
- Stylists: stylist ID, outlet, level, tenure and leaving date.
- Product sales: SKU, quantity, gross/net amount and visit/appointment linkage.
- Walk-ins: outlet, visit time, service and amount; client identity may be unavailable.

**Privacy:** Do not commit personal data, phone numbers, names, dates of birth, client IDs or raw commercial records to a public GitHub repository. Use synthetic or anonymised sample data for a public portfolio. Keep raw data local and excluded by `.gitignore`.

## Setup

Python 3.10+ is recommended.

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd salon-experiment-causal-analysis

python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
jupyter lab
```

Open `notebooks/02_analysis.ipynb` and follow the sections in order. The notebook is a scaffold and will require the actual dataset and a confirmed column mapping before the analysis can run end-to-end.

## Analysis sequence

1. Inspect schemas, row counts, date ranges, keys and missingness.
2. Recover likely no-shows using the documented rule and manually audit a 300-record sample.
3. Map outlet-specific service names using RapidFuzz; auto-map scores >=90, manually review 70–89, and leave scores <70 unmapped.
4. Build visit-level and client-level tables; reconcile revenue to POS within 0.5%.
5. Validate one assignment per client and run SRM on the assignment file before exclusions.
6. Check pre-treatment balance; report standardised mean differences (SMDs).
7. Estimate ITT effects and 95% confidence intervals; bootstrap at client level.
8. Run DiD, event study, pre-trend slope comparison, placebo dates and sensitivity analysis.
9. Estimate segment interactions and apply Benjamini-Hochberg FDR control.
10. Apply CUPED using pre-randomisation covariates only; compare confidence-interval widths and sample savings.
11. Apply the pre-specified GO / NO-GO / EXTEND rule.

## Important analytical cautions

- Do not treat anonymous walk-ins as identifiable clients for retention.
- Do not silently combine cancellations and no-shows.
- Do not run SRM on a post-exclusion analysis table.
- Do not bootstrap appointment rows; resample clients.
- With staggered rollout, avoid naive two-way fixed-effects DiD when treatment effects may vary over time.
- With few treated clusters, conventional cluster-robust standard errors may be unreliable.
- Failure to reject a pre-trend test does not prove parallel trends.
- CUPED covariates and theta must use pre-treatment information only.
- Do not claim results until actual data have been analysed.

## Deliverables

- `docs/01_experiment_design_v2.docx` — revised experiment design and analysis plan.
- `notebooks/02_analysis.ipynb` — reproducible analysis notebook scaffold.
- `outputs/` — generated result tables and decision-memo inputs.
- `reports/` — exported figures and final one-page decision memo (to be added after analysis).

## License and data provenance

Add a license only after deciding how you want the code shared. The case study is fictional. Any future dataset must have its source, permissions, anonymisation method and limitations documented here.
