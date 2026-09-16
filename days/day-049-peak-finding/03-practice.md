---
day: 49
track: practice
title: "Practice — Peak finding, and searching data that is structured but not sorted"
status: written
---

# Day 049 · Practice

**DSA topic:** Peak finding, and searching data that is structured but not sorted
**System design topic:** Composition over inheritance

**Theme:** Routing and middleware

---

## Code these, in this order

One rule today: **for every problem, say the invariant and the discard proof out loud before writing a
line.** These problems have no target and no monotone question — the proof is all you have, and if you
cannot state it you are guessing.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Peak Index in a Mountain Array | LeetCode 852 (Medium) | The rule, with the answer guaranteed unique so nothing can distract you. |
| 2 | Find Peak Element | LeetCode 162 (Medium) | The same code with the guarantee removed — and whether you accept a non-unique answer. |
| 3 | Find Minimum in Rotated Sorted Array | LeetCode 153 (Medium) | The mirror: a valley. Re-derive it as local structure, not as a rotation trick. |
| 4 | Find a Peak Element II | LeetCode 1901 (Medium) | The 2D version, and whether you search columns and take each column's maximum row. |

### On problem 1, do the proof first

Before typing: *if it rises to the right of the middle, either it climbs to the end — and the last
element beats the imaginary negative infinity beyond it — or it turns over somewhere, and the turning
point is a peak. Either way a peak exists to the right.* Then write four lines. Then confirm the
guarantee that makes the answer unique changes nothing about the code.

### On problem 2, resist checking your answer against the maximum

Run it on `[1, 3, 2, 4, 7, 9, 5, 6, 2]`. It returns index 7, value 6 — and 9 is in the array. That is
correct. Write the `is_peak` helper from §5 and use it to check your answers, rather than comparing
against `max(nums)`. If you find yourself wanting the maximum, say out loud why that is O(n) and
cannot be beaten.

### On problem 3, do not look at day 045

Re-derive it as a valley: the minimum is the one element smaller than both neighbours, with the
wrap-around counted. Compare `nums[mid]` against `nums[hi]`, and say why comparing against `nums[lo]`
returns the maximum on an un-rotated array. Then notice you have written today's code with one
comparison flipped.

### On problem 4, get the axis right

Search over the **columns**, and inside each candidate column take the row holding that column's
largest value. That element already beats its up and down neighbours for free, which is what collapses
the problem back to one dimension. Write the version that scans the *row* instead and see it fail —
then say precisely why the discard is not justified in that version.

### The proof drill

Say each out loud, in under thirty seconds:

1. Why does every array have at least one peak?
2. Why does "it rises to the right" guarantee a peak to the right? Name the two cases and the fact
   that rules out a third.
3. Why is `hi = mid` and not `hi = mid - 1` in the falling branch?
4. Why is `mid + 1` always a valid index?
5. Why is the loop condition strictly `<`?

### The breakage drill

Produce each failure yourself and record what happens — a crash with a named exception, a silent wrong
answer, or a hang:

1. `while lo <= hi` with `hi = mid`, on `[1, 2, 3]`.
2. `hi = mid - 1` in the falling branch, on `[1, 2, 1, 3, 5, 6, 4]`.
3. Comparing with `nums[mid - 1]` instead of `nums[mid + 1]`, on `[1, 2]`.
4. `[1, 2, 2, 2, 1]` on the correct solution — what does it return, and is it a peak?

Number 4 is not a bug in your code. Say whose problem it is and what you would have asked for.

### The sortedness drill

For each, say whether binary search applies, and what the discard proof is:

1. A sorted array, find a target.
2. A rotated sorted array, find a target.
3. An unsorted array, find any peak.
4. An unsorted array, find the maximum.
5. An unsorted array of distinct values, find the third largest.
6. A monotone yes-or-no question over a range of capacities.

Two of these six have no discard proof. Name them and say what the cost is instead.

### The hierarchy refactor drill

Take this and rework it out loud in five minutes:

```python
class Notification: ...
class EmailNotification(Notification): ...
class SmsNotification(Notification): ...
class UrgentEmailNotification(EmailNotification): ...
class UrgentSmsNotification(SmsNotification): ...
class ScheduledEmailNotification(EmailNotification): ...
class ScheduledSmsNotification(SmsNotification): ...
```

1. Name the axes. How many are there, and what is the tell in the class names?
2. Which axis is the identity and which are things the object *has*?
3. Name each extracted component as a capability, not as a variant.
4. Count the classes now, and after adding a third channel, and after adding a fourth delivery
   timing.
5. Name the duplication that exists in the current version and where it goes.
6. Write the construction line for an urgent SMS.
7. Say what you gave up.

### The count drill

Fill in the table from memory, then check it:

```
axes                              inheritance      composition
3 channels                        ?                ?
3 channels x 3 timings            ?                ?
3 x 3 x 2 (with attachment)       ?                ?
adding a 4th channel              ? new classes    ? new classes
```

### The still-inheritance drill

For each, say compose or inherit, with the one-sentence reason:

