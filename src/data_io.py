"""
Data loading and cleaning for Birds Biodiversity project.

Note: This dataset has weird formatting issues - counts stored as datetime,
messy column names, whitespace everywhere. This module handles all that.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def extract_count_from_datetime(dt_series):
    """
    Extract actual count from datetime-encoded columns.
    
    Yeah, the Excel file stores counts as datetime. The count is in the 
    nanosecond component. So 1970-01-01 00:00:00.000000005 = 5 birds.
    """
    if pd.api.types.is_datetime64_any_dtype(dt_series):
        # get the nanosecond part
        counts = (dt_series.astype(np.int64) % 1000000000)
        return counts.astype(float)
    
    # If it's already numeric, coerce safely to numeric floats
    if pd.api.types.is_numeric_dtype(dt_series):
        return pd.to_numeric(dt_series, errors='coerce').astype(float)

    # For object or string dtypes, attempt two strategies:
    # 1) Parse as datetime (to extract encoded counts)
    dt_parsed = pd.to_datetime(dt_series, errors='coerce', infer_datetime_format=True)
    if dt_parsed.notna().any():
        result = pd.Series(np.nan, index=dt_series.index, dtype=float)
        mask = dt_parsed.notna()
        # extract ns only for valid datetimes
        ns = (dt_parsed[mask].astype(np.int64) % 1000000000).astype(float)
        result.loc[mask] = ns
        return result

    # 2) Fallback: coerce to numeric (strings like '5', blanks, etc.)
    numeric = pd.to_numeric(dt_series, errors='coerce')
    return numeric.astype(float)

def load_excel_data(filepath):
    """
    Load all three sheets from the Excel file.
    
    Handles the non-standard formatting:
    - ESPECES: bad headers, need manual column names
    - GPS-MILIEU: datetime-encoded GPS coords
    - NOM FRANÇAIS: messy column names, counts split by detection method
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Can't find data file: {filepath}")
    
    print(f"Loading data from {filepath}...")
    print("This might take 30-60 seconds...")
    
    # Load ESPECES sheet - skip bad headers, manually name columns
    df_species = pd.read_excel(filepath, sheet_name='ESPECES', header=None, skiprows=1)
    df_species.columns = ['_empty1', '_empty2', 'french_name', 'scientific_name', 'status']
    df_species = df_species[['french_name', 'scientific_name', 'status']].copy()
    
    # clean whitespace
    for col in df_species.columns:
        if df_species[col].dtype == 'object':
            df_species[col] = df_species[col].str.strip()
    
    print(f"✓ Loaded {len(df_species)} species")
    
    # Load GPS-MILIEU sheet
    df_gps = pd.read_excel(filepath, sheet_name='GPS-MILIEU', header=None, skiprows=1)
    df_gps.columns = ['_empty1', '_empty2', 'transect_name', 'gps_x', 'gps_y', 
                      'habitat_type', 'site_id', 'point_id']
    df_gps = df_gps[['transect_name', 'habitat_type', 'site_id', 'point_id']].copy()
    
    # clean whitespace
    for col in df_gps.columns:
        if df_gps[col].dtype == 'object':
            df_gps[col] = df_gps[col].str.strip()
    
    print(f"✓ Loaded {len(df_gps)} GPS points")
    
    # Load main observations sheet
    df_obs = pd.read_excel(filepath, sheet_name='NOM FRANÇAIS')
    
    # rename to something sensible
    column_mapping = {
        'Nom observateur': 'observer_name',
        'code département': 'department_code',
        'Nom transect': 'transect_name',
        'date': 'date',
        '1er, 2e ou 3e passage': 'visit_number',
        'nuages': 'cloud_cover_raw',
        'pluie': 'rain',
        'vent': 'wind',
        'visibilité': 'visibility',
        'N° point': 'point_number',
        'heure début': 'start_time',
        'ESPECE': 'species_name',
        'distances de contact': 'distance_category_raw',
        'totaux': 'count_auditory',
        'Unnamed: 22': 'count_visual_no_flight',
        'Unnamed: 23': 'count_audio_visual_no_flight',
        'Unnamed: 24': 'count_audio_visual_flight',
        'Unnamed: 25': 'notes'
    }
    
    df_obs = df_obs.rename(columns=column_mapping)
    
    # convert the count columns to numeric (they're mixed type with headers in row 1)
    print("Converting count columns to numeric...")
    count_cols = ['count_auditory', 'count_visual_no_flight', 
                  'count_audio_visual_no_flight', 'count_audio_visual_flight']
    
    for col in count_cols:
        df_obs[col] = pd.to_numeric(df_obs[col], errors='coerce')
    
    # sum across all detection methods to get total count
    df_obs['individual_count'] = df_obs[count_cols].sum(axis=1)
    
    # convert date properly
    df_obs['date'] = pd.to_datetime(df_obs['date'], errors='coerce')
    df_obs['year'] = df_obs['date'].dt.year
    
    # clean whitespace from text columns
    for col in ['observer_name', 'transect_name', 'species_name', 'start_time', 'notes']:
        if col in df_obs.columns:
            df_obs[col] = df_obs[col].astype(str).str.strip()
    
    print(f"✓ Loaded {len(df_obs)} observation records")
    
    return {
        'observations': df_obs,
        'species': df_species,
        'gps': df_gps
    }

def clean_observations(df):
    """
    Clean and validate observations.
    
    Handles:
    - Negative wind values (data errors)
    - Zero/missing counts
    - Missing essential fields
    - Creates observation IDs
    """
    df_clean = df.copy()
    
    print("\n=== Data Cleaning ===")
    print(f"Starting with {len(df_clean)} records")
    
    # fix negative wind values
    if 'wind' in df_clean.columns:
        n_negative = (df_clean['wind'] < 0).sum()
        if n_negative > 0:
            print(f"⚠ Found {n_negative} negative wind values - setting to NaN")
            df_clean.loc[df_clean['wind'] < 0, 'wind'] = np.nan
    
    # remove zero/negative counts
    before = len(df_clean)
    df_clean = df_clean[df_clean['individual_count'] > 0]
    removed = before - len(df_clean)
    if removed > 0:
        print(f"Removed {removed} records with zero/negative counts")
    
    # remove records missing essential fields
    essential_cols = ['year', 'species_name', 'individual_count', 'transect_name']
    before = len(df_clean)
    df_clean = df_clean.dropna(subset=essential_cols)
    removed = before - len(df_clean)
    if removed > 0:
        print(f"Removed {removed} records with missing essential data")
    
    # create observation ID
    df_clean['observation_id'] = range(1, len(df_clean) + 1)
    
    # summary
    print(f"\n✓ Final dataset: {len(df_clean)} records")
    print(f"  Years: {df_clean['year'].min()} - {df_clean['year'].max()}")
    print(f"  Unique species: {df_clean['species_name'].nunique()}")
    print(f"  Unique transects: {df_clean['transect_name'].nunique()}")
    print(f"  Unique observers: {df_clean['observer_name'].nunique()}")
    print("=====================\n")
    
    return df_clean

def get_annual_summary(df):
    """Generate annual summary stats."""
    summary = df.groupby('year').agg({
        'observation_id': 'count',
        'species_name': 'nunique',
        'individual_count': 'sum',
        'transect_name': 'nunique',
        'observer_name': 'nunique'
    }).rename(columns={
        'observation_id': 'n_observations',
        'species_name': 'n_species',
        'individual_count': 'total_abundance',
        'transect_name': 'n_transects',
        'observer_name': 'n_observers'
    })
    
    return summary