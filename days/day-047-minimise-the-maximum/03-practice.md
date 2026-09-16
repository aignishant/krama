---
day: 47
track: practice
title: "Practice — Minimise the maximum: the capacity family"
status: written
---

# Day 047 · Practice

**DSA topic:** Minimise the maximum: the capacity family
**System design topic:** Polymorphism

**Theme:** HTTP clients

---

## Code these, in this order

For every problem, **ask the direction question out loud before writing anything**: does more of this
quantity make the task easier or harder? Write the answer down. Then the range, the check, and the
monotonicity sentence — then the loop, copied unchanged.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Minimized Maximum of Products Distributed to Any Store | LeetCode 2064 (Medium) | The gentlest minimise-the-maximum, with a ceiling-division check. |
| 2 | Split Array Largest Sum | LeetCode 410 (Hard) | Whether you reach for binary search instead of dynamic programming. |
| 3 | Magnetic Force Between Two Balls | LeetCode 1552 (Medium) | The mirror: maximise the minimum, and the sort you must not forget. |
| 4 | Divide Chocolate | LeetCode 1231 (Hard) | The same mirror behind deliberately confusing wording. |

### On problem 1, get the ceiling right

`(q + limit - 1) // limit` is the number of stores a quantity of `q` needs at a limit of `limit`.
Check it by hand on `q = 11, limit = 3`: four stores, not three. Then confirm `lo = 1` and not 0 by
running the check with `limit = 0` and collecting the
`ZeroDivisionError: integer division or modulo by zero`.

### On problem 2, write the DP first, then throw it away

Spend ten minutes writing the `O(n²k)` dynamic-programming solution. Get it right or get it nearly
right — it does not matter. Then write the binary search version and time both on a thousand elements
with k = 50. Say the ratio out loud. Having felt the difference once is what makes you reach for the
right tool under pressure, and being able to say "there's a DP at O(n²k) and I'm not using it because"
is stronger than not knowing it exists.

### On problem 3, break it two ways deliberately

First, run it on unsorted input and watch the answer come out wrong with no error. Then run the
version that uses the minimise-the-maximum direction — `if can_place(mid): hi = mid` — and watch it
return 1 every time. Say which failure each one is: a broken precondition on the check, and a search
pointed at the wrong end. They look the same from the outside and they are completely different bugs.

### On problem 4, translate the wording first

Before coding, rewrite the problem in your own words as a decision question with a limit in it. It is
"can I cut the bar into at least k+1 pieces, every piece summing to at least s?" — and once that
sentence exists the code is problem 3 with a different check. If you cannot produce that sentence,
you do not understand the problem yet, and no amount of coding will fix that.

### The direction drill

For each, say **easier or harder**, therefore **first True or last True**, in under five seconds:

1. A bigger ship capacity, with a day limit.
2. A bigger required gap between placed items.
3. A faster eating speed, with an hour limit.
4. A bigger allowed part sum, with a part-count limit.
5. A bigger minimum sweetness per piece, with a piece-count target.
6. A bigger budget, maximising items bought.

### The translation drill

Turn each optimisation phrase into a `works(x) -> bool` sentence, out loud, in one line each:

1. "Minimise the largest part sum over k contiguous parts."
2. "Maximise the smallest distance between c placed items."
3. "Minimise the maximum products any of n stores handles."
4. "Maximise the smallest piece when cutting into k+1 pieces."
5. "Minimise the number of days to finish, given a fixed daily rate."

Then say which of the five has a check that needs its input sorted first, and why the others do not.

### The greedy-proof drill

Say the exchange argument out loud, in under ninety seconds, for the contiguous-split check: why is
filling each part as full as possible optimal? Then answer the harder half — what exactly breaks when
the parts no longer have to be contiguous, and what is the honest thing to say to an interviewer at
that point?

### The hang drill

Write the mirrored maximise template with `mid = (lo + hi) // 2` and run it. Kill it with Ctrl-C and
read the traceback. Then fix it with the ceiling midpoint. Then delete both and write the
first-False-minus-one version instead, and say why that is the one to keep.

### The switch-removal drill

Take this and refactor it out loud in four minutes:

```python
def notify(user, message, channel):
    if channel == "email":
        smtp.send(user.email, message)
    elif channel == "sms":
        gateway.post(user.phone, message)
    elif channel == "push":
        fcm.push(user.device_token, message)
    else:
        raise ValueError(channel)
```

