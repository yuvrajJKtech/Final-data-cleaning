import pandas as pd
import logging
from utils import clean_game_name, fuzzy_match

logger = logging.getLogger(__name__)


def load_dataset(filepath):
    """Load dataset and assign column names."""
    try:
        df = pd.read_csv(filepath, header=None, names=['user_id', 'game_name', 'action', 'hours', 'unknown'])
        logger.info("Dataset loaded successfully.")
        return df
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        raise


def apply_cleaning(df):
    """Add a clean_name column by cleaning game names."""
    df['clean_name'] = df['game_name'].apply(clean_game_name)
    logger.info("Applied game name cleaning.")
    return df


def create_standardized_mapping(df, threshold=90):
    """Map similar cleaned names to a standard name."""
    unique_clean = df['clean_name'].unique()
    mapping = {}

    for name in unique_clean:
        if name not in mapping:
            matches = fuzzy_match(name, unique_clean, threshold)
            if matches:
                standard = max(matches, key=lambda x: x[1])[0]
                mapping[name] = standard

    logger.info("Standardized mapping created.")
    return mapping


def analyze_potential_duplicates(df):
    """Return groups of different original names under the same standardized name."""
    grouped = df.groupby('standard_name')['game_name'].unique().apply(list)
    return grouped[grouped.apply(len) > 1]
