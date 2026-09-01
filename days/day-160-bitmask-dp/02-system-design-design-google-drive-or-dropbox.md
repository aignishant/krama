---
day: 160
track: system-design
title: "Design Google Drive or Dropbox"
phase: "High-level design case studies"
status: written
---

# Design Google Drive or Dropbox

## 1. What this is, and why they ask it

A file sync service keeps a folder on your laptop, your phone, your other laptop, and a server **all showing
the same thing** — and does it while you are editing files offline, on a bad connection, from two devices at
once.

They ask it because **it is the only design in this set where the difficulty is not scale.** The traffic is
modest. There is no fan-out problem, no celebrity, no thundering herd. **What makes it hard is correctness:
several devices editing the same data, going offline, and coming back with conflicting histories.**

Three things carry the interview.

**Chunking and deduplication.** A file is split into blocks, each identified by a hash of its contents. **Edit
one paragraph of a 50 MB document and you upload one 4 MB block, not 50 MB** — and the same block appearing in
a thousand users' accounts is stored once. Both of those are enormous wins and they come from the same idea.

**Sync, which is the real problem.** How does a client know what changed? **Polling every file is impossible;
the answer is a per-user monotonic version cursor**, and getting that right is most of the design.

**And conflicts, which cannot be avoided, only handled.** Two devices edit the same file while offline. There
is no correct merge for a binary file, **so the honest answer is to keep both and tell the user** — which
sounds like giving up and is actually the right design.

**Naming the difference between this and Instagram is a good opening move**: Instagram uploads are immutable
and write-once. **Here files change, repeatedly, from several places, and the system's job is to converge.**

By the end of this lesson you can design chunking and dedup, the sync protocol with its cursor, conflict
handling, sharing and permissions, and size the storage saving.

---

## 2. The story

The workshop made two kinds of steel door and the drawings lived in a green folder, and for eleven years the
green folder was the only copy.

**Which was fine, until the second workshop opened across town.**

Because now there were two green folders, and the drawings had to be the same in both, **and they were not.**

The first arrangement was that anyone changing a drawing sent the new sheet across by the boy on the scooter.
**It worked when there was one change a week.** By the time there were four a day, the boy was doing nothing
else, and Vasant — who had started the second workshop and cared about this more than anyone — began sending
the whole folder every Friday.

**Which was eleven kilograms of paper to change one measurement.**

His fix, which he was quite proud of, was the numbering.

**Every sheet got a number in the corner, and when a sheet changed, the number went up.** Then the boy carried
a list — sheet 14 is now version 9, sheet 22 is now version 3 — **and the other workshop only asked for the
sheets whose numbers had moved.**

**One list instead of eleven kilograms.**

Then two things happened that took another year.

**The first was that a sheet came back with the same number and different contents**, because two people had
edited version 8 in the two workshops on the same day. **Both had made version 9. They were different sheets.**

