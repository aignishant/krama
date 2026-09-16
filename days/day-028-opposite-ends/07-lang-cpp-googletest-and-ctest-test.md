---
day: 28
track: lang-cpp
title: "GoogleTest and CTest: TEST, EXPECT_EQ, and fixtures"
theme: "Testing"
phase: "Languages: advanced features"
status: written
---

# Day 028 · C++ — GoogleTest and CTest: TEST, EXPECT_EQ, and fixtures

**Today's theme:** Testing

**After today you can:** You can write a test file in each language and make it fail on purpose to see the report.

**The interviewer asks it as:** *How do you test a function with ten input cases?*

## 1. What this is, and why it matters

GoogleTest supplies TEST and TEST_F cases with fatal and nonfatal assertions. CTest can discover and run the built test executable.

You use this when discussing testing in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Leela buys three small jars for the kitchen. Before filling them, she checks whether the lids close. She tries an empty jar, one half full of water, and one filled close to the top. Each check answers a slightly different question. A lid that works only on an empty jar is not good enough.

Her brother offers to help. Instead of saying that the jars look fine, she tells him exactly what to do and what he should see. Turn the jar over above the sink. No water should escape. If it leaks, say which jar and how full it was. A clear failed check is more useful than a cheerful guess.

They use fresh water for each attempt. If they leave a wet lid from one attempt on the next jar, they cannot tell whether new water leaked or old water merely dripped. Starting from a known state makes the result easier to trust.

Leela then loosens one lid deliberately. Water spills, and her brother reports the failure. This matters: a check that always says everything is fine would be useless, even if it looked thorough.

After replacing the bad jar, they repeat the same checks. The descriptions are short enough that either person can perform them. They include ordinary cases and awkward ones, and the result says what failed without requiring someone to remember the entire morning.

## 3. The idea in plain English

Leela’s known setup becomes a test **fixture**, a class derived from testing::Test. Each TEST_F gets a fresh fixture instance. EXPECT_EQ records a failure but continues; ASSERT_EQ stops the current test function when later checks would be unsafe.

GoogleTest is an external dependency, not part of the C++ standard library. CMake builds the executable and links gtest_main, which supplies main. GoogleTest discovery registers individual tests with CTest. Pin the dependency in a real project so different machines do not silently test against different versions.

## 4. The picture

```text
known setup -> action -> compare actual with expected -> named result
```

A useful test makes both the starting state and the expected outcome explicit.

## 5. The code, built step by step

First isolate the important operation:

```cpp
TEST_F(SumTest, Positive) {
    EXPECT_EQ(sum(2, 3), 5);
}
```

Use fatal assertions for prerequisites.

The complete example follows. This needs GoogleTest and CMake installed, with GTest discoverable by CMake. Save the C++ block as `sum_test.cpp`. The CMake file and build commands appear below the example.

```cpp
#include <gtest/gtest.h>

int sum(int left, int right) { return left + right; }

class SumTest : public ::testing::Test {
protected:
    int zero = 0;
};
TEST_F(SumTest, Zero) {
    EXPECT_EQ(sum(zero, zero), 0);
}
TEST_F(SumTest, Positive) {
    EXPECT_EQ(sum(2, 3), 5);
}
TEST_F(SumTest, Cancel) {
    EXPECT_EQ(sum(-2, 2), 0);
}
```

**Check the result:** Three tests pass. Save this second file as `CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.20)
project(day28 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
find_package(GTest CONFIG REQUIRED)
enable_testing()
add_executable(sum_test sum_test.cpp)
target_link_libraries(sum_test PRIVATE GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(sum_test)
```

Run `cmake -S . -B build`, `cmake --build build --config Debug`, then `ctest --test-dir build -C Debug --output-on-failure`. If GTest is not found, install it and point `CMAKE_PREFIX_PATH` at its installation. Changing + to - makes the positive test compare -1 with 5.

## 6. How the other two languages do it

**Python**

```python
@pytest.mark.parametrize("name, expected", [("aunt", 0), ("missing", None)])
```

pytest discovers test functions and gives detailed assertion failures. Parameterisation runs one test against several explicit input/output cases.

**Go**

```go
t.Run(test.name, func(t *testing.T) {
    if got := sum(test.left, test.right); got != test.want {
        t.Fatalf("got %d, want %d", got, test.want)
    }
})
```

go test discovers Test functions in _test.go files. Table-driven tests give each input and expected result a named subtest.

pytest parameterisation, Go table tests, and GoogleTest all encode cases and assertions. Fixtures organise setup; they should not hide the expected behaviour.

## 7. The traps

**Near-miss:** use EXPECT_NE(pointer, nullptr) and then dereference a null pointer anyway. Use ASSERT_NE when continuing would be invalid. A deliberate wrong sum produces a GoogleTest report headed `Expected equality of these values:` with actual -1 and expected 5. Compiler and framework formatting vary.

## 8. Say it out loud

**How it gets asked:** “How do you test a function with ten input cases?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I separate test construction from execution. GoogleTest gives me named cases, assertions, and fixtures; CMake builds the executable; CTest runs the registered cases. I use fatal assertions when the rest of a test requires a condition to hold. Expected values come from the contract, and I test a representative defect to confirm the report names the broken behaviour. Dependency setup is part of making the example reproducible.

**Follow-ups**

1. **Why keep expected values independent?** An expected result computed by the same buggy code is not a useful oracle.

2. **When use ASSERT instead of EXPECT?** When a failed prerequisite makes the remaining test unsafe or meaningless.

3. **Is GoogleTest in the standard library?** No. It must be installed or supplied as an explicit project dependency.

**Model answer:** GoogleTest supplies TEST and TEST_F cases with fatal and nonfatal assertions. CTest can discover and run the built test executable. A test should fail for the behaviour it claims to protect.

## 9. Recall card

- Use fatal assertions for prerequisites.
- TEST_F gets a fixture instance per test.
- CTest runs registered tests.
- A test should fail for the behaviour it claims to protect.

Further reading: [Official reference](https://google.github.io/googletest/primer.html).
