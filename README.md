# Birds Biodiversity Temporal Trends Analysis

**Team Members:** Ollie, Kenichi, Sathya

## Project Overview
Analysis of Martinique bird monitoring data (2012-2025) to quantify biodiversity temporal trends.

## Setup Instructions

### 1. Clone Repository
```bash
git clone git@github.com:kenichisutan/birds-biodiversity.git
cd birds-biodiversity
```

### 2. Install requiremnets (y'all can do it in venv if you want)
```bash
pip install -r requirements.txt
```

### 4. Verify requiremnts installed
```bash
python3 -c "import pandas; print('Setup successful!')"
```

### 5. Test everything:
```
python3 test_setup.py
```

## Project Structure
```
birds-biodiversity/
├── data/
│   ├── raw/              # Original data
│   └── processed/        # Cleaned data 
├── src/                  # Helper modules
├── notebooks/            # Analysis notebooks
├── figures/              # Exported figures
├── results/              # Exported tables
├── report/               # Final report
└── docs/                 # Project documentation
```
