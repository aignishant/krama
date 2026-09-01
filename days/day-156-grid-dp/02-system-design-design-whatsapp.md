---
day: 156
track: system-design
title: "Design WhatsApp"
phase: "High-level design case studies"
status: written
---

# Design WhatsApp

## 1. What this is, and why they ask it

WhatsApp delivers a message from one person to another, quickly, reliably, and in order — **and it is a
completely different shape of system from everything else this week.**

Twitter and Instagram are read-heavy broadcast systems: one write, many reads, and staleness is invisible.
**Messaging is write-heavy and point-to-point.** Every message has exactly one or a few recipients, it must
arrive within a second, and **a message that arrives twice or out of order is something a human immediately
notices and complains about.**

They ask it because of three things that appear nowhere else in this course.

**Connections, not requests.** A phone must receive a message it did not ask for, so the server holds a
persistent connection to every online device. **A hundred million concurrent connections is a different
engineering problem from a hundred million requests a second** — it is bounded by memory and file descriptors
rather than by CPU.

**Ordering and delivery guarantees that users can see.** The two ticks, then the blue ticks, are a
user-visible acknowledgement protocol. **Nobody notices a stale tweet; everybody notices a message that
arrives out of order or twice.**

**And end-to-end encryption, which removes options.** If the server cannot read the messages, it cannot do
server-side search, cannot filter spam by content, and cannot re-encrypt for a new device. **Every one of those
becomes a client problem**, and knowing which capabilities encryption costs you is what separates a real answer
from a diagram.

By the end of this lesson you can design the connection layer, the message flow with acknowledgements, offline
delivery, group messaging, media, and encryption — and size all of it.

---

## 2. The story

There were two hundred and forty houses in the village and one telephone, and it was in Rukmini's front room
because that is where the line had reached in 1987.

**And the job that came with it, which nobody had asked her to take on, was that she was the delivery.**

The phone would ring. It would be somebody's son from Dubai, or a hospital in the town, or a man about a
tractor. And whoever it was for was not in her front room.

**So there was a system, and it grew one problem at a time.**

**The first thing was that she wrote it down.** Not the whole conversation — a name, who it was from, and what
they said in a line. Because the boy she sent to fetch people took eleven minutes and the caller would not
wait.

**The second thing was the boy.** He went, he found them, they came. And on the days he could not find them —
they were in the fields, they were at the market — **the note stayed on the shelf until they came past.**

**The third thing was the shelf itself**, which she divided with chalk lines into sections, one per household
that got calls regularly, so a note never went to the wrong family.

**The fourth thing took a year and it was because of a specific argument.**

A woman came in furious because her brother had said he had telephoned twice about the date of a wedding and
she had only heard once. Rukmini had no way to say whether that was true. **The note was gone from the shelf,
which meant somebody had taken it, and that was all she knew.**

So she started making the person sign.

**A line in a book: the note, the date, and their mark when they took it.** And after a while she added a
second thing, which was whether they had actually read it out to her, **because taking the note and reading
the note turned out to be different events**, and the difference was where the arguments lived.

And the last part, which she never wrote down anywhere, was this. **She could hear every conversation, and
everybody knew it, and so there were things people did not say on that telephone.**

They wrote letters instead, and the letters were sealed. **Rukmini carried them, and had no idea what was in
them, and could not have told you even if she had wanted to.**

---

## 3. The idea in plain English

Rukmini built a messaging system, including the acknowledgement book and the sealed letters, and her shelf is
the offline queue.

**Start with why this is not a request-response system.**

**A message arrives for you when the sender sends it, not when you ask.** So the server must be able to push,
which means **a persistent connection held open per online device.**

```
HTTP polling         "anything for me?" every 5 s
                     -> up to 5 s of latency, and 99% of requests
                        return nothing. Wasteful and slow.
long polling         hold the request open until something arrives
                     -> better, and still one request per message
WEBSOCKET            one connection, bidirectional, stays open
                     -> the standard answer
```

**WebSockets are the design**, and the consequence is the interesting part: **your servers now hold state.**
A stateless web tier can be load-balanced anywhere; **a connection server owns specific users for the duration
of their session**, and something has to know which server holds which user.

**That something is a connection registry**: `user_id → server_id`, in Redis, updated when a device connects
and disconnects. **Every message delivery starts with a lookup in it.**

**Now the message flow, which is Rukmini's book.**

```
1. Alice's phone sends the message over her WebSocket
2. the server assigns an id, persists it, and ACKs to Alice   -> ONE TICK
3. the server looks up Bob in the registry
4a. Bob is online   -> push over his WebSocket
4b. Bob is offline  -> store in his offline queue
5. Bob's device acknowledges receipt                          -> TWO TICKS
6. Bob opens the chat; his device sends a read receipt        -> BLUE TICKS
```

