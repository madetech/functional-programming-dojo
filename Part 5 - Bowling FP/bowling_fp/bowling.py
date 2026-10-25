PINS_PER_FRAME = 10
FRAMES_PER_GAME = 10

STRIKE_SHAPE = (1, 2)
SPARE_SHAPE = (2, 1)
OPEN_SHAPE = (2, 0)


def score(rolls, frames_remaining=FRAMES_PER_GAME):
    if frames_remaining == 0:
        return 0
    rolls_used, bonus_rolls = frame_shape(rolls)
    frame_score = sum(rolls[: rolls_used + bonus_rolls])
    return frame_score + score(rolls[rolls_used:], frames_remaining - 1)


def frame_shape(rolls):
    if is_strike(rolls):
        return STRIKE_SHAPE
    if is_spare(rolls):
        return SPARE_SHAPE
    return OPEN_SHAPE


def is_strike(rolls):
    return rolls[0] == PINS_PER_FRAME


def is_spare(rolls):
    return rolls[0] + rolls[1] == PINS_PER_FRAME