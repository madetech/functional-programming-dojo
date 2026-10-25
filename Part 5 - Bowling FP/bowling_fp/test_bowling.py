from bowling import score

GUTTER_ROLL = 0
SINGLE_PIN = 1
STRIKE_ROLL = 10
ROLLS_IN_GAME_WITHOUT_BONUSES = 20
ROLLS_IN_PERFECT_GAME = 12
ONE_SPARE = (5, 5)


def many(pins, count):
    return (pins,) * count


def test_gutter_game_scores_zero():
    assert score(many(GUTTER_ROLL, ROLLS_IN_GAME_WITHOUT_BONUSES)) == 0


def test_all_ones_scores_twenty():
    assert score(many(SINGLE_PIN, ROLLS_IN_GAME_WITHOUT_BONUSES)) == 20


def test_spare_adds_next_roll_as_bonus():
    assert score(ONE_SPARE + (3,) + many(GUTTER_ROLL, 17)) == 16


def test_strike_adds_next_two_rolls_as_bonus():
    assert score((STRIKE_ROLL, 3, 4) + many(GUTTER_ROLL, 16)) == 24


def test_spare_in_last_frame_earns_one_bonus_roll():
    assert score(many(GUTTER_ROLL, 18) + ONE_SPARE + (7,)) == 17


def test_strike_in_last_frame_earns_two_bonus_rolls():
    assert score(many(GUTTER_ROLL, 18) + (STRIKE_ROLL, 7, 3)) == 20


def test_perfect_game_scores_three_hundred():
    assert score(many(STRIKE_ROLL, ROLLS_IN_PERFECT_GAME)) == 300


def test_scoring_does_not_change_its_input():
    rolls = many(SINGLE_PIN, ROLLS_IN_GAME_WITHOUT_BONUSES)
    score(rolls)
    assert rolls == many(SINGLE_PIN, ROLLS_IN_GAME_WITHOUT_BONUSES)


def test_scoring_twice_gives_the_same_answer():
    rolls = many(STRIKE_ROLL, ROLLS_IN_PERFECT_GAME)
    assert score(rolls) == score(rolls)

