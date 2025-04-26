import logging
from rapidfuzz import fuzz, process, utils

logger = logging.getLogger(__name__)


def clean_game_name(name):
    """Standardize a game name."""
    name = name.lower()
    name = name.replace(' - ', ' ').replace('-', ' ')
    name = name.replace('game of the year edition', 'goty')
    name = name.replace('directors cut', 'directorscut')
    name = name.replace('edition', '')
    name = ''.join(char for char in name if char.isalnum() or char == ' ')
    return ' '.join(name.split())


def fuzzy_match(name, name_list, threshold=85):
    """Return fuzzy matches using token_sort_ratio."""
    cleaned = clean_game_name(name)
    return process.extract(
        cleaned,
        name_list,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=threshold
    )


def fuzzy_match_with_utils(name, name_list, threshold=85):
    """Return fuzzy matches using utils.default_process."""
    cleaned = utils.default_process(name)
    return process.extract(
        cleaned,
        name_list,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=threshold
    )
