# Introduction to Functional Programming with TDD - Part One

> This is Part One (Python, Sections 1-6). Part Two (Elm, Sections 7-12, plus the KSB mapping) is in [fp-tdd-workshop-part-2-handout.md](fp-tdd-workshop-part-2-handout.md).

*Learner handout for apprentice software engineers.*

**Format:** half-day (4 hours) plus a retro. **Language:** Python for Part One, Elm for Part Two. **Prerequisites:** basic Python, nothing else. No FP, Elm or Elixir knowledge is assumed.

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

> **A note on "KSBs":** *Knowledge, Skills and Behaviours* are the competencies your apprenticeship standard says you must demonstrate. Each section names the ones it supports, and the KSB mapping table at the end of [Part Two](fp-tdd-workshop-part-2-handout.md#ksb-mapping) tells you what evidence to capture. KSB wording varies slightly between standard versions, so check the codes against your own apprenticeship's document.

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

Create a working folder with this layout. You can copy this from the "Part 0 - Project Template" folder. You will add files as you go:

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

def squares_of_evens_imperative(numbers):
    result = []
    for number in numbers:
        if is_even(number):
            result.append(square(number))
    return result

def is_even(number):
    return number % 2 == 0

def square(number):
    return number * number

def squares_of_evens_declarative(numbers):
    return [square(number) for number in numbers if is_even(number)]

def test_both_styles_give_the_same_answer():
    assert squares_of_evens_imperative(numbers) == squares_of_evens_declarative(numbers) == [4, 16, 36]
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
def fibonacci_imperative(position):
    previous = 0
    current = 1
    for _ in range(position):
        next_number = previous + current
        previous = current
        current = next_number
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

**Additional Video Resource**: https://www.youtube.com/watch?v=dDokMfPpfu4 

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

### Subsection 3.3 - Pure functions and the test pyramid

**Why this matters:** how you write code decides how easy it is to test. This subsection explains why pure functions are the easiest code of all to test, and how teams use that to build test suites that are fast and that they actually trust.

**The test pyramid**

There are three common kinds of automated test. The **test pyramid** is a rule of thumb for how many of each to write.

```text
        /\          Few    End-to-end
       /  \
      /----\        Some   Integration
     /      \
    /--------\      Many   Unit
```

| Kind | What it checks | Speed | Typical problems |
|---|---|---|---|
| **Unit** | One small piece, usually one function, on its own | Milliseconds | Very few. When one fails, it points straight at the function that broke |
| **Integration** | Several parts working together, for example your code and a real database | Seconds | Needs setup: a database running, test data loaded |
| **End-to-end** | The whole system, used the way a real user would, from the screen through to the database and back | Seconds to minutes each | **Brittle**: they fail for reasons that aren't bugs, such as a slow network, a button that moved, or test data someone changed |

Why that shape? Lots of cheap, fast tests at the bottom catch most mistakes within seconds. A few expensive tests at the top check that the pieces join up. Turn the pyramid upside down (mostly end-to-end tests) and you get slow feedback and tests that fail randomly, until the team learns to ignore them with "it's probably just flaky".

Analogy: building a car. You test each part on the bench (unit), check the engine fits the gearbox (integration), then take the finished car for a test drive (end-to-end). You wouldn't hunt for a faulty spark plug by driving round the block a hundred times.

**What are test doubles?**

A unit test is meant to check one piece *on its own*. But a lot of real code can't run on its own: it reads from a database, sends an email, checks the time, or calls another company's API. Using the real thing in a unit test causes trouble. It's slow, it may not be available on your laptop, it might send real emails to real customers, and some answers (like the time) change every time you ask.

So we swap in a stand-in, called a **test double** after the stunt doubles in films. A stunt double looks enough like the actor for the scene, but it isn't the real person. There are a few kinds:

- **Stub:** gives a fixed answer. "Whenever anyone asks the time, it's 9am."
- **Fake:** a simple working version of the real thing, for example a plain Python list pretending to be a database.
- **Mock:** records how it was used, so the test can check things like "was `send_email` called exactly once, with this address?"

You don't need to memorise these. Many people just say "mock" for all of them.

Doubles are useful, but they cost something:

- **Setup.** Every test needs extra lines to build the double and plug it in, often more lines than the code being tested.
- **Tests tied to the inside of the code.** A mock that checks "was the database called like *this*?" breaks when you change *how* the code talks to the database, even though the result is still correct.
- **The double can be wrong.** If the fake behaves differently from the real thing, your tests pass and production fails.

**Why pure functions need few or no doubles**

A function needs a double when it reaches *out* to get something (the clock, a database) or *does* something to the outside world (sends an email, saves a file). These are the side effects from Section 2.3.

A pure function does neither. Everything it needs arrives as arguments, and everything it produces comes back as the return value. To test it, you pass in real values and check what comes out. There's nothing to fake.

An example in words: a function decides whether to say "Good morning" or "Good afternoon".

- If the function **checks the clock itself**, testing the morning case means faking the clock so it says 9am. That needs a double.
- If the **hour is passed in as an argument**, you just call it with 9 and check the answer. The rule is the same, but there's no double, because getting the hour has moved *outside* the function.

That is why FP pushes you towards a wide base of the pyramid: the more of your logic lives in pure functions, the more of it you can test with fast, simple unit tests.

**The common design: functional core, imperative shell**

You can't make a whole program pure. At some point it has to read input, save data or show something on screen, and that's what makes it useful. The trick is to push those side effects to the edges.

**Functional core, imperative shell** splits the code into two layers:

- **The core** is pure functions that make the decisions and hold the rules: working out a price, scoring a game, checking a form is valid. It never touches the database, the network or the clock. You test it heavily with unit tests.
- **The shell** is a thin outer layer that talks to the world. It fetches the data, hands it to the core, takes the answer and saves or displays it. It contains as little logic as possible, so a handful of integration tests is enough.

```text
outside world  ->  shell: fetch  ->  core: decide  ->  shell: save or show  ->  outside world
                   (impure)          (pure)            (impure)
```

Analogy: a restaurant. The kitchen (core) turns ingredients into dishes by following recipes. Front of house (shell) takes orders, passes them to the kitchen, carries the plates out and takes payment. You can check a recipe in the kitchen without a single customer, and front-of-house checks are about whether orders get through, not whether the food tastes right.

You've already seen a core with no shell: every Fibonacci function in Section 2. You'll build another in Section 5, and Section 6 shows a small core-and-shell example with a discount rule.

**What you gain**

| Benefit | Why |
|---|---|
| **Fast tests** | Pure-function tests run in milliseconds, so thousands run in seconds and you can run them after every change |
| **Less setup** | No doubles to build, so each test is a few lines long and easy to read |
| **Tests that survive refactoring** | They check *answers*, not *how* the code talks to other systems, so you can restructure the inside freely |
| **Failures that point at the cause** | A failing unit test names the function and the inputs that broke it |
| **Rules that are easy to change** | The rules the business changes most often live in one place, away from database and network code |
| **Fewer integration tests** | The shell is thin, so there's less of it to test the slow way |

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
