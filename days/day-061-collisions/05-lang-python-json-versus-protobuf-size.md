---
day: 61
track: lang-python
title: "JSON versus protobuf: size and speed, measured"
theme: "Protocol Buffers: what and why"
phase: "Languages: Protocol Buffers and gRPC"
status: written
---

# Day 061 · Python — JSON versus protobuf: size and speed, measured

**Today's theme:** Protocol Buffers: what and why

**After today you can:** You can explain what a schema is, why binary beats text on the wire, and write your first .proto file.

**The interviewer asks it as:** *Why would you use protobuf instead of JSON?*

---

## 1. What this is, and why it matters

**Protocol Buffers**, protobuf for short, is a way of turning a structured record into bytes and
back that is smaller and faster than JSON, because both sides agree on the record's shape in
advance. That agreement is written in a `.proto` file, called a **schema**: it names each field,
gives it a type, and gives it a number. A compiler turns the schema into a Python class, and
that class knows how to write itself as compact bytes, with no field names on the wire, and read
itself back. JSON, which you have used since [day 40](../day-040-2d-prefix-sums/README.md),
carries every field name in every message and spells every number out in decimal text.

At work protobuf is what services inside a company say to each other, and gRPC, which arrives
on day 67, is built on it. In interviews, "why protobuf instead of JSON" is the opening question
of the whole gRPC topic, and the answer they want has numbers in it: how many bytes, how many
microseconds, and what you give up.

## 2. The story

Kavita scores for the college cricket team, and she has trained three people to do it. The
scorebook is a grid: one row per ball, and the columns are always the same, batter, bowler,
runs, extras, wicket. Everyone who has ever scored knows the columns. So when Kavita is at the
boundary and the scorer at the table shouts across to her after a ball, all he shouts is "seven,
two, four". Batter seven, bowler two, four runs. Three words, and she has written the whole row
before the bowler has turned round.

Last Sunday the regular scorer was ill and his cousin filled in. The cousin had never seen the
book. After the first ball he shouted: "The tall one in the red cap hit it hard through the
covers, I think it went for four, the left-arm bowler, nobody was out." Kavita understood him
perfectly. It took him twelve seconds to say and her eight seconds to work out which column each
piece went in, and by then the next ball had been bowled.

Both of them were telling her the same thing. The difference was that the regular scorer and
Kavita had agreed, months ago, what the columns meant and in what order they would come. The
cousin had no such agreement, so he had to label everything as he went: "the batter was", "the
runs were". Labelling every piece is what makes it slow, and it is also what makes it
understandable to a stranger.

At the end of the day Kavita looked at the two halves of the book. The regular scorer's half
was neat rows of small numbers. The cousin's half, which she had transcribed from his shouting,
was the same rows. Nothing was lost either way. But the cousin's way would never have kept up
with a fast bowler, and the regular scorer's way would have meant nothing to anyone who had not
learned the columns.

## 3. The idea in plain English

The agreed columns are the **schema**, the `.proto` file. It says: field 1 is `id`, a whole
number; field 2 is `customer`, text; field 3 is `item_ids`, a list of whole numbers; and so on.
Both sides have the file. Neither needs to be told the column names at match time.

"Seven, two, four" is a **protobuf message** on the wire: just the field numbers and the values,
packed as bytes, with no names. The cousin's shouting is **JSON**: every value labelled with
its name, every number spelled out in decimal characters, brackets and quotes and commas to
show where things start and end. JSON is readable by anyone; protobuf is readable by anyone
holding the schema.

The compiler, `protoc`, reads the schema and writes a Python module, `order_pb2.py`, with a
class `Order` in it. `Order(id=..., customer=...)` builds a message; `SerializeToString()`
writes the bytes; `Order.FromString(data)` reads them back. You never write the byte format by
hand, and you never edit the generated file.

The measured difference is the point of today. The same order is 85 bytes as JSON and 29 as
protobuf, and a Python round trip, encode then decode, is about eight microseconds for JSON and
about one for protobuf. Three times smaller and seven times faster, in the language where
protobuf is slowest. Those are the numbers to carry into the interview.

What you give up is the cousin's virtue: you cannot read the bytes without the schema, `curl`
cannot show you a message, and both sides must have the same `.proto`. Day 64 is about what
happens when they do not.

## 4. The picture

```text
  JSON, 85 bytes: every name, every number in decimal text

  {"id":1234567,"customer":"meera","item_ids":[101,202,303],"total":1499.5,"paid":true}

  protobuf, 29 bytes: field number + wire type, then the value, no names

  08 87 ad 4b        field 1, varint  1234567  (3 bytes for a 7-digit number)
  12 05 6d 65 65 72 61   field 2, length 5, "meera"
  1a 05 65 ca 01 af 02   field 3, length 5, packed varints 101 202 303
  21 00 00 00 00 00 6e 97 40   field 4, 8-byte double 1499.5
  28 01              field 5, varint 1 (true)
```

Notice the first byte of each field, `08`, `12`, `1a`, `21`, `28`: the field number shifted
left three bits, plus a code for how the value is laid out. The name `customer` is nowhere. The
schema is what turns `12` back into `customer`.

