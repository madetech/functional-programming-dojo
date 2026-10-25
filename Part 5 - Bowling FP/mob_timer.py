import argparse
import time

SECONDS_PER_MINUTE = 60
TERMINAL_BELL = "\a"


def rotate(team):
    return team[1:] + team[:1]


def describe(team):
    driver, navigator, *mob = team
    return (
        f"Driver:    {driver} (types only what the navigator says)\n"
        f"Navigator: {navigator} (says what to type, in plain words)\n"
        f"Mob:       {', '.join(mob) if mob else '(nobody)'} (suggest, review, keep time)"
    )


def run_mob_session(team, minutes_per_turn, turns):
    for turn_number in range(1, turns + 1):
        print(f"\n--- Turn {turn_number} of {turns}: {minutes_per_turn} minutes ---")
        print(describe(team))
        time.sleep(minutes_per_turn * SECONDS_PER_MINUTE)
        print(f"{TERMINAL_BELL}Time! Commit if green, then rotate.")
        team = rotate(team)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Mob programming rotation timer")
    parser.add_argument("names", nargs="+", help="at least two names, in starting order")
    parser.add_argument("--minutes", type=float, default=4)
    parser.add_argument("--turns", type=int, default=6)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    run_mob_session(arguments.names, arguments.minutes, arguments.turns)