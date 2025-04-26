import logging
from model import (
    load_dataset,
    apply_cleaning,
    create_standardized_mapping,
    analyze_potential_duplicates,
)
from utils import fuzzy_match, fuzzy_match_with_utils

# Setup logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    df = load_dataset('dataset.csv')

    print("Original Data:")
    print(df.head())

    df = apply_cleaning(df)

    print("\nCleaned Game Names:")
    print(df[['game_name', 'clean_name']].head())

    # Examples of fuzzy matching
    examples = ['The Elder Scrolls V Skyrim', 'BioShock Infinite']
    for game in examples:
        print(f"\nFuzzy match for '{game}':")
        print(fuzzy_match(game, df['clean_name'].unique()))

        print(f"\nFuzzy match with utils for '{game}':")
        print(fuzzy_match_with_utils(game, df['clean_name'].unique()))

    # Apply standardization
    mapping = create_standardized_mapping(df)
    df['standard_name'] = df['clean_name'].map(mapping)

    print("\nStandardized name examples:")
    print(df[['game_name', 'standard_name']].drop_duplicates().head(20))

    print("\nPotential duplicates:")
    print(analyze_potential_duplicates(df).head(10))


if __name__ == '__main__':
    main()
