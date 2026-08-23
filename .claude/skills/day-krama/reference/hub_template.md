# Day N — <Title>

> <The question of the day, in one sentence, no jargon.>

**Owns:** `XXX-NN` · `XXX-NN`  |  **Phase P — <Phase title>**

## 1. The question of the day

<One paragraph. What you cannot do yet, and will be able to do by the end.>

## 2. The map

Read in this order.

| Part | Title | The idea | ID |
|---|---|---|---|
| [1.1](parts/01-<section-slug>/1.1-<slug>.md) | | | |
| [1.2](parts/01-<section-slug>/1.2-<slug>.md) | | | |
| [2.1](parts/02-<section-slug>/2.1-<slug>.md) | | | |

**Section 1** is about <the shared mental model>. **Section 2** is about <the other one>.

## 3. What you already have

| ID | From | Why it is needed today |
|---|---|---|
| `XXX-NN` | Day M | |

## 4. Setup

```bash
./k scaffold N
```

## 5. The build brief

Implement in `days/day-NN-<day-slug>/lab/implement.py`:

```python
def <name>(<args>) -> <ret>:
    """<one-line contract>

    Pre:   <preconditions>
    Post:  <postcondition / invariant on return>
    Time:  <required complexity>
    Space: <required complexity>
    """
```

**Forbidden today:** <imports and builtins that would do the work for you.>

Done when `pytest days/day-NN-<day-slug>/lab -q` is green and
`python days/day-NN-<day-slug>/lab/bench.py` shows the ratio column behaving the way
§7 of part <X.Y> says it must.

## 6. The problem ladder

**Warm-up** — fire the mechanism once.
- *<Title>* (<source>) — testing: <what>

**Core** — solve from an empty file, without re-reading the lesson.
- *<Title>* (<source>) — testing: <what>
- *<Title>* (<source>) — testing: <what>

**Stretch** — today's idea combined with `<PRIOR-ID>`.
- *<Title>* (<source>) — testing: <what>

**Interview** — narrate aloud before you type.
- *<Title>* (<source>) — testing: <what>

## 7. The gate

Before ticking the checklist, say these out loud, without notes:

1. <…>
2. <…>
3. <…>
