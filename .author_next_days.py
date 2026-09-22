from pathlib import Path
import contextlib
import io
import platform
import textwrap

# Each teaching block is executed while its transcript is authored.

ROOT = Path(__file__).resolve().parent
def folder(day, track):
    return next(next((ROOT / 'days').glob(f'day-{day:03d}-*')).glob(f'{track}_*'))

def write(path, value):
    path.write_text(textwrap.dedent(value).strip() + '\n', encoding='utf-8')

def chapter(day, track, title, prereq, answer, story, idea, mechanism, code, explanation, production, questions, source):
    code = textwrap.dedent(code).strip()
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(code, f'day-{day}-{track}-teaching', 'exec'), {})
    observed = output.getvalue().rstrip()
    number, outcome = {'dsa': ('1.1', 'DSA'), 'sd': ('2.1', 'SD'), 'lang': ('3.1', 'PY')}[track]
    cold = ('Start with the cold assignment in [README.md](README.md). Open this repair lesson only\n'
            'after the attempt, or record the explanation as help.\n\n') if day == 21 else ''
    result = f'''---
day: {day}
part: "{number}"
title: "{title}"
ids: [{outcome}-{day}]
level: working
prerequisites: ["{prereq}"]
failure: true
---

# {title}

{cold}Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

{answer}

## The story

{story}

## The idea in plain language

{idea}

## Why Krama needs it

This develops {outcome}-{day} in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

{source}
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

{mechanism}

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
{code}
```

**Line by line:** {explanation}

Author verification on Python {platform.python_version()}, 2026-09-22 (teaching evidence, not learner progress):

```text
{observed}
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

{production}

## Check yourself

### Readiness before practice

{questions}

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
'''
    write(folder(day, track) / 'CONCEPTS.md', result)
    print(f'Authored and executed Day {day} {track}')

chapter(21, 'dsa', 'Recover the proof before the pattern', 'Days 15–20 two pointers and windows',
'Choose a pointer move by the candidates it safely eliminates, and state the input assumption that permits it.',
'A memorized two-pointer template can pass one example and fail as soon as negatives or repeated characters appear. Review tests whether you can recover the reason for each move from a blank page.',
'''A cold attempt uses no lesson, hint, or prior implementation. Afterward, repair the first
missing reasoning step. An invariant is a statement preserved by every update; a counterexample
is one valid input that disproves a claim. For sorted pairs, endpoint ordering rules out a
whole set of partners. For distinct substrings, the retained window contains no repeated code
point. For a positive threshold window, positivity justifies stopping after the sum falls short.
These are different proofs even though all use moving indices.''',
'''Keep the scheduled 5 minutes recall + two 20-minute attempts + 10 critique + 5 logging.
Re-solve Day 15 and Day 19 from blank code; an unresolved hard problem may replace the second.
The local Day 21 fixture checks only Day 19's substring contract. Day 15's local result is a
boolean, while its online companion returns one-based indices. Use the original Day 15
fixtures for that re-solve. Score correctness/explanation/complexity/tests 0–2 each; pass at
6/8 with correctness=2 and at least one hint-free solve. Reading this repair is help.

| Repair topic | Mechanism to reconstruct | Original lesson |
| --- | --- | --- |
| Sorted pairs | Too small eliminates left; too large eliminates right | [Day 15](../../day-015-sorted-pair-existence/dsa_sorted-pair-existence/CONCEPTS.md) |
| Unique triples | Fix one value, search suffix, skip duplicate answers | [Day 16](../../day-016-unique-triples/dsa_unique-triples/CONCEPTS.md) |
| Container capacity | A shorter endpoint limits all narrower pairs retaining it | [Day 17](../../day-017-container-capacity/dsa_container-capacity/CONCEPTS.md) |
| Fixed window | Subtract departure, add arrival | [Day 18](../../day-018-fixed-window-maximum-sum/dsa_fixed-window-maximum-sum/CONCEPTS.md) |
| Distinct substring | Repair repetition without moving left backward | [Day 19](../../day-019-longest-distinct-substring/dsa_longest-distinct-substring/CONCEPTS.md) |
| Positive threshold | Record and shrink repeatedly while qualifying | [Day 20](../../day-020-minimum-positive-window/dsa_minimum-positive-window/CONCEPTS.md) |

Repair trace for `abba`: after a, left=0 and best=1; after b, best=2. The second b moves
left to 2. The final a was last seen at 0, outside the active window. Left stays 2, and the
best remains 2. Assigning left=previous+1 without a maximum moves it backward to 1 and
incorrectly counts `bba`. The active-set approach uses expected O(n) time, O(k) storage for
the largest active window; a last-seen map instead stores up to O(u) distinct code points.
Sorted pair elimination uses O(n) time and O(1) auxiliary space. Nested rescanning can
erase these bounds; justify total pointer moves, not merely the number of loops.''',
'''
def distinct_length(text, guard):
    last = {}
    left = best = 0
    for right, char in enumerate(text):
        if char in last:
            candidate = last[char] + 1
            left = max(left, candidate) if guard else candidate
        last[char] = right
        best = max(best, right - left + 1)
    return best

wrong = distinct_length('abba', False)
fixed = distinct_length('abba', True)
print('backward boundary:', wrong, 'monotone boundary:', fixed)
assert wrong == 3 and fixed == 2
assert distinct_length('', True) == 0
''',
'The map records historical positions. The guard controls whether old history can undo a later boundary. Both versions run on the same counterexample; the assertions distinguish them and include empty input.',
'''Use the smallest failing input to repair one claim, then rerun independent boundaries.
Do not call a code-point result a grapheme-cluster count. Record actual help and remaining
uncertainty; memorizing the demonstrated function is not a cold re-solve.''',
'''1. Why does moving left backward invalidate the substring invariant?
2. What sorted-pair candidates are discarded when the endpoint sum is too small?
3. Why do negative values invalidate the positive-window stopping rule?
4. Which contract and fixtures belong to each of the two review attempts?''',
'Use the six original lessons linked below for their verified sources; this review introduces no new algorithm contract.')

