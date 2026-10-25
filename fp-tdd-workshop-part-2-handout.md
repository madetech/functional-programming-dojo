# Introduction to Functional Programming with TDD - Part Two

*Learner handout for apprentice software engineers.*

**Format:** 1.5 hours plus a 20-minute retro. **Language:** Elm. **Prerequisites:** [Part One](fp-tdd-workshop-part-1-handout.md) (the timing overview and Sections 1-6 live there). No Elm knowledge is assumed.

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