**The three states are three separate events and they are genuinely distinct** — that is the argument the
woman had with Rukmini. **Sent** means the server has it. **Delivered** means the device has it. **Read** means
a human looked at it. **Conflating delivered and read is the classic error**, and the whole two-ticks-versus-
blue-ticks design exists because they are not the same.

**Persist before acknowledging.** If the server ACKs and then crashes before writing, the message is gone and
the sender believes it was sent. **Write first, ACK second** — the order is the guarantee.

**Then: offline delivery, which is the shelf.**

A message for an offline user goes into a per-user queue, ordered, and is delivered when they reconnect.
**WhatsApp's specific choice is that the queue is deleted once delivered** — the server stores messages only
until delivery, not forever. **That is a storage decision with a privacy justification, and it is worth saying
out loud** because it makes the storage numbers dramatically smaller than people assume.

**And it means the phone is the archive**, which is why restoring a WhatsApp backup is a thing users have to
do.

**Now ordering and duplicates, which is where messaging is unforgiving.**

**Ordering within a conversation is what matters**, not global ordering. Two messages in different chats can
arrive in any order and nobody cares. **Two messages in the same chat arriving reversed is a visible bug.**

**So: a per-conversation sequence number.** The client sends messages with increasing sequence numbers, the
server preserves them, and the receiving client can detect a gap and request a resend. **A global ordering
would need coordination across the whole system and buys nothing.**

**Duplicates come from retries.** The network drops an acknowledgement, the client resends, and the server
sees the same message twice. **A client-generated message id makes the send idempotent** — the server keeps
recent ids and drops repeats. **The id must come from the client**, because a server-generated one is
different on each attempt.

**Groups, which are fan-out again but bounded.**

A group message is delivered to every member. **WhatsApp caps groups at around a thousand members**, which is
what makes this tractable: **a thousand deliveries is a bounded fan-out, not a celebrity problem.** Twitter has
to invent a hybrid because followers are unbounded; here the product simply forbids it.

**The interesting part is that the sender's device does the work under encryption.** With end-to-end
encryption there is no group key the server holds, so the sender encrypts the message once per recipient
device — **a thousand members with two devices each is two thousand encryptions on a phone.** The Signal
protocol's sender-key optimisation reduces this to one encryption plus a distributed group key, which is
exactly why it exists.

**Media, which is Instagram's problem again but smaller.**

**The message carries a reference, not the bytes.** The sender uploads the encrypted blob to storage, and the
message contains the URL and the decryption key. **The recipient downloads and decrypts.**

**And the deduplication is worth knowing**: the same forwarded video is uploaded once and referenced many
times, keyed by a hash of the content. **That is why forwarding a large video is instant.**

**Finally, encryption, and what it costs you.**

**End-to-end means the server holds ciphertext it cannot read.** Keys live on devices; the server distributes
public keys and nothing else.

**And the costs are real and worth naming:**

```
no server-side search           search must run on the device, over local data
no server-side spam filtering   you can only use metadata: who, how often,
                                how many recipients — not what
no multi-device without work    each device needs its own keys; adding one
                                cannot be done by the server re-encrypting
no server-side backup           a backup is either unencrypted, or encrypted
                                with a key only the user has — and then a
                                lost key is lost history
```

**Naming those trade-offs is the answer to "how does encryption affect the design".** The protocol details —
Double Ratchet, X3DH — are worth a sentence and not more.

---

## 4. The picture

The connection layer, and why it is stateful:

```
   phones                    connection servers            registry
                                                        (Redis)
  [Alice] ====WS=========> [ conn-server-7 ]
  [Bob]   ====WS=========> [ conn-server-2 ]      alice -> conn-server-7
  [Carol] ====WS=========> [ conn-server-7 ]      bob   -> conn-server-2
  [Dev]   (offline)                               carol -> conn-server-7
                                                  dev   -> (absent)

  Every delivery starts with a registry lookup.
  A stateless web tier can be load-balanced anywhere;
  a CONNECTION server owns specific users until they disconnect.

  100,000,000 concurrent connections is a MEMORY and FILE-DESCRIPTOR
  problem, not a CPU one.
```

The message flow and the three ticks:

```
  Alice                server                 Bob

    |---- send -------->|
    |                   | persist FIRST
    |<--- ack (id) -----|                          ONE TICK  (sent)
    |                   |
    |                   |---- lookup Bob ---->  registry
    |                   |
    |                   |======= push ========>|
    |                   |<------ ack ----------|
    |<--- delivered ----|                          TWO TICKS (delivered)
    |                   |
    |                   |<---- read receipt ---|   (Bob opened the chat)
    |<--- read ---------|                          BLUE TICKS (read)

  PERSIST BEFORE ACK. If the server acks then crashes, the message is
  gone and the sender believes it was sent.

  DELIVERED and READ are different events. Conflating them is the
  classic mistake, and the whole tick design exists because they differ.
```

Offline delivery, which is Rukmini's shelf:

