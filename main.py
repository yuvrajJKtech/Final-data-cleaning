import pandas as pd
from rapidfuzz import fuzz, process, utils


def load_dataset(filepath):
    """Load and return the dataset from the specified CSV file."""
    return pd.read_csv(filepath, header=None, names=['user_id', 'game_name', 'action', 'hours', 'unknown'])


def clean_game_name(name):
    """Clean and standardize the format of a game name."""
    name = name.lower()
    name = name.replace(' - ', ' ').replace('-', ' ')
    name = name.replace('game of the year edition', 'goty')
    name = name.replace('directors cut', 'directorscut')
    name = name.replace('edition', '')
    name = ''.join(char for char in name if char.isalnum() or char == ' ')
    return ' '.join(name.split())


def apply_cleaning(df):
    """Apply the cleaning function to the game_name column."""
    df['clean_name'] = df['game_name'].apply(clean_game_name)
    return df


def find_similar_games(df, game_name, threshold=85):
    """Find similar game names in the dataset using fuzzy matching."""
    cleaned_input = clean_game_name(game_name)
    return process.extract(
        cleaned_input,
        df['clean_name'].unique(),
        scorer=fuzz.token_sort_ratio,
        score_cutoff=threshold
    )


def find_similar_games_with_utils(df, game_name, threshold=85):
    """Find similar game names using RapidFuzz utils for preprocessing."""
    cleaned_input = utils.default_process(game_name)
    return process.extract(
        cleaned_input,
        df['clean_name'].unique(),
        scorer=fuzz.token_sort_ratio,
        score_cutoff=threshold
    )


def create_standardized_mapping(df, threshold=90):
    """Create a mapping of cleaned game names to standardized names."""
    unique_clean = df['clean_name'].unique()
    mapping = {}

    for game in unique_clean:
        if game not in mapping:
            matches = process.extract(
                game,
                unique_clean,
                scorer=fuzz.token_sort_ratio,
                score_cutoff=threshold
            )
            standard = max(matches, key=lambda x: x[1])[0]
            mapping[game] = standard

    return mapping


def analyze_potential_duplicates(df):
    """Identify potential duplicate entries based on standardized names."""
    grouped = df.groupby('standard_name')['game_name'].unique().apply(list)
    return grouped[grouped.apply(len) > 1]


def main():
    # Load dataset
    df = load_dataset('dataset.csv')
    print("Original Data:")
    print(df.head())

    # Clean game names
    df = apply_cleaning(df)
    print("\nCleaned Game Names:")
    print(df[['game_name', 'clean_name']].head())

    # Example fuzzy matches
    examples = ['The Elder Scrolls V Skyrim', 'BioShock Infinite']
    for game in examples:
        print(f"\nSimilar games to '{game}':")
        print(find_similar_games(df, game))

        print(f"\nSimilar games to '{game}' using utils:")
        print(find_similar_games_with_utils(df, game))

    # Create standardized name mapping
    standard_mapping = create_standardized_mapping(df)
    df['standard_name'] = df['clean_name'].map(standard_mapping)

    print("\nStandardized name examples:")
    print(df[['game_name', 'standard_name']].drop_duplicates().head(20))

    # Analyze potential duplicates
    print("\nPotential duplicates to review:")
    print(analyze_potential_duplicates(df).head(10))


if __name__ == "__main__":
    main()