chapter(22, 'dsa', 'Find the first true boundary', 'Sorted arrays; integer indices and half-open ranges',
'Lower bound finds the first index whose value is at least the target, keeping known-false and known-true regions outside the search interval.',
'A sorted price list contains repeated prices. Finding any matching price is insufficient when a new entry must be inserted before all equal prices.',
'''A nondecreasing array turns `nums[i] >= target` into a false-then-true predicate.
Recognize a first qualifying position, including an insertion point when the target is absent.
Use the half-open element interval [lo, hi): lo starts at 0, hi at n. Indices before lo are
known too small; existing indices at or after hi are known large enough. The answer is a
boundary in [lo, hi], including n. That boundary is not necessarily a readable array index.
Duplicates are permitted locally. Do not sort inside the function: sorted input is the premise.''',
'''For values [2, 4, 4, 9, 12] and target 4:

| lo | hi | mid | Observation | Update |
| --- | --- | --- | --- | --- |
| 0 | 5 | 2 | 4 qualifies; an earlier value may qualify | hi=2 |
| 0 | 2 | 1 | 4 qualifies | hi=1 |
| 0 | 1 | 0 | 2 is too small | lo=1 |

At lo=hi=1 the partition is complete. If mid is too small, sorted order proves that every
index through mid is too small, so lo=mid+1. Otherwise mid may be the answer, so hi=mid.
The uncertain interval shrinks on both branches. Equality must follow the qualifying branch;
returning the first equality encountered gives an arbitrary duplicate.

For target 13 the answer is 5, one past the end. Empty input yields 0 without reading an
element. A linear first-match scan is an O(n) baseline. Halving an indexable interval takes
O(log n) comparisons (O(1) for empty input), O(1) auxiliary storage, and one integer output.
Do not slice the list at each step or assume linked-list midpoint access is constant time.''',
'''
from bisect import bisect_left

def boundary(values, target, wrong_equality=False):
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target or (wrong_equality and values[mid] == target):
            lo = mid + 1
        else:
            hi = mid
    return lo

values = [2, 4, 4, 9, 12]
print('discarding equals:', boundary(values, 4, True), 'lower bound:', boundary(values, 4))
assert boundary(values, 4, True) == 3
for data in ([], [4], [4, 4], values):
    for target in (0, 4, 13):
        assert boundary(data, target) == bisect_left(data, target)
print('boundary checks passed')
''',
'The optional wrong branch discards equality and actually finds an upper bound. The standard-library oracle checks empty, duplicate, and outside-range cases; it is teaching verification, not a replacement for your own exercise.',
'''Distinguish finding a position from inserting: inserting into a Python list can shift O(n)
items even when search is logarithmic. A changed sort key or concurrent mutation can invalidate
the partition. The online companion uses distinct values and a judge method; the local JSON
adapter also admits duplicates and empty input. Both ask for a zero-based insertion boundary.''',
'''1. What is known about indices before lo and at or after hi?
2. Why does equality set hi=mid instead of returning immediately?
3. Why can n be a correct answer but never a valid element access?
4. What makes lo=mid unsafe when hi=lo+1?''',
'[Python bisect partition semantics](https://docs.python.org/3.12/library/bisect.html) and [LeetCode 35](https://leetcode.com/problems/search-insert-position/) support the boundary and companion contracts.')

chapter(23, 'dsa', 'Find a run with two boundaries', 'Day 22 lower-bound invariant',
'Find the first value >= target and the first value > target; the equal run lies between those boundaries.',
'A log groups equal timestamps together. One equality match says nothing about how many adjacent records share that timestamp.',
'''Start with [Day 22](../../day-022-lower-bound/dsa_lower-bound/CONCEPTS.md).
Lower bound L is the first index with value >= target; upper bound U is the first with value
> target. Sorted order makes all target occurrences contiguous. Their half-open range is
[L,U), length U-L. The requested output instead uses inclusive endpoints, [L,U-1], and
[-1,-1] when absent. A boundary alone does not certify that the target exists.''',
'''For [1, 3, 3, 3, 8, 10] and target 3, both searches start with lo=0 and hi=6:

| Search | mid and decision sequence | Final boundary |
| --- | --- | --- |
| First >=3 | 3 qualifies → hi=3; 1 qualifies → hi=1; 0 too small → lo=1 | L=1 |
| First >3 | 3 equal → lo=4; 5 greater → hi=5; 4 greater → hi=4 | U=4 |

Thus the result is [1,3] and there are three matches. For target 4, both boundaries equal
4, but nums[4] is 8: return [-1,-1]. Before reading nums[L], check L<n. An equivalent
absence test is L==U when both correct boundary searches have already run.

Lower search preserves the Day 22 partition. Upper search treats equality as too far left,
so its false region contains all values <= target. Combining the partitions proves that
exactly the positions from L through U-1 equal target. Both intervals shrink independently.
Two O(log n) searches still take O(log n) time and O(1) auxiliary/output space. Finding one
match and walking outward costs O(n) on an all-equal array. A full scan is a useful baseline
but cannot justify the requested logarithmic worst-case bound.''',
'''
from bisect import bisect_left, bisect_right

def endpoints(values, target):
    left = bisect_left(values, target)
    if left == len(values) or values[left] != target:
        return [-1, -1]
    return [left, bisect_right(values, target) - 1]

values = [1, 3, 3, 3, 8, 10]
wrong = [bisect_left(values, 4), bisect_right(values, 4) - 1]
print('unchecked absence:', wrong, 'checked:', endpoints(values, 4))
assert wrong == [4, 3]
assert endpoints(values, 3) == [1, 3]
assert endpoints([], 3) == [-1, -1]
assert endpoints([3, 3, 3], 3) == [0, 2]
print('inclusive endpoints:', endpoints(values, 3))
''',
'The library functions expose the two boundaries without filling your exercise. Subtracting one before checking absence creates an inverted range. The repaired adapter distinguishes absent, empty, and all-equal inputs.',
'''Keep boundary semantics explicit in APIs: [L,U) composes cleanly with slicing, but this
exercise requests an inclusive last index. Prefer a direct > predicate to searching for
target+1; the latter assumes a discrete successor and can overflow in fixed-width languages.
Optional depth: count occurrences with U-L without materializing the matching slice.''',
'''1. Why are equal values one contiguous run?
2. Which inequality changes between the two searches?
3. What does L=U mean, and why is [L,U-1] then the wrong public result?
4. Why does expansion from one match lose the logarithmic guarantee?''',
'[Python bisect](https://docs.python.org/3.12/library/bisect.html) defines both partitions; [LeetCode 34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) supplies the companion output contract.')

chapter(24, 'dsa', 'Search the sorted half of a rotation', 'Day 22 shrinking search intervals; strict sorted order',
'After checking the midpoint, identify a sorted half and keep it only if its value range contains the target.',
'A sorted inventory was rotated when its circular buffer wrapped. Ordinary binary search discards the wrong half because the whole visible list is no longer sorted.',
'''A rotation of a strictly increasing array has at most one descending seam. Therefore at
least one half adjacent to the midpoint is sorted. Use an inclusive candidate interval
[lo,hi], unlike Day 22's half-open boundary search. The invariant is that an existing target
remains inside this interval. Empty input sets hi=-1 and returns -1; no rotation is also valid.
Distinctness is essential to identifying the sorted half from endpoint comparisons.''',
'''Search [8, 10, 12, 1, 3, 5, 6] for 10:

| lo | hi | mid/value | Sorted half and target test | Next interval |
| --- | --- | --- | --- | --- |
| 0 | 6 | 3 / 1 | Right [1..6] sorted; 10 outside (1,6] | [0,2] |
| 0 | 2 | 1 / 10 | Midpoint equals target | return 1 |

Always test equality first. If nums[lo]<=nums[mid], the left half is sorted. Keep it when
nums[lo]<=target<nums[mid] by setting hi=mid-1; otherwise set lo=mid+1. If the left half
is not sorted, the right half is sorted. Keep it when nums[mid]<target<=nums[hi] by setting
lo=mid+1; otherwise set hi=mid-1. The strict midpoint comparisons exclude a value already
checked; the non-strict outer comparisons preserve a target at an endpoint.

Inside a sorted half, an outside-range target cannot occur. When the target is inside that
range, distinct rotation order puts the other half outside it. This justifies either discard.
Every unsuccessful iteration excludes the midpoint and roughly half the remaining indices,
giving O(log n) time and O(1) auxiliary space. A linear index scan is the O(n) oracle.''',
'''
def locate(values, target, rotation_aware):
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if values[mid] == target:
            return mid
        if not rotation_aware:
            keep_left = target < values[mid]
        elif values[lo] <= values[mid]:
            keep_left = values[lo] <= target < values[mid]
        else:
            keep_left = not (values[mid] < target <= values[hi])
        if keep_left:
            hi = mid - 1
        else:
            lo = mid + 1
    return -1

values = [8, 10, 12, 1, 3, 5, 6]
print('ordinary search:', locate(values, 10, False), 'rotation-aware:', locate(values, 10, True))
assert locate(values, 10, False) == -1
for size in range(8):
    base = list(range(0, size * 2, 2))
    for pivot in range(max(1, size)):
        rotated = base[pivot:] + base[:pivot]
        for target in range(-1, size * 2 + 1):
            expected = rotated.index(target) if target in rotated else -1
            assert locate(rotated, target, True) == expected
print('all tiny rotations checked')
''',
'The ordinary branch mistakes the midpoint for a global ordering boundary. The corrected branch determines a sorted half. Exhaustive tiny rotations compare every result with linear search, including absence and empty input.',
'''Do not sort the input to repair it: sorting loses original indices and costs O(n log n).
Optional changed contract: duplicates can make both endpoints and mid equal while hiding a
seam, as in [1,0,1,1,1]. Resolving that ambiguity may require linear work. Today's logarithmic
proof covers distinct values only. Compare endpoint targets, absent targets, singletons,
unrotated input, and seams on either side of mid.''',
'''1. Why is at least one half sorted?
2. Why must midpoint equality be checked before selecting a half?
3. Which interval convention changed from Day 22, and what is the loop condition now?
4. Why does [1,0,1,1,1] defeat the distinct-value inference?''',
'[LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/) specifies rotated distinct values and a logarithmic search target. The elimination proof above is derived from that input contract.')

