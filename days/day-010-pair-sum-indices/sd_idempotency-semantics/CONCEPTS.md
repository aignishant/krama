---
day: 10
part: "1.1"
title: "Give retries a durable operation identity"
ids: [SD-10]
level: working
prerequisites: ["HTTP methods", "Source of truth"]
failure: true
---

# Give retries a durable operation identity

Core: retry identity, replay/conflict decisions, and atomic storage. Cross-service effects and
retention sizing are optional depth. Complete one bounded request trace within the existing session.

## One-line answer

Treat a repeated operation key as the same logical request only when its payload matches, and commit its effect with its replay record.

## The story

A shop submits a new short link and sees a timeout. It cannot tell whether the service failed
before saving the link or merely lost the response. Clicking again should recover the original
result, while a genuinely new request should still create a new link.

## The idea in plain language

[HTTP method semantics](../../day-009-frequency-ranking/sd_http-methods/CONCEPTS.md) do not make
an ordinary POST safe to retry automatically. Give a logical create an identity chosen by its
client before the first send. Reuse that identity across network attempts, but not across distinct
business operations. A key created anew on each retry defeats deduplication.

The server stores a scoped key, normalized request payload, and completed response. Replaying
means returning the saved result without performing the create again. A conflict means the same
key names different requested work; silently replaying would claim to have accepted that work.
Recognize the need whenever an effect may occur before the caller receives acknowledgment.

## Why Krama needs it

[Timeout propagation](../../day-012-range-sums/sd_timeout-propagation/CONCEPTS.md) can stop waiting
without undoing committed work. Idempotency supplies a way to resolve that uncertain outcome.

## The source behind it

[HTTP Semantics, idempotent methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)
(`RFC 9110`, checked 2026-09-22) defines idempotency in terms of intended effect. The keyed
create protocol here is an application design, not a claim that the RFC standardizes this header.

## The mechanism

### Worked trace

Scope the key by authenticated owner and operation: `(owner, create-link, key)`.

| Stored state | Incoming request | Action |
| --- | --- | --- |
| Absent | Valid key and payload A | Atomically create link and save result for A |
| Completed for A | Same key, payload A | Replay stored status/body; no new effect |
| Completed for A | Same key, payload B | Reject conflict; preserve original result |
| Competing uncommitted claim | Same key | Wait within deadline or return declared retryable in-progress response |

Payload comparison uses an explicit normalization policy including all effect-changing fields.
Raw JSON whitespace is not a business difference; changing the destination is. Authentication
and authorization still run on replay. Do not allow a guessed key to disclose another owner's result.

A unique constraint on the scoped key arbitrates concurrent claims. The record and link creation
belong to one database transaction: either both commit or neither does. Otherwise a crash between
the two writes can leave an effect without a replay record, or a record without its promised effect.
This gives at most one committed local creation per scoped key during retention, not guaranteed
delivery and not exactly-once effects across independent services.

## When it breaks

This sequential toy checks identity and conflict decisions. It does not simulate a durable
transaction, concurrent requests, or process crashes.

```python
records = {}
effects = []

def create(key, payload):
    if key in records:
        old_payload, result = records[key]
        if old_payload != payload:
            raise ValueError("key reused with different payload")
        return result
    result = f"link-{len(effects) + 1}"
    effects.append(payload)
    records[key] = (payload, result)
    return result

print("same operation:", [create("A/create/k1", "url-a") for _ in range(3)])
print("committed effects in model:", len(effects))
try:
    create("A/create/k1", "url-b")
except ValueError as error:
    print(f"ValueError: {error}")
else:
    raise AssertionError("payload conflict was ignored")
assert len(effects) == 1
```

**Line by line:** the dictionary retains a normalized payload and result for each scoped key.
Lookup occurs before creating a new effect. A payload mismatch raises rather than replays.
The repeated calls model one attempt plus two retries. The list and dictionary updates are
separate Python writes and are deliberately not a production atomicity implementation.

Author verification on Python 3.12.10, 2026-09-22:

```text
same operation: ['link-1', 'link-1', 'link-1']
committed effects in model: 1
ValueError: key reused with different payload
```

## In production

Bound key size, scope, storage, and retention. If accepted logical creates arrive at rate r per
second and records live T seconds, roughly rT records remain before overhead and workload variation.
Deleting a replay record permits later reuse to create another effect; specify that boundary.
Keep sensitive results protected and decide whether stable failures are replayed or retried.

For a remote payment or message effect, one local transaction cannot atomically commit the remote
service. Carry a stable operation identity downstream or use an explicit reconciliation design.
A reviewer should ask about two simultaneous attempts and a crash after commit but before response,
not just the sequential retry demonstrated above.

## Check yourself

### Readiness before practice

1. Who chooses the key, and when must it remain unchanged?
2. Why is payload equality part of replay eligibility?
3. What goes wrong if effect and replay record commit separately?
4. What promise ends when the replay record expires?

Run the model, explain the crash boundary aloud, then use [the reference](REFERENCE_DESIGN.md)
before guided practice or after an independent [DESIGN.md](DESIGN.md) attempt.

[Navigation](README.md) · [Recall](../../../docs/SD_RECALL.md#day-010-idempotency-semantics)
