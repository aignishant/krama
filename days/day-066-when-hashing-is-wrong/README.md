# Day 066 — When a hash map is the wrong answer

| Track | Today |
|---|---|
| **DSA** | When a hash map is the wrong answer |
| **System design** | Builder |
| **Languages** | The Go protobuf API |
| &nbsp;&nbsp;Python | Python protobuf API: SerializeToString, ParseFromString, MessageToJson |
| &nbsp;&nbsp;Go | proto.Marshal, proto.Unmarshal, proto.Equal, protojson, and protoreflect |
| &nbsp;&nbsp;C++ | SerializeToString, ParseFromString, and util::MessageToJsonString |

## What you can do by tonight

- **DSA** — You can name the three cases where sorting or an array beats a dictionary.
- **System design** — You can build an object with fifteen optional fields without a fifteen-argument constructor.
- **Languages** — You can marshal, unmarshal, compare, and print messages, and say what the Go API does differently.

## The questions today answers

- *You used a hash map. Could you do it with O(1) space instead?*
- *This constructor takes twelve parameters. Fix it.*
- *How do you convert a protobuf message to JSON, and what gets lost?*

## Read in this order

1. [01-dsa-when-a-hash-map.md](01-dsa-when-a-hash-map.md) — the DSA lesson
2. [02-system-design-builder.md](02-system-design-builder.md) — the system design lesson
3. [05-lang-python-python-protobuf-api-serializetostring.md](05-lang-python-python-protobuf-api-serializetostring.md) — the Python lesson
4. [06-lang-go-proto-marshal-proto-unmarshal.md](06-lang-go-proto-marshal-proto-unmarshal.md) — the Go lesson
5. [07-lang-cpp-serializetostring-parsefromstring-and-util.md](07-lang-cpp-serializetostring-parsefromstring-and-util.md) — the C++ lesson
6. [03-practice.md](03-practice.md) — DSA, system design, and all three languages

## Where this sits

- DSA phase: **Hashing: maps and sets**
- System design phase: **Design patterns**
- Languages phase: **Languages: Protocol Buffers and gRPC**

---

[← Day 065](../day-065-hashing-custom-objects/README.md) · [All days](../README.md) · [Day 067 →](../day-067-hashing-revision/README.md)