chapter(21, 'lang', 'Review who advances and who closes', 'Days 15–20 iteration and generators',
'Trace cursor ownership, advancement, suspension, and cleanup before deciding that an iterable can be reused.',
'A validation pass succeeds, then the export writes nothing. Both functions received the same exhausted iterator; no data disappeared from storage.',
'''Begin cold: choose one surprise from your own Days 15–20 notes, predict its output, reproduce
it from memory, and add a regression assertion for the repair. Use 3 minutes prediction,
8 experiment, 4 explanation/testing. Afterward, this repair lesson connects the models.
An iterable supplies an iterator; the iterator carries traversal state. A generator is an
iterator with suspended execution. Exhaustion, explicit closure, and normal return are
distinct events. A wrapper must preserve the parts of this contract its consumer relies on.''',
'''Repair navigation: [iterator protocol](../../day-015-sorted-pair-existence/lang_iterator-protocol/CONCEPTS.md),
[laziness](../../day-016-unique-triples/lang_generator-laziness/CONCEPTS.md),
[cleanup](../../day-017-container-capacity/lang_generator-cleanup/CONCEPTS.md),
[delegation](../../day-018-fixed-window-maximum-sum/lang_yield-delegation/CONCEPTS.md),
[consumption](../../day-019-longest-distinct-substring/lang_iterator-consumption/CONCEPTS.md), and
[pipelines](../../day-020-minimum-positive-window/lang_streaming-pipeline/CONCEPTS.md).

Trace one cursor over [2,4,6]: creation consumes nothing; asking whether 4 is present reads
2 and 4; converting the remainder to a list yields [6]; a second conversion yields [].
Membership did work even though its public result was only True. To support two complete
passes over a finite source, snapshot before either consumer. That costs O(n) time and
space up front. A fresh source factory can avoid retaining all items if reopening is cheap
and the source remains consistent. A one-pass pipeline can instead change the contract.

The repair is correct because each traversal of the stored sequence gets a fresh cursor;
it is not correct because iter was called twice on the same iterator. Large or infinite
sources rule out unconditional materialization. Cleanup ownership still needs a separate
decision: exhaustion during normal use does not guarantee early-stop cleanup.''',
'''
cursor = iter([2, 4, 6])
found = 4 in cursor
remaining = list(cursor)
print('membership:', found, 'remaining:', remaining, 'again:', list(cursor))
assert remaining == [6]
snapshot = tuple(iter([2, 4, 6]))
assert 4 in snapshot
assert list(snapshot) == [2, 4, 6]
assert list(snapshot) == [2, 4, 6]
print('replay:', list(snapshot))
''',
'The first consumer advances the shared cursor. The snapshot is created from a fresh source before any read, so membership and later traversal do not share a traversal position. Repeated assertions verify replay.',
'''Name who owns resource closure when a consumer stops early. A lazy pipeline may still
retain unbounded data if a stage caches or sorts everything. Keep the regression small and
predictable; evidence should explain a language mechanism, not merely paste the output.''',
'''1. Which operations in the trace advance the cursor?
2. Why does iter(cursor) fail to provide a fresh traversal?
3. When is snapshotting a bad repair?
4. What evidence would distinguish early closure from normal exhaustion?''',
'[Python 3.12 iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types) supports the cursor model; use the original six lessons for their generator-specific references.')

chapter(22, 'lang', 'Design useful object representations', 'Objects; special methods; public versus secret fields',
'Use repr for diagnostic identity and str for a readable label, with an explicit allowlist of safe fields.',
'A connection object reaches an exception message. A convenient dump of its entire attribute dictionary also exposes the credential it stores.',
'''The representation protocol lets tools ask an object for diagnostic or readable text.
`repr(obj)` calls its type's __repr__; `str(obj)` calls __str__ and falls back to __repr__
when no __str__ is supplied. Both methods must return strings. Container displays such as
lists use element repr, so a safe __str__ alone does not protect diagnostic output.
Treat field selection as part of the class contract. A representation can be useful without
being executable constructor syntax; secrets should not be included just to make it reconstructible.''',
'''Consider an endpoint with public host `api.example` and synthetic token `demo-secret`.

| Expression | Intended result | Audience |
| --- | --- | --- |
| str(endpoint) | endpoint at api.example | Human-facing label |
| repr(endpoint) | Endpoint(host='api.example', token=<redacted>) | Debugging |
| repr([endpoint]) | List containing the diagnostic representation | Debugging containers |

Select host explicitly, quote it with !r in repr so escapes are visible, and substitute a
constant redaction marker for token. This preserves diagnostic object type and destination
without retaining the secret in these output strings. Dumping __dict__ is an open-ended
policy: a new secret field would silently become visible. An allowlist stays closed when
unrelated attributes are added. Building a representation costs time and output storage
proportional to the displayed text; avoid reading remote data or formatting huge payloads.''',
'''
class UnsafeEndpoint:
    def __init__(self):
        self.host = 'api.example'
        self.token = 'demo-secret'
    def __repr__(self):
        return f'UnsafeEndpoint({self.__dict__!r})'

class Endpoint(UnsafeEndpoint):
    def __repr__(self):
        return f'Endpoint(host={self.host!r}, token=<redacted>)'
    def __str__(self):
        return f'endpoint at {self.host}'

unsafe, safe = UnsafeEndpoint(), Endpoint()
print('unsafe representation includes synthetic token:', unsafe.token in repr(unsafe))
print(str(safe))
print(repr([safe]))
for rendered in (str(safe), repr(safe), repr([safe]), f'{safe!r}'):
    assert safe.token not in rendered
assert 'api.example' in repr(safe)
''',
'The first class deliberately dumps all attributes. The repaired class overrides diagnostic and readable forms. A list exercises repr indirectly, and the assertions check that each tested rendering excludes the synthetic token.',
'''Use only artificial credentials in experiments. An allowlisted field is safe only under
its data contract: a host field containing a credential-bearing URL would still leak through
this example. Redacting repr does not sanitize explicit attribute logging, serialization,
traceback locals, or memory. Optional depth: truncate large public fields and test escaping
and container rendering without hiding the identity needed to debug.''',
'''1. Why can print(obj) look safe while print([obj]) leaks?
2. Why is an explicit field allowlist safer than dumping all attributes?
3. What should happen if __repr__ returns a non-string?
4. Which debugging details does your safe representation preserve?''',
'[Python 3.12 representations](https://docs.python.org/3.12/reference/datamodel.html#object.__repr__) defines repr/str dispatch; field redaction is an application design decision illustrated here.')

