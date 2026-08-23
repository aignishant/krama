---
id: XXX-NN
day: N
section: S
subtopic: T
title: <the idea, as a noun phrase>
requires: [<prior IDs>]
---

# S.T — <Title>

## 1. The one-line answer

<One sentence. No term defined later in this document.>

## 2. The story

<A scene. 200–500 words. A person, a place, a constraint, a cost of being wrong.
No jargon. No code. No variables. The mechanics of the idea are present but unnamed.>

## 3. The idea in plain language

<The story, renamed. Every term introduced by pointing at something the story established.>

> **Formally:** <the idea, stated precisely, in one indented block.>

## 4. Where this actually shows up

- **<Named system 1>** — <what it does with this idea, specifically.>
- **<Named system 2>** — <same.>
- **Asked as:** <how an interviewer disguises it.>

## 5. The mechanism

<Diagram — Mermaid for structure, ASCII for memory/arrays. Captioned.>

**The invariant:** <what is true before every step and after every step.>

<A trace of one small concrete input, state shown at each step.>

## 6. Line by line

```python
<fragment, ≤10 lines>
```

<Why this line and not the obvious alternative.>

```python
<next fragment>
```

<…>

**The near-miss.** <The version that looks right, and the exact input that kills it.>

## 7. The cost, derived

**Technique:** <summation | recurrence | accounting | potential | expectation>

<The working. Show it.>

| Case | Cost | The input that causes it |
|---|---|---|
| Best | | |
| Average | | |
| Worst | | |

**Space:** <auxiliary vs total; recursion stack counted.>

**What the constant hides:** <cache, allocation, comparison cost, interpreter overhead.>

## 8. When it breaks

```
<the real, pasted error text or the exact wrong output>
```

<What caused it. Then the fix, and why the fix is not just a patch.>

## 9. In production

**At scale.** <n = 10⁹, on disk, concurrent, distributed. Locality. Memory. Tail latency.>

**What a senior reviewer says.**

> "<verbatim review comment>"

**What an interviewer probes.**

1. <question> — *checking: <what>*
2. <question> — *checking: <what>*
3. <question> — *checking: <what>*

## 10. Check yourself

1. <easiest>
   <details><summary>answer</summary>

   <answer>
   </details>

2. <…>

3. **Break it.** <Construct the input that defeats this.>
   <details><summary>answer</summary>

   <answer>
   </details>

4. **Connects to `<PRIOR-ID>`.** <How do these two relate?>
   <details><summary>answer</summary>

   <answer>
   </details>
