# Supply Chain Management Analytics Dashboard

An interactive Streamlit dashboard for exploring supply chain operations across revenue, orders, delivery reliability, supplier performance and inventory risk.

## Dashboard features
- KPI cards for revenue, order volume, on-time delivery, average lead time and low-stock records
- Date, region and product-category filters
- Monthly revenue trend
- Delivery status distribution
- Revenue by product category
- Supplier delivery performance
- Inventory reorder-risk monitor
- Interactive operational data table and filtered CSV download

## Tech stack
Python • Streamlit • Pandas • Plotly • NumPy

## Project structure
```text
supply-chain-management-dashboard/
├── app.py
├── data/
│   └── supply_chain_data.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## Run locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/supply-chain-management-dashboard.git
cd supply-chain-management-dashboard
```

### 2. Create and activate a virtual environment (recommended)
Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the dashboard
```bash
streamlit run app.py
```
The app will open in your browser, usually at `http://localhost:8501`.

## Dataset
`data/supply_chain_data.csv` contains 1,200 generated sample order records. All records are synthetic and intended for learning and portfolio demonstration. Replace the CSV with authorized business data to use this dashboard operationally.

## GitHub upload
```bash
git init
git add .
git commit -m "Build supply chain analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/supply-chain-management-dashboard.git
git push -u origin main
```

## Suggested GitHub repository description
Interactive supply chain analytics dashboard built with Python, Streamlit, Pandas and Plotly. Includes delivery, supplier, revenue and inventory risk analysis.

## Future enhancements
- Connect a live SQL database or ERP source
- Add demand forecasting and safety-stock recommendations
- Add supplier scorecards and purchase-order tracking
- Add user authentication and role-based access