chapter(23, 'lang', 'Decline unsupported comparisons correctly', 'Special methods; equality versus ordering',
'Return NotImplemented when an operand pair is unsupported so Python can try the other operand or its final fallback.',
'A custom quantity returns False for every unfamiliar object. A second type could have compared the values, but it never gets the chance.',
'''False means the comparison was understood and its answer is false. NotImplemented means
this method does not handle the operand pair. It is a return value, not NotImplementedError.
For ordering, __lt__ and __gt__ form a reflected pair: left < right may try right.__gt__(left).
If neither supports ordering, the expression raises TypeError. Equality instead has an
identity-based fallback when both methods decline. Do not use NotImplemented as a boolean.''',
'''In the demonstration, Low.__lt__ declines comparison with High. High.__gt__ recognizes Low
and returns True, so Low() < High() is True. If a bad Low.__lt__ returns False, dispatch has
an answer already and the reflected method is not tried. Neither Low nor a plain object
understands their ordering, so Low() < object() raises TypeError.

| Step for unrelated operand classes | Result |
| --- | --- |
| left.__lt__(right) | NotImplemented permits another attempt |
| right.__gt__(left) | A supported result completes the expression |
| Both decline | Ordering raises TypeError |

There is a subclass priority rule: when the right operand's type is a strict subclass of
the left operand's type, its reflected method has priority. This demo uses unrelated classes
to make the simple trace visible. Implementing one comparison does not automatically define
every other ordering operation. Correctness means the supported domain and order are clear;
do not invent an order between unrelated types just to suppress errors. Dispatch itself is
bounded overhead, but comparing payloads can cost O(m) for m-element sequences.''',
'''
class Low:
    def __lt__(self, other):
        print('Low declines')
        return NotImplemented

class High:
    def __gt__(self, other):
        if isinstance(other, Low):
            print('High accepts reflected comparison')
            return True
        return NotImplemented

class BadLow(Low):
    def __lt__(self, other):
        return False

print('premature False:', BadLow() < High())
assert (Low() < High()) is True
try:
    Low() < object()
except TypeError:
    print('unsupported ordering: TypeError')
else:
    raise AssertionError('unsupported ordering should fail')
x, y = Low(), Low()
assert (x == x) is True and (x == y) is False
''',
'BadLow supplies a definitive False. Low declines and High handles the reflected comparison. The final ordering has no implementation, and the caught exception confirms that boundary. The equality assertions demonstrate a different fallback.',
'''Document whether subclasses share your value semantics. Changing equality also requires
revisiting hashing; reuse the [hash/equality lesson](../../day-004-reverse-a-segment/lang_hash-and-equality/CONCEPTS.md)
before using custom values as keys. Optional depth: explicitly trace subclass priority and
verify a total ordering's transitivity instead of assuming dispatch guarantees it.''',
'''1. What information differs between False and NotImplemented?
2. Which method reflects __lt__?
3. What happens when both operands decline equality versus ordering?
4. Why is raising NotImplementedError the wrong way to decline an operand?''',
'[Python 3.12 rich comparisons](https://docs.python.org/3.12/reference/datamodel.html#object.__lt__) specifies reflected dispatch, subclass priority, and final fallbacks.')

chapter(24, 'lang', 'Make a collection safely repeatable', 'Day 15 iterator protocol; representation ownership',
'Keep immutable contents separate from traversal state, and give each iteration a fresh cursor.',
'A tiny collection stores one iterator and returns it to every loop. The first display works; the next loop sees nothing, even though len still reports three items.',
'''The assignment needs three operations: len(collection), iter(collection), and value in
collection. Define __len__, __iter__, and __contains__ on the class. Their meanings should
agree about which items belong to the collection. The collection should retain contents;
each iterator retains only its own traversal position. A tuple snapshot of immutable values
is a simple backing representation. Snapshotting a list of mutable objects does not freeze
the objects, and a tuple-valued attribute alone does not prevent attribute rebinding.''',
'''For a collection snapshot (2,4,6), len returns 3. Iterator a and iterator b each start
before 2. Advancing a yields 2 and then 4; advancing b still yields 2. A membership test
for 4 consults contents without changing either cursor. A new traversal yields all three.

| Operation | Tuple-backed cost in this teaching design | State changed |
| --- | --- | --- |
| Construction from finite source | O(n) time and O(n) stored references | Snapshot created |
| len | O(1) | None |
| iter | O(1) cursor allocation | New independent cursor |
| Full traversal | O(n) with O(1) cursor state | That cursor only |
| contains | O(n) worst-case equality checks | No traversal cursor |

The demonstration uses a tuple subclass for an immutable integer collection and explicitly
delegates the three requested hooks. __slots__=() prevents an instance attribute dictionary;
the inherited tuple payload cannot be reassigned. Integer contents make this example deeply
immutable as well. The exercise can use another representation if its immutability contract
is explicit. Without __contains__, membership can fall back to iteration; repeated traversal
still depends on a correctly implemented __iter__.''',
'''
class BadCollection:
    def __init__(self, items):
        self.items = tuple(items)
        self.cursor = iter(self.items)
    def __len__(self):
        return len(self.items)
    def __iter__(self):
        return self.cursor

class IntCollection(tuple):
    __slots__ = ()
    def __new__(cls, items):
        values = tuple(items)
        if not all(type(value) is int for value in values):
            raise TypeError('integer items required')
        return super().__new__(cls, values)
    def __len__(self):
        return tuple.__len__(self)
    def __iter__(self):
        return tuple.__iter__(self)
    def __contains__(self, value):
        return tuple.__contains__(self, value)

bad = BadCollection([2, 4, 6])
print('shared cursor:', list(bad), list(bad), 'length:', len(bad))
source = [2, 4, 6]
good = IntCollection(source)
source.append(8)
a, b = iter(good), iter(good)
assert next(a) == 2 and next(a) == 4 and next(b) == 2
assert 4 in good and 8 not in good and len(good) == 3
assert list(good) == list(good) == [2, 4, 6]
try:
    good[0] = 9
except TypeError:
    print('immutable payload: TypeError')
print('fresh traversal:', list(good))
''',
'BadCollection stores one cursor, causing its second traversal to be empty. IntCollection snapshots and validates inputs, delegates each protocol to immutable tuple storage, and verifies separate cursors, source independence, membership, and rejected mutation.',
'''Choose between order and faster lookup deliberately: adding a set can accelerate repeated
membership but adds O(n) storage and requires hashable elements. A tuple holding mutable
elements promises only an immutable outer structure. State that limit if you broaden this
example beyond integers. Special methods belong on the type; assigning a hook only to one
instance is not a reliable way to customize implicit protocol operations.''',
'''1. Why can len(bad) remain three after iteration is exhausted?
2. Which object owns contents and which owns position?
3. Why does a tuple of lists fail to promise deep immutability?
4. What test detects two loops accidentally sharing one cursor?''',
'[Python 3.12 container protocol](https://docs.python.org/3.12/reference/datamodel.html#emulating-container-types) and [iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types) define the operation hooks and cursor expectations.')