```
  Bob is offline

  message -> [ offline queue: bob ]  ordered, persisted
                    |
             Bob reconnects
                    |
                    v
             deliver in order, wait for acks
                    |
                    v
             DELETE from the queue

  WhatsApp stores messages only until delivery, not forever.
  -> the phone is the archive
  -> the server's storage is tiny compared with a social product
  -> and restoring a backup is a thing users must do
```

Ordering: per-conversation, not global:

```
  conversation alice<->bob:   seq 1, 2, 3, 4 ...
  conversation alice<->carol: seq 1, 2, 3 ...

  These two are INDEPENDENT. Nobody notices if a message to Carol
  arrives before an earlier one to Bob.

  Within one conversation, out-of-order is IMMEDIATELY VISIBLE:

     "yes"                    "what time?"
     "what time?"    vs       "yes"
     -> nonsense               -> fine

  A gap in the sequence lets the receiving client detect loss and
  ask for a resend. Global ordering would need cluster-wide
  coordination and buys nothing.
```

Groups, and why the cap matters:

```
  GROUP of 1,000 members

  server-side fan-out: 1,000 registry lookups + 1,000 pushes
                       BOUNDED, because the product caps group size

  Twitter cannot cap followers, so it needs a hybrid.
  WhatsApp caps groups, so it does not. The product decision
  removed an entire class of engineering problem.

  UNDER ENCRYPTION, though, the sender does the work:
     1,000 members x ~2 devices = 2,000 separate encryptions
     ON A PHONE, before the message is even sent

  -> the Signal "sender key" optimisation: encrypt ONCE with a group
     key, distribute that key pairwise. 2,000 encryptions -> 1,
     plus a one-off key distribution.
```

What encryption takes away:

```
  the server holds ciphertext and cannot read it. Therefore:

  server-side search        IMPOSSIBLE -> search on the device only
  content spam filtering    IMPOSSIBLE -> metadata only: who, how often,
                                          how many recipients, how fast
  server-side backup        IMPOSSIBLE without a user-held key
                            -> lose the key, lose the history
  adding a new device       the server cannot re-encrypt for it
                            -> device-to-device key transfer, or
                               per-device keys and N-way encryption

  These are the answer to "how does E2E affect the design".
  The protocol names are one sentence; the LOST CAPABILITIES are
  the substance.
```

---

## 5. How it actually works

### The connection registry

```python
def on_connect(user_id: int, device_id: str, server_id: str) -> None:
    redis.hset(f"conn:{user_id}", device_id, server_id)
    redis.expire(f"conn:{user_id}", 300)       # heartbeats refresh it
    deliver_queued(user_id, device_id)         # drain the offline queue

def on_disconnect(user_id: int, device_id: str) -> None:
    redis.hdel(f"conn:{user_id}", device_id)
```

**A hash per user, not a single value**, because one user has several devices — phone, laptop, tablet — and
each needs its own entry. **A message goes to all of them.**

**The `expire` matters**, because disconnects are not always clean: a phone that loses signal never sends a
disconnect, and without a TTL the registry fills with entries pointing at connections that no longer exist.
**Heartbeats refresh it; silence lets it lapse.**

### Sending a message

```python
def handle_send(sender_id: int, msg: dict) -> dict:
    client_id = msg["client_message_id"]       # CLIENT-generated: idempotency
    if existing := message_store.by_client_id(sender_id, client_id):
        return {"id": existing.id, "duplicate": True}    # a retry, not a new one

    message = message_store.create(
        id=snowflake.next_id(),
        conversation_id=msg["conversation_id"],
        sequence=next_sequence(msg["conversation_id"]),
        sender_id=sender_id,
        ciphertext=msg["ciphertext"],          # the server never sees plaintext
        created_at=time.time(),
    )
    ack(sender_id, message.id)                 # ONE TICK — after persisting
    route(message)
    return {"id": message.id}
```

**The `client_message_id` check is the idempotency**, and it must be the client's id: **a retry after a lost
acknowledgement carries the same client id, while a server-generated id would differ on every attempt.** That
is the same rule as [day 122](../day-122-autocomplete/README.md)'s idempotency keys.

**`ack` comes after `message_store.create`.** Reverse them and a crash between the two loses a message the
sender believes was delivered — **and the sender will never retry, because it saw the tick.**

### Routing

```python
def route(message) -> None:
    for recipient_id in conversation.members(message.conversation_id):
        if recipient_id == message.sender_id:
            continue
        devices = redis.hgetall(f"conn:{recipient_id}")
        if devices:
            for device_id, server_id in devices.items():
                push_to_server(server_id, device_id, message)
        else:
            offline_queue.push(recipient_id, message)     # the shelf
```

**A message goes to every device of every recipient**, which is why the registry is a hash. **And a user with
one device online and one offline needs both paths** — push to the connected one, queue for the other — so in
practice the check is per device rather than per user.

### Delivery acknowledgement

