from bowling import Game

GUTTER_ROLL = 0
SINGLE_PIN = 1
SPARE_FIRST_AND_SECOND_ROLL = 5
STRIKE_ROLL = 10
ROLLS_IN_GAME_WITHOUT_BONUSES = 20
ROLLS_IN_PERFECT_GAME = 12


def roll_many(game, count, pins):
    for _ in range(count):
        game.roll(pins)


def roll_spare(game):
    game.roll(SPARE_FIRST_AND_SECOND_ROLL)
    game.roll(SPARE_FIRST_AND_SECOND_ROLL)


def roll_strike(game):
    game.roll(STRIKE_ROLL)


def test_gutter_game_scores_zero():
    game = Game()
    roll_many(game, ROLLS_IN_GAME_WITHOUT_BONUSES, GUTTER_ROLL)
    assert game.score() == 0


def test_all_ones_scores_twenty():
    game = Game()
    roll_many(game, ROLLS_IN_GAME_WITHOUT_BONUSES, SINGLE_PIN)
    assert game.score() == 20


def test_spare_adds_next_roll_as_bonus():
    game = Game()
    roll_spare(game)
    game.roll(3)
    roll_many(game, 17, GUTTER_ROLL)
    assert game.score() == 16


def test_strike_adds_next_two_rolls_as_bonus():
    game = Game()
    roll_strike(game)
    game.roll(3)
    game.roll(4)
    roll_many(game, 16, GUTTER_ROLL)
    assert game.score() == 24


def test_perfect_game_scores_three_hundred():
    game = Game()
    roll_many(game, ROLLS_IN_PERFECT_GAME, STRIKE_ROLL)
    assert game.score() == 300