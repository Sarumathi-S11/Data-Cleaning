# Online Retail Data Cleaning

**Internship Task 3 – Clean the Dataset**

This project cleans the UCI Online Retail dataset collected in Task 2. The raw source file is never overwritten. The script creates a cleaned CSV and a text report containing before/after quality checks.

## Dataset
- Source: UCI Machine Learning Repository – Online Retail
- Official page: https://archive.ics.uci.edu/dataset/352/online+retail
- DOI: https://doi.org/10.24432/C5BW33
- Expected source columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
- Attribution: Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository.

## Before running
1. Complete Task 2 and download the original Excel workbook.
2. Copy that original workbook into this project's `data/raw/` folder.
3. Do not rename or edit the source workbook. The script automatically detects an Excel file in `data/raw/`.

## Project structure
```text
Online_Retail_Data_Cleaning_Task3/
├── data/
│   ├── raw/                 # Copy the original Task 2 Excel file here
│   └── processed/           # Cleaned CSV is generated here
├── reports/                 # Cleaning report is generated here
├── clean_dataset.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Run on Windows
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python clean_dataset.py
```

## Cleaning rules
- Trim whitespace in text columns.
- Remove exact duplicate rows.
- Remove rows missing `CustomerID` or `Description` so customer/product analysis is possible.
- Convert `Quantity` and `UnitPrice` to numeric values; remove invalid, zero, or negative values.
- Parse `InvoiceDate`; remove rows with invalid dates.
- Keep cancellation invoice rows (InvoiceNo values beginning with `C`) out of the cleaned sales dataset, and report their count. This makes the output suitable for positive sales analysis.
- Create `TotalPrice = Quantity × UnitPrice`.
- Preserve the original raw file.

These are explicit project choices, not universal rules for every retail analysis. Cancellation rows are counted in the report before exclusion.

## Outputs
- `data/processed/online_retail_cleaned.csv`
- `reports/data_cleaning_report.txt`

The script prints row counts at each stage and a sample of the cleaned data. Actual counts depend on the exact source workbook.

## GitHub
Do not upload the raw or processed dataset unless your internship instructions permit it. The `.gitignore` excludes them by default. You can commit the code, README, and report after reviewing the report for any personal or restricted data. If your evaluator needs the output dataset, follow their upload instructions.

## Task 3 submission checklist
- [ ] Copy Task 2 raw Excel workbook into `data/raw/`.
- [ ] Install requirements.
- [ ] Run `python clean_dataset.py` without errors.
- [ ] Check the cleaned CSV and cleaning report.
- [ ] Push code and README to GitHub.
- [ ] Submit the repository URL in the internship portal.