chapter(21, 'sd', 'Review ownership through a failed request', 'Days 15–20 design decisions',
'Revise one weak decision by following an acknowledged operation across failure and recovery.',
'Two workers make an application look resilient until a process restart erases a job the client was told had been accepted.',
'''Choose your weakest prior design using your own evidence before reading this repair.
Name a user-visible promise, trace how the existing decision can violate it, revise one
diagram or memo, and defend an alternative. This lesson's job-acceptance example is a
hypothetical review choice, not a diagnosis of your work. Ownership means identifying the
authoritative home of each fact: accepting process memory is different from durable storage.''',
'''Use the original concepts for targeted repair:
[domain model](../../day-015-sorted-pair-existence/sd_domain-model/CONCEPTS.md),
[API contract](../../day-016-unique-triples/sd_api-contract/CONCEPTS.md),
[stateless workers](../../day-017-container-capacity/sd_stateless-workers/CONCEPTS.md),
[sync/async](../../day-018-fixed-window-maximum-sum/sd_sync-versus-async/CONCEPTS.md),
[compatibility](../../day-019-longest-distinct-substring/sd_compatibility/CONCEPTS.md), and
[module boundaries](../../day-020-minimum-positive-window/sd_modular-monolith/CONCEPTS.md).

Worked failure: a worker creates job j in a local dictionary, returns accepted, then crashes.
The next worker has no j and cannot return status. Adding more workers did not preserve
the accepted fact. Revision: commit the job to a shared durable store before replying;
workers claim pending jobs and write results there. A lost response still allows a retry,
so a request identity must map to one job. A worker crash after an effect but before its
completion record still requires idempotency or reconciliation.

The changed invariant is: every accepted job has an authoritative record available after
the modeled worker failure. Durability adds a storage dependency and write latency; it does
not prove zero data loss under every database failure. Keep 5 minutes cold recall, 10 minutes
failure/concept comparison, 12 minutes revision, and 3 minutes critique. Read the
[complete reference](REFERENCE_DESIGN.md) only after the cold attempt.''',
'''
worker_memory = {'j': 'pending'}
accepted = 'j'
worker_memory.clear()  # model a worker restart
print('local-only accepted job survives:', accepted in worker_memory)
durable_store = {'j': 'pending'}  # separate authority in this model
replacement_worker = {}
print('external authority retains:', durable_store[accepted])
assert accepted not in worker_memory
assert durable_store[accepted] == 'pending'
''',
'Clearing one dictionary models loss of one process. Keeping the authority in a separate dictionary demonstrates the ownership distinction only; no persistence engine or crash recovery has been tested.',
'''A useful defense names the residual failure and when its alternative wins. Synchronous
completion can simplify short operations; accepted asynchronous work fits long tasks only
when a real status and recovery contract exists. Do not replace one weak decision with a
full platform redesign or claim that a reference determines your personal weakest topic.''',
'''1. What user promise does the original failure violate?
2. Where does the revised design keep the authoritative acceptance fact?
3. What remains uncertain after the effect succeeds but status is not recorded?
4. What changes would make synchronous completion preferable?''',
'This review reuses the original design lessons linked below and their sources. Its durable-job workflow is a stated design proposal, not a claim of an executed service.')

chapter(22, 'sd', 'Put data rules at the write boundary', 'Day 15 domain identities; tables and keys',
'Use constraints for facts that must stay true for every write, and choose lookup indexes from separate access patterns.',
'Two requests both check that a short code is unused and then insert it. A read-before-write check alone cannot protect uniqueness under concurrent writers.',
'''A table row represents an entity. A primary key identifies it; UNIQUE prevents repeated
key values; NOT NULL requires a value; a foreign key requires an existing referenced key.
For this design, each link has one owner and a globally unique non-null code. Many links
may share an owner or destination. A foreign key protects existence, not whether the caller
is authorized to act for that owner. A product invariant and a useful lookup path are
different decisions even when the database implements a constraint with an index.''',
'''Map the product rules before choosing SQL:

| Rule | Proposed database artifact | Why |
| --- | --- | --- |
| Owner has stable identity | owners.id PRIMARY KEY | One referenced entity |
| Link has stable identity | links.id PRIMARY KEY | Edits preserve identity |
| Code maps to one link globally | code NOT NULL UNIQUE | No ambiguous redirect |
| Every link belongs to an existing owner | owner_id NOT NULL REFERENCES owners(id) | No orphan ownership |
| Owner listing should be fast | A separate candidate index on owner/time | Performance, not validity |

Race trace: A checks code `spruce`, B checks the same code, both see absent, A inserts,
B inserts. Without enforced uniqueness, two rows satisfy the application's local check.
A database uniqueness constraint makes the second conflicting committed value unacceptable.
The service must handle the conflict and return a documented response or choose another code.
Two sequential application checks do not reproduce the concurrent race.

The [reference](REFERENCE_DESIGN.md) supplies complete proposed PostgreSQL DDL and deletion
policy. Non-null identity fields avoid treating missing values as real keys. PostgreSQL's
ordinary unique constraint can otherwise admit multiple nulls. Keys incur index storage and
write maintenance. A foreign key on links.owner_id does not automatically create a lookup
index on that referencing column; assess that path separately.''',
'''
rows = []
a_saw_free = not any(row['code'] == 'spruce' for row in rows)
b_saw_free = not any(row['code'] == 'spruce' for row in rows)
if a_saw_free:
    rows.append({'code': 'spruce', 'owner': 1})
if b_saw_free:
    rows.append({'code': 'spruce', 'owner': 2})
print('check-then-insert duplicates:', len(rows))
assert len({row['code'] for row in rows}) < len(rows)

accepted_codes = set()
def constrained_insert(code):
    if code in accepted_codes:
        raise ValueError('duplicate code')
    accepted_codes.add(code)

constrained_insert('spruce')
try:
    constrained_insert('spruce')
except ValueError as error:
    print('serialized rule model:', error)
assert accepted_codes == {'spruce'}
''',
'Both prechecks run before either insert, deliberately modeling an interleaving. The second half models a serialized uniqueness decision; this Python function is not itself a concurrent database substitute.',
'''Decide owner deletion explicitly. RESTRICT rejects deletion while links remain; CASCADE
would remove dependent rows and needs a product justification. A single-row CHECK cannot
enforce every cross-row business rule. Application validation remains useful for good errors
and URL policy, but it complements authoritative integrity checks. Inspect existing data
before proposing a migration that assumes the new constraints already hold.''',
'''1. Why can two successful prechecks still produce duplicates?
2. Which rule permits many links per owner?
3. Why does an owner foreign key not prove caller authorization?
4. Which proposed index is about lookup cost rather than product validity?''',
'[PostgreSQL 18 constraints](https://www.postgresql.org/docs/18/ddl-constraints.html) documents primary, unique, non-null, and foreign-key semantics. The link product rules are explicit assumptions.')

