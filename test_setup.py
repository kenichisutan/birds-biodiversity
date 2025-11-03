import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("Testing setup...")

# Test 1: Data file
data_path = Path("data/raw/Observations 2012-2025.xlsx")
assert data_path.exists(), "Data file missing!"
print("âœ… Data file found")

# Test 2: Load data
df = pd.read_excel(data_path, sheet_name='NOM FRANÇAIS')
print(f"âœ… Loaded {len(df)} observations")

# Extract year from date column
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year

# Test 3: Basic computation
print(f"âœ… Years: {df['year'].min()} - {df['year'].max()}")
print(f"âœ… Species: {df['ESPECE'].nunique()} unique")

# Test 4: Plotting
fig, ax = plt.subplots(figsize=(8, 4))
df.groupby('year').size().plot(ax=ax)
ax.set_title("Observations per Year")
plt.savefig("figures/test_plot.png", dpi=150)
plt.close()
print("âœ… Test plot saved to figures/")

print("\n🎉 ALL TESTS PASSED! Ready to start analysis.")