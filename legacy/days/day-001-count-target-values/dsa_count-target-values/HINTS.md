# Hints — Count target values

Read [the topic explanation](CONCEPTS.md) before practice. These are extra prompts for applying
the lesson after an independent attempt, not a substitute for receiving the explanation first.

<details><summary>Hint 1 — representation</summary>

Trace a match, a non-match, and a second match. Is your saved count still describing all
processed elements, or only the most recent element?

</details>

<details><summary>Hint 2 — proof obligation</summary>

If you return from inside the loop, explain how you know what the unread elements contain.
Try a two-element input with a match only at the end. Then check the empty-input path.

</details>

<details><summary>Hint 3 — targeted debugging</summary>

Find the first item where your count differs from a hand trace. Check whether you reset on a
non-match, skipped the last item, or counted unique values instead of occurrences. Independently
check that reading the input did not change it. Correct output alone does not prove preservation.

</details>