## 5. The code, built step by step

Install the runtime and the compiler. `grpcio-tools` bundles `protoc` so you do not need a
separate download.

```bash
pip install protobuf grpcio-tools
```

The schema, `order.proto`. `syntax` must be the first line; `package` prevents name clashes
between files; each field is type, name, `=`, number.

```protobuf
syntax = "proto3";

package shop;

message Order {
  int64 id = 1;
  string customer = 2;
  repeated int32 item_ids = 3;
  double total = 4;
  bool paid = 5;
}
```

`repeated` means "a list of". The numbers are not defaults or values; they are the field's
identity on the wire, and day 64 explains why they must never change.

Compile it. The command reads the schema and writes `order_pb2.py` next to it.

```bash
python -m grpc_tools.protoc -I. --python_out=. order.proto
```

Build one message and look at it two ways. The generated class takes keyword arguments for
every field.

```python
import json
from order_pb2 import Order

order = Order(id=1234567, customer="meera", item_ids=[101, 202, 303], total=1499.5, paid=True)
as_dict = {"id": 1234567, "customer": "meera", "item_ids": [101, 202, 303],
           "total": 1499.5, "paid": True}
```

The size comparison. `separators=(",", ":")` gives JSON its most compact form, so the comparison
is fair.

```python
json_bytes = json.dumps(as_dict, separators=(",", ":")).encode()
proto_bytes = order.SerializeToString()
print(f"json:  {len(json_bytes):3d} bytes  {json_bytes!r}")
print(f"proto: {len(proto_bytes):3d} bytes  {proto_bytes!r}")
```

The speed comparison: a hundred thousand round trips each, timed with `perf_counter` from
[day 41](../day-041-prefix-revision/README.md).

```python
N = 100_000
start = time.perf_counter()
for _ in range(N):
    json.loads(json.dumps(as_dict, separators=(",", ":")))
json_time = time.perf_counter() - start

start = time.perf_counter()
for _ in range(N):
    Order.FromString(order.SerializeToString())
proto_time = time.perf_counter() - start
```

Run it:

```bash
python measure.py
```

```text
json:   85 bytes  b'{"id":1234567,"customer":"meera","item_ids":[101,202,303],"total":1499.5,"paid":true}'
proto:  29 bytes  b'\x08\x87\xadK\x12\x05meera\x1a\x05e\xca\x01\xaf\x02!\x00\x00\x00\x00\x00n\x97@(\x01'
json:  100000 round trips in 0.79s  (7.9 us each)
proto: 100000 round trips in 0.12s  (1.2 us each)
```

Twenty-nine bytes against eighty-five, and about seven times faster. Run it again and the
seconds move a little; the ratio does not. Here is the complete `measure.py`:

```python
import json
import time

from order_pb2 import Order

order = Order(id=1234567, customer="meera", item_ids=[101, 202, 303], total=1499.5, paid=True)
as_dict = {"id": 1234567, "customer": "meera", "item_ids": [101, 202, 303],
           "total": 1499.5, "paid": True}

json_bytes = json.dumps(as_dict, separators=(",", ":")).encode()
proto_bytes = order.SerializeToString()
print(f"json:  {len(json_bytes):3d} bytes  {json_bytes!r}")
print(f"proto: {len(proto_bytes):3d} bytes  {proto_bytes!r}")

N = 100_000
start = time.perf_counter()
for _ in range(N):
    json.loads(json.dumps(as_dict, separators=(",", ":")))
json_time = time.perf_counter() - start

start = time.perf_counter()
for _ in range(N):
    Order.FromString(order.SerializeToString())
proto_time = time.perf_counter() - start

print(f"json:  {N} round trips in {json_time:.2f}s  ({json_time / N * 1e6:.1f} us each)")
print(f"proto: {N} round trips in {proto_time:.2f}s  ({proto_time / N * 1e6:.1f} us each)")
```

## 6. How the other two languages do it

**Go**

```go
order := &pb.Order{Id: 1234567, Customer: "meera", ItemIds: []int32{101, 202, 303}, Total: 1499.5, Paid: true}
data, err := proto.Marshal(order)      // 29 bytes, the same 29
var back pb.Order
err = proto.Unmarshal(data, &back)
```

The same schema, compiled with `protoc --go_out`, gives a struct with exported fields and the
`proto.Marshal` and `proto.Unmarshal` functions from `google.golang.org/protobuf/proto`. The
bytes are identical, because the wire format is the schema's, not the language's.

**C++**

```cpp
shop::Order order;
order.set_id(1234567);
order.set_customer("meera");
order.add_item_ids(101);
std::string data;
order.SerializeToString(&data);       // 29 bytes again
shop::Order back;
back.ParseFromString(data);
```

Setters instead of constructor arguments, and `add_` for repeated fields; the generated header
and source are compiled into your program and linked against `libprotobuf`.