```python
def handle_delivery_ack(recipient_id: int, message_id: int) -> None:
    message_store.mark_delivered(message_id, recipient_id)
    offline_queue.remove(recipient_id, message_id)        # only NOW is it safe
    notify_sender(message_id, "delivered")                # TWO TICKS

def handle_read_receipt(recipient_id: int, message_id: int) -> None:
    message_store.mark_read(message_id, recipient_id)
    notify_sender(message_id, "read")                     # BLUE TICKS
```

**Removing from the queue only after the acknowledgement is the delivery guarantee.** Delete on push instead
and a message dropped by a flaky connection is gone forever. **The consequence is at-least-once — the message
can be pushed twice — which the client's id-based deduplication absorbs.**

**Two separate handlers because they are two separate events**, and read receipts can be turned off by the
user while delivery receipts cannot.

### The offline queue

```python
def push(user_id: int, message) -> None:
    redis.zadd(f"queue:{user_id}", {message.id: message.sequence})
    redis.expire(f"queue:{user_id}", 30 * 86400)          # 30-day give-up

def drain(user_id: int, device_id: str) -> None:
    for message_id in redis.zrange(f"queue:{user_id}", 0, -1):   # IN ORDER
        push_to_device(device_id, message_store.get(message_id))
```

**`zrange` on a sorted set scored by sequence delivers in order**, which is the whole reason for the
structure.

**The 30-day expiry is the give-up point.** A user who never comes back does not accumulate messages forever
— **and the sender is told the message was never delivered, which is more honest than an unbounded queue.**

### Groups

```python
MAX_GROUP = 1024

def send_to_group(sender_id: int, group_id: int, ciphertexts: dict) -> None:
    members = group_store.members(group_id)               # <= 1024, bounded
    for member_id in members:
        if member_id == sender_id:
            continue
        for device_id in device_store.devices(member_id):
            route_one(device_id, ciphertexts[device_id])  # per-device ciphertext
```

**`ciphertexts` is keyed per device**, because under end-to-end encryption the sender encrypted separately for
each one. **The server is a router that cannot read anything it routes.**

**The cap is what makes this simple**, and it is a product decision doing the work of an architecture: **a
thousand deliveries is a loop, not a fan-out system.**

### Media

```python
def send_media(sender_id: int, conversation_id: int, blob: bytes) -> dict:
    key = secrets.token_bytes(32)
    ciphertext = aes_gcm_encrypt(blob, key)
    content_hash = hashlib.sha256(ciphertext).hexdigest()

    if not blob_store.exists(content_hash):               # forwarding is free
        blob_store.put(content_hash, ciphertext)

    return {"url": f"/media/{content_hash}",
            "key": key}                                   # sent INSIDE the message
```

**The decryption key travels inside the end-to-end encrypted message**, so the server stores a blob it cannot
decrypt and has no way to obtain the key.

**And the content hash gives free deduplication of forwards** — the same viral video is stored once however
many times it is forwarded, which is why forwarding a 30 MB video is instant. **Note it is the hash of the
*ciphertext*, so this only works when the same key is reused for a forward**, which is exactly what
"forwarding" means as opposed to re-uploading.

### Presence, which is deceptively expensive

```python
def on_heartbeat(user_id: int) -> None:
    redis.set(f"last_seen:{user_id}", time.time(), ex=60)
    for watcher in presence_subscriptions(user_id):       # who has this chat open
        push_presence(watcher, user_id, "online")
```

**Presence is the most expensive small feature in the system**, because it changes constantly and fans out to
everyone currently looking at that chat. **The mitigation is to send presence only to users with the
conversation open**, not to every contact — and to throttle updates to at most one every few seconds.

### The real systems

```
Erlang / BEAM     WhatsApp's original stack — built for millions of
                  lightweight processes, one per connection
ejabberd          the XMPP server WhatsApp forked
Signal Protocol   X3DH for key agreement, Double Ratchet for forward secrecy
Mnesia            Erlang's built-in store, used for routing state
FreeBSD           WhatsApp famously ran ~2M connections on ONE machine
```

**That last figure is the good one to cite**: WhatsApp demonstrated two million concurrent connections on a
single server in 2012, which reframes the whole problem — **a hundred million connections is dozens of
machines, not thousands.**

---

## 6. The numbers

**Traffic.**

```
2,000,000,000 users
500,000,000 concurrent at peak
100,000,000,000 messages/day

100e9 / 86,400 = ~1,160,000 messages/second average
peak ~3x       = ~3,500,000 messages/second
```

**A million messages a second is a genuinely large write rate**, and it is the opposite of the social products:
**write-heavy, tiny payloads, point-to-point.**

**Connections, which is the real constraint.**

```
500,000,000 concurrent WebSocket connections

per connection: ~10 KB of kernel and application memory (tuned)
                a naive stack uses 50-100 KB

500,000,000 x 10 KB = 5 TB of RAM across the fleet

at 128 GB per machine, ~40 GB usable for connections:
  -> 4,000,000 connections per machine (aggressive, WhatsApp-style)
  -> ~125 machines

at a more typical 500,000 per machine:
  -> 1,000 machines
```

