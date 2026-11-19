# Week 6 – Interactive Sales Dashboard

## Project overview
An interactive sales analytics dashboard built from the supplied `sales_data.csv` file. It combines statistical visualizations (Seaborn/Matplotlib) with interactive Plotly charts and Streamlit filters.

## Dataset
- Records: 100
- Columns: 10
- Date range: 2024-01-01 to 2024-04-09
- Fields: Date, Product, Quantity, Price, Customer_ID, Region, Total_Sales

## Key results from the supplied data
- Total recorded sales: 12,365,048
- Total units sold: 478
- Unique customers: 100
- Average transaction sales: 123,650.48
- Highest-revenue product: Laptop
- Highest-revenue region: North

## Visualizations
Monthly trend, revenue by product, revenue by region, box plot, violin plot, correlation heatmap, 2×2 overview and interactive Plotly line, bar, pie, violin, box, scatter and heatmap charts.

## Project structure
```text
week6_interactive_sales_dashboard/
├── dashboard.ipynb
├── dashboard.py
├── sales_data.csv
├── requirements.txt
├── README.md
├── dashboard_demo.gif
├── documentation/project_report.pdf
└── visualizations/ (7 PNG charts)
```

## Setup
1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Optional virtual environment: `py -m venv .venv` then `.venv\\Scripts\\activate` on Windows.
4. Install packages: `pip install -r requirements.txt`
5. Start app: `streamlit run dashboard.py`
6. Open the local URL shown in the terminal.

Open `dashboard.ipynb` in Jupyter or VS Code and run cells from top to bottom. Keep `sales_data.csv` beside the notebook.

## Dashboard controls
Date range, product multi-select, region multi-select, interactive hover details, filtered transaction table and CSV download.

## Interpretation guide
- Monthly line chart: changes in recorded sales across months.
- Product and region charts: compare recorded revenue by category.
- Box plot: median, spread and possible outliers in unit price.
- Violin plot: distribution shape across regions.
- Heatmap: pairwise linear correlations; correlation does not establish causation.
- Scatter plot: quantity versus transaction sales; hover displays transaction details.

## Data quality note
The notebook checks whether `Total_Sales` equals `Quantity × Price`. Review mismatches before presenting financial conclusions. `Customer_ID` is an identifier, not demographic information; this dataset cannot support demographic segmentation or customer lifetime value analysis.

## Testing checklist
- [ ] Dependencies install.
- [ ] Notebook runs top to bottom.
- [ ] Streamlit app starts.
- [ ] Filters update the displayed results.
- [ ] Plotly hover details work.
- [ ] Filtered CSV download works.
- [ ] Capture screenshots from the running app for submission.

## GitHub
Commit the project files and push the folder to a GitHub repository. Do not upload virtual environments or secrets.