chapter(23, 'sd', 'Order an index around the query', 'Day 22 link schema; equality filters and sorting',
'For an owner-specific newest-first listing, lead with owner equality and follow it with the requested order and a unique tie breaker.',
'An index on every relevant column can still scan many irrelevant records if its leading order interleaves all owners.',
'''An index is a maintained access path. A multicolumn B-tree orders key tuples, comparing
earlier components first. For `WHERE owner_id = ? ORDER BY created_at DESC, id DESC`,
placing owner first groups the relevant rows, and the suffix orders that group for output.
Selectivity is the fraction of rows matching a predicate; it affects whether a path is
attractive. An index helps a workload under assumptions, not every query touching its columns.''',
'''Toy records use logical time ticks, not measured timestamps:

| id | owner | created tick |
| --- | --- | --- |
| 1 | A | 10 |
| 2 | B | 30 |
| 3 | A | 20 |
| 4 | B | 40 |
| 5 | A | 20 |

For owner A, the expected newest-first IDs are 5,3,1. Keys
(owner ASC, created DESC, id DESC) place those three adjacent and ordered. Swapping the
first columns to (created DESC, owner ASC, id DESC) gives global order 4,2,5,3,1;
an owner-A query may examine unrelated B rows before finding its results. The timestamp
tie needs id DESC so two rows created together still have a deterministic order.

This explains suitability, not an absolute prohibition: PostgreSQL can use non-leading
conditions, and PostgreSQL 18 may use skip scan when its cost model favors it. Actual row
distribution and LIMIT matter. A conceptual B-tree seek plus k matching entries is often
described as O(log N+k); heap access, visibility, extra filters, and page locality still
determine database work. An owner-only index narrows rows but may still require sorting.
An index ordered by time first instead fits a global newest-links feed.''',
'''
rows = [('A', 10, 1), ('B', 30, 2), ('A', 20, 3), ('B', 40, 4), ('A', 20, 5)]
owner_first = sorted(rows, key=lambda r: (r[0], -r[1], -r[2]))
time_first = sorted(rows, key=lambda r: (-r[1], r[0], -r[2]))
print('owner-first IDs:', [r[2] for r in owner_first])
print('time-first IDs:', [r[2] for r in time_first])
wrong = [r[2] for r in time_first[:2] if r[0] == 'A']
right = [r[2] for r in owner_first if r[0] == 'A'][:2]
print('limit before owner filter:', wrong, 'owner result:', right)
assert wrong == [] and right == [5, 3]
''',
'Sorting tuple keys illustrates the two index orders. Taking the global top two before filtering owner is a deliberately wrong query transformation, not what PostgreSQL does. Filtering the correct owner before limiting preserves semantics.',
'''Each extra index consumes storage and adds write work. Including a large URL payload can
increase that cost; an index-only path also depends on visibility and query coverage, not
just column presence. Optional depth: a continuation predicate on (created_at,id) can avoid
large offsets, but cursor design belongs to the earlier pagination contract. Inspect a plan
and representative owner distributions before claiming a latency improvement.''',
'''1. Why put an equality-constrained owner before the ordered suffix?
2. Why is created_at alone insufficient for deterministic ties?
3. Which workload would favor time-first ordering?
4. Why is “non-leading columns can never use an index” too strong?''',
'[PostgreSQL 18 multicolumn indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html) and [index ordering](https://www.postgresql.org/docs/18/indexes-ordering.html) support the access-path tradeoff and skip-scan qualification.')

chapter(24, 'sd', 'Read a query plan as a flow of rows', 'Days 22–23 schema and indexes',
'Follow rows from scan through filtering, ordering, and limit, distinguishing planner estimates from executed evidence.',
'A plan says rows=20 and cost=40. Neither proves the query examines only twenty rows nor takes forty milliseconds.',
'''SQL states the required result; a plan proposes physical operations producing it.
EXPLAIN without ANALYZE reports an estimated plan. EXPLAIN ANALYZE executes the query and
adds observed execution statistics. A node emits rows to its parent. A filter rejects rows
already visited by its scan, while an index condition can restrict the index search. A sort
establishes output order unless the chosen access path already supplies it.''',
'''For the owner listing from [Day 23](../../day-023-target-range/sd_index-selection/CONCEPTS.md),
a conceptual path is scan links → filter owner=7 → sort by created_at/id descending → limit 20.
This is a hand-drawn possibility, not captured EXPLAIN output. Read it bottom-up even if a
printed plan displays Limit at the top. PostgreSQL can attach the filter directly to the
scan node; it need not appear as a separate node.

With illustrative rows [(A,1),(B,9),(A,4),(A,3)], scanning visits four rows, filtering emits
three A rows, sorting produces A4,A3,A1, and limit two emits A4,A3. Limiting before sorting
the matching input would emit A4,A1 instead. LIMIT does not always avoid upstream work:
a sort may need to consider all qualifying rows before identifying the best ones.

With the owner/time index, an ordered index scan may feed Limit without a separate Sort.
For a tiny table or a low-selectivity request, scan plus sort can still be reasonable.
Plan cost is in planner units, not milliseconds; rows estimates are output counts per node.
Parent cost includes child work, so adding all node costs double-counts. In executed plans,
actual time and rows are reported per loop when a node runs repeatedly. Buffer counts
describe page activity, not direct end-to-end response time. The [reference](REFERENCE_DESIGN.md)
shows a complete interpretation and an optional read-only validation query.''',
'''
rows = [('A', 1), ('B', 9), ('A', 4), ('A', 3)]
filtered = [r for r in rows if r[0] == 'A']
ordered = sorted(filtered, key=lambda r: -r[1])
right = ordered[:2]
wrong = sorted(filtered[:2], key=lambda r: -r[1])
print('visited/emitted/returned:', len(rows), len(filtered), len(right))
print('limit before sort:', wrong, 'sort before limit:', right)
assert wrong != right
assert right == [('A', 4), ('A', 3)]
''',
'The lists model row flow and make the misplaced limit observable. The counts are actual Python model counts; they are not database estimates, query execution timings, or benchmark results.',
'''Find the first large estimate error and the work amplified downstream. Skewed owners or
stale statistics can undermine a planner assumption; do not force an index solely because
an index exists. For optional measurement use representative data and SELECT in a controlled
database. ANALYZE executes its statement, so it is not a harmless preview for arbitrary
writes. Keep database execution time separate from application and network latency.''',
'''1. How can a scan visit a million rows but emit only twenty?
2. Why is planner cost not elapsed milliseconds?
3. When can an ordered index remove a Sort node?
4. Which observations require ANALYZE rather than plain EXPLAIN?''',
'[PostgreSQL 18 Using EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html) defines estimated and actual plan fields; [index ordering](https://www.postgresql.org/docs/18/indexes-ordering.html) explains avoiding an explicit sort.')