**The spread between those two numbers is the entire engineering story of the connection tier**, and it is why
WhatsApp used Erlang: **the per-connection overhead is the design.**

**Message size and bandwidth.**

```
average text message: ~200 bytes of ciphertext + ~100 bytes of metadata

1,160,000 msg/s x 300 B = 348 MB/s = ~2.8 Gbps

compare Instagram: 350 Gbps

-> 125x less bandwidth for 40x more events.
   Messaging is about CONNECTIONS and LATENCY, not bytes.
```

**Storage, and this is where the design choice shows.**

```
IF messages were stored forever:
  100e9/day x 300 B = 30 TB/day = 11 PB/year
  x 3 replicas      = 33 PB/year

WhatsApp's actual model: store only until delivered
  ~95% of messages are delivered within seconds
  offline queue holds maybe 1% of a day's messages at any moment
  100e9 x 1% x 300 B = 300 GB
  plus a 30-day tail for long-offline users:  a few TB

-> the server-side storage is measured in TERABYTES, not petabytes.
   The phone is the archive.
```

**That contrast — 33 petabytes a year against a few terabytes — is the single best number in this
interview.**

**Media, which is the actual storage:**

```
~5,000,000,000 media messages/day, average 1 MB
  but heavily deduplicated by content hash (forwards)
  effective unique: maybe 20%

5e9 x 1 MB x 20% = 1 PB/day of unique media
retained 30 days = 30 PB

-> media is 10,000x the storage of the text messages.
   Same as Instagram: the bytes are all pictures.
```

**Latency budget.**

```
phone -> connection server (WebSocket, already open)   ~30 ms
persist + ack                                          ~5 ms
registry lookup                                        ~1 ms
push to the recipient's connection server              ~2 ms
connection server -> recipient's phone                 ~30 ms
                                                       -------
                                                       ~70 ms

users perceive under ~200 ms as instant, so there is real headroom
— and it is spent on mobile network variance, not on the servers.
```

**Groups.**

```
a 1,000-member group message:
  1,000 registry lookups (pipelined)     ~5 ms
  ~2,000 device pushes                   ~20 ms
  -> under 50 ms, bounded, no fan-out infrastructure

and UNDER ENCRYPTION, on the sender's phone:
  2,000 encryptions at ~1 ms each        = 2 SECONDS
  -> unusable

with sender keys:
  1 encryption + a one-off key distribution
  -> milliseconds
```

**That two-second figure is the concrete justification for sender keys**, and it is a better answer than
naming the protocol.

**Presence, which is surprisingly large:**

```
500,000,000 online users
each changes state (typing, online, last-seen) ~20 times/hour
  = 10,000,000,000 events/hour = ~2,800,000 events/second

if each fanned out to 100 contacts: 280,000,000 pushes/second
  -> LARGER than the message traffic itself

mitigation: send presence only to users with that chat OPEN
  ~1-2 watchers per user on average
  -> ~5,000,000 pushes/second. Manageable.
```

**Presence being bigger than messaging without that mitigation is the surprise**, and noticing it unprompted
is a strong signal.

**Cost, roughly:**

```
connection tier   ~500 machines           ~$500,000/month
message store     modest — TBs, not PBs   ~$50,000/month
media storage     30 PB + CDN egress      ~$1,500,000/month
                                          ------------------
                                          ~$2M/month for 2 billion users

= about $0.001 per user per month, which is why the product
  could be free with 50 engineers.
```

---

## 7. The trade-offs

**Stateful connections against a stateless tier.** WebSockets are the only reasonable way to push, and they
make the connection servers stateful: **a deploy disconnects everybody it holds, and a crash disconnects
theirs at once.** Reconnection storms are real, so clients need exponential backoff with jitter —
[day 125](../day-125-what-a-graph-is/README.md)'s thundering herd, caused by your own deploy.

**At-least-once against at-most-once.** Removing a message from the queue only after acknowledgement means a
message can be delivered twice; **deleting on push means a dropped connection loses it forever.** For
messaging, a duplicate the client can deduplicate is strictly better than a loss — **so at-least-once plus
client-side ids, always.**

**Per-conversation ordering against global ordering.** Per-conversation is cheap, is what users can perceive,
and lets each client detect gaps. **Global ordering would need cluster-wide coordination and would buy
nothing**, because nobody can observe the relative order of two different chats.

**Store-until-delivered against store-forever.** WhatsApp's choice makes server storage tiny and gives a
genuine privacy property — **there is no archive to subpoena.** The cost is that **the phone is the archive**,
so losing a phone loses history unless the user made a backup, and restoring is a user-visible chore. **A
product that stores server-side gets seamless multi-device and search, and gives up the privacy claim.**

