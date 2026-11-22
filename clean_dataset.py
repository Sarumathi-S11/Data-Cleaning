"""
Task 3: Clean the UCI Online Retail dataset.
The original raw workbook is read only and never overwritten.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
REPORT_DIR = ROOT / "reports"

EXPECTED = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country"
]

def find_source_file():
    candidates = sorted(
        list(RAW_DIR.glob("*.xlsx")) + list(RAW_DIR.glob("*.xls")),
        key=lambda p: p.name.lower()
    )
    if not candidates:
        raise FileNotFoundError(
            "No Excel file found in data/raw/. Copy the original Task 2 "
            "Online Retail workbook into this folder, then run again."
        )
    if len(candidates) > 1:
        raise RuntimeError(
            "More than one Excel file found in data/raw/. Keep only the "
            "original Online Retail workbook in this folder."
        )
    return candidates[0]

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    source = find_source_file()
    print(f"Reading raw dataset: {source.name}")
    df = pd.read_excel(source, engine="openpyxl")
    original_rows = len(df)

    missing_columns = [c for c in EXPECTED if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing expected columns: {missing_columns}")

    # Work on a copy; the original workbook remains unchanged.
    clean = df.copy()

    # Standardize text fields.
    for col in ["InvoiceNo", "StockCode", "Description", "Country"]:
        clean[col] = clean[col].astype("string").str.strip()

    # Remove exact duplicate records.
    before = len(clean)
    clean = clean.drop_duplicates()
    duplicates_removed = before - len(clean)

    # Convert fields to suitable data types.
    clean["Quantity"] = pd.to_numeric(clean["Quantity"], errors="coerce")
    clean["UnitPrice"] = pd.to_numeric(clean["UnitPrice"], errors="coerce")
    clean["InvoiceDate"] = pd.to_datetime(clean["InvoiceDate"], errors="coerce")
    clean["CustomerID"] = pd.to_numeric(clean["CustomerID"], errors="coerce")

    missing_customer = int(clean["CustomerID"].isna().sum())
    missing_description = int(clean["Description"].isna().sum())
    invalid_dates = int(clean["InvoiceDate"].isna().sum())
    invalid_quantity = int(clean["Quantity"].isna().sum())
    invalid_price = int(clean["UnitPrice"].isna().sum())

    # Drop rows required for reliable customer/product sales analysis.
    clean = clean.dropna(subset=["CustomerID", "Description", "InvoiceDate",
                                 "Quantity", "UnitPrice", "InvoiceNo", "StockCode"])

    # Exclude cancellations from the positive-sales analysis output, but count them.
    cancellation_mask = clean["InvoiceNo"].str.upper().str.startswith("C", na=False)
    cancellation_rows = int(cancellation_mask.sum())
    clean = clean.loc[~cancellation_mask].copy()

    # Keep only positive sales quantities and prices.
    nonpositive_quantity = int((clean["Quantity"] <= 0).sum())
    nonpositive_price = int((clean["UnitPrice"] <= 0).sum())
    clean = clean.loc[(clean["Quantity"] > 0) & (clean["UnitPrice"] > 0)].copy()

    # CustomerID is an identifier; use nullable integer representation.
    clean["CustomerID"] = clean["CustomerID"].round().astype("Int64")
    clean["TotalPrice"] = (clean["Quantity"] * clean["UnitPrice"]).round(2)

    # Reorder columns with TotalPrice at the end.
    ordered = EXPECTED + ["TotalPrice"]
    clean = clean[ordered]

    output_csv = PROCESSED_DIR / "online_retail_cleaned.csv"
    clean.to_csv(output_csv, index=False, encoding="utf-8-sig")

    report = [
        "ONLINE RETAIL – DATA CLEANING REPORT",
        "=" * 48,
        f"Source workbook: {source.name}",
        f"Original row count: {original_rows:,}",
        f"Original column count: {len(df.columns)}",
        f"Exact duplicate rows removed: {duplicates_removed:,}",
        f"Rows missing CustomerID before row filtering: {missing_customer:,}",
        f"Rows missing Description before row filtering: {missing_description:,}",
        f"Rows with invalid InvoiceDate before row filtering: {invalid_dates:,}",
        f"Rows with invalid Quantity before row filtering: {invalid_quantity:,}",
        f"Rows with invalid UnitPrice before row filtering: {invalid_price:,}",
        f"Cancellation rows excluded: {cancellation_rows:,}",
        f"Rows with non-positive Quantity excluded: {nonpositive_quantity:,}",
        f"Rows with non-positive UnitPrice excluded: {nonpositive_price:,}",
        f"Final cleaned row count: {len(clean):,}",
        f"Final column count: {len(clean.columns)}",
        f"Output file: {output_csv.relative_to(ROOT)}",
        "",
        "Missing values in cleaned output:",
        clean.isna().sum().to_string(),
        "",
        "Cleaned data preview:",
        clean.head(5).to_string(index=False),
        "",
        "Note: Raw source workbook was not modified.",
    ]
    report_path = REPORT_DIR / "data_cleaning_report.txt"
    report_path.write_text("\n".join(report), encoding="utf-8")

    print("\nDATA CLEANING COMPLETED")
    print(f"Original rows: {original_rows:,}")
    print(f"Cleaned rows:  {len(clean):,}")
    print(f"Cleaned data:  {output_csv}")
    print(f"Report:        {report_path}")
    print("\nNext: review the report and use the cleaned CSV for Task 4 – Analyze the Data.")

if __name__ == "__main__":
    main()
