# Introduction to Functional Programming with TDD

*A facilitator-and-learner walkthrough for apprentice software engineers.*

**Format:** half-day (4 hours) plus a retro. **Language:** Python for Part One, Elm for Part Two. **Prerequisites:** basic Python, nothing else. No FP, Elm or Elixir knowledge is assumed.

> 🎓 **Facilitator note:** Each section has learner-facing text and facilitator notes. Read the notes aloud or paraphrase them. The `💬 Discussion` gaps are deliberate. Resist the urge to fill the silence. Count to ten in your head before rescuing anyone.

## Timing overview

| Section | Name | Minutes | Running total |
|---|---|---|---|
| **Part One - The Basics** | | **150** | |
| 1 | What is functional programming? | 20 | 0:20 |
| 2 | Core concepts through Fibonacci | 35 | 0:55 |
| 3 | Strengths and weaknesses | 15 | 1:10 |
| 4 | Worked example: Bowling Kata (OOP, with a bug) | 35 | 1:45 |
| 5 | Mob programming: Bowling Kata, functionally | 35 | 2:20 |
| 6 | Discussion: FP on real projects | 10 | 2:30 |
| **Part Two - A Functional Language** | | **90** | |
| 7 | Meet Elm: setup and syntax primer | 20 | 2:50 |
| 8 | Pair-programming TDD kata | 35 | 3:25 |
| 9 | Show and tell | 15 | 3:40 |
| 10 | Discussion: dedicated FP language vs FP in Python | 10 | 3:50 |
| 11 | Reflection | 10 | 4:00 |
| **Retro** | | **20** | |
| 12 | Retrospective | 20 | - |

Part One runs 2h30 and Part Two 1h30, which makes 4 hours. The retro sits on top (15-30 minutes, planned at 20).

> 🎓 **Facilitator note:** Hold a 10-minute comfort break between Part One and Part Two. It is not counted in the table, so either start 10 minutes earlier or shave a minute or two off several sections. The running totals above are teaching time only.

> **A note on "KSBs":** *Knowledge, Skills and Behaviours* are the competencies your apprenticeship standard says you must demonstrate. Each section names the ones it supports, and the final table tells you what evidence to capture. KSB wording varies slightly between standard versions, so check the codes against your own apprenticeship's document.

## Before you start

**Learner setup (Part One):**

You need Python 3.10 or newer. Check what you have first:

```bash
python3 --version
```

If that prints 3.10 or higher, skip to *Create a virtual environment* below.

**Installing Python on a Mac**