1. Run the six-step recipe from the lesson, naming each step as you do it.
2. Name the question the switch is answering — that becomes the method name.
3. Say what step six is and why skipping it means the switch comes back next year.
4. Count the edits to add WhatsApp, both ways.
5. Say the one cost you have accepted by refactoring.
6. Then answer the pushback: *"isn't that the same amount of code, just spread out?"*

### The is-it-polymorphism drill

For each, say whether polymorphism is the right tool, or whether an `if` should stay — with the
reason:

1. Four vehicle types, branched on in three separate functions.
2. `if amount > 10000: require_approval()`.
3. Seven days of the week, each with a different opening time.
4. Three payment gateways, with a fourth expected next quarter.
5. `if order.status == "CANCELLED": return`.
6. Two export formats today, and the product manager keeps asking for more.

---

## Build these, in all three languages

*Three exercises, easiest first. Each one says what it is really testing. Every
exercise is done three times: once in Python, once in Go, once in C++.*

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Same port, five times | Whether you can see connection reuse in a server log instead of trusting the library. |
| 2 | Retry a flaky endpoint | Telling a 500 from a timeout, and knowing which requests are safe to repeat. |
| 3 | A tiny command-line client | Mapping the three outcomes, dead line, server said no, and success, onto exit codes. |

All three exercises, and all three lessons, talk to the same local server. Save it as
`fixture.py` and run `python fixture.py` in a separate terminal; stop it with Ctrl-C. It prints
one line per request with the port the request came from, and that port is how every exercise
below is checked.

```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import time

USERS = {1: {"id": 1, "name": "Meera", "city": "Pune"}}
FLAKY_CALLS = 0


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # keep-alive, so a reused connection stays open

    def reply(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        port = self.connection.getpeername()[1]
        print(f"GET  {self.path} from port {port}", flush=True)
        if self.path == "/slow":
            time.sleep(3)
            self.reply(200, {"ok": True})
        elif self.path == "/fail":
            self.reply(500, {"error": "database down"})
        elif self.path == "/flaky":
            global FLAKY_CALLS
            FLAKY_CALLS += 1
            if FLAKY_CALLS % 3:
                self.reply(500, {"error": "try again", "call": FLAKY_CALLS})
            else:
                self.reply(200, {"ok": True, "call": FLAKY_CALLS})
        elif self.path == "/whoami":
            self.reply(200, {"headers": dict(self.headers)})
        elif self.path.startswith("/users/"):
            user = USERS.get(int(self.path.rsplit("/", 1)[1]))
            if user:
                self.reply(200, user)
            else:
                self.reply(404, {"error": "no such user"})
        else:
            self.reply(404, {"error": "no such path"})

    def do_POST(self) -> None:
        port = self.connection.getpeername()[1]
        print(f"POST {self.path} from port {port}", flush=True)
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        if self.headers.get("Content-Type") != "application/json":
            self.reply(415, {"error": "send application/json"})
            return
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self.reply(400, {"error": "body is not JSON"})
            return
        new_id = max(USERS) + 1
        USERS[new_id] = {"id": new_id, **data}
        self.reply(201, USERS[new_id])

    def log_message(self, format: str, *args: object) -> None:
        pass


if __name__ == "__main__":
    print("fixture listening on 127.0.0.1:8090", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8090), Handler).serve_forever()
```

Routes: `GET /users/1` answers 200 with a user, `GET /users/99` answers 404, `POST /users` with a
JSON body answers 201 and a 415 without the right `Content-Type`, `GET /fail` is always 500,
`GET /slow` waits three seconds, `GET /flaky` answers 500 twice and then 200, repeating, and
`GET /whoami` echoes your request headers back so you can see what you actually sent.

### 1. Same port, five times

Write a program that calls `GET /users/1` five times through one client, then five times through
the per-request function or a fresh client each time: `httpx.get` in Python, `(&http.Client{}).Get`
with the body never read in Go, `cpr::Get` in C++. Copy the ten fixture lines into a comment at
the top of the program: the first five must show one port, the last five must show five. Then
call `/whoami` once through the shared client and confirm your `User-Agent` and `Accept` headers
arrive. Done means the comment is in the file and the headers echo back.

### 2. Retry a flaky endpoint

