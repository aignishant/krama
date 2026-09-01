---
day: 180
track: practice
title: "Practice — The last week, and the questions you ask"
status: written
---

# Day 180 · Practice

**DSA topic:** Final revision, and the week before the interview
**System design topic:** Final revision, and the week before the interview

---

## Code these, in this order

**There are no new problems today, and that is deliberate.** **The last exercise in this course is the ten
templates, typed from memory, twice.**

| # | Template | What it must do without being derived | The line people get wrong |
|---|---|---|---|
| 1 | Binary search, lower bound | First position where the target could be inserted | `high = len(values)`, not `len - 1` |
| 2 | Sliding window with a constraint | Longest stretch with at most k distinct | deleting the key when its count hits zero |
| 3 | Two pointers on a sorted list | Three-sum with no duplicate answers | both skip lines |
| 4 | Monotonic stack | Largest rectangle in a histogram | the sentinel that flushes the stack |
| 5 | BFS on a grid | Fewest steps to the far corner | marking as seen on ENQUEUE |
| 6 | DFS on a tree | Diameter: return one value, record another | the two different numbers |
| 7 | Topological sort | An order, or empty if there is a cycle | `len(order) != n` as the cycle test |
| 8 | Union-Find | Connected components, near constant time | path halving, and union returning a bool |
| 9 | Heap for top-k | The k most frequent | a MIN-heap gives you the k LARGEST |
| 10 | Two-dimensional DP | Edit distance | `a[i-1]`, because row `i` is the first `i` characters |

### The rule

**Type them. Do not read them.** **Then run them against the examples in the lesson.** **Then do it again
tomorrow.** **Anything that takes more than ninety seconds, or comes out wrong, goes on a list — and that list
is what you revise on day five.**

### Then write your error list

**Go back through the last three months of your own solutions and find the bugs you actually made.** Not bugs
in general — **yours.**

```
   Ten lines. Something like:

   1. off-by-one in the window's right edge
   2. forgot the empty-input case
   3. marked BFS nodes as seen on dequeue
   4. did not ask about duplicates
   5. used `/` where I meant `//`
   6. did not bracket a shift
   7. started coding before stating the cost
   8. forgot to state complexity unprompted
   9. defended an idea after a hint
  10. did not test the case I was unsure about

   Twenty minutes to write. Three minutes to re-read on
   the morning. Nothing else in this course has that ratio.