There was an argument, and then a rule, and the rule was the sensible one: **when that happened, both stayed.**
Sheet 22 version 9, and sheet 22 version 9 (Vasant's copy), and somebody had to look at them and decide. It
happened perhaps twice a month **and every single time it was somebody's judgement, not a procedure.**

**The second was the discovery that most of the sheets were the same as each other.**

The door frames differed. The hinge detail did not — **the same hinge detail was on ninety of the drawings**,
redrawn each time. Vasant's son, who was nineteen and had been given the filing to do, pointed out that they
could draw the hinge once, give it a number, and write *hinge as sheet 51* on the other ninety.

**Which they did, and the folder became a third of the weight.**

---

## 3. The idea in plain English

Vasant's numbering is the version cursor, his rule about both sheets staying is conflict handling, and his
son's hinge detail is deduplication.

**Start with the model, because the vocabulary matters.**

**A file is not stored as a file.** It is split into **chunks** — fixed or variable-size blocks, typically
around 4 MB — **and each chunk is identified by the hash of its contents.** The file itself becomes a small
piece of metadata: a name, a version, and an ordered list of chunk hashes.

```
report.pdf  v7  ->  [ a3f9..., 8c21..., a3f9..., 0b7e... ]
                       ^                ^
                    the SAME chunk appears twice — stored once
```

**Two enormous consequences fall out of that one decision.**

**One: you only upload what changed.** Edit a paragraph in the middle of a 50 MB file, and **only the chunks
containing that paragraph have new hashes.** The client computes the hashes, asks the server which ones it
already has, and uploads the handful that are new. **That is Vasant's list of changed sheets.**

**Two: identical chunks are stored once, across all users.** The same PDF sent to a thousand people is one
copy of each chunk on the server. **The saving in a corporate account is enormous** — everybody has the same
attachments, the same installers, the same shared documents.

**And there is a subtlety about fixed versus variable chunking that is worth knowing.**

**Fixed 4 MB boundaries break on insertion.** Add one byte at the start of a file and **every subsequent
boundary shifts**, so every chunk hash changes and you re-upload the whole file.

**Content-defined chunking fixes it.** Choose boundaries where a rolling hash of the last few dozen bytes
matches a pattern, so **the boundaries move with the content**. An insertion changes one chunk and leaves the
rest aligned. **Most production systems do this**, and knowing why is a real signal.

**Now sync, which is the actual design problem.**

**The question is: how does a client find out what changed?**

**Polling every file's timestamp is impossible** — a user with 100,000 files would issue 100,000 requests to
learn that nothing happened.

**The answer is a monotonic version cursor per user.** Every change to that user's files — create, edit,
rename, delete, share — **appends a row to a per-user change log with an increasing sequence number.** A client
remembers the last number it processed and asks: *what has happened since 4,417?*

```
GET /changes?cursor=4417
-> [ {seq: 4418, path: "/a.txt", op: "modify", chunks: [...]},
     {seq: 4419, path: "/b.pdf", op: "delete"} ],
   cursor: 4419
```

**That is one request instead of a hundred thousand**, and it is the core of the whole protocol.

**And the client should not have to poll it either.** A long-lived connection — a WebSocket, or long polling —
lets the server say "something changed, come and fetch". **The notification carries no data; it is just a
nudge**, which keeps it cheap and means a missed notification is harmless because the cursor is authoritative.

**Then conflicts, which are unavoidable.**

**Two devices edit the same file while offline. Both come back. Both have a version derived from version 7.**

**There is no correct automatic merge for a binary file.** You cannot merge two JPEGs. You cannot merge two
spreadsheets without understanding spreadsheets.

**So the honest design is: keep both.** One becomes `report.pdf` and the other becomes
`report (conflicted copy from Ravi's laptop).pdf`, **and a human decides.**

**That sounds like giving up and it is the right answer**, because the alternative — last-write-wins — silently
destroys somebody's work, and the user finds out days later. **Vasant's rule, exactly.**

**Detecting the conflict needs the right comparison.** Not timestamps — clocks disagree, as
[day 123](../day-123-word-search-ii/README.md) covers. **The test is whether the version the client edited is
the current server version.** If the client says "I am changing version 7" and the server is on version 8,
that is a conflict — **an optimistic-concurrency check, and it is exact.**

**Then sharing and permissions, which is where the metadata gets interesting.**

**A shared folder appears in several users' accounts**, and a change by one must appear for all of them. **So
the change log is per user, but a change to a shared item appends to every member's log.** That is a small
fan-out, bounded by the share size.

**And permission checks must be on every path.** The chunks themselves are content-addressed, **so knowing a
hash must not be enough to fetch it** — otherwise deduplication becomes a data leak: upload a file you suspect
exists, see that the server already has the chunk, and you have learned something about another user's data.
**Real systems either check ownership on every chunk fetch or deduplicate only within a user's own account.**

**Finally, the numbers, which are not the hard part but are worth having.**

**The storage saving from dedup is the headline** — typically 30–50% for personal accounts and much more for
corporate ones. **The bandwidth saving from delta sync is larger still**, because the common case is a small
edit to an existing file.

**And the metadata is the surprising part.** A user with a hundred thousand files has a hundred thousand rows
of metadata and a change log that grows forever. **The change log needs compaction** — old entries collapsed
into a snapshot — or a long-lived account accumulates millions of rows nobody will ever read.

---

## 4. The picture

The model: files are metadata, chunks are content:

```
  METADATA STORE (small, relational)     CHUNK STORE (large, immutable)

  file: /work/report.pdf                 a3f9... -> [4 MB of bytes]
    version: 7                           8c21... -> [4 MB of bytes]
    chunks: [a3f9, 8c21, a3f9, 0b7e]     0b7e... -> [1.2 MB of bytes]
    owner: ravi                            ^
    modified: ...                          content-addressed:
                                           the NAME is the hash

  file: /shared/hinge.pdf
    chunks: [a3f9, 4d02]
              ^
        SAME CHUNK. Stored once, referenced twice.

  -> the metadata is tiny and changes constantly
  -> the chunks are large and never change (a new version = new chunks)
```

Why chunking makes edits cheap:

```
  50 MB file, 4 MB chunks = 13 chunks
  the user edits one paragraph in the middle

  WITHOUT CHUNKING:  upload 50 MB
  WITH CHUNKING:     chunk 7's hash changed; the other 12 did not
                     upload 4 MB

  12x less. And the client knows WHICH chunks changed without
  asking, because it hashes them locally.

  the protocol:
     client: "I have chunks [a3f9, 8c21, NEW9f, 0b7e, ...]"
     server: "I already have all of those except NEW9f"
     client: uploads ONE chunk
```

Fixed against content-defined boundaries:

```
  FIXED 4 MB BOUNDARIES

  original:  [----A----][----B----][----C----]
  insert 1 byte at the start:
             [X---A'---][---B'----][---C'----]
              ^ every boundary shifted by one byte
              -> EVERY chunk hash changed
              -> re-upload the whole file

  CONTENT-DEFINED BOUNDARIES (a rolling hash picks the cut points)

  original:  [--A--][----B----][--C--]
  insert 1 byte at the start:
             [X-A'-][----B----][--C--]
              ^ only the first chunk changed;
                the cut points RE-SYNCHRONISE with the content
              -> upload one chunk

  This is why production systems use content-defined chunking.
```

The sync cursor, which is Vasant's numbering:

```
  per-user CHANGE LOG (append-only, monotonic sequence)

  seq   path              op        version
  ----------------------------------------------
  4415  /a.txt            modify    3
  4416  /photos/x.jpg     create    1
  4417  /old.doc          delete    -
  4418  /a.txt            modify    4
  4419  /shared/plan.pdf  modify    12    <- from another member

  client remembers: cursor = 4417
  client asks:      GET /changes?cursor=4417
  server returns:   4418, 4419  and the new cursor 4419

  ONE REQUEST, whatever the account size.
  Polling 100,000 files individually is the alternative.

  And a push notification is just a NUDGE — it carries no data,
  so a lost one is harmless: the cursor is the authority.
```

Conflict detection and what to do:

```
  server: report.pdf is at version 7

  Laptop A (offline)          Laptop B (offline)
    edits v7 -> v8              edits v7 -> v8
        |                            |
        | comes online first         |
        v                            |
  server accepts: v8                 | comes online
                                     v
                        client says "changing v7"
                        server is at v8
                        -> BASE VERSION MISMATCH -> CONFLICT

  WRONG: last-write-wins by timestamp
         -> silently destroys A's work; the user finds out in a week
         -> and the timestamps come from two clocks that disagree

  RIGHT: keep both
         report.pdf                              (A's version)
         report (conflicted copy from B).pdf     (B's version)
         -> a human decides. Which is honest, and is the only
            correct answer for a binary file.
```

The dedup leak, which is the non-obvious security point:

```
  content-addressed chunks: the NAME is the hash of the contents

  ATTACK:
    1. I guess a file's exact contents (a leaked document, a
       salary spreadsheet with a known format)
    2. I compute its chunk hashes
    3. I "upload" it — the server says "I already have those"
    4. I have learned that SOMEBODY ELSE has that exact file

  -> deduplication has leaked information across accounts

  DEFENCES:
    - check ownership on every chunk FETCH (dedup storage, not access)
    - deduplicate only within one user's account (less saving, no leak)
    - never reveal whether a chunk already existed (upload anyway,
      discard server-side)
```

---

## 5. How it actually works

### Chunking a file

```python
import hashlib

AVERAGE_CHUNK = 4 * 1024 * 1024
WINDOW = 48
MASK = (1 << 22) - 1                          # ~1 in 4M bytes is a boundary

def content_defined_chunks(data: bytes):
    """Boundaries chosen by content, so an insertion shifts only one chunk."""
    start, rolling = 0, 0
    for i, byte in enumerate(data):
        rolling = ((rolling << 1) + byte) & 0xFFFFFFFF        # a toy rolling hash
        if i - start >= WINDOW and (rolling & MASK) == 0:
            yield data[start:i + 1]
            start = i + 1
    if start < len(data):
        yield data[start:]

def chunk_hashes(data: bytes) -> list[str]:
    return [hashlib.sha256(c).hexdigest() for c in content_defined_chunks(data)]
```

**The `(rolling & MASK) == 0` test is the whole idea**: a boundary happens where the recent bytes hash to a
particular pattern, **so the boundaries follow the content rather than the offset.**

**Real implementations use a proper rolling hash** — Rabin fingerprinting or Buzhash — which can be updated in
`O(1)` per byte rather than recomputed. **The toy version above is for the shape, not for use.**

### The upload protocol

```python
def upload_file(path: str, data: bytes) -> None:
    hashes = chunk_hashes(data)
    missing = api.post("/chunks/check", {"hashes": hashes})["missing"]
    for chunk, h in zip(content_defined_chunks(data), hashes):
        if h in missing:
            api.put(f"/chunks/{h}", chunk)    # only the new ones
    api.post("/files", {"path": path, "chunks": hashes,
                        "base_version": local_version(path)})
```

**Three steps, and the middle one is where the saving is.** A one-paragraph edit to a 50 MB file uploads one
chunk.

**`base_version` is the conflict check** — the version this edit was made against — **and sending it is what
makes the server able to detect a conflict at all.**

### The server side of a write

```python
def apply_change(user_id: int, path: str, chunks: list[str],
                 base_version: int) -> dict:
    current = metadata.get(user_id, path)
    if current and current.version != base_version:
        conflict_path = conflicted_name(path, device_of(user_id))
        metadata.create(user_id, conflict_path, chunks, version=1)
        append_change(user_id, conflict_path, "create")
        return {"conflict": True, "saved_as": conflict_path}

    version = (current.version + 1) if current else 1
    metadata.upsert(user_id, path, chunks, version)
    append_change(user_id, path, "modify")
    for member in shared_members(user_id, path):
        append_change(member, path, "modify")      # bounded fan-out
    return {"conflict": False, "version": version}
```

**The version comparison is the conflict test, and it is exact** — no clocks involved. **`current.version !=
base_version` means somebody else changed it since this client last saw it.**

**And the conflicting version is saved rather than rejected.** Rejecting would mean the client has an edit it
cannot store anywhere, which is worse than a second file.

**The fan-out to shared members is bounded by the share size**, which is why sharing does not become a
Twitter-scale problem here.

### The change log and the cursor

```python
def append_change(user_id: int, path: str, op: str) -> int:
    seq = sequences.next_for(user_id)         # monotonic, per user
    change_log.insert(user_id, seq, path, op, time.time())
    notifier.nudge(user_id)                   # "something changed" — no payload
    return seq

def get_changes(user_id: int, cursor: int, limit: int = 500) -> dict:
    rows = change_log.after(user_id, cursor, limit)
    return {"changes": rows,
            "cursor": rows[-1].seq if rows else cursor,
            "has_more": len(rows) == limit}
```

**`sequences.next_for(user_id)` must be monotonic per user**, and it does not need to be globally ordered —
**per-user is enough, because a client only ever asks about its own account.** That makes it shardable by
user.

**And the notification carries no data**, which is deliberate: **a lost notification is harmless**, because the
client will discover the change on its next poll and the cursor is the source of truth. **A notification
carrying the change would have to be reliable, and this one does not.**

### The client's sync loop

```python
def sync_loop(cursor: int) -> None:
    while True:
        wait_for_nudge_or_timeout(seconds=60)          # push, with a poll fallback
        result = api.get(f"/changes?cursor={cursor}")
        for change in result["changes"]:
            apply_locally(change)
        cursor = result["cursor"]
        save_cursor(cursor)                   # AFTER applying, not before
```

**Saving the cursor after applying is the durability rule.** Save it first and a crash mid-apply loses changes
permanently — **the client would never ask for them again.** Saving after means a crash replays some changes,
which is harmless because applying is idempotent.

**The timeout is the fallback**: if the notification connection dies, sync still happens within a minute.
**Push for latency, poll for correctness.**

### Local change detection

```python
def scan_for_local_changes(root: str, index: dict) -> list[str]:
    changed = []
    for path in walk(root):
        stat = os.stat(path)
        cached = index.get(path)
        if cached and (stat.st_mtime, stat.st_size) == (cached.mtime, cached.size):
            continue                          # cheap check: skip hashing entirely
        if hash_file(path) != (cached.content_hash if cached else None):
            changed.append(path)
    return changed
```

**The `(mtime, size)` check is what makes this affordable.** Hashing a hundred thousand files takes minutes;
**checking two numbers per file takes a second**, and the hash is computed only for the handful that look
different.

**And filesystem watch APIs — `inotify`, `FSEvents`, `ReadDirectoryChangesW` — replace the scan entirely in the
normal case**, with the scan kept as a fallback for missed events and for startup.

### Sharing and permissions

```python
def fetch_chunk(user_id: int, chunk_hash: str) -> bytes:
    if not metadata.user_references_chunk(user_id, chunk_hash):
        raise Forbidden                       # dedup must not become a leak
    return chunk_store.get(chunk_hash)
```

**This check is the whole defence against the dedup information leak**, and it is easy to omit because the
chunk store is content-addressed and looks like it can be public. **Knowing a hash must not be sufficient to
read the data.**

### The real systems

```
Dropbox         Magic Pocket, their own storage after leaving S3;
                content-defined chunking; the sync engine was famously
                rewritten (Nucleus) because the original was
                unmaintainable
Google Drive    tightly coupled to Docs, which changes the model —
                collaborative editing is operational transforms, not files
rsync           the original delta-transfer algorithm, with a rolling
                checksum — the intellectual ancestor of all of this
git             content-addressed chunks with a Merkle tree, and
                explicit merge instead of conflicted copies
S3 / GCS        the chunk store, for anyone who has not built their own
```

**Naming Dropbox's move off S3 is a good detail**: at their scale the economics inverted and building their own
storage saved enough to justify it — **the same break-even argument as Netflix's CDN.**

---

## 6. The numbers

**Scale, and it is modest — which is the point.**

```
500,000,000 users
~50,000,000 daily active
average 100,000 files per user, average file 1 MB

edits: ~10 per active user per day = 500,000,000 changes/day
                                   = ~5,800 changes/second average
                                     peak ~20,000/second
```

**Five thousand writes a second is small** compared with anything else this week. **The difficulty here is
correctness, not throughput**, and saying that early is the right framing.

**Storage, before and after dedup.**

```
raw: 500,000,000 users x 100,000 files x 1 MB
   = 50,000,000,000,000 MB = 50 EB

-> obviously not real; most accounts are far smaller.
   Take the realistic figure instead:

average stored per user: ~10 GB
500,000,000 x 10 GB = 5 EB raw
```

```
DEDUPLICATION:
  personal accounts     ~30% saving   (shared installers, common documents)
  corporate accounts    ~70% saving   (everyone has the same attachments)
  blended               ~40%

5 EB x 0.6 = 3 EB stored
+ 3 replicas             = 9 EB

at $0.01/GB/month (own hardware, not cloud list price):
  9,000,000,000 GB x $0.01 = ~$90M/month
```

**Bandwidth, which is where delta sync pays.**

```
500,000,000 changes/day, average file 1 MB

WITHOUT delta sync: 500e6 x 1 MB = 500 TB/day uploaded
WITH delta sync:    only changed chunks
                    a typical edit touches ~1 chunk of ~4 MB
                    but MOST changed files are small (< 4 MB, one chunk)
                    -> ~100 TB/day

and DOWNLOAD is the multiplier: each change syncs to every
other device the user has (~3 on average)
  without dedup-aware sync: 3 x 500 TB = 1.5 PB/day
  with it:                  3 x 100 TB = 300 TB/day

-> 5x, and it is the difference between a usable product and one
   that saturates people's home connections.
```

**The metadata, which is the surprising cost.**

```
500,000,000 users x 100,000 files x ~500 bytes of metadata
  = 25 TB of metadata

that is SMALL in bytes and enormous in ROWS:
  50,000,000,000 rows

-> sharded by user id, which is natural because every query is
   scoped to one user
-> and it is queried far more often than the chunks are
```

**The change log, which grows forever.**

```
500,000,000 changes/day x ~200 bytes = 100 GB/day
  x 365                              = 36 TB/year
  and it never stops growing

COMPACTION is required:
  a client that has been offline for a year does not need
  a million individual changes — it needs the CURRENT STATE

  so: keep the last ~30 days of individual changes,
      and collapse everything older into a snapshot
  -> a client whose cursor is too old gets "resync from scratch"
     instead of a year of history
```

**That "resync from scratch" path is a real part of the design**, not an error case — and it is why the cursor
protocol needs a "your cursor is too old" response.

**The sync-latency budget:**

```
change committed on the server        ~20 ms
nudge to the other device             ~50 ms (open WebSocket)
device requests changes               ~30 ms
device downloads a 4 MB chunk         ~2 s on a home connection
                                      --------
                                      a few seconds, dominated by bytes

-> the protocol is fast; the transfer is not, which is exactly
   why chunking matters more than any latency optimisation.
```

**The dedup saving, made concrete:**

```
a 30 MB PDF sent to 1,000 people in a company

without dedup: 1,000 x 30 MB = 30 GB
with dedup:    30 MB + 1,000 small metadata rows = ~30 MB

1,000x for that file.

and the FIRST upload is the only one that transfers bytes:
the other 999 uploads are "server already has these chunks",
which is a few kilobytes of hashes.
```

---

## 7. The trade-offs

**Content-defined chunking against fixed-size chunking.** Fixed is trivial to implement and **breaks
completely on insertion** — one byte at the front of a file re-uploads everything. Content-defined survives
insertions and costs a rolling hash over every byte on every scan, **which is real CPU on a client that is
also trying to be invisible.** For a service where files are mostly appended to or replaced wholesale, fixed
is defensible; **for general documents it is not.**

**Global dedup against per-user dedup.** Global saves far more — a corporate account is largely the same files
repeated — and **creates an information leak**: a user can learn whether a chunk already exists, and therefore
whether someone else has a file they can guess. **Per-user dedup has no leak and much less saving.** The middle
answer is global storage with an ownership check on every fetch, **which keeps the saving and closes the
obvious hole**, at the cost of a metadata lookup per chunk read.

**Conflicted copies against automatic merge.** Keeping both is honest and puts work on the user. **Merging is
possible only for formats you understand** — text, and structured documents where you have an editor. **For
binary files there is no merge**, and last-write-wins is not a simpler answer, it is a wrong one that destroys
data silently. **Google Drive's answer is different in kind**: for its own document formats it does real
collaborative editing with operational transforms, **which is a different product, not a better sync
algorithm.**

**Push notifications against polling.** Push gives seconds of latency and needs a persistent connection per
device — the connection tier from [day 156](../day-156-grid-dp/README.md). **Polling is stateless and means
minutes of delay.** The right answer uses both, **and the important design decision is that the notification
carries no data**, so it does not have to be reliable.

**Change log retention against resync cost.** Keeping every change forever is 36 TB a year and lets any client
catch up incrementally. **Compacting means a long-absent client must resync from scratch**, which for a
100,000-file account is a large download. **Thirty days is the usual compromise**, and the resync path has to
exist and be tested, because it runs rarely and always in unhappy circumstances.

**When would I not build this?** **When files do not change** — an asset store, a backup archive — where
versioning and conflict handling are pure overhead and object storage plus a CDN is the whole system. **When
the real requirement is collaborative editing**, which is a different problem entirely: operational transforms
or CRDTs over a document model, not chunks over a filesystem. **And obviously below any serious scale**, where
S3 with a sync library is cheaper than a team.

---

## 8. In the interview

### How it gets asked

- *"Design Dropbox."* or *"Design Google Drive."* — the standard prompt.
- *"How does a client know what changed?"* — the sync cursor question.
- *"I edit a 50 MB file. What gets uploaded?"* — chunking and delta sync.
- *"Two devices edit the same file offline. What happens?"* — the conflict question.
- *"How much storage does deduplication save?"*
- *"What is the security risk with deduplication?"* — the good one.

### The first ninety seconds

> "The first thing I would say is that **this is the one design where the difficulty is not scale.** Five
> hundred million users generating five thousand changes a second is small — there is no fan-out problem, no
> celebrity, no thundering herd.
>
> **What is hard is correctness: several devices editing the same data, going offline, and coming back with
> conflicting histories.**
>
> **Three ideas carry it.**
>
> **First, files are stored as chunks, addressed by the hash of their contents.** A file becomes metadata — a
> name, a version, and an ordered list of chunk hashes — and the bytes live in a separate content-addressed
> store.
>
> **Two big things fall out of that one decision.** **You only upload what changed**: edit a paragraph in a
> fifty-megabyte file and only one chunk's hash differs, so you upload four megabytes instead of fifty. **And
> identical chunks are stored once across all users**, which in a corporate account saves most of the storage,
> because everybody has the same attachments.
>
> **And I would use content-defined chunk boundaries rather than fixed ones.** With fixed four-megabyte
> boundaries, **inserting one byte at the start of a file shifts every boundary and changes every hash**, so
> you re-upload everything. Content-defined boundaries are chosen by a rolling hash of the recent bytes, **so
> they move with the content and an insertion changes one chunk.**
>
> **Second, sync, which is the real design problem.** The question is how a client learns what changed.
> **Polling a hundred thousand files is impossible**, so: **a monotonic version cursor per user.** Every change
> appends to a per-user log with an increasing sequence number, and the client asks 'what has happened since
> 4,417?' **One request, whatever the account size.**
>
> **With a push notification as a nudge that carries no data** — so a lost notification is harmless, because
> the cursor is the authority. Push for latency, polling as the fallback for correctness.
>
> **Third, conflicts, which cannot be prevented.** Two devices edit offline; both come back with a version
> derived from version seven. **There is no correct merge for a binary file**, so the answer is to keep both
> and name one as a conflicted copy. **That sounds like giving up and it is right**, because last-write-wins
> silently destroys work and the user finds out a week later.
>
> **And detection uses the base version, not timestamps** — the client says which version it edited, and if
> the server has moved on, that is a conflict. **Exact, and no clocks involved.**"

### The follow-ups

**"How does a client know what changed?"**

> "This is the core of the protocol, and the naive answers fail for a specific reason worth naming.
>
> **Polling every file is impossible.** A user with a hundred thousand files would make a hundred thousand
> requests to learn that nothing had happened, and they would do it every few seconds.
>
> **Comparing modification times is also wrong**, even ignoring the request count: **clocks on two machines
> disagree**, so 'newer' is not reliable, and a file whose contents were reverted has a new timestamp and
> unchanged contents.
>
> **The answer is a monotonic version cursor per user.** Every change to that user's files — create, modify,
> rename, delete, a share appearing — **appends a row to a per-user change log with a strictly increasing
> sequence number.**
>
> **A client stores the last sequence it processed and asks for everything after it.** One request returns the
> handful of changes, plus a new cursor. **One request instead of a hundred thousand, and it is `O(changes)`,
> not `O(files)`.**
>
> **It only needs to be monotonic per user, not globally** — a client only ever asks about its own account —
> **so the sequence is shardable by user id**, which matters because a global counter would be a bottleneck.
>
> **Two details I would insist on.**
>
> **The push notification carries no data.** It is a nudge saying 'come and fetch'. **That means a lost
> notification is harmless** — the client picks up the change on its next poll, and the cursor is the single
> source of truth. **A notification carrying the actual change would have to be delivered reliably, and this
> one does not.**
>
> **And the client saves its cursor after applying the changes, not before.** Save it first and a crash
> mid-apply loses those changes permanently, because the client will never ask for them again. **Saving after
> means a crash replays a few changes, which is harmless because applying is idempotent** — that asymmetry is
> the whole reason for the ordering.
>
> **One more thing the protocol needs: a 'your cursor is too old' response.** The log is compacted after about
> thirty days, so **a client that has been offline for a year cannot catch up incrementally and must resync
> from scratch.** That path is rare, always happens in unhappy circumstances, and therefore needs testing more
> than the common path does."

**"Two devices edit the same file while offline. What happens?"**

> "They conflict, and **the design decision is what to do about it, because it cannot be prevented.**
>
> **Detecting it first.** When a client uploads, it sends the version it based its edit on. **If the server's
> current version is not that version, somebody else has changed the file since this client last saw it** —
> that is the conflict, and the test is exact.
>
> **I would specifically not use timestamps.** Two devices' clocks disagree, so 'later' is not a reliable
> ordering — and a device with a clock two minutes fast would win every conflict it participated in, forever,
> with nothing reporting it.
>
> **Now what to do, and there are three options with very different honesty.**
>
> **Last-write-wins is the simplest and it silently destroys work.** One person's afternoon disappears, they
> do not find out for a week, and by then there is no way to recover it. **I would not do this, and I would say
> why rather than just rejecting it.**
>
> **Automatic merge works only when you understand the format.** Text merges reasonably; a spreadsheet needs a
> spreadsheet-aware merge; **two JPEGs cannot be merged at all, in principle.** So a general file sync service
> cannot merge.
>
> **So: keep both.** One file stays at its path, the other becomes `report (conflicted copy from Ravi's
> laptop).pdf`. **A human looks at them and decides.**
>
> **That looks like giving up and it is the correct answer**, because the system genuinely does not have the
> information to decide, **and pretending otherwise means losing data.** The name carries the device and the
> time so the user can tell which is which.
>
> **What I would add is making it rare and making it visible.** **Rare** by syncing aggressively when online,
> so the window for divergence is small. **Visible** by surfacing conflicted copies in the interface rather
> than leaving a mysterious extra file in a folder — **the failure mode of the honest design is that users do
> not notice the second file for months.**
>
> **And I would name the alternative for a specific case.** For its own document formats, Google Drive does
> real-time collaborative editing with operational transforms, so there is nothing to conflict. **That is a
> different product built on a document model, not a better sync algorithm** — and it is worth being clear
> about which question is being asked."

**"What is the security risk with deduplication?"**

> "There is a real one, it is not obvious, and it is a good test of whether you have thought about the design
> rather than drawn it.
>
> **Global deduplication means the server tells you whether it already has a chunk.** That is how the upload
> protocol saves bandwidth: the client sends hashes and the server replies with the ones it is missing.
>
> **Which means an attacker can ask 'does anyone have this file?'**
>
> **The attack is concrete.** Suppose I know a company uses a standard salary spreadsheet template and I can
> guess the exact contents for a particular person — or I have a leaked document and want to know whether a
> specific person has a copy. **I compute its chunk hashes and start an upload. If the server says it already
> has those chunks, I have learned that the file exists in someone else's account.**
>
> **No file was downloaded, and information crossed an account boundary.**
>
> **A worse version exists**: if the server is willing to serve any chunk to anyone who knows its hash — which
> is tempting, because content-addressed storage looks like it can be public — **then guessing the contents
> lets me actually retrieve the file**, which is a full data breach.
>
> **Three defences, and I would take the third.**
>
> **Deduplicate only within a single user's account.** No cross-account leak at all, and it throws away most of
> the saving — the whole point is that a thousand people have the same attachment.
>
> **Never reveal existence: always upload, and discard server-side if the chunk is already there.** Keeps the
> storage saving and loses the bandwidth saving, which is the larger of the two.
>
> **Or: deduplicate storage globally, but check ownership on every read.** The chunk store is shared; **fetching
> a chunk requires that the requesting user's metadata actually references it.** That keeps both savings, and
> it costs a metadata lookup per chunk read.
>
> **It still leaks the existence signal through the upload path**, so for accounts with a high confidentiality
> requirement I would combine it with the always-upload approach — **and I would raise that as a decision for
> the product rather than making it silently.**"

### The model answer

*"Design a file sync service: five hundred million users, a folder on each of their devices that stays in sync,
offline support, and sharing."*

> "Let me frame it first, because the framing is half the answer here. **Five hundred million users generating
> about five thousand changes a second is a small system by this week's standards.** There is no fan-out
> problem and no hot spot. **The difficulty is correctness under concurrent offline edits**, and I will spend
> the time there.
>
> **The model: a file is metadata plus a list of chunk hashes.** Metadata is small, relational, and changes
> constantly — sharded by user id, which is natural because every query is scoped to one account. **Chunks are
> large, immutable and content-addressed** in a separate store.
>
> **Chunking is content-defined, not fixed.** Boundaries are chosen by a rolling hash of the recent bytes, so
> **an insertion at the start of a file shifts one chunk rather than all of them.** With fixed boundaries a
> one-byte insertion re-uploads the entire file, which is the single worst common case.
>
> **Upload protocol: hash locally, ask the server which chunks it is missing, upload only those, then commit
> the metadata with a base version.** A one-paragraph edit to a fifty-megabyte file uploads four megabytes.
>
> **Sync: a monotonic per-user change log with a cursor.** The client asks 'what since 4,417?' — **one request
> regardless of account size.** A push notification acts as a nudge and **carries no data, so losing one is
> harmless.** The client saves its cursor **after** applying, so a crash replays rather than skips.
>
> **And the log is compacted after about thirty days**, which means the protocol needs a 'cursor too old,
> resync from scratch' response — **a path that runs rarely and always during an incident, so it needs testing
> more than the happy path.**
>
> **Conflicts: detected by base version, never by timestamp** — clocks disagree and a fast clock would win
> every conflict forever. **When detected, keep both files**, naming one as a conflicted copy with the device
> and time. **There is no correct merge for a binary file, and last-write-wins is not simpler, it is wrong.**
>
> **Sharing: a change to a shared item appends to every member's change log.** That is a fan-out, and it is
> bounded by the share size, so it never becomes a Twitter problem. **Permissions are checked on the metadata
> path and, crucially, on every chunk fetch.**
>
> **Which brings me to the thing I would raise unprompted: deduplication is an information leak.** Because the
> server tells a client which chunks it already has, **an attacker who can guess a file's exact contents can
> learn whether somebody else has it.** I would deduplicate storage globally for the saving, **check ownership
> on every chunk read** so a hash is not sufficient to fetch data, and treat the residual existence signal in
> the upload path as a product decision rather than one I make quietly.
>
> **Sizing.** Deduplication saves roughly thirty percent on personal accounts and seventy on corporate ones —
> call it forty percent blended. **Delta sync is the bigger win on bandwidth**, roughly five times, because a
> change syncs to every other device the user owns and most changed files are small.
>
> **The metadata is the surprising cost:** fifty billion rows for a hundred thousand files per user, tiny in
> bytes and enormous in rows, **and it is queried far more often than the chunks are.**
>
> **Two client-side details that matter more than they look.** **Local change detection uses `(mtime, size)`
> before hashing** — hashing a hundred thousand files takes minutes, checking two numbers takes a second —
> **with filesystem watch APIs replacing the scan in the normal case and the scan kept as a fallback.**
>
> **And the sync latency budget is dominated by bytes, not by the protocol.** The change reaches the other
> device in under a tenth of a second and the four-megabyte chunk takes two seconds on a home connection.
> **Which is why chunking is worth more than any latency optimisation** — and is a good reminder that the
> interesting engineering here is in transferring less, not in being faster."

---

## 9. Recall card

**The difficulty is correctness, not scale** — ~5,000 changes/second, no fan-out, no hot spots. **Files are
metadata plus a list of content-addressed chunk hashes**; the bytes live in a separate immutable store.

**Content-defined chunking, not fixed:** a rolling hash picks boundaries so they move with the content —
**with fixed boundaries, inserting one byte at the start changes every hash and re-uploads the whole file.**
Upload = hash locally → ask which chunks are missing → send only those (4 MB, not 50).

**Sync is a monotonic per-user change log with a cursor**: "what since 4,417?" is **one request whatever the
account size**, versus polling 100,000 files. **The push notification carries no data**, so losing one is
harmless — the cursor is the authority. **Save the cursor AFTER applying**, so a crash replays (idempotent)
rather than skips (permanent loss). **Compaction after ~30 days needs a "cursor too old, resync" path.**

**Conflicts are detected by BASE VERSION, never timestamps** — clocks disagree, and a fast clock wins every
conflict forever. **There is no correct merge for a binary file, so keep both** as a named conflicted copy.
**Last-write-wins is not simpler, it is wrong** — it destroys work silently and the user finds out a week
later.

**Deduplication is an information leak**, and this is the best follow-up in the topic: the server telling you
it already has a chunk lets an attacker who can guess a file's contents learn that someone else has it. **Fix:
dedup storage globally, but check ownership on every chunk FETCH** — knowing a hash must not be enough to
read.

**Dedup saves ~30% personal / ~70% corporate; delta sync saves ~5× on bandwidth** (every change syncs to ~3
devices). **The metadata is 50 billion rows** — tiny in bytes, huge in rows, queried far more than the chunks.
**Client-side: check `(mtime, size)` before hashing**, with filesystem watch APIs replacing the scan.
