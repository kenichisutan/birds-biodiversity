# Birds Biodiversity Temporal Trends Analysis

**Team Members:** [Add names and student IDs here]

## Project Overview
Analysis of Martinique bird monitoring data (2012-2025) to quantify biodiversity temporal trends.

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/your-team/birds-biodiversity.git
cd birds-biodiversity
```

### 2. Get Data File
Download `Observations 2012-2025.xlsx` from Google Drive (link in team chat) and place in:
```
data/raw/Observations 2012-2025.xlsx
```

### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Verify Setup
```bash
python -c "import pandas; print('Setup successful!')"
```

## Project Structure
```
birds-biodiversity/
├── data/
│   ├── raw/              # Original data (not in git)
│   └── processed/        # Cleaned data (not in git)
├── src/                  # Helper modules
├── notebooks/            # Analysis notebooks
├── figures/              # Exported figures
├── results/              # Exported tables
├── report/               # Final report
└── docs/                 # Project documentation
```

## Running the Analysis
1. `notebooks/01_data_exploration.ipynb`
2. `notebooks/02_indicator_trends.ipynb`
3. `notebooks/03_species_analysis.ipynb`

## Collaboration Workflow
- Create feature branches for major work: `git checkout -b analysis/person-name-indicator`
- Push frequently: `git push origin your-branch-name`
- Merge to main after team review
- Pull before starting work: `git pull origin main`

