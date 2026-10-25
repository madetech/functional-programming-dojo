import random

import test_bowling

SHUFFLE_ROUNDS = 20

test_names = [name for name in dir(test_bowling) if name.startswith("test_")]
for _ in range(SHUFFLE_ROUNDS):
    random.shuffle(test_names)
    for name in test_names:
        getattr(test_bowling, name)()
print("Every order passed")