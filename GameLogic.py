from random import randint

def numbers(mode: str) -> list[int, bool]:
    """
    Numbers game.
    :param mode:"""

    value = randint(1, 100)

    return [value, True] if (value >= 50 and mode == 'more') or (value < 50 and mode == 'less') else [value, False]
        
def heads_and_tails(value: int) -> bool:
    """
    Heads and tails game.
    :param mode:"""

    rand = randint(0, 10)

    return True if (rand < 5 and value == 'head') or (rand > 5 and value == 'tail') else False