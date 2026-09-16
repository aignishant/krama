---
day: 28
track: lang-python
title: "pytest: fixtures, parametrize, and assert introspection"
theme: "Testing"
phase: "Languages: advanced features"
status: written
---

# Day 028 · Python — pytest: fixtures, parametrize, and assert introspection

**Today's theme:** Testing

**After today you can:** You can write a test file in each language and make it fail on purpose to see the report.

**The interviewer asks it as:** *How do you test a function with ten input cases?*

## 1. What this is, and why it matters

pytest discovers test functions and gives detailed assertion failures. Parameterisation runs one test against several explicit input/output cases.

You use this when discussing testing in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Leela buys three small jars for the kitchen. Before filling them, she checks whether the lids close. She tries an empty jar, one half full of water, and one filled close to the top. Each check answers a slightly different question. A lid that works only on an empty jar is not good enough.

Her brother offers to help. Instead of saying that the jars look fine, she tells him exactly what to do and what he should see. Turn the jar over above the sink. No water should escape. If it leaks, say which jar and how full it was. A clear failed check is more useful than a cheerful guess.

They use fresh water for each attempt. If they leave a wet lid from one attempt on the next jar, they cannot tell whether new water leaked or old water merely dripped. Starting from a known state makes the result easier to trust.

Leela then loosens one lid deliberately. Water spills, and her brother reports the failure. This matters: a check that always says everything is fine would be useless, even if it looked thorough.

After replacing the bad jar, they repeat the same checks. The descriptions are short enough that either person can perform them. They include ordinary cases and awkward ones, and the result says what failed without requiring someone to remember the entire morning.

## 3. The idea in plain English

Leela’s fresh water is a **fixture**, a function that supplies test setup. pytest requests it by parameter name. The fixture below returns a new dictionary for each test invocation, so mutation in one case does not leak into another.

`parametrize` lists cases independently of the assertion. The expected value is a literal, not another call to the implementation. Assertion introspection reports the compared values when a check fails. Include an absent key and a present zero because day 23 showed they exercise different branches.

## 4. The picture

```text
known setup -> action -> compare actual with expected -> named result
```

A useful test makes both the starting state and the expected outcome explicit.

## 5. The code, built step by step

First isolate the important operation:

```python
@pytest.mark.parametrize("name, expected", [("aunt", 0), ("missing", None)])
```

Make each expected value independent of the implementation.

The complete example follows. Save as `test_counts.py`. Install pytest in your environment with `python -m pip install pytest`, then run `python -m pytest -q test_counts.py`.

```python
import pytest

def lookup(counts: dict[str, int], name: str) -> int | None:
    return counts.get(name)

@pytest.fixture
def counts() -> dict[str, int]:
    return {"aunt": 0, "cousin": 2}

@pytest.mark.parametrize("name, expected", [
    ("aunt", 0), ("cousin", 2), ("missing", None)
])
def test_lookup(counts: dict[str, int], name: str, expected: int | None) -> None:
    assert lookup(counts, name) == expected
```

**Check the result:** pytest reports `3 passed` with a machine-dependent duration. Change get(name) to get(name) or 1 and verify failures before restoring it.

## 6. How the other two languages do it

**Go**

```go
t.Run(test.name, func(t *testing.T) {
    if got := sum(test.left, test.right); got != test.want {
        t.Fatalf("got %d, want %d", got, test.want)
    }
})
```

go test discovers Test functions in _test.go files. Table-driven tests give each input and expected result a named subtest.

**C++**

```cpp
TEST_F(SumTest, Positive) {
    EXPECT_EQ(sum(2, 3), 5);
}
```

GoogleTest supplies TEST and TEST_F cases with fatal and nonfatal assertions. CTest can discover and run the built test executable.

pytest parameterisation, Go table tests, and GoogleTest all encode cases and assertions. Fixtures organise setup; they should not hide the expected behaviour.

## 7. The traps

**Near-miss:** compute expected by calling lookup again; both sides can share the same bug. With the suggested broken implementation, the zero case includes `assert 1 == 0` in the failure report. A module-scoped mutable fixture would also share state between tests unless reset deliberately.

## 8. Say it out loud

**How it gets asked:** “How do you test a function with ten input cases?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I derive cases from the contract, including boundaries and failure paths, and name their expected results explicitly. Parameterisation avoids repeating the test body. Fixtures provide controlled setup with a deliberate lifetime. I introduce a representative defect once to check that the assertions catch it, then restore the implementation. Tests are evidence for selected behaviours; three passing examples are not a proof for every possible input.

**Follow-ups**

1. **Why keep expected values independent?** Reusing the same implementation to compute the oracle can reproduce the bug.

2. **What does a fixture control?** Setup, cleanup when needed, and how long shared resources live.

3. **Must each case use a separate test function?** No. Parameterisation gives each case a separate result from one body.

**Model answer:** pytest discovers test functions and gives detailed assertion failures. Parameterisation runs one test against several explicit input/output cases. A deliberate defect checks whether the test can actually fail.

## 9. Recall card

- Make each expected value independent of the implementation.
- Fixtures provide known starting state.
- Parameterisation names multiple cases.
- A deliberate defect checks whether the test can actually fail.

Further reading: [Official reference](https://docs.pytest.org/en/stable/how-to/fixtures.html).