1. `CardDeclined` and `PaymentError`.
2. `ElectricCar` and `Car`, in a system that also varies by size.
3. `JsonFormatter` and `logging.Formatter`.
4. `PremiumSubscriber` and `Subscriber`, where the difference is a discount rate.
5. `RetryingHttpClient` and `HttpClient`.
6. `TimestampMixin` on four unrelated model classes.

Say the one property shared by every "inherit" answer.

---

## Build these, in all three languages

*Three exercises, easiest first. Each one says what it is really testing. Every
exercise is done three times: once in Python, once in Go, once in C++.*

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Turned-back requests in the log | Whether your logging sits outside your auth, so a 401 still gets a line. |
| 2 | The caller's name reaches the route | How a value computed before routing gets into the handler, in three very different ways. |
| 3 | Reuse an incoming request id | Reading a header on the way in and echoing it on the way out, so one id follows a request across services. |

All three start from the lesson's server. Drive it with `curl -i` in a second terminal and keep
the server's terminal visible, because the log lines are the thing being checked.

### 1. Turned-back requests in the log

Send four requests: `/health` with no key, `/users/1` with no key, `/users/1` with a bad key, and
`/users/1` with the right key. The server must print exactly four log lines with statuses 200,
401, 401, 200, each carrying a request id, and every response must carry the same id in
`X-Request-ID`. Then break it on purpose: in Go, swap the chain to `auth(logging(mux))`; in Python,
move the key check into the middleware and return a 401 response from there before `call_next`;
in C++, move the log line into the `timed` wrapper and delete `set_logger`. Paste the four lines,
or the missing ones, into a comment, and say in one sentence what disappeared and why. Done means
four lines with the right statuses in all three, and a comment naming the broken order.

### 2. The caller's name reaches the route

Make `GET /users/{id}/greeting` answer `{"message": "hello Meera, from meera"}` where the second
name is whoever the API key belongs to. In Python it is `Depends(current_user)` as a parameter.
In Go, the auth middleware puts the caller on the request context with `context.WithValue` and
`r.WithContext`, under a key of an unexported type, and the handler reads it back. In C++, the
request is `const` inside a route, so choose: look the key up again in the route, set a response
header in the pre-routing handler and read it back with `res.get_header_value`, or keep a
mutex-guarded map from `std::this_thread::get_id()` to caller. Write a comment on the C++ version
saying which you chose and the one thing wrong with it. Done means the greeting is correct with
two different keys in all three languages.

### 3. Reuse an incoming request id

If the caller sends `X-Request-ID`, use it instead of making one; if not, make one. Prove it with
`curl -i -H "X-Request-ID: abc123" ...` and without the header, and paste both log lines. Then
call yesterday's day 47 client program from one server's handler to another server's `/health`,
passing the id along in the outgoing request's header, and show the same id appearing in both
servers' terminals. Done means one id in two logs in at least one language, and the header
round-trip working in all three.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find a peak element in O(log n).*
   Deal with the sortedness objection first, confirm the two conventions, state that an answer always
   exists, give the rule with its proof in one breath, and close on the peak-versus-maximum contrast.

2. *Refactor this class hierarchy. Why is your version better?*
   Name the axes from the class names, pick the identity, name the capability, give the count both
   ways, name the duplication removed, and concede the cost.

3. *Why does binary search work here? There is no order.*
   The general statement — binary search needs a discard proof, not sortedness — then this problem's
   proof, then two other days where the proof was something else.

### Languages

*Three questions from today. Answer each in two minutes, standing up, no notes.*

1. How would you add request logging to every endpoint?
   One wrapper, not forty edits: where it sits in each language, what one line contains, where
   the request id comes from, why it must sit outside auth, and the Go catch about reading the
   status back.
2. Where does authentication live, and how does the health check skip it?
   A router dependency in Python, a middleware with a path exception in Go, a pre-routing
   handler returning `Handled` in C++; and the reason `/health` is open in all three.
3. Middleware or a dependency: how do you choose?
   Middleware for what every request gets and what needs the response on the way out;
   dependencies or context values for what a route needs as a value. Give one example of each
   and one thing that goes wrong if you swap them.

## Before you move on

- [ ] I stated the discard proof before writing code on all four problems.
- [ ] I checked my peak answers with `is_peak`, not against `max(nums)`.
- [ ] I produced all four breakages and can say which is a crash, which is silent, and which hangs.
- [ ] I can say why finding the maximum is O(n) and cannot be beaten.
- [ ] I refactored the notification hierarchy and gave the class count for four axes both ways.
- [ ] I can name the property shared by every case where inheritance is still right.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] The three lesson servers log every request with a status and a request id, including the ones auth turned back.
- [ ] Exercise 1 shows four correct lines in all three, and I can say what the broken order loses.
- [ ] Exercise 2 greets from the right caller with two keys in all three, and my C++ comment names the flaw in the approach I chose.
- [ ] Exercise 3 carries one id through two servers' logs in at least one language.
- [ ] I can write the Go middleware signature and the `statusRecorder` from memory, and say why the recorder exists.
- [ ] I can say what a missing `Header` default does in FastAPI, what `Unhandled` after `reply` does in cpp-httplib, and why the C++ logger needs a mutex.