**End-to-end encryption against every server-side feature.** It is the right default for a messenger, and the
costs are not small: **no server-side search, no content-based spam filtering, no server-side backup, and
multi-device becomes a real engineering problem** because the server cannot re-encrypt for a new device.
**Spam is fought on metadata alone** — who, how often, to how many, how fast — which works less well and is
the honest answer.

**Group size caps against unlimited groups.** Capping at about a thousand removes the celebrity problem
entirely: **a bounded fan-out is a loop.** Uncapped groups would need Twitter's hybrid and would break the
sender-side encryption cost even harder. **This is the clearest case in the course of a product decision
deleting an architecture problem**, and it is worth saying in those words.

**When would I not build this?** **When the product is a chat feature rather than a messenger** — support
chat, a game lobby, comments on a document — where a managed service or a simple long-polling endpoint over
the existing database is the entire thing. **When encryption is not required**, which removes most of the
difficulty and enables search and moderation. **And for anything small, a hosted service** — Twilio
Conversations, Stream, Sendbird — is cheaper than the connection tier alone.

---

## 8. In the interview

### How it gets asked

- *"Design WhatsApp."* — usually with a scale like a billion users.
- *"How does the server push a message to a phone?"* — the WebSocket question.
- *"How do the two ticks work?"* — the acknowledgement protocol.
- *"What happens if the recipient is offline?"*
- *"How does end-to-end encryption change the design?"* — the best question in the set.
- *"How do groups work?"*

### The first ninety seconds

> "This is a completely different shape from the last few systems, and I want to say why before designing
> anything.
>
> **Twitter and Instagram are read-heavy broadcast systems — one write, many reads, and staleness is
> invisible.** Messaging is **write-heavy and point-to-point**: every message has one or a few recipients, it
> must arrive in under a second, **and a duplicate or an out-of-order message is something a human
> immediately notices.**
>
> **Three things drive the design.**
>
> **First, the server must push.** A phone receives messages it did not ask for, so polling is wrong — five
> seconds of latency and ninety-nine percent of requests returning nothing. **WebSockets: one persistent
> connection per device.**
>
> **And the consequence is that my servers are now stateful.** A connection server owns specific users until
> they disconnect, so I need **a registry mapping user to connection server** — Redis, a hash per user because
> a user has several devices — and every delivery starts with a lookup in it.
>
> **Second, the guarantees are visible to users.** Sent, delivered, read are **three distinct events**, which
> is exactly what one tick, two ticks and blue ticks are. **Conflating delivered and read is the classic
> mistake** — the device having it and a human having read it are different, and the whole design exists
> because they differ.
>
> **And persist before acknowledging.** If I ack and then crash, the message is gone and the sender saw a tick,
> so it will never retry. **Write first, ack second, and the order is the guarantee.**
>
> **Third, end-to-end encryption, which removes options rather than adding components.** The server holds
> ciphertext, so there is **no server-side search, no content-based spam filtering, and no server-side
> backup** — and adding a new device is a real problem because the server cannot re-encrypt for it. **Those
> lost capabilities are the substance; the protocol names are one sentence.**
>
> **Scale, and one number reframes it.** A hundred billion messages a day is about a million a second — large.
> **But the payloads are three hundred bytes, so it is 2.8 gigabits a second, against Instagram's 350.**
> **This system is bounded by concurrent connections and latency, not by bytes** — five hundred million
> connections at about ten kilobytes each is five terabytes of RAM, and WhatsApp famously ran two million
> connections on one machine.
>
> **One question: do I need message history on the server, or is the phone the archive?** Because WhatsApp
> deletes after delivery, and that single choice is the difference between a few terabytes and thirty-three
> petabytes a year."

### The follow-ups

**"How do the ticks work, and what happens if the recipient is offline?"**

> "Three separate events with three separate acknowledgements, and the offline case is where the delivery
> guarantee lives.
>
> **One tick is 'the server has it'.** Alice's phone sends over its WebSocket, the server **persists the
> message and then acknowledges.** That order is not stylistic: **if I ack first and crash, the message is
> lost and Alice saw a tick, so her client will never retry.**
>
> **Two ticks is 'the recipient's device has it'.** The server looks Bob up in the registry, pushes over his
> connection, **and Bob's device sends back a delivery acknowledgement**, which the server relays to Alice.
>
> **Blue ticks is 'a human opened the chat'.** A separate event from the device, which is why users can turn
> read receipts off but not delivery receipts — **they are genuinely different facts.**
>
> **Now offline.** Bob is not in the registry, so the message goes into a **per-user offline queue** — a Redis
> sorted set scored by sequence number, so it drains in order — and Alice sees one tick and no more.
>
> **When Bob reconnects, the queue drains in order, and each message is removed only after his device
> acknowledges it.** That last part is the guarantee: **delete on push instead, and a message dropped by a
> flaky connection is gone forever.**
>
> **The consequence is at-least-once delivery** — a message can be pushed twice if an acknowledgement is lost —
> **which the client absorbs by deduplicating on the message id.** For messaging that is unambiguously the
> right trade: a duplicate the client can filter is much better than a loss the user notices.
>
> **And I would cap the queue at about thirty days.** A user who never returns should not accumulate messages
> forever, and **telling the sender it was never delivered is more honest than an unbounded queue.**
>
> **One more piece: if Bob is offline entirely, a push notification wakes the app** — through APNs or FCM,
> carrying no content because the server cannot read it, just a signal to connect and fetch."

