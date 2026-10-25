PINS_PER_FRAME = 10
FRAMES_PER_GAME = 10
ROLLS_PER_NORMAL_FRAME = 2


class Game:
    rolls = []

    def roll(self, pins):
        self.rolls.append(pins)

    def score(self):
        total = 0
        roll_index = 0
        for _ in range(FRAMES_PER_GAME):
            if self._is_strike(roll_index):
                total += PINS_PER_FRAME + self._strike_bonus(roll_index)
                roll_index += 1
            elif self._is_spare(roll_index):
                total += PINS_PER_FRAME + self._spare_bonus(roll_index)
                roll_index += ROLLS_PER_NORMAL_FRAME
            else:
                total += self._open_frame_score(roll_index)
                roll_index += ROLLS_PER_NORMAL_FRAME
        return total

    def _is_strike(self, roll_index):
        return self.rolls[roll_index] == PINS_PER_FRAME

    def _is_spare(self, roll_index):
        return self._open_frame_score(roll_index) == PINS_PER_FRAME

    def _open_frame_score(self, roll_index):
        return self.rolls[roll_index] + self.rolls[roll_index + 1]

    def _strike_bonus(self, roll_index):
        return self.rolls[roll_index + 1] + self.rolls[roll_index + 2]

    def _spare_bonus(self, roll_index):
        return self.rolls[roll_index + 2]