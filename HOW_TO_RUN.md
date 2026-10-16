# How to Run — E-commerce Sales Analytics Dashboard

Works on **Windows**, **macOS**, and **Linux**. You need Python 3.9+ and Git installed.

## 1. Clone the repo
```bash
git clone https://github.com/ArfanOrewa/ecommerce-sales-analytics-dashboard.git
cd ecommerce-sales-analytics-dashboard
```

## 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Generate the dataset
```bash
python generate_data.py        # Windows
python3 generate_data.py       # macOS / Linux
```
This creates `data/ecommerce_orders.csv` (5,000 synthetic orders). The CSV is git-ignored on purpose — it regenerates deterministically with seed 42.

## 5. Run the analysis
```bash
python analysis.py             # Windows
python3 analysis.py            # macOS / Linux
```
Prints the KPI summary: total revenue, AOV, monthly trends, top products, region/category breakdowns.

## 6. Launch the dashboard
```bash
streamlit run dashboard.py
```
Opens automatically in your browser at `http://localhost:8501`. Use the sidebar filters (region, category, date range) to explore. Press `Ctrl+C` in the terminal to stop it.

> First launch: Streamlit may ask for an email for its newsletter — just press **Enter** to skip.