**The difference that matters:** the bytes are the same in all three, and that is the whole
reason protobuf exists: a Go service can `Marshal` a message and a Python one can `FromString` it
without either knowing the other's language. The speed ratio is where they differ. Python's
seven-to-one is the widest, because Python's JSON is pure interpretation and its protobuf is C
underneath; in Go and C++ both sides are compiled and the ratio narrows to about three or four
to one. Say "three times smaller everywhere, and from three to seven times faster depending on
the language".

## 7. The traps

**The near-miss: comparing against pretty JSON.** `json.dumps(as_dict)` with default
separators gives 96 bytes, and `indent=2` gives more. The compact form, 85, is the honest
comparison; anything else is protobuf beating a straw man. Measure against the smallest JSON you
would actually send.

**Reading the bytes as text.** `proto_bytes.decode()`:

```text
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x87 in position 1: invalid start byte
```

Protobuf is binary. `0x87` is part of a varint, not a character. Print with `!r` or `.hex()`,
never `.decode()`.

**Importing the generated module with the wrong runtime.** The generated file checks the
`protobuf` package version it was made for:

```text
TypeError: Descriptors cannot be created directly.
If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
```

The compiler and the runtime come from two packages, `grpcio-tools` and `protobuf`, and they
must agree. Upgrade both together, and regenerate.

**Setting a field that is not in the schema.** `Order(customer_name="meera")`:

```text
ValueError: Protocol message Order has no "customer_name" field.
```

This is the schema doing its job: JSON would have accepted the key silently, and the reader
would have looked for `customer` and found nothing.

**Assigning a repeated field.** `order.item_ids = [1, 2]`:

```text
AttributeError: Assignment not allowed to map, or repeated field "item_ids" in protocol message object.
```

Repeated fields are containers you `append` to or `extend`, or pass in the constructor;
they are not lists you can replace.

**Thinking smaller is always the answer.** A `curl` against a protobuf endpoint prints garbage;
a browser cannot read it; a log line with a protobuf body is useless. For a public API that
humans and browsers call, JSON is still the right answer. Protobuf is for service-to-service
traffic where both ends are yours.

## 8. Say it out loud

**How it gets asked**

- Why would you use protobuf instead of JSON?
- What is a schema, and what does the compiler generate from it?
- How much smaller and faster is it, actually?
- When would you still choose JSON?

**The ninety-second script**

Protobuf and JSON both turn a record into bytes; the difference is that protobuf makes both
sides agree on the record's shape in advance, in a `.proto` file called a schema, so the wire
carries field numbers and values and no names. I measured it: an order with five fields is
85 bytes as compact JSON and 29 bytes as protobuf, about three times smaller, and a Python
encode-decode round trip is about eight microseconds for JSON and about one for protobuf. The
compiler, `protoc`, turns the schema into a class in each language, `Order` in Python with
`SerializeToString` and `FromString`, a struct in Go with `proto.Marshal`, a class in C++ with
setters, and the bytes are identical across all three, which is what lets services in different
languages talk. The cost is readability: you cannot `curl` it or read it in a log without the
schema, and both sides must have the schema. So protobuf for traffic between services I control,
where volume makes the bytes and microseconds matter, and JSON for public APIs and anything a
browser or a person reads.

**The follow-ups**

- **Where do the savings actually come from?** *No field names on the wire, numbers as binary
  instead of decimal text, and no quotes, brackets, or commas. The `1234567` is three bytes as a
  varint and seven as text; `"customer":` is eleven bytes of JSON that protobuf replaces with
  one.*
- **Does the schema mean I cannot add a field later?** *You can add fields freely; old readers
  skip numbers they do not know. What you cannot do is change a field's number or type, which is
  day 64.*
- **Is it just size, or does it change the API design?** *It changes it: the schema is a
  contract both sides compile against, so a field typo is a compile error instead of a runtime
  surprise. That is the reason as much as the bytes.*

**A model answer**

"Both sides share a schema, so the wire carries numbers and values, not names. Measured: 85 bytes
JSON versus 29 protobuf for a five-field order, and 7.9 microseconds versus 1.2 per round trip
in Python. `protoc` generates `Order` with `SerializeToString` and `FromString`; the same schema
gives identical bytes from Go and C++. The trade is that the bytes are unreadable without the
schema, so it is for service-to-service traffic, and JSON stays for public and browser-facing
APIs."

## 9. Recall card

- A schema is a `.proto` file: `syntax = "proto3"; package shop; message Order { int64 id = 1; string customer = 2; repeated int32 item_ids = 3; ... }`. Numbers are the field's identity on the wire.
- `python -m grpc_tools.protoc -I. --python_out=. order.proto` writes `order_pb2.py`; never edit it. `Order(id=..., customer=...)`, `SerializeToString()`, `Order.FromString(data)`.
- Measured: 85 bytes compact JSON versus 29 bytes protobuf; 7.9 µs versus 1.2 µs per Python round trip. About three times smaller, three to seven times faster by language.
- The bytes are field number plus wire type, then the value, no names; identical from Python, Go, and C++. That is why services in different languages can talk.
- Cost: unreadable without the schema, no `curl`, both ends must share the `.proto`. Protobuf between your own services; JSON for public and browser-facing APIs.