write(folder(21, 'sd') / 'REFERENCE_DESIGN.md', '''
# Week 3 reference review — accepted jobs survive a worker restart

Read after your cold attempt. This is an author-selected example of a weak decision from
Days 15–20, not a claim about your personal work. [CONCEPTS.md](CONCEPTS.md) teaches the review;
[DESIGN.md](DESIGN.md) remains your evidence file.

## Assumptions and requirement

Consider a hypothetical link-export service. An authenticated owner requests an export, receives
a job ID, and polls its status. Acceptance promises that the job can still be found after an
application worker restarts; it does not promise immediate success. Storage durability and
availability are explicit service dependencies. Export completion latency and workload are
unmeasured; this memo requires no invented traffic or timing targets.

## Weak decision and revised artifact

The old worker puts the job in its local map and replies accepted. That violates the promise
if the next status request reaches another worker or the original process crashes.

```text
Owner -> API worker -> shared jobs table: commit pending job + request identity
Owner <- API worker: accepted(job_id), only after commit
Job worker -> shared jobs table: claim pending work with recoverable lease
Job worker -> export storage: publish result under stable job identity
Job worker -> shared jobs table: record success + result location
Owner -> any API worker -> shared jobs table: authorize and read status
```

The job module owns job state; the link module supplies authorized export data through its
interface. A row includes job_id, owner_id, request_key, request_fingerprint, status,
lease_expiry, and result_location. Uniqueness of (owner_id,request_key) makes a matching retry
return the same job; a changed fingerprint is a conflict. Keep the record and request identity
in one transaction. The export input consistency policy must also be stated: this proposal
exports data visible when execution starts, not a snapshot at acceptance.

States are pending → running → succeeded or failed. A recoverable lease permits running →
pending when a worker disappears. Lease duration would be chosen from measured task and
heartbeat behavior; no universal duration is asserted. Terminal states remain queryable for
an explicit retention period set by the product before implementation.

## Decision and alternative

Choose asynchronous durable jobs because this hypothetical export can outlast a request.
The cost is a jobs store, status API, recovery logic, and delayed visibility. Synchronous
generation is a credible alternative for bounded small exports that fit the measured request
budget; it reduces state and operational complexity. A separate message broker is another
possible execution path, but adding it would require a transaction-safe handoff. It is not
necessary to demonstrate this revision.

## Failure walkthrough

1. The API commits job j but loses the response. The caller retries the same identity and
   payload; the durable record yields j again rather than a second export.
2. A worker claims j and crashes. The record survives. After the claim expires, recovery
   permits another attempt; duplicate execution must be tolerated.
3. If the crash follows writing the result but precedes the success update, retry uses the
   same result identity and checks/reconciles it. Conflicting output must not be published as
   a second independent user result. This is not a claim of exactly-once execution.
4. If the jobs store is unavailable before commit, the API cannot honestly return acceptance.
   An ambiguous commit requires retry/reconciliation using request identity.

## Self-review

The revised ownership preserves accepted state across the modeled worker failure. It leaves
database disaster recovery, lease timing, export consistency, and retention as explicit limits.
Next validation would kill a worker after commit and after result publication, retry through
another API instance, and verify one job identity and a recoverable status. Those are proposed
tests, not observed results. The Python model in the concepts lesson tests only ownership.
The [Day 18 reference](../../day-018-fixed-window-maximum-sum/sd_sync-versus-async/REFERENCE_DESIGN.md)
provides related handoff reasoning. This completes the assigned revision, alternative defense,
and failure walkthrough without recording learner completion.
''')

write(folder(22, 'sd') / 'REFERENCE_DESIGN.md', '''
# Schema reference — owners and links

This is a complete proposed answer to today's schema task. SQL is an authored PostgreSQL 18
artifact, not an executed migration. [CONCEPTS.md](CONCEPTS.md) explains the rules;
[DESIGN.md](DESIGN.md) belongs to your practice.

## Assumptions and product rules

Every link has one existing owner. A case-sensitive short code is globally unique and cannot
be empty. Link identity survives destination edits. Different links may share a destination,
and one owner may create many links. Owner deletion is rejected while links remain. Creation
time is stored with time-zone semantics and never intentionally edited by this application.
These are chosen product rules, not inferred universal URL-shortener requirements.

## Proposed schema

```sql
CREATE TABLE owners (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    display_name text NOT NULL
);

CREATE TABLE links (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_id bigint NOT NULL REFERENCES owners(id) ON DELETE RESTRICT,
    code text COLLATE "C" NOT NULL UNIQUE CHECK (length(code) > 0),
    destination_url text NOT NULL CHECK (length(destination_url) > 0),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

The primary keys provide stable identity. The code constraint enforces one redirect identity
even if requests race. The explicit C collation makes the code comparison case-sensitive for
this design. The owner foreign key prevents orphan rows, while NOT NULL disallows unowned links.
The length checks reject empty strings; they do not establish URL validity. The application
separately validates the accepted URL schemes and syntax and derives owner_id from authorization.
Foreign-key existence alone would not stop a caller from naming another existing owner.

Product rules and lookup needs are distinct:

| Artifact | Purpose | Deliberately not implied |
| --- | --- | --- |
| links.code UNIQUE | Global code identity; also supports exact lookup | Unique destination URLs |
| links.owner_id foreign key | Valid ownership reference | One link per owner or caller authorization |
| Proposed owner/time index on Day 23 | Fast ordered owner listing | A new validity rule |

PostgreSQL creates supporting unique indexes for primary/unique constraints. It does not
automatically create an index on the referencing owner_id column. Its ordinary unique-null
behavior is avoided here by requiring code. These semantics come from the
[constraints documentation](https://www.postgresql.org/docs/18/ddl-constraints.html).

## Decision and alternative

Global uniqueness fits a redirect path that contains only the code. An alternative unique
(owner_id,code) constraint allows each owner to reuse a code, but then owner context must
also participate in resolution. Do not switch without changing the public lookup contract.
RESTRICT makes owner removal an explicit workflow. CASCADE is defensible only if deleting an
owner is intended to remove all owned links and its consequences have been accepted.

## Failure walkthrough

Two transactions request `spruce`. Both application prechecks find it absent. The database
constraint arbitrates conflicting inserts: both cannot commit that same code. Map a conflict
to a stable API outcome; for generated codes retry with a different code within a bounded
policy. For an explicitly requested alias, report conflict rather than silently changing it.
The exact winner is timing-dependent, not assumed here. Similarly, deletion of an owner with
links is rejected; perform an explicit link-removal or ownership-transfer workflow first.

## Self-review

This schema covers identities, global code uniqueness, mandatory ownership, and a deletion
choice. It does not enforce every URL or lifecycle policy, nor prove lookup latency. Before
implementation, verify code normalization, authorization, migration handling for existing
duplicates, and owner-deletion behavior. Test duplicate codes, missing owners, empty values,
and a concurrent collision in a real database. No such database test is claimed here.
''')

