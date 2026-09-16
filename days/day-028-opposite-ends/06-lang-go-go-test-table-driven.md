---
day: 28
track: lang-go
title: "go test, table-driven tests, and t.Run subtests"
theme: "Testing"
phase: "Languages: advanced features"
status: written
---

# Day 028 · Go — go test, table-driven tests, and t.Run subtests

**Today's theme:** Testing

**After today you can:** You can write a test file in each language and make it fail on purpose to see the report.

**The interviewer asks it as:** *How do you test a function with ten input cases?*

## 1. What this is, and why it matters

go test discovers Test functions in _test.go files. Table-driven tests give each input and expected result a named subtest.

You use this when discussing testing in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Leela buys three small jars for the kitchen. Before filling them, she checks whether the lids close. She tries an empty jar, one half full of water, and one filled close to the top. Each check answers a slightly different question. A lid that works only on an empty jar is not good enough.

Her brother offers to help. Instead of saying that the jars look fine, she tells him exactly what to do and what he should see. Turn the jar over above the sink. No water should escape. If it leaks, say which jar and how full it was. A clear failed check is more useful than a cheerful guess.

They use fresh water for each attempt. If they leave a wet lid from one attempt on the next jar, they cannot tell whether new water leaked or old water merely dripped. Starting from a known state makes the result easier to trust.

Leela then loosens one lid deliberately. Water spills, and her brother reports the failure. This matters: a check that always says everything is fine would be useless, even if it looked thorough.

After replacing the bad jar, they repeat the same checks. The descriptions are short enough that either person can perform them. They include ordinary cases and awkward ones, and the result says what failed without requiring someone to remember the entire morning.

## 3. The idea in plain English

Leela’s jar descriptions become rows in a table. A **subtest**, created with t.Run, gives each row an independent name and report. `t.Fatalf` stops that subtest after a failed check, while `t.Errorf` records a failure and continues.

Keep setup local when cases should be independent. Parallel subtests are opt-in and require safe handling of any shared resources. The sum function here is deliberately tiny so you can focus on the testing contract. The same pattern applies to the DSA cases in the shared practice file.

## 4. The picture

```text
known setup -> action -> compare actual with expected -> named result
```

A useful test makes both the starting state and the expected outcome explicit.

## 5. The code, built step by step

First isolate the important operation:

```go
t.Run(test.name, func(t *testing.T) {
    if got := sum(test.left, test.right); got != test.want {
        t.Fatalf("got %d, want %d", got, test.want)
    }
})
```

Use _test.go and TestXxx for discovery.

The complete example follows. Save as `sum_test.go` in a new directory. Run `go mod init example.com/day28` once, then `go test -v`. The test runner supplies main.

```go
package day28

import "testing"

func sum(left, right int) int { return left + right }

func TestSum(t *testing.T) {
    cases := []struct {
        name string
        left, right, want int
    }{
        {"zero", 0, 0, 0},
        {"positive", 2, 3, 5},
        {"cancel", -2, 2, 0},
    }
    for _, test := range cases {
        t.Run(test.name, func(t *testing.T) {
            if got := sum(test.left, test.right); got != test.want {
                t.Fatalf("got %d, want %d", got, test.want)
            }
        })
    }
}
```

**Check the result:** go test -v reports passing zero, positive, and cancel subtests. Replace + with - to see the positive case report `got -1, want 5`.

## 6. How the other two languages do it

**Python**

```python
@pytest.mark.parametrize("name, expected", [("aunt", 0), ("missing", None)])
```

pytest discovers test functions and gives detailed assertion failures. Parameterisation runs one test against several explicit input/output cases.

**C++**

```cpp
TEST_F(SumTest, Positive) {
    EXPECT_EQ(sum(2, 3), 5);
}
```

GoogleTest supplies TEST and TEST_F cases with fatal and nonfatal assertions. CTest can discover and run the built test executable.

pytest parameterisation, Go table tests, and GoogleTest all encode cases and assertions. Fixtures organise setup; they should not hide the expected behaviour.

## 7. The traps

**Near-miss:** log a mismatch with t.Logf; logging alone does not fail the test. The deliberate subtraction defect prints `got -1, want 5` and FAIL when reported with Fatalf. A filename without _test.go does not get the intended test discovery.

## 8. Say it out loud

**How it gets asked:** “How do you test a function with ten input cases?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I place input and expected output together in a case table and use t.Run to identify each case. The comparison reports both actual and expected values. I keep state isolated unless sharing is part of the test and avoid adding parallel execution without a reason. I select boundaries from the function’s contract and verify that a meaningful implementation defect makes the suite fail.

**Follow-ups**

1. **Why use named subtests?** They identify the failing case and can be selected with -run.

2. **Does logging fail a test?** No. Use Errorf or Fatalf for failed expectations.

3. **What changes when tests run in parallel?** Shared state and resource lifetimes need synchronisation or isolation.

**Model answer:** go test discovers Test functions in _test.go files. Table-driven tests give each input and expected result a named subtest. Parallel test execution does not make shared state safe.

## 9. Recall card

- Use _test.go and TestXxx for discovery.
- Give cases readable names.
- Report actual and expected values.
- Parallel test execution does not make shared state safe.

Further reading: [Official reference](https://go.dev/blog/subtests).