Write `get_with_retry(client, path, attempts)` that calls `GET path` and retries on a 5xx status
or on a timeout, waiting 100 milliseconds, then 200, then 400 between attempts. It must not retry
on a 4xx, and it must not exist for POST: write the one-sentence comment that says why a POST that
creates a user cannot be retried the same way. Run it against `/flaky` and print each attempt's
status; the third attempt must succeed, and the `call` field in the body proves the fixture saw
three requests. Run it against `/slow` with a two-second timeout and one attempt; it must give up
without a traceback in Python, a panic in Go, or `status 0` in C++. Run it against `/users/99` and
prove it did not retry. Done means all three runs are pasted into a comment and the ports in the
fixture log are the same across every retry.

### 3. A tiny command-line client

Build `client`, a program run as `client get /users/1` or `client post /users Arjun Delhi`, with
an optional `--timeout 2` argument, using the argument handling from
[day 15](../day-015-the-write-pointer/README.md). It prints the status line and the body, pretty
printed with the JSON library from [day 40](../day-040-2d-prefix-sums/README.md), and exits with
0 for a 2xx, 1 for any other status, and 2 for a dead line, with a one-line reason on standard
error for the last two. Test all six: `get /users/1`, `get /users/99`, `post /users Arjun Delhi`,
`get /fail`, `get /slow --timeout 1`, and any path with the fixture stopped. Done means the six
exit codes are correct in all three languages and the `--timeout` flag is honoured.

## Compare

*One sentence per language: what was easiest, what was hardest, and why.*

- **Python** — `httpx.Client` in a `with` block did the pooling and the body reading for you, and the only thing you had to remember was `raise_for_status`, because a 500 is not an exception until you ask.
- **Go** — the client and its transport pooled connections for free, but exercise 1 only showed one port once you read and closed every body, and exercise 2 needed `errors.As` on `*url.Error` to tell a timeout from a refused connection.
- **C++** — `cpr::Session` made the calls as short as Python's, and every mistake in exercises 2 and 3 came from checking `status_code` before `r.error`, because nothing throws and a timeout looks like status zero.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Split the array into k parts, minimising the largest part sum.*
   The direction question, the decision restatement, the range with reasons, the greedy check, the
   exchange argument, and the DP you are choosing not to write, with numbers.

2. *What is polymorphism? Show me, do not tell me.*
   Write the switch, say what is wrong with it, write the polymorphic version, count the edits both
   ways, and name the cost you accepted.

3. *Maximise the minimum gap. How do you do it without writing a second template?*
   Negate the question, search the first False with `hi + 1`, subtract one — and say what goes wrong
   with the mirrored version if the midpoint does not round up.

### Languages

*Three questions from today. Answer each in two minutes, standing up, no notes.*

1. What goes wrong if you create a new HTTP client for every request?
   The handshake per call, with the round-trip arithmetic, the leaked connections, and the
   one-client-per-process fix; then the Go-specific half, that reuse depends on closing the body.
2. The downstream service returns a 500. What does your code see in each language, and what does
   it do next?
   A normal response in all three, `err == nil` in Go and `r.error` clear in C++; the status check
   that has to be yours; and the retry rule, with why a POST is different from a GET.
3. How do you tell a timeout from a connection refused, and why does it matter?
   `ReadTimeout` against `ConnectError`, `Client.Timeout exceeded while awaiting headers` against
   `connection refused`, `OPERATION_TIMEDOUT` against `CONNECTION_FAILURE`; one means the server
   is slow, the other means it is gone, and you retry them differently.

## Before you move on

- [ ] I asked the direction question before writing code on all four problems.
- [ ] I wrote the DP for LeetCode 410, timed it against the binary search, and can quote the ratio.
- [ ] I broke the placement problem both ways — unsorted input, and the wrong direction — and can tell
      the two failures apart.
- [ ] I made the mirrored template hang, read the traceback, and then chose the version that cannot.
- [ ] I ran the switch-removal recipe on the notifier, including step six.
- [ ] I can sort all six cases into "polymorphism" and "leave the `if`" with a reason each.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] The three lesson programs run against the fixture and print one port for five requests.
- [ ] Exercise 1 shows one port and then five ports in all three languages, and my headers echo back from `/whoami`.
- [ ] Exercise 2 succeeds on the third attempt against `/flaky`, gives up cleanly on `/slow`, and does not retry a 404.
- [ ] Exercise 3 returns the six correct exit codes in all three languages.
- [ ] I can say, without looking, how each language reports a dead line, and that none of them reports a 500 without being asked.