```

### Then design one thing out loud, timed

**Forty-five minutes, a clock, nobody there.** **Pick a product you use.** Run the six beats. **Then read
somebody's written-up version and note only the things you did not think to ask** — not the things you got
differently, the things you did not think to ask.

### Then run through the low-level order once

Pick something small — a lift, a card game, a booking form. **Requirements as verbs, entities, relationships,
interface, the thing that will change.** **Then have somebody ask you to add a feature, and count how many
existing files you would have to edit.**

### Then recite the numbers sheet, cold

**Time, latency, throughput, sizes, availability, money.** **Out loud, without looking.** Then use two of them
to answer "do I need to shard?" in one sentence.

### Then write your two questions

**For the specific company.** **In your own words.** **Write them down where you will see them on the day.**

**And write your STAR notes** — two or three stories, in beats not sentences. **Situation, task, action,
result, learned.** **Test each one: were you actually wrong about something? Does it end with a habit?**

### Then the taper drill

**Say the seven-day plan from memory.** Then say what happens if the interview is in three days instead of
seven, and which items you drop first.

### Then stop

**That is the last exercise in this course.** **Everything after this point is the interview, and the most
useful thing you can do the day before is nothing.**

---

### The templates drill

1. Type all ten from memory. Time each one.
2. For each, say the line people get wrong.
3. Say why `lower_bound` is the binary search worth memorising.
4. Say what `union` returning a boolean is for.
5. Say why a min-heap gives you the k largest.

### The taper drill

1. Give the seven-day plan, day by day.
2. Say what the line at minus two days is, and why.
3. Say how long something new takes to become retrievable.
4. Say why tiredness is the only variable worth managing.
5. Say what to drop first if you only have three days.

### The revise-or-leave drill

1. Give six things to revise.
2. Give six things to leave alone.
3. Say which single item has the best ratio, and its numbers.
4. Say why other people's problem counts are worthless to you now.

### The night-before drill

1. Give the six things to sort out the night before.
2. Say what the actual objective of the evening is.
3. Say what a hard problem can do for you at that point.
4. Say what belongs on the one page you re-read.

### The on-the-day drill

1. Say what you do the morning of.
2. Give the reset between rounds, all four steps.
3. Say what one bad round means, and what turns it into three.
4. Say what to do within an hour of finishing, and why.

### The behavioural drill

1. Give the five beats of a STAR answer, with lengths.
2. Say which beat is the point of the question.
3. Give the two tests a story must pass.
4. Say what is wrong with "I worked all weekend and solved it".
5. Say why you learn the beats and never the sentences.

### The two-orders drill

1. Give both six-beat running orders.
2. Say the opening sentence for a design round.
3. Say what each round's closing checklist contains.
4. Say what happens if you run the wrong framework.

### The building-blocks drill

1. Name fifteen building blocks.
2. For any five, say what it is for, what it costs, and what happens when it dies.
3. Say what makes a feed design different from a video design, in terms of which blocks dominate.

### The trade-offs drill

For each pair, argue both directions in thirty seconds:

1. SQL / NoSQL
2. strong / eventual consistency
3. synchronous / asynchronous
4. normalise / denormalise
5. fan-out on write / on read
6. cache-aside / write-through
7. monolith / microservices
8. committed / on-demand capacity

### The numbers drill

1. Seconds in a day, and the number you round it to.
2. Four latency figures.
3. Four throughput figures.
4. Availability at four levels, in minutes.
5. Storage, egress and cross-zone prices.
6. The ratio between serving 30 TB and storing it.
7. Series against parallel, in one sentence.

### The questions drill

1. Give four questions to ask, one from each category.
2. Say what a specific answer to the paging question tells you.
3. Say what a vague one tells you.
4. Say what is wrong with "no, you've covered everything".
5. Say what you ask at the very end.

### The break-it drill

For each, say what happens:

1. Learning a new pattern three days before the interview.
2. A hard problem the night before.
3. Comparing your problem count with somebody else's.
4. Carrying a bad round into the next one.
5. Not writing down the questions afterwards.
6. A word-perfect rehearsed behavioural answer.
7. Reading case studies instead of designing out loud.
8. Running the high-level framework in a low-level round.
9. Answering "do you have any questions" with "no".

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Tell me about a problem you found hard, and what you learned from it.*
   Situation, task, action — with you being wrong in it — result with a number, and the habit you changed.
   Not the heroic version.

2. *What are you going to do in the seven days before your interview?*
   The day-by-day plan, the line at minus two days, what you revise and what you leave, and why tiredness is
   the only variable left.

3. *Do you have any questions for us?*
   Four questions from four categories, why each one is informative, and what you listen for in how they are
   answered.

---

## Before the interview

- [ ] I can type all ten templates from memory in under ninety seconds each.
- [ ] I know the line people get wrong in each of them.
- [ ] I have written my own error list — my bugs, not bugs in general.
- [ ] I know the seven-day plan and the rule at minus two days.
- [ ] I know nothing new goes in after that, and why.
- [ ] I know what to revise and what to leave alone.
- [ ] I will not do a hard problem the night before.
- [ ] The machine, the room, the link and the food are decided.
- [ ] I have the twenty patterns and their tells, cold.
- [ ] I have both design running orders, from memory.
- [ ] I can recite the numbers sheet without looking.
- [ ] I can argue all ten trade-off pairs in both directions.
- [ ] I can name fifteen building blocks and what each costs.
- [ ] I say which kind of design round I am in, in the first minute.
- [ ] I close every design with monitoring, SLO, security, cost, failure and one honest weakness.
- [ ] I have two or three STAR stories, as beats and not sentences.
- [ ] Each story has me being wrong in it, and ends with a habit.
- [ ] I have two questions written down for this specific company.
- [ ] I know what to listen for in how they answer.
- [ ] I will reset between rounds: stand up, one sentence, name the next round.
- [ ] I know one bad round is one round.
- [ ] I will write down every question within an hour of finishing.
- [ ] I answered all three questions above out loud.

---

## After day 180

**That is the course.**

**One hundred and eighty days, two tracks, and the last of them ends where the interview does — with you
asking the questions.**

**What you have is not a list of solved problems.** **It is twenty patterns you can recognise from a sentence,
ten templates that arrive without being derived, two running orders that hold under pressure, a page of
numbers that turn opinions into decisions, and the habit of saying what you are thinking while you think it.**

**None of that expires.** **Go and use it.**
