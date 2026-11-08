# Online Retail Customer Analytics

A data analytics project exploring customer purchasing behavior, product performance, and geographic sales patterns using the **UCI Online Retail II** dataset.

## Project Overview

Online retailers generate large volumes of transaction data that can reveal patterns in customer purchasing behavior, product performance, and sales across markets.

This project analyzes historical transaction records from a UK-based giftware retailer to identify meaningful customer, product, and market patterns that can inform retail business decisions.

### Research Objective

To analyze customer purchasing behavior and sales performance to identify meaningful customer, product, and market patterns.

### Research Questions

1. Which customer segments generate the most revenue?
2. Which products contribute most to sales?
3. How frequently do customers purchase, and what distinguishes repeat customers?
4. How does purchasing behavior differ across countries?

## Dataset

**Source:** [UCI Machine Learning Repository – Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

The dataset contains historical transaction records from 2009–2011 for a UK-based online retailer specializing in unique giftware.

It includes information such as:
- Invoice and transaction dates
- Product codes and descriptions
- Quantities and unit prices
- Customer identifiers
- Countries

The project uses the selected Online Retail II dataset file, `raw_online_retail_II.csv`.

## Repository Structure

```text
online-retail-ii/
│
├── data/
│   ├── raw_online_retail_II.csv
│   └── processed/
│       └── online_retail_cleaned.csv
│
├── notebooks/
│   └── 01_EDA.ipynb
│
├── reports/
│   ├── DataDictionary.csv
│   └── figures/
│
├── src/
│   └── data/
│       ├── download_data.py
│       └── data_cleaning.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

**Note:** Dataset files are generated locally and are excluded from version control. The `data/` directory and processed output may need to be created when setting up the project.

## Getting Started

### 1. Clone the Repository

```powershell
git clone https://github.com/g-ritvik/online-retail-customer-analytics.git
cd online-retail-customer-analytics
```

### 2. Create a Virtual Environment

Create an isolated Python environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use the following command for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### 3. Install Dependencies

Upgrade pip and install the required packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download the Dataset

Run the data download script:

```powershell
python src/data/download_data.py
```

The script downloads the dataset and prepares the raw data file under the project's `data/` directory.

**Expected raw dataset path:**

```text
data/raw_online_retail_II.csv
```

### 5. Run the Exploratory Data Analysis

Open the notebook:

```powershell
jupyter notebook notebooks/01_EDA.ipynb
```

Alternatively, open the repository in VS Code and select the `.venv` Python interpreter as the notebook kernel.

The notebook documents the initial exploration of:
- Dataset structure and missing values
- Invoice and transaction patterns
- Quantity and price distributions
- Duplicate records
- Customer purchasing behavior
- Product-level patterns
- Geographic distribution
- Data quality findings

Figures generated during the analysis are stored in `reports/figures/`.

### 6. Run the Data Cleaning Pipeline

After downloading the raw dataset, execute:

```powershell
python src/data/data_cleaning.py
```

The cleaning pipeline performs the following operations:

1. Loads the raw transaction dataset.
2. Standardizes column names and data types.
3. Assesses missing values.
4. Recovers missing product descriptions where an unambiguous StockCode mapping exists.
5. Removes exact duplicate records.
6. Investigates repeated transaction combinations.
7. Assesses unusual quantity and price values.
8. Creates transaction classification indicators.
9. Constructs the transaction-level `line_value` variable.
10. Validates and exports the cleaned dataset.

**Expected cleaned dataset path:**

```text
data/processed/online_retail_cleaned.csv
```

The pipeline preserves records with unusual transaction values and unresolved missing information rather than automatically discarding them.

## Analytical Approach

The project uses Python and SQL for data preparation and analysis.

Planned analytical components include:

- **Customer Analysis:** RFM segmentation, purchasing frequency, and repeat-purchase behavior.
- **Product Analysis:** Product-level transaction and sales performance.
- **Geographic Analysis:** Purchasing patterns across countries.
- **Sales Analysis:** Transaction trends and sales performance over time.
- **Visualization:** Tableau dashboards to communicate key findings.

## Tools and Technologies

- Python
- Pandas
- Jupyter Notebook
- SQL / Databricks
- Tableau
- Git and GitHub
