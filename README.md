# InsightFlow

Scenario-based Business Intelligence & Decision Support System.

Upload CSV/Excel sales data → get business analytics, customer segmentation,
anomaly detection, forecasting, and a **What-If Scenario Engine** that
estimates the effect of hypothetical changes (price, discount, demand,
region) on historical performance. Scenario results are estimates based on
historical patterns, not guaranteed predictions.

## Status

Phase 0: project skeleton — a minimal Flask app that runs, with a home page
and a `/health` endpoint. No analytics, ML, or dashboard functionality yet.

## Tech Stack

Python · Flask · Jinja2 · Pandas · NumPy · Scikit-learn · MySQL · SQLAlchemy
· Plotly · HTML/CSS/vanilla JS · AWS

## Local Setup (Windows)

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Then open http://127.0.0.1:5000 in a browser.

## Running Tests

```bat
pytest
```

## Project Structure

```
app/
├── routes/       Flask blueprints — request/response only
├── templates/    Jinja2 HTML templates
├── static/css/   Stylesheets
├── __init__.py   Application factory
└── config.py     Environment-based configuration
tests/            Pytest test suite
run.py            Local development entry point
wsgi.py           Production entry point (Gunicorn)
```

Future phases will add `app/services/`, `app/analytics/`, and `app/models/`
as each feature (upload, cleaning, RFM, anomaly detection, forecasting,
what-if scenarios) is built.

## Data Assumptions

Expected source columns: `Order_ID, Order_Date, Customer_ID, Product,
Category, Region, Quantity, Unit_Price, Discount, Revenue`. `Revenue` is
validated/recalculated from quantity, unit price, and discount rather than
trusted as-is (documented in the cleaning module once built).