**"How does end-to-end encryption change the design?"**

> "It changes almost nothing about the message flow and it removes four capabilities, and **the lost
> capabilities are the real answer** — the protocol names are a sentence.
>
> **The mechanics: keys live on devices. The server distributes public keys and routes ciphertext it cannot
> read.** Signal's protocol — X3DH to agree a key, Double Ratchet for forward secrecy so a compromised key
> does not expose past messages. **That is as much as I would say about the cryptography.**
>
> **What it costs, and each one is a product feature that has to move or die.**
>
> **No server-side search.** Searching your own chat history has to happen on the device, over locally stored
> data. **Which is fine for a phone and awkward for a new device with no history.**
>
> **No content-based spam filtering.** I cannot see what is being sent, **so abuse detection runs on metadata
> alone**: who is messaging whom, how often, how many distinct recipients, how fast a new account ramps up.
> **That works less well than reading the content, and it is the honest answer** rather than pretending
> encryption is free.
>
> **No server-side backup.** A backup is either unencrypted — which throws away the property — or encrypted
> with a key only the user holds, **and then losing the key loses the history permanently.** That is a real
> support burden and a real product decision.
>
> **And multi-device is genuinely hard.** The server cannot re-encrypt an old message for a new device, because
> it cannot read it. **So either the new device gets keys transferred from an existing one, or each device has
> its own identity and every message is encrypted separately per device.**
>
> **That last one is what makes groups expensive.** With per-device encryption, a thousand-member group with
> two devices each means **two thousand separate encryptions on the sender's phone before the message is even
> sent** — at about a millisecond each, that is two seconds, which is unusable.
>
> **Hence sender keys**: encrypt the message once with a group key, and distribute that group key pairwise,
> once. **Two thousand encryptions become one plus a one-off setup**, and that arithmetic is why the
> optimisation exists."

**"How do groups work?"**

> "Groups are fan-out, and the interesting part is that **a product decision deletes the hard version of the
> problem.**
>
> **WhatsApp caps groups at around a thousand members.** So a group message is a bounded loop: look up each
> member in the registry, push to each of their devices, queue for the offline ones. **A thousand deliveries
> is under fifty milliseconds and needs no fan-out infrastructure at all.**
>
> **Compare Twitter, which cannot cap followers** and therefore has to invent a hybrid push-pull design for
> celebrities. **Here the product simply forbids the case that would require it**, and I think that is worth
> saying explicitly, because recognising when a constraint can be imposed rather than engineered around is a
> real skill.
>
> **Where it does get expensive is encryption, on the sender's device.** With per-device keys, the sender
> encrypts separately for every recipient device — a thousand members with two devices each is two thousand
> encryptions, about two seconds on a phone. **Sender keys fix it: one encryption with a shared group key, and
> the key distributed pairwise once.**
>
> **Membership changes are the fiddly part under encryption.** When someone leaves a group, **the group key
> must be rotated**, or they could still decrypt future messages. When someone joins, they get the current key
> and **cannot read anything sent before** — which is a deliberate property, and a support question.
>
> **And a detail that matters at scale: I would store group membership separately from the message path**, and
> cache it aggressively, because every message triggers a membership read. **A group of a thousand active
> people generates a lot of reads of the same small list.**
>
> **One thing I would raise: the cap is doing more work than it looks.** If the product wanted broadcast
> channels with a million subscribers — which WhatsApp later added — **that is a different system**, closer to
> a feed, and I would build it separately rather than removing the group cap."

### The model answer

*"Design WhatsApp: two billion users, five hundred million concurrent, a hundred billion messages a day,
end-to-end encrypted."*