write(folder(23, 'sd') / 'REFERENCE_DESIGN.md', '''
# Index reference — one owner's newest links

This proposed answer uses the [Day 22 schema](../../day-022-lower-bound/sd_schema-constraints/REFERENCE_DESIGN.md).
No index has been deployed or benchmarked. [DESIGN.md](DESIGN.md) remains your practice file.

## Workload and query assumptions

The main request lists one authorized owner's latest 20 links. Twenty rows is an illustrative
page size selected for this example, not a measured limit. Owners have unequal link counts;
we do not assume uniform distribution. Newest means created_at descending, with id descending
to break equal timestamps. Identity and creation time are stable across traversal.

```sql
SELECT id, code, destination_url, created_at
FROM links
WHERE owner_id = $1
ORDER BY created_at DESC, id DESC
LIMIT 20;

CREATE INDEX links_owner_newest_idx
ON links (owner_id, created_at DESC, id DESC);
```

The parameter is supplied by the authorized request context. Leading owner equality narrows
the ordered key range. Within it, the suffix matches the requested order and can let a scan
stop after enough visible qualifying rows. The id tie breaker gives deterministic ordering;
it does not claim transaction commit order. The selected payload can require heap access:
destination_url and code are not in this index.

## Why column order changes usefulness

Assume five illustrative entries (owner,tick,id): (A,10,1), (B,30,2), (A,20,3), (B,40,4),
(A,20,5). Ticks represent order only. The proposed index groups A's IDs as 5,3,1 before B's
4,2. A time-first index instead orders IDs 4,2,5,3,1, interleaving owners. It can serve a
global newest feed well but may examine many other owners for an owner-specific request.
The model's small count is not a prediction of pages read on a deployed database.

[PostgreSQL multicolumn B-tree rules](https://www.postgresql.org/docs/18/indexes-multicolumn.html)
support leading equality with an ordered suffix. A time-first index is not categorically
unusable: non-leading conditions and, in PostgreSQL 18, suitable skip-scan choices may help.
The chosen path depends on statistics and cost. Matching index order can avoid a separate
sort, as described by [index ordering](https://www.postgresql.org/docs/18/indexes-ordering.html).

## Alternative and costs

An owner-only index is smaller and can narrow the matching set before sorting it. It may be
adequate if each owner has few links. A time-first index is preferable for global feeds.
Maintain the proposed composite index only if owner listings justify its storage and insert/
update overhead. Including long URL payloads might reduce some heap reads but expands the
index and still does not guarantee index-only execution; measure before choosing that variant.

## Failure walkthrough

A time-first scan seeks the newest global rows for an owner with sparse activity. Many rows
belong to other owners, so returning 20 may require much more work than the page size suggests.
The user sees slow listings even though an index exists. Correct filtering still returns the
right owner; moving LIMIT ahead of the owner filter would instead create a correctness bug.
Repair the access path around owner equality, then compare actual scanned work and latency.
An independent correctness failure occurs when equal timestamps have no tie breaker: repeated
requests can return unstable ordering. Keeping id in both query order and index fixes that
ambiguity under the stated stable-key assumption.

## Self-review and next verification

The key order is justified by one explicit query. It does not accelerate every lookup or
promise a fixed response time. Compare plans and executions for small, large, and sparse
owners, including tied timestamps, and inspect write overhead and index size. Day 24 explains
those plans. Preserve the same predicates, ORDER BY, and result semantics while comparing;
the proposed improvement remains unmeasured.
''')

write(folder(24, 'sd') / 'REFERENCE_DESIGN.md', '''
# Query-plan reference — scan, filter, order, and limit

This is a completed interpretation of a proposed query using the
[Day 22 schema](../../day-022-lower-bound/sd_schema-constraints/REFERENCE_DESIGN.md) and
[Day 23 index](../../day-023-target-range/sd_index-selection/REFERENCE_DESIGN.md).
No database was run. The shapes below are conceptual possibilities, not captured EXPLAIN
output. [DESIGN.md](DESIGN.md) is your own artifact and evidence file.

## Assumptions and query

Owner 7 is an illustrative existing owner ID. The client requests the newest 20 links,
ordered by creation timestamp and then ID descending. Twenty is a chosen page size in rows;
it is not an estimate of scanned rows. Owner cardinalities, table size, cache state, latency,
and planner statistics are unknown.

```sql
EXPLAIN
SELECT id, code, destination_url, created_at
FROM links
WHERE owner_id = 7
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

## Read the row flow

One possible shape without a useful ordered access path is:

```text
Limit: emit at most 20 rows
  Sort: created_at DESC, id DESC
    Sequential scan of links, with filter owner_id = 7
```

Read from the leaf upward. The scan visits table rows, applies the owner predicate, and
emits matching rows. The sort considers those matches and supplies the requested order.
Limit consumes at most 20 sorted results. PostgreSQL may use a bounded sort strategy; that
does not imply it avoids examining the qualifying input. If five illustrative stored rows
include three owner-7 rows, the scan can visit five, filter to three, and limit emit three.
Those are hand-trace counts, not estimates from a real plan.

With links_owner_newest_idx, another possible shape is:

```text
Limit: emit at most 20 rows
  Ordered index scan using links_owner_newest_idx
    Index condition: owner_id = 7
```

The owner condition narrows the key range and the suffix supplies order, potentially removing
Sort. Heap visibility and payload retrieval still matter. Extra predicates could appear as
filters and make more entries necessary. A small table may legitimately use scan plus sort.

## Interpret the fields without inventing measurements

| Field | Meaning in this review |
| --- | --- |
| cost=startup..total | Planner cost units; neither milliseconds nor a service deadline |
| rows | Estimated output rows for a node; not all visited input rows |
| width | Estimated output row width in bytes |
| actual time/rows/loops | Execution observations from ANALYZE; per-loop time/row figures need loop context |
| Buffers | Database buffer/page activity, not full client latency |

Parent costs include child costs. Summing costs down a path therefore double-counts.
[PostgreSQL Using EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html) supplies
these distinctions; [index ordering](https://www.postgresql.org/docs/18/indexes-ordering.html)
explains the candidate Sort elimination. These sources support interpretation, not a claim
that either conceptual plan will be chosen for an unmeasured data set.

## Decision and alternative

Start by inspecting plain EXPLAIN for the real schema and representative owner IDs. If
measurement is appropriate in a controlled database, this read-only query can be run as:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, code, destination_url, created_at
FROM links
WHERE owner_id = 7
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

ANALYZE here executes SELECT; it adds load and returns instrumentation rather than the query's
normal result set. Do not treat ANALYZE as a dry run of arbitrary writes. The alternative is
to reason from estimates only, with lower operational impact but no claim of actual speed.
Separate SQL timings from connection wait, serialization, transport, and user-visible latency.

## Failure walkthrough

Suppose the planner expects few matching rows but this owner actually owns a large fraction
of the table. A path chosen from that estimate can do far more work than expected, especially
with additional filtering or sorting. The client experiences delay. Compare estimate and
actual cardinality at the first divergent node, inspect statistics and data skew, then assess
updated statistics or a revised access path. Forcing an index because its name exists can
make things worse. This is a hypothetical incident and proposed investigation, not an observed
slow query or proof that stale statistics caused one.

## Self-review

The artifact explains scan, filter, sort, limit, both access-path choices, and estimated
versus observed evidence. It intentionally contains no fabricated plan costs or timings.
Next verification is a captured plan with database version, representative data distribution,
query parameters, row results checked separately, and actual execution observations if run.
The concepts lesson's Python model only verifies the row-ordering example.
''')