The `python3` that ships with macOS (via Apple's Command Line Tools) is usually 3.9, which is too old for this workshop. The simplest fix is to install a current Python with [Homebrew](https://brew.sh), the macOS package manager.

1. **Install Apple's Command Line Tools** (compilers and `git` that Homebrew relies on). A dialog will pop up; click *Install* and wait for it to finish:

   ```bash
   xcode-select --install
   ```

   If it says the tools are already installed, carry on.

2. **Install Homebrew** (skip if `brew --version` already works). Paste this into Terminal and follow the prompts; it will ask for your Mac password:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Add Homebrew to your PATH.** On Apple Silicon Macs (M1 and later) the installer prints a "Next steps" block; run the commands it shows, which are normally:

   ```bash
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```

   Intel Macs install to `/usr/local`, which is already on the PATH, so this step is not needed there. Check it worked with `brew --version`.

4. **Install Python:**

   ```bash
   brew install python@3.13
   ```

5. **Open a new Terminal window** and confirm the new version is picked up:

   ```bash
   python3 --version   # should now show 3.13.x
   which python3       # should be under /opt/homebrew or /usr/local, not /usr/bin
   ```

   If it still shows the old version, close every Terminal window and try again, or check step 3.

> 💡 **Not on a Mac?** On Windows, install Python from [python.org](https://www.python.org/downloads/) and tick *Add python.exe to PATH* in the installer. On Linux, use your distribution's package manager (for example `sudo apt install python3 python3-venv`).

**Create a virtual environment**

From your workshop folder:

```bash
python3 --version          # 3.10 or newer
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install pytest
```

Create a working folder with this layout. You will add files as you go:

```text
fp-workshop/
├── fibonacci.py
├── bowling_oop/
│   ├── bowling.py
│   └── test_bowling.py
└── bowling_fp/
    ├── bowling.py
    └── test_bowling.py
```

Run tests from inside the folder you are working in with `python -m pytest -v`.

**Part One - The Basics (2.5 hours)**

## Section 1 - What is functional programming?

**Timing:** 20 minutes (10 talk, 5 activity, 5 discussion)
**Learning objective:** Explain the difference between imperative and declarative programming, and place FP, OOP, Infrastructure as Code (IaC) and query/markup languages on that spectrum.
**KSBs:** K7, S17

### Subsection 1.1 - Telling versus asking

Imagine getting to a friend's house.

- **Imperative** is giving *directions*: "Turn left at the chippy, go straight for 400 metres, take the second right." You spell out **how**, step by step.
- **Declarative** is typing the postcode into a sat-nav: "Take me to LE11 3TU." You say **what** you want and something else works out the how.

Definitions, so nobody has to pretend:

- **Imperative programming:** code that is a sequence of instructions that change the program's **state** (state is just "the values your program is remembering right now").
- **Declarative programming:** code that describes the **result** you want and leaves the steps to the language, library or tool.

You have used both already. Compare these two ways of getting the squares of even numbers:

```python
numbers = [1, 2, 3, 4, 5, 6]

squares_of_evens_imperative = []
for number in numbers:
    if number % 2 == 0:
        squares_of_evens_imperative.append(number * number)

squares_of_evens_declarative = [number * number for number in numbers if number % 2 == 0]

assert squares_of_evens_imperative == squares_of_evens_declarative == [4, 16, 36]
```

The first version says "make an empty box, loop, check, add." The second says "I want the squares of the even numbers." Same answer, different mindset.

### Subsection 1.2 - It is a spectrum, not a switch

Few languages sit at one extreme, and many let you mix styles (Python certainly does).

| Style | Typical examples | Imperative ↔ Declarative | What you describe | Analogy |
|---|---|---|---|---|
| **OOP** (object-oriented) | Java, C#, Python classes | Mostly imperative | Objects that hold state and change it via methods | A kitchen of staff, each with their own notebook |
| **FP** (functional) | Elm, Elixir, Haskell, Python used carefully | Leans declarative | Transformations of data using functions that don't change anything | A recipe card: same ingredients in, same meal out |
| **IaC** (Infrastructure as Code) | Terraform, CloudFormation, Kubernetes manifests | Declarative (Ansible and scripts are more mixed) | The servers and networks you *want to exist* | Ordering a room layout, not carrying the furniture |
| **Query languages** | SQL, GraphQL | Highly declarative | The rows you want, not how to find them | Asking a librarian for "all books about sharks since 2020" |
| **Markup languages** | HTML, CSS, Markdown | Highly declarative | What the page *is*, not how to draw it | A blueprint |

```text
IMPERATIVE <------------------------------------------------> DECLARATIVE
 C, scripts    OOP        Python mixed     FP        IaC       SQL, HTML
```

> 🎓 **Facilitator note:** Expect the pushback "isn't OOP declarative if I just call `order.total()`?" Good instinct. The *call site* reads declaratively, but inside the method it's usually step-by-step state changes. Spectrum, not binary. Don't spend more than two minutes on this.

> 🛠️ **Activity (5 min, pairs):** Take the squares-of-evens example. Add a requirement: "also skip any number divisible by 3." Change both versions. Which one was easier to edit without breaking? Which has more places for a typo?

> 💬 **Discussion (5 min):**
> 1. Where have you already used a declarative tool at work (SQL, HTML, a config file) without calling it that?
> 2. What do you gain by *not* controlling the steps? What do you lose?
> 3. Is a recipe imperative or declarative? Argue both sides.

## Section 2 - Core concepts through Fibonacci

**Timing:** 35 minutes (10 talk, 15 activity, 10 discussion and wrap-up)
**Learning objective:** Recognise and write pure functions, use immutable data, and write a simple recursive function, by evolving the same Fibonacci function from imperative to functional.
**KSBs:** K7, S14, K6

> **Reassurance:** In the next half hour you'll meet three words: **pure function**, **immutability** and **recursion**. They sound like they came from a maths textbook. They didn't. Each one is a very ordinary idea with an intimidating name, and by the end of this session you'll be using all three without noticing.

### Subsection 2.1 - The Fibonacci sequence

Fibonacci numbers start `0, 1` and every following number is the **sum of the previous two**: `0, 1, 1, 2, 3, 5, 8, 13, 21, 34 ...`

Create `fibonacci.py`. We'll build up the file through this section.

### Subsection 2.2 - Version 1: imperative

```python
FIRST_TWO_FIBONACCI_NUMBERS = (0, 1)


def fibonacci_imperative(position):
    previous, current = FIRST_TWO_FIBONACCI_NUMBERS
    for _ in range(position):
        previous, current = current, previous + current
    return previous
```

This works, and it's a perfectly good Python function. Notice that it *changes variables in a loop*. Keep that in mind.

### Subsection 2.3 - Pure functions

**Side effect:** anything a function does besides returning a value, such as changing a variable outside itself, printing, writing a file, or calling an API.

**Pure function:** a function that (1) always gives the same output for the same input and (2) has no side effects. Think of a **vending machine**: press B4, always get the same crisps, and the machine doesn't secretly rearrange the shop.

Here is a function that is **not** pure:

```python
fibonacci_so_far = [0, 1]


def next_fibonacci_impure():
    fibonacci_so_far.append(fibonacci_so_far[-1] + fibonacci_so_far[-2])
    return fibonacci_so_far[-1]


print(next_fibonacci_impure(), next_fibonacci_impure())  # 1 2 - different every call
```

Same input (nothing), different output each time, and it modifies a list that lives outside the function. Now the pure alternative:

```python
def next_pair(pair):
    previous, current = pair
    return (current, previous + current)


assert next_pair((0, 1)) == (1, 1)
assert next_pair((0, 1)) == (1, 1)  # call it as often as you like
```

> 🛠️ **Activity (3 min, solo):** Which of these are pure? Write P or I for each.
> `len("hello")`, `random.randint(1, 6)`, `datetime.now()`, `sorted(numbers)`, `numbers.sort()`, `print("hi")`.
>
> *Answers in the facilitator note below.*

> 🎓 **Facilitator note:** `len` P, `randint` I (different output each time), `datetime.now()` I, `sorted(numbers)` P (returns a new list), `numbers.sort()` I (mutates the list and returns `None`), `print` I (side effect: writes to screen). The `sorted`/`sort` pair is the best bridge to the next idea.

### Subsection 2.4 - Immutability

**Immutable** means "can't be changed after it's created." Python's `tuple` and `str` are immutable; `list` and `dict` are **mutable** (changeable). In FP, instead of editing a thing you make a *new* thing.

```python
fibonacci_start = (0, 1)
fibonacci_extended = (*fibonacci_start, 1)

assert fibonacci_start == (0, 1)        # the original is untouched
assert fibonacci_extended == (0, 1, 1)  # a brand new tuple
```

Analogy: a Google Doc with version history versus a whiteboard. On the whiteboard, once somebody wipes it, the old state is gone and you can't tell who did it. Keep this analogy handy for Section 4.

### Subsection 2.5 - Recursion

**Recursion** is when a function solves a problem by calling *itself* on a smaller version of the problem, until it reaches one so small the answer is obvious (the **base case**). Think of Russian nesting dolls: open one, find a smaller one, repeat until you reach the solid doll in the middle.

```python
FIRST_RECURSIVE_POSITION = 2


def fibonacci_recursive(position):
    if position < FIRST_RECURSIVE_POSITION:
        return position
    return fibonacci_recursive(position - 1) + fibonacci_recursive(position - 2)
```

Read it aloud: "The Fibonacci number at position 0 or 1 is just that position. Otherwise it's the sum of the previous two." The code reads like the *definition*. No loop, no variables being reassigned: pure, immutable and recursive in one.

There is a faster style that passes the running totals along as arguments (an **accumulator**), which we'll meet again in Section 3:

```python
def fibonacci_with_accumulator(position, previous=0, current=1):
    if position == 0:
        return previous
    return fibonacci_with_accumulator(position - 1, current, previous + current)
```

### Subsection 2.6 - Prove they agree (TDD in miniature)

```python
EXPECTED_FIRST_TEN = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
FIRST_TEN_POSITIONS = range(10)


def test_all_versions_produce_the_same_sequence():
    for fibonacci in (fibonacci_imperative, fibonacci_recursive, fibonacci_with_accumulator):
        assert [fibonacci(position) for position in FIRST_TEN_POSITIONS] == EXPECTED_FIRST_TEN
```

Notice what the test did *not* need: no setup, no fake database, no cleanup. You called a function and checked the answer. Hold that thought for Section 3.

> 🛠️ **Activity (15 min, pairs, "red-green-refactor" warm-up):**
> 1. **Red:** write `test_negative_position_is_rejected` expecting `ValueError` for `fibonacci_recursive(-1)`. Run it and watch it fail.
> 2. **Green:** make it pass with the smallest change.
> 3. **Refactor:** extract the validation into a small, well-named function.
>
> **Hint:** `pytest.raises(ValueError)` is a context manager that passes only if the code inside raises that error.
> **Pitfall:** the current recursion never stops for negative input. `-1 < 2` returns `-1` actually, so the *wrong answer* comes back silently. Silent wrongness is worse than a crash.
> **Stretch (faster pairs):** write a pure `fibonacci_sequence(length)` that returns a tuple of the first `length` numbers using `next_pair`. **Stretch 2:** time `fibonacci_recursive(30)` versus `fibonacci_with_accumulator(30)` with `timeit`, and predict the result before running.

> 🎓 **Facilitator note:** The naive recursive version recomputes the same values exponentially many times, so it's slow for larger inputs. Mention it now and tie it to the "performance" downside in Section 3. Don't rescue pairs who find this themselves; let them have the moment.

> 💬 **Discussion (7 min):**
> 1. Which version was easiest to *read*? Which was easiest to *trust*?
> 2. Where did you feel the urge to "just add a variable"? What would that have cost you?
> 3. Have you ever had a bug where a value was changed by something you didn't expect?

## Section 3 - Strengths and weaknesses

**Timing:** 15 minutes (8 talk, 7 discussion)
**Learning objective:** Give an honest, balanced account of FP's benefits and costs, and explain the link between pure functions, the test pyramid and mocking.
**KSBs:** K14, K4, K7

### Subsection 3.1 - What FP buys you

| Benefit | Why it follows from the core ideas |
|---|---|
| **Testability** | Pure function: input in, output out. Nothing else to set up. |
| **Fewer shared-state bugs** | If nothing mutates, nothing can be changed behind your back. |
| **Easier reasoning** | You can understand a function by reading it alone, like a maths equation. |
| **Concurrency** | **Concurrency** means several things happening at once (e.g. a web server handling many users). Two threads can't fight over data neither can change. |

### Subsection 3.2 - What FP costs you (honestly)

| Cost | The reality |
|---|---|
| **Learning curve** | Thinking without loops and reassignment feels like writing with your other hand. |
| **Recursion depth** | Each recursive call is stacked in memory. Python gives up around 1,000 deep. |
| **Performance** | Creating new data instead of editing can be slower. Naive recursion can be *much* slower. |
| **Unfamiliar idioms** | `map`, `fold`, "currying", "monads": your colleagues may not speak this yet. |
| **Verbosity** | In some languages, tasks that are easy with a mutable variable need more ceremony. |

Prove the recursion limit to yourself:

```python
import sys


def fibonacci_with_accumulator(position, previous=0, current=1):
    if position == 0:
        return previous
    return fibonacci_with_accumulator(position - 1, current, previous + current)


print(sys.getrecursionlimit())  # usually 1000
try:
    fibonacci_with_accumulator(5000)
except RecursionError:
    print("Python ran out of stack. Languages built for FP avoid this.")
```

> 🎓 **Facilitator note:** Be honest. Python does **not** optimise "tail calls" (a recursive call as the very last step), but Elm and Elixir do, which is one reason to use them for recursion-heavy FP. Don't oversell FP. The strongest sales pitch is "here is the bug class it removes", which you'll show in Sections 4 and 5.

### Subsection 3.3 - Pure functions and the test pyramid

The **test pyramid** is a model for how many tests of each kind to write.

```text
        /\          Few    End-to-end (UI to database, slow, brittle)
       /  \
      /----\        Some   Integration (several parts talking, medium)
     /      \
    /--------\      Many   Unit tests (one small piece, fast, reliable)
```

- **Unit test:** checks one small piece (usually one function) in isolation.
- **Mocking / test doubles:** fakes (a *mock*, *stub* or *fake*) standing in for real collaborators, such as a database or email service, so the unit under test can run alone.

Impure code needs doubles, because its behaviour depends on the outside world. **Pure functions need few or none**: everything they depend on arrives as arguments, so you can just pass in real values. That is why FP pushes you towards a fat, fast base of unit tests. A common design is "**functional core, imperative shell**": pure logic in the middle (heavily unit-tested), thin impure code at the edge (a few integration tests).

> **Business value (K4):** Fast, trustworthy tests mean teams ship changes sooner and spend less time chasing bugs, and that saves real money. When you present your work, say that, not just "it's cleaner".

> 💬 **Discussion (7 min):**
> 1. Think of a test you've written or seen that used a mock. Could the logic have been a pure function instead?
> 2. If your whole team hated recursion, would you still use FP techniques? Which ones?
> 3. Which "cost" above worries you most, and which "benefit" tempts you most?

## Section 4 - Worked example: Bowling Kata

**Timing:** 35 minutes (5 kata rules and code tour, 20 bug hunt, 10 reveal and debrief)
**Learning objective:** Use hypothesis-driven problem solving (observe, hypothesise, test, confirm) to find a bug caused by mutable shared state.
**KSBs:** S11, S14, K14

### Subsection 4.1 - The kata rules (summary)

A **kata** is a small practice exercise you repeat to build skill, like scales on a piano. Bowling scores a game of **10 frames**:

- Each frame has up to **two rolls** to knock down **10 pins**.
- **Open frame:** fewer than 10 pins in two rolls. Score = pins knocked down.
- **Spare:** all 10 pins down in two rolls. Score = 10 + the pins from the **next one roll** (the bonus).
- **Strike:** all 10 pins down with the first roll (the frame ends). Score = 10 + the pins from the **next two rolls**.
- **Tenth frame:** a spare earns one extra roll; a strike earns two extra rolls. These bonus rolls only count as bonuses, they're not frames of their own.
- A **perfect game** is twelve strikes in a row and scores **300**.

Your program has two jobs: `roll(pins)` records a roll, and `score()` returns the total. It doesn't need to validate impossible games.

### Subsection 4.2 - The object-oriented implementation

Create `bowling_oop/bowling.py`:

```python
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
```

And `bowling_oop/test_bowling.py`:

```python
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
```

> 🎓 **Facilitator note:** Hand out the code and run `python -m pytest -v` from `bowling_oop/` **live, on the projector, before explaining anything**. Expected result: **1 passed, 4 failed** (the gutter game passes; the other four fail). Do not mention the bug. Say only: "The scoring rules look right to me. Someone tell me why these are red." Then run `python -m pytest -v -k all_ones` and watch faces when it goes green.

### Subsection 4.3 - Bug hunt: observe, hypothesise, test, confirm

**Hypothesis-driven problem solving** means resisting "poke it until it works". Instead you form a *specific, testable guess* about the cause and design a cheap experiment that could prove it wrong. Scientists do it. So should debuggers.

> 🛠️ **Activity (20 min, groups of 3, S11):** Copy this template into a file called `bug-hunt-notes.md` and fill it in as you go. **This is your KSB evidence.**
>
> ```markdown
> ## Observe  (facts only, no theories)
> - Which tests fail? Which pass?
> - What do they report (expected vs actual)?
> - What changes when a test is run alone?
>
> ## Hypothesis  (one specific, falsifiable sentence)
> "I think ___ because ___. If I'm right, then ___ should happen."
>
> ## Test  (the cheapest experiment)
> - What exactly did we run or change?
>
> ## Confirm / reject
> - What happened? Was the hypothesis supported? If not, return to Observe.
> ```
>
> **Ground rules:** do not edit `Game` until you have written a hypothesis down. Try to write at least two hypotheses.
>
> **Hint 1 (after 5 min):** What differs between running `-k all_ones` and running the whole file?
> **Hint 2 (after 10 min):** Add `print(id(game.rolls), len(game.rolls))` at the start of `score()`. What do you see across tests?
> **Hint 3 (after 15 min):** Where is `rolls` created, and how many times does that line run?
> **Pitfall:** "The scoring logic is wrong." It isn't. Each test passes when run alone, so the logic is fine, which is a strong clue.
> **Stretch:** After you fix the bug, write a regression test that fails against the buggy version and passes against the fixed one. Why does it need *two* `Game` objects?

> 🎓 **Facilitator answer key (do not share before the reveal):**
>
> **The bug.** `rolls = []` is declared in the **class body**, not in `__init__`. A class attribute belongs to the *class*, so every `Game` instance shares **one single list**. `self.rolls.append(pins)` doesn't create a per-game attribute; it finds the shared list through the class and mutates it.
>
> **Why the tests behave as they do.** Pytest runs the tests in file order in one process:
> 1. The gutter game appends 20 zeros to the shared list, then scores 0, which is correct, so it **passes**.
> 2. `test_all_ones` creates a *new* `Game`, but it's still the same list. It now holds 20 zeros followed by 20 ones. `score()` reads from the start of the list, so it scores the *previous game's* zeros and returns 0, not 20. **Fail.**
> 3. Every later test scores from those same first twenty zeros, so each returns 0 and fails.
> 4. Run any test alone and the list starts empty, so it passes. That's the diagnostic fingerprint of shared mutable state: **order-dependent results**.
>
> **Why it exists (the human story).** It looks harmless, even tidy: "declare my fields at the top of the class". Python's class syntax makes the wrong thing look like the normal thing. And the mistake is invisible when you run one test at a time or when you only ever create one `Game` in production.
>
> **The classic fix:**
>
> ```python
> class Game:
>     def __init__(self):
>         self.rolls = []
> ```
>
> **The bigger lesson.** The fix works, but notice the root cause is that the *design allows* a list to be mutated by anyone, from anywhere, without anyone noticing. We patched the symptom. In Section 5 we'll remove the cause.
>
> **Reference hypotheses a good group might write:**
> - *"Test order matters."* Test: run with `-p no:randomly -k` variants or reorder tests. Supported.
> - *"The list isn't reset between games."* Test: print `len(game.rolls)` at the start of each test. Supported (this is the winner).
> - *"The spare/strike logic is off by one."* Test: run `test_all_ones` alone. Rejected.

> 💬 **Discussion (10 min, includes the reveal):**
> 1. Which hypothesis did your group reject, and what rejected it? Was that a wasted effort?
> 2. How long would this have taken to find in a 50,000-line codebase with no tests?
> 3. Could a code review have spotted it? What would you have looked for?

## Section 5 - Mob programming: the Bowling Kata, functionally

**Timing:** 35 minutes (5 briefing, 24 mobbing in six 4-minute turns, 6 debrief: 3 min experiment, 3 min discussion)
**Learning objective:** Re-implement the Bowling Kata using FP techniques and TDD in a mob, and explain why this style makes the Section 4 bug much less likely.
**KSBs:** S13, B1, S14, K14, K4

### Subsection 5.1 - What is mob programming?

**Mob programming** is the whole team working on one problem, at one keyboard, at the same time. Only one person types. Everyone else thinks. It sounds slow. In practice it's surprisingly quick, because nobody is stuck alone and nobody is waiting on a code review afterwards.

Think of a pub quiz team: one person writes the answers, but the whole table is working out what to write.

| Role | Does | Does **not** |
|---|---|---|
| **Driver** | Types exactly what the navigator says. Asks if unclear. | Decide the design. Argue. |
| **Navigator** | Says what to do in plain words ("create a test called...", "return the sum"). One voice at a time. | Grab the keyboard. |
| **Mob** (everyone else) | Suggests ideas **to the navigator**, spots typos, checks the plan against the rules, keeps time. | Shout over the navigator. Look at their phones. |

**Rotation:** every 4 minutes the driver goes to the back of the mob, the navigator becomes the driver, and the next person in the mob becomes the navigator. The timer script below announces it and tells you who's who.

> 🎓 **Facilitator note:** Mobs of 4-6 work best. In a room of 12, run two mobs on two screens (or two laptops with a shared view). Confident talkers tend to hog the navigator seat, so use the rotation timer as your referee, not your own voice. Quiet apprentices often shine as navigators because they have to *say* the plan aloud, so watch for it and praise it afterwards.

### Subsection 5.2 - The rotation timer

Save this as `mob_timer.py`. It has no dependencies. Start it with the mob's names in order, for example `python mob_timer.py Ana Ben Cat Dev --minutes 4 --turns 6`.

```python
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
```

Notice the `rotate` function is pure: it returns a **new** list and never edits the old one. Even the timer follows the lesson.

### Subsection 5.3 - Design decisions before typing

Spend two of your five briefing minutes agreeing three things as a mob:

1. **The input is a tuple of rolls**, for example `(10, 10, 10, ...)`. A tuple can't be changed once created (immutability, Section 2.4).
2. **`score` is one pure function**: rolls in, number out. There is no `Game` object and no `roll()` method that stores anything.
3. **Recursion walks the frames:** score one frame, then ask `score` to handle "the rest of the rolls" with one frame fewer to go. The base case is "no frames left".

### Subsection 5.4 - The TDD progression

Work in `bowling_fp/`. At each step, the whole mob agrees on the *smallest* thing that turns the test green. If you catch yourself writing code for a test you haven't written, stop.

| Step | Red (new test) | Green (smallest change) | Refactor prompt |
|---|---|---|---|
| 1 | Gutter game scores 0 | `return sum(rolls)` (yes, really) | None needed yet |
| 2 | All ones scores 20 | Nothing! It's already green | Discuss: is a test that passes first time useful? (Yes: it documents behaviour and guards it.) |
| 3 | Spare adds the next roll | Split the rolls into frames; add the bonus roll for a spare | Name the "is it a spare?" check |
| 4 | Strike adds the next two rolls | Add the strike case: a strike uses **one** roll, with **two** bonus rolls | Spot the pattern: each frame type is just "rolls used" plus "bonus rolls" |
| 5 | Spare in the last frame earns one bonus roll | Probably already green. Check! | Remove duplication |
| 6 | Strike in the last frame earns two bonus rolls | Probably already green | Replace the number-pair with named constants |
| 7 | Perfect game scores 300 | Should be green | Final tidy: read it aloud, rename anything unclear |
| 8 | Scoring doesn't change its input, and gives the same answer twice | Green already | These tests *prove the purity* we claimed |

> 🛠️ **Activity (24 min, mob, S13 and B1):** Start the timer. Build the solution by following the table. Commit (or save a copy) every time the tests go green. Someone other than the current driver should write down, at each rotation, *one thing the mob learned*, which you'll use in the debrief.
>
> **Hint (stuck on step 3):** Think of `score` as "score the first frame, then add `score(everything after that frame)`". What do you need to know about the first frame to decide how many rolls it *uses* and how many extra rolls it *peeks at*?
> **Hint (stuck on recursion):** Write the base case first. When no frames are left, what's the score?
> **Pitfall:** A strike uses one roll but *looks at* the next two, which stay in the list for the following frame. Remove only the rolls the frame *uses*, not the ones it peeks at.
> **Pitfall:** Reaching for `rolls.pop(0)` or a running `total` variable. That's the imperative reflex. Ask the mob: "Can we return a new value instead?"
> **Stretch (quick mobs):** Add validation, so impossible rolls (say, 7 then 8 in one frame) raise a clear `ValueError`. Where does it belong, inside `score` or in a separate pure function? **Stretch 2:** Write a pure `frame_scores(rolls)` that returns the score of each of the ten frames as a tuple.

### Subsection 5.5 - A reference solution

> 🎓 **Facilitator note:** Don't hand this out until the mob has finished or time is up. Mobs often produce something different and equally good, so use this as a comparison point rather than the "right answer". This solution has been run against the tests below (all nine pass).

`bowling_fp/bowling.py`:

```python
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
```

`bowling_fp/test_bowling.py`:

```python
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
```

Read `score` slowly: it scores one frame, then calls itself on the remaining rolls. It never changes the input, it keeps no running total, and it has no state to forget to reset.

### Subsection 5.6 - Why this bug class (mostly) disappears

Remember the OOP bug: a list shared by every `Game`, silently growing between tests. Now look at what the FP version does differently:

| In the OOP version | In the FP version |
|---|---|
| The game's rolls live **inside an object**, hidden between calls | The rolls are an **argument**: everything `score` uses is visible in its call |
| `rolls` is a mutable list that anything can append to | `rolls` is a tuple; `append` isn't even available |
| Results depend on **what ran before** (test order) | Results depend only on the **input**, so order is irrelevant |
| The bug needed a human to notice order-dependent failures | There is no hidden state for the bug to live in |

> 🛠️ **Activity (3 min, mob, optional "try to break it"):** Two quick experiments:
>
> 1. In a Python shell, run `(1, 2).append(3)`. Read the error.
> 2. Write a test that runs the nine tests in a random order, 20 times. Does anything fail?
>
> ```python
> import random
>
> import test_bowling
>
> SHUFFLE_ROUNDS = 20
>
> test_names = [name for name in dir(test_bowling) if name.startswith("test_")]
> for _ in range(SHUFFLE_ROUNDS):
>     random.shuffle(test_names)
>     for name in test_names:
>         getattr(test_bowling, name)()
> print("Every order passed")
> ```

> 🎓 **Facilitator note (be honest):** FP techniques make this bug *much less likely*, not impossible. Python will happily let someone pass in a list instead of a tuple, or write a function that mutates a global. In Python, immutability is a **discipline**, helped by tuples, frozen dataclasses (`@dataclass(frozen=True)`) and code review. In a language like Elm it's enforced by the compiler, which previews Part Two nicely. The tests `does_not_change_its_input` and `twice_gives_the_same_answer` are cheap guard-rails that turn the discipline into something executable.

> 💬 **Discussion (3 min, debrief):**
> 1. What was it like to drive? To navigate? Which was harder?
> 2. When did the mob disagree, and how did you settle it?
> 3. Did the tests change *how* you designed `score`? Did they ever stop you taking a shortcut?

## Section 6 - Discussion: how and when to use FP techniques on real projects

**Timing:** 10 minutes (3 talk, 7 discussion)
**Learning objective:** Decide where FP techniques add value in everyday work and where they don't.
**KSBs:** K4, K7, S16, B2

### Subsection 6.1 - Take the ideas, not the whole religion

You don't need a new language to benefit. Practical moves you can make in your next pull request:

| Technique | Try it when | Be careful when |
|---|---|---|
| **Pull logic into pure functions** | Business rules (discounts, eligibility, scoring, validation) | The "logic" is mostly calling other systems |
| **Prefer tuples, frozen dataclasses, `sorted()` over `.sort()`** | Data is passed between functions or threads | Large data structures copied in a hot loop (measure first) |
| **"Functional core, imperative shell"** | You can pull the maths and rules out of the code that talks to databases, APIs and screens | The project is a thin wrapper with no logic |
| **Comprehensions, `map` and `filter`** | Transforming a collection | The comprehension needs three nested conditions and nobody can read it |
| **Recursion** | Naturally nested data (trees, folders, JSON) | Depth is unbounded in Python, because of the recursion limit |

A tiny example of the "core and shell" idea. The rule is a pure function that needs no mocks, and the shell stays thin:

```python
PREMIUM_DISCOUNT_RATE = 0.10
PREMIUM_DISCOUNT_THRESHOLD = 100


def apply_discount(order_total, is_premium_customer):
    if is_premium_customer and order_total >= PREMIUM_DISCOUNT_THRESHOLD:
        return round(order_total * (1 - PREMIUM_DISCOUNT_RATE), 2)
    return order_total


def test_premium_customer_gets_discount_at_threshold():
    assert apply_discount(200, True) == 180.0


def test_other_customers_pay_full_price():
    assert apply_discount(200, False) == 200
    assert apply_discount(50, True) == 50
```

The "shell" would be the few lines that load the order from a database, call `apply_discount`, and save the result. Those lines need an integration test, but the *rule*, the bit that changes most often, needs only unit tests.

> **Business value (K4):** The discount rule is the part of the code the business changes most often and where an error costs real money. Making it pure and cheap to test means changes ship faster and wrong prices ship less often.

> 🛠️ **Activity (3 min, solo, S16 and B2):** On a sticky note or in your learning log, write one function from your *current* work project that could be made pure. What would you have to move out of it?

> 💬 **Discussion (7 min):**
> 1. Where in your current project would FP techniques help most? Where would they be a bad idea?
> 2. How would you introduce a new style to a team that doesn't know it? What would convince *you* if you were the sceptic?
> 3. When is "good enough, mutable, and finished" the right answer?

**Part Two - A Functional Language (1.5 hours)**

## Section 7 - Meet Elm: setup and syntax primer

**Timing:** 20 minutes (10 setup, 10 primer)
**Learning objective:** Install the Elm toolchain, read basic Elm syntax, and run a first test.
**KSBs:** K7, S16, B2

### Subsection 7.1 - Why Elm, not Elixir?

Either language would work. We use **Elm** for this session:

| | Elm | Elixir |
|---|---|---|
| **Setup** | Two npm packages, five minutes | Erlang/OTP, Elixir and usually a version manager. More that can go wrong on a locked-down laptop |
| **Purity** | **Enforced by the compiler.** A function *cannot* modify anything or talk to the outside world | Mostly functional, but processes, side effects and macros are a short step away |
| **Types** | Statically typed: the compiler catches mistakes before you run anything | Dynamically typed |
| **Error messages** | Famously friendly: they read like a helpful colleague | Good, but terser |
| **Honest downsides** | Aimed at web front ends, small ecosystem, fewer jobs than JavaScript | Bigger ecosystem and a strong back-end story, but more to learn before the "functional" part clicks |

For a first taste of FP in 90 minutes, the compiler doing the policing is a huge advantage. It's the "immutability is enforced, not a discipline" language we promised at the end of Section 5.

> 🎓 **Facilitator note:** If your apprentices' employers use Elixir, swap in Elixir with ExUnit. The kata (Section 8) and the discussion prompts work unchanged, but budget extra setup time and test installs in advance. **Whichever you choose, test the setup on a spare machine, ideally one with your organisation's usual security restrictions, before the day.** If installs are blocked, a pre-configured GitHub Codespace or dev container is the best plan B.

### Subsection 7.2 - Setup

> 🛠️ **Activity (10 min, individually, then help a neighbour):**
>
> ```bash
> node --version                       # needs a reasonably recent Node.js
> npm install --global elm elm-test
> elm --version                        # should print 0.19.something
>
> mkdir roman-numerals
> cd roman-numerals
> elm init                             # answer y when asked
> elm-test init                        # answer y when asked
> ```
>
> You should now have `src/`, `tests/` and an `elm.json` file. Run `elm-test`. A passing (or deliberately failing) example test means you're ready.
>
> **Pitfall:** global npm installs failing with permission errors. Use `npx elm-test` for tests and ask the facilitator rather than using `sudo`.
> **Stretch (early finishers):** Read the generated `tests/Example.elm`, then help someone who is stuck.

### Subsection 7.3 - A ten-minute syntax primer

Elm looks odd for about ten minutes and then looks calm. Here are the differences from Python that matter today.

| Python | Elm | Note |
|---|---|---|
| `def add(a, b): return a + b` | `add a b = a + b` | No brackets or commas for arguments, no `return`: the function *is* the expression |
| `x = 5` then later `x = 6` | Not allowed | Names are bound once. Immutability is enforced |
| `for` / `while` | Recursion, or `List.map`, `List.filter`, `List.foldl` | There are no loops at all |
| `if/else` statements | `if ... then ... else ...` **expressions**, which always return a value | `else` is mandatory |
| `None` | `Maybe` (`Just 5` or `Nothing`) | No null, so no "NoneType has no attribute" crashes |
| `[1, 2]`, `(1, 2)` | `[ 1, 2 ]` (all the same type), `( 1, 2 )` | |
| `"a" + "b"` | `"a" ++ "b"` | `++` joins strings and lists |
| `# comment` | `-- comment` | |

Create `src/Primer.elm` and read it top to bottom:

```elm
module Primer exposing (describeNumber, double, doubleAll, firstOrZero, sumAll)


doublingFactor : Int
doublingFactor =
    2


double : Int -> Int
double number =
    number * doublingFactor


describeNumber : Int -> String
describeNumber number =
    if number < 0 then
        "negative"

    else if number == 0 then
        "zero"

    else
        "positive"


doubleAll : List Int -> List Int
doubleAll numbers =
    List.map double numbers


sumAll : List Int -> Int
sumAll numbers =
    case numbers of
        [] ->
            0

        first :: rest ->
            first + sumAll rest


firstOrZero : List Int -> Int
firstOrZero numbers =
    List.head numbers |> Maybe.withDefault 0
```

Things to notice:

- The line `double : Int -> Int` is a **type annotation**: "takes an `Int`, returns an `Int`". It's optional but good practice, and it's checked by the compiler.
- `case ... of` is **pattern matching**: "if the list is empty, do this; if it has a first item and the rest, do that." `first :: rest` means "a list that starts with `first`, followed by `rest`". It's the recursion from Section 2 with the base case spelled out.
- `|>` is the **pipe**: "take what's on the left and feed it into the function on the right". It reads like a sentence, left to right.
- `List.head` returns a `Maybe`, because an empty list has no head. The compiler *forces* you to handle both cases.

Try it in the REPL (the interactive prompt):

```bash
elm repl
```

```elm
> import Primer exposing (..)
> doubleAll [ 1, 2, 3 ]
> sumAll [ 10, 20, 30 ]
> firstOrZero []
> describeNumber -4
```

> 💬 **Discussion (included in the primer, 2 min):**
> 1. What does Elm *stop* you from doing that Python allows? Is that annoying, comforting, or both?
> 2. Which line did you find hardest to read, and why?

> 🎓 **Facilitator note:** Don't teach more syntax than this. The kata only needs lists, tuples, `case`, recursion, `String` functions and the test library. Learners will absorb more by doing than by being told.

## Section 8 - Pair-programming TDD kata: Roman Numerals

**Timing:** 35 minutes (5 briefing, 30 pairs)
**Learning objective:** Apply red-green-refactor in an unfamiliar language, working as a pair.
**KSBs:** S14, S13, B1, K14, K6

### Subsection 8.1 - Why this kata?

Roman Numerals is a different shape of problem from Bowling: no state and no game, only one pure function that turns a number into text. That makes it a good fit for a language where pure is the only option.

### Subsection 8.2 - The rules

Write `toRoman : Int -> String`, converting a whole number from 1 to 3999 into Roman numerals.

| Symbol | I | V | X | L | C | D | M |
|---|---|---|---|---|---|---|---|
| Value | 1 | 5 | 10 | 50 | 100 | 500 | 1000 |

- Symbols are written largest to smallest and **added**: `VIII` = 5 + 1 + 1 + 1 = 8.
- A symbol can be repeated up to three times: `III` = 3, but 4 is **not** `IIII`.
- To avoid four in a row, a smaller symbol **before** a larger one is **subtracted**. There are only six such pairs: `IV` (4), `IX` (9), `XL` (40), `XC` (90), `CD` (400), `CM` (900).
- Example: 1994 = 1000 + 900 + 90 + 4 = `MCMXCIV`.

You do not need to handle 0, negative numbers or numbers above 3999.

### Subsection 8.3 - Pairing with ping-pong

**Pair programming** is two people at one computer. **Ping-pong pairing** suits TDD well:

1. **Person A** writes a failing test (red) and passes the keyboard.
2. **Person B** makes it pass with the smallest change (green), then they **refactor together**.
3. **Person B** writes the next failing test, and the keyboard goes back.

Talk constantly. If you're silent, you're not pairing, you're just taking turns.

### Subsection 8.4 - Suggested progression

Create `tests/RomanNumeralsTest.elm` with the helper and the first test only, and an empty module `src/RomanNumerals.elm` containing a stub, so the first failure is a *test* failure rather than a compile error.

```elm
module RomanNumerals exposing (toRoman)


toRoman : Int -> String
toRoman _ =
    ""
```

```elm
module RomanNumeralsTest exposing (suite)

import Expect
import RomanNumerals exposing (toRoman)
import Test exposing (Test, describe, test)


expectRoman : Int -> String -> Test
expectRoman number expected =
    test (String.fromInt number ++ " is " ++ expected) <|
        \_ ->
            Expect.equal expected (toRoman number)


suite : Test
suite =
    describe "toRoman"
        [ expectRoman 1 "I"
        ]
```

Then add one test at a time, in this order:

| Step | New test (red) | Smallest change (green) | Refactor prompt |
|---|---|---|---|
| 1 | `1` is `I` | `toRoman _ = "I"` (a deliberate cheat!) | None |
| 2 | `2` is `II` | `String.repeat number "I"` | Is the cheat gone? |
| 3 | `3` is `III` | Already green | Notice what this proves: the repeat rule works |
| 4 | `4` is `IV` | A special case for 4 | Ugly, but honest. Leave it |
| 5 | `5` is `V`, `6` is `VI` | Handle 5 and the remainder | Is a pattern appearing? |
| 6 | `9` is `IX`, `10` is `X`, `14` is `XIV` | More special cases... | **Stop and look.** You're writing the same shape over and over |
| 7 | Refactor, with all tests still green | Replace the special cases with a **table** of value/symbol pairs, largest first, and recurse over it | Name the table. Read it aloud |
| 8 | `40` is `XL`, `49` is `XLIX`, `90` is `XC` | Should be green, because they're just more table rows | Surprised? That's the payoff of finding the pattern |
| 9 | `400` is `CD`, `900` is `CM`, `1994` is `MCMXCIV`, `3999` is `MMMCMXCIX` | Should be green | Final tidy |

> 🛠️ **Activity (30 min, pairs, S14 and S13):** Follow the table. Commit with `git` (or save a numbered copy) after every green so there's evidence of the red-green rhythm. Swap keyboard at every new test.
>
> **Hint (stuck at step 7):** Think of a list of pairs like `( 1000, "M" )`, `( 900, "CM" )`, and so on, largest first. Ask: "Is my number at least as big as the first value? If so, write the symbol and subtract. If not, move down the table."
> **Hint (Elm syntax):** To take apart a list use `case table of [] -> ... ; ( value, symbol ) :: smallerEntries -> ...`
> **Pitfall:** Forgetting `else`: Elm `if` always needs one. Another is indenting `case` branches inconsistently; the compiler's message will tell you exactly where.
> **Pitfall:** Treating a compiler error as failure. In Elm, *the compiler is your first test*. Read the message aloud to your partner before touching anything.
> **Stretch (faster pairs):** Add the reverse, `fromRoman : String -> Int`. Which tests would you write first? **Stretch 2:** Property-style check: for every number 1 to 3999, `fromRoman (toRoman n)` should equal `n`.

> 🎓 **Facilitator reference solution (hold back until pairs have finished or time is up):**
>
> ```elm
> module RomanNumerals exposing (toRoman)
>
>
> numeralTable : List ( Int, String )
> numeralTable =
>     [ ( 1000, "M" )
>     , ( 900, "CM" )
>     , ( 500, "D" )
>     , ( 400, "CD" )
>     , ( 100, "C" )
>     , ( 90, "XC" )
>     , ( 50, "L" )
>     , ( 40, "XL" )
>     , ( 10, "X" )
>     , ( 9, "IX" )
>     , ( 5, "V" )
>     , ( 4, "IV" )
>     , ( 1, "I" )
>     ]
>
>
> toRoman : Int -> String
> toRoman number =
>     toRomanUsing numeralTable number
>
>
> toRomanUsing : List ( Int, String ) -> Int -> String
> toRomanUsing table remaining =
>     case table of
>         [] ->
>             ""
>
>         ( value, symbol ) :: smallerEntries ->
>             if remaining >= value then
>                 symbol ++ toRomanUsing table (remaining - value)
>
>             else
>                 toRomanUsing smallerEntries remaining
> ```
>
> **How it works:** If the number is at least as big as the largest remaining value, emit its symbol and subtract; otherwise move to the next entry. The tricky subtractive pairs (`CM`, `IV`, and so on) are simply rows in the table, so the algorithm contains no special cases at all.
>
> **Teaching point:** the table is *data*, and the function is a generic walk over it. That's the declarative flavour of FP again (Section 1): you describe the numerals and let the recursion do the how.

> 🎓 **Facilitator note on testing the Elm code:** The reference algorithm and every expected value in the progression table were checked with an equivalent Python port. The Elm files themselves were written to Elm 0.19 syntax but **were not compiled in the environment used to prepare this document**. Run `elm-test` on the whole kata yourself before delivering. If you find a slip, fix it in the reference solution and the progression table together.

## Section 9 - Show and tell

**Timing:** 15 minutes (about 2 minutes per demo plus 1 minute of feedback, for up to 5 pairs)
**Learning objective:** Present your solution clearly and give and receive constructive feedback.
**KSBs:** S1, B1

> 🛠️ **Activity (15 min, pairs present to the room, S1):** Each pair gets **two minutes** to show: (1) the shape of their solution, (2) one thing that surprised them, and (3) one test they're proud of. Don't present the whole thing, just the interesting bit.
>
> **For presenters:** Say what the code *does* before how it works. Lead with the problem, not the syntax.
> **For the audience:** After each demo, give feedback in this form (30-60 seconds):
>
> - ★ **One thing that worked** ("I liked how you named...")
> - ★ **Another thing that worked**
> - ❓ **One question or wish** ("I wonder what would happen if...")
>
> **Evidence for S1:** Take a quick photo of your screen, jot down the feedback you received, and write two sentences on what you'd change about how you presented.
>
> **Pitfall:** Apologising for your code before showing it ("it's a bit rubbish..."). Skip the disclaimer; show it.
> **If you're in a bigger group:** run a *gallery walk* instead. Pairs rotate between laptops in 3-minute slots. The feedback format stays the same.

> 🎓 **Facilitator note:** Model good feedback on the first demo. Notice which pairs reach for the table-and-recursion solution and which stayed with special cases. Both are valid; ask the second group what they'd do next with another hour.

## Section 10 - Discussion: a dedicated functional language vs FP in Python

**Timing:** 10 minutes
**Learning objective:** Compare enforcing FP in the language with practising it as a discipline, and judge the trade-offs.
**KSBs:** K7, K20, K4

| | FP techniques in Python | A dedicated language such as Elm |
|---|---|---|
| **Purity** | A habit. Nothing stops a slip | Guaranteed by the compiler |
| **Mutation** | `list.append` is always one keystroke away | Doesn't exist |
| **Guard-rails** | Tests, code review, linters | The compiler plus tests |
| **Recursion** | Limited by Python's recursion depth | Tail calls optimised, so deep recursion works |
| **Hiring and team skills** | Everybody already knows Python | A narrower talent pool |
| **Ecosystem** | Enormous | Smaller, more focused |
| **Where it bites** | Bugs like Section 4 can still be written | Learning curve, and fewer places to use it |

> 💬 **Discussion (10 min):**
> 1. Elm refused to compile code that Python would have happily run. Did that feel like help or friction? Did it change over the session?
> 2. If you were starting a brand-new project, what would make you pick a dedicated functional language? What would make you refuse?
> 3. Which Section 4 bug-hunt moment would the Elm compiler have prevented? Which would it not?

## Section 11 - Reflection

**Timing:** 10 minutes (5 individual writing, 5 sharing)
**Learning objective:** Reflect on transferring skills to a new language and on how TDD supported learning.
**KSBs:** S16, B2, S14

> 🛠️ **Activity (5 min writing, 5 min sharing, S16 and B2):** In your learning log, answer the four prompts below. Pick one answer to share with a neighbour.
>
> ```markdown
> ## Reflection - Elm kata
> 1. How easy or hard was it to apply what I knew to a new language? (1-5, and why)
> 2. What from Python or from today's earlier sections transferred straight over?
> 3. How did TDD help me, especially when I was confused by syntax or the compiler?
> 4. One thing I'll try at work in the next two weeks, and one thing I'll read, watch or practise to follow up.
> ```
>
> **Evidence:** the completed log entry.
> **Pitfall:** Writing "it was fine". Be specific: *which moment* was hardest, and what did you do next?

> 💬 **Discussion (5 min, shared with the room):**
> 1. When you were stuck on syntax, what did the tests give you that you wouldn't have had without them?
> 2. Would you have learned Elm faster or slower without TDD?
> 3. What was the first thing you wanted to reach for that Elm didn't have, and what did you do instead?

> 🎓 **Facilitator note:** Common answers: the tests gave "a small next step", "a safety net while refactoring", and "proof I hadn't broken the earlier cases". If the room says TDD was *slower*, agree: for the first twenty minutes it often is. Ask whether it stayed slower once they'd found the table.

**Optional follow-up reading:** The official Elm guide (guide.elm-lang.org) and the Elm and Elixir tracks on Exercism (exercism.org) offer free, test-driven practice. The Bowling Kata reference used in Section 4 is at https://learn.madetech.com/technology/katas/bowling/ (this document summarises the rules, so the link is optional).

**Retro (15-30 minutes)**

## Section 12 - Retrospective

**Timing:** 20 minutes (flex between 15 and 30 depending on how the day has gone)
**Learning objective:** Review the session as a group and agree improvements.
**KSBs:** B1, B2, S16

> 🛠️ **Activity (20 min, whole group):** Run a **Start / Stop / Continue** retro:
>
> | Minutes | What happens |
> |---|---|
> | 3 | Facilitator sets the scene: "We're reviewing the *session*, not each other." |
> | 5 | Silent writing: each person writes sticky notes (physical or digital) for **Start** (we should try this), **Stop** (this didn't help) and **Continue** (keep doing this) |
> | 7 | Group the notes, then talk through the biggest cluster in each column |
> | 5 | Choose **one action** for the next session or for working practice, and give it an owner |
>
> **Evidence for B1 and B2:** a photo of the board and your own sentence: "One thing I'll do differently after this retro is...".

> 💬 **Discussion (within the retro):**
> 1. What's one practice from today that your team would benefit from? What would stop them adopting it?
> 2. What did the group do well together? What would you change about how we worked as a mob or in pairs?

> 🎓 **Facilitator note:** Make "Stop" safe. Thank people for criticism. Whatever feedback you get on *this* walkthrough, write it down, because the best version of the session is the one that's been retro'd a few times.

## KSB mapping

### Evidence table

| # | Activity | Section | KSBs | Evidence the apprentice can capture |
|---|---|---|---|---|
| 1 | Imperative vs declarative edit exercise and spectrum discussion | 1 | K7, S17 | A short note: one imperative and one declarative tool you use at work and why each suits its job |
| 2 | Fibonacci evolution and pure/impure quiz | 2 | K6, K7 | Your `fibonacci.py` with all three versions, and a note of your pure/impure answers |
| 3 | Red-green-refactor warm-up (negative input) | 2 | S14 | Git commits (or saved copies) showing test, fix and refactor in that order |
| 4 | Strengths and weaknesses, test pyramid and mocking discussion | 3 | K14, K4, K20 | A written paragraph: where pure functions need fewer test doubles, and the business value of fast reliable tests |
| 5 | Bowling Kata bug hunt (observe, hypothesise, test, confirm) | 4 | S11, S14, K14 | `bug-hunt-notes.md` with at least two hypotheses and what each test showed |
| 6 | Functional Bowling Kata mob | 5 | S13, B1, S14, K6 | The commit history of the mob, your one-line learning from each rotation, and the nine passing tests |
| 7 | "Try to break it" experiments | 5 | S14, K14 | Screenshot of the tuple error and the shuffled-order run |
| 8 | FP on real projects: pure-function sticky note | 6 | K4, K7, S16 | A named function from your own work, and the refactoring you'd do |
| 9 | Elm setup and primer | 7 | K7, S16, B2 | Screenshot of a working `elm-test` run and notes on what you got stuck on |
| 10 | Roman Numerals pair kata | 8 | S14, S13, B1, K14, K6 | Git history showing red, green, refactor; your reflection on ping-pong pairing |
| 11 | Show and tell | 9 | S1, B1 | Photo of your demo, feedback received, two sentences on what you'd change |
| 12 | Dedicated language vs Python discussion | 10 | K7, K20, K4 | Notes comparing the two approaches and your decision rule for choosing |
| 13 | Reflection | 11 | S16, B2, S14 | The completed learning-log entry |
| 14 | Retrospective | 12 | B1, B2, S16 | Photo of the board and your "one thing I'll do differently" |

> ⚠️ **K6 and K20 need your confirmation.** The brief listed K6 and K20 without describing them, and the wording differs between apprenticeship standard versions. I've attached them where the evidence is most general (K6: programming and design practice, rows 2, 6 and 10; K20: judging the suitability and trade-offs of approaches, rows 4 and 12). Check the codes against your own standard and move them if they don't match.

### Coverage check

| KSB | Covered by (rows) |
|---|---|
| S14 | 3, 5, 6, 7, 10, 13 |
| K14 | 4, 5, 7, 10 |
| K7 / S17 | 1, 2, 8, 9, 12 (K7); 1 (S17) |
| S16 / B2 | 8, 9, 13, 14 |
| S11 | 5 |
| S13 | 6, 10 |
| S1 | 11 |
| B1 | 6, 10, 11, 14 |
| K4 | 4, 8, 12 |
| K6 | 2, 6, 10 |
| K20 | 4, 12 |

> 🎓 **Facilitator note:** S17 (IaC) is only lightly covered, through the Section 1 spectrum. If your apprentices need stronger S17 evidence, add a 10-minute extension to Section 1, for example writing a small Terraform or Kubernetes-style declaration and discussing why "what, not how" suits infrastructure. Be aware that this extension isn't in the timings.

## Quality checklist

| Check | Result |
|---|---|
| Timings add up | Part One: 20 + 35 + 15 + 35 + 35 + 10 = **150 min**. Part Two: 20 + 35 + 15 + 10 + 10 = **90 min**. Total teaching time 240 min, plus a 20-minute retro (flexible 15-30). The 10-minute comfort break sits outside the table |
| Every KSB covered | Yes, see the coverage table. S17 is the thinnest (see note) |
| Seeded bug reproducible | Yes: in the OOP Bowling Kata, `pytest` run in file order gives one pass (gutter game) and four failures, and each test passes alone. Fixed by moving `rolls` into `__init__` |
| FP solution avoids it | Yes: the functional Bowling tests pass, including in 20 shuffled orders, and there is no shared state for the bug to live in |
| Code runs and tests pass | Python code was run and verified, using a small test-runner script because `pytest` could not be installed offline, so **run `python -m pytest -v` once before the day**. Elm code was **not compiled** (no Elm toolchain available), so run `elm-test` once before the day |
| Tone | Light humour and analogies throughout, with honest drawbacks. Please read it aloud once, and cut anything that sounds patronising in your own voice |