> "The constraints in that prompt point in an unusual direction, so let me name the shape first.
>
> **A hundred billion messages a day is about a million a second — write-heavy, which is the opposite of the
> social products.** But the payloads are three hundred bytes, so the total bandwidth is **2.8 gigabits a
> second, against Instagram's three hundred and fifty.** **This system is bounded by concurrent connections
> and by latency, not by bytes**, and that reframes what to optimise.
>
> **The connection tier, which is the hard part.** Five hundred million concurrent WebSockets. At about ten
> kilobytes per connection — kernel buffers plus application state, aggressively tuned — that is **five
> terabytes of RAM across the fleet.** WhatsApp demonstrated two million connections on one machine using
> Erlang, so **this is on the order of a few hundred machines, not thousands** — and the per-connection
> overhead is the entire engineering story of this tier.
>
> **A registry in Redis maps user to connection server**, a hash per user because a user has several devices.
> **With a TTL refreshed by heartbeats**, because a phone that loses signal never sends a clean disconnect and
> without expiry the registry fills with dead entries.
>
> **The message flow: persist, then ack, then route.** One tick after the write, two ticks after the device
> acknowledges, blue ticks after the human opens the chat — **three separate events, and conflating delivered
> with read is the classic error.**
>
> **Ordering is per conversation, not global** — a sequence number per conversation so a client can detect a
> gap and request a resend. **Global ordering would need cluster-wide coordination and nobody can perceive it.**
>
> **Idempotency on a client-generated message id**, because a retry after a lost ack carries the same id and a
> server-generated one would not.
>
> **Offline: a per-user sorted set, drained in order, and messages removed only after acknowledgement.**
> At-least-once, absorbed by client-side deduplication — **a duplicate is much better than a loss here.**
> Thirty-day expiry, and the sender is told when a message was never delivered.
>
> **Now the storage decision, which is the biggest number in the design.** If messages were kept forever, a
> hundred billion a day at three hundred bytes is **eleven petabytes a year, thirty-three with replicas.**
> **Storing only until delivery makes it a few terabytes** — because ninety-five percent are delivered within
> seconds. **Four orders of magnitude, from one product decision.**
>
> **The cost is that the phone is the archive**, so a lost phone loses history and restoring a backup is a
> user-visible chore. **I would state that as the deliberate trade it is**, along with its privacy benefit:
> there is no server-side archive to compel.
>
> **Media is where the actual storage is** — five billion media messages a day, deduplicated by content hash so
> forwarding a viral video stores nothing new — **about a petabyte a day of unique content, thirty petabytes
> retained.** Ten thousand times the text. **Same as Instagram: the bytes are all pictures.**
>
> **Encryption, and its costs.** Signal protocol, keys on devices, the server routes ciphertext. **No
> server-side search, no content-based spam filtering — abuse detection is metadata-only — no server-side
> backup without a user-held key, and multi-device requires per-device keys.** That last one makes groups
> expensive: **a thousand-member group at two devices each is two thousand encryptions on a phone, about two
> seconds**, hence sender keys.
>
> **Groups are capped at around a thousand**, which removes the celebrity fan-out problem entirely — **a
> bounded fan-out is a loop.** A product decision doing the work of an architecture.
>
> **Two things I would flag as risks.**
>
> **Deploys and reconnection storms.** A connection server going down disconnects everyone it holds, and they
> all reconnect at once. **Clients need exponential backoff with jitter**, and deploys need to drain slowly —
> otherwise my own release is a self-inflicted thundering herd.
>
> **And presence, which is bigger than messaging if built naively.** Five hundred million users changing state
> twenty times an hour is 2.8 million events a second, and **fanning each to a hundred contacts would be 280
> million pushes a second — larger than the message traffic itself.** **The mitigation is to send presence only
> to users with that chat currently open**, which takes it to about five million a second. **I would design
> that constraint in from the start rather than discover it.**"

---

## 9. Recall card

**Opposite shape from the social systems: write-heavy, point-to-point, latency-critical, and duplicates and
reordering are user-visible.** 100B messages/day is ~1M/s, but at 300 bytes that is **2.8 Gbps against
Instagram's 350** — **bounded by connections and latency, not bytes.**

**WebSockets, one per device, so the servers are STATEFUL.** A registry (`user → connection server`, a hash
per user for multiple devices, **with a heartbeat-refreshed TTL** because unclean disconnects are normal).
500M connections × ~10 KB = **5 TB of RAM**; WhatsApp ran 2M connections on one machine.

**Three distinct events: sent / delivered / read = one tick / two ticks / blue ticks.** **Persist BEFORE
acking** — ack-then-crash loses a message the sender believes was sent, and the client will never retry.
**Idempotency on a CLIENT-generated message id.** **Ordering is per conversation, not global.**

**Offline queue = a sorted set drained in order, and messages are removed only after acknowledgement** —
delete-on-push loses messages. At-least-once, absorbed by client-side dedup. 30-day give-up.

**Store-until-delivered is the biggest number in the design: 33 PB/year → a few TB.** The phone becomes the
archive. **Media is the real storage** (~1 PB/day unique after content-hash dedup, which is why forwarding is
instant).

**E2E encryption removes capabilities, and that is the answer:** no server-side search, **spam fought on
metadata only**, no server-side backup without a user-held key, and multi-device needs per-device keys —
which makes a 1,000-member group **2,000 encryptions ≈ 2 seconds on a phone**, hence **sender keys**.
**Groups are capped at ~1,000, which deletes the celebrity fan-out problem** — a product decision doing an
architecture's job. **And presence, built naively, is larger than the message traffic itself.**
