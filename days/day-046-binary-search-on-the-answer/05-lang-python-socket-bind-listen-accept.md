---
day: 46
track: lang-python
title: "socket, bind, listen, accept, and a threaded echo server"
theme: "TCP sockets: an echo server"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 046 · Python — socket, bind, listen, accept, and a threaded echo server

**Today's theme:** TCP sockets: an echo server

**After today you can:** You can write a server that accepts a connection and echoes bytes back, in each language, and test it with a client.

**The interviewer asks it as:** *What happens when a client connects to your server?*

---

## 1. What this is, and why it matters

A socket is the object your program uses to send and receive bytes over the network. A TCP
server makes one socket, gives it an address, tells the operating system it is open for
business, and then waits for clients to arrive. An echo server is the smallest possible server:
whatever bytes a client sends, it sends straight back.

Every web framework, every database driver, and every message queue you will ever use sits on
top of exactly these four calls. Interviewers ask "what happens when a client connects" to
check you know that a connection is something the operating system hands you, one at a time,
and that a server which handles one client at a time is a server that everybody else is waiting
on. You met TCP on [day 4](../day-004-the-growth-curves/README.md) and threads on
[day 31](../day-031-fixed-window/README.md). Today they meet.

## 2. The story

Meera opens a small eatery on the corner of a busy road. Before anyone can visit, she needs
one thing: a street number. She gets it painted above the door, number forty-two, so that a
person who has heard of the place can actually find it.

Then she flips the sign on the door to say open. That is all it does. It does not bring anyone
in. It tells people walking past that if they knock, someone will answer.

Her cousin Arjun stands at the door. When a family arrives, he does not take their order. He
walks them to an empty table, and then he goes straight back to the door, because there is
already a second group behind them. Arjun never leaves the door for long. If he did, people
would pile up on the pavement and some would give up and go home.

Each table gets its own waiter. The waiter does something slightly odd. Whatever the customer
says, the waiter says back to them, word for word. "Two plates of rice." "Two plates of rice."
"And one lime soda." "And one lime soda." The customers find it funny, but it is useful: they
hear at once if something was misheard.

The waiter at table three has no idea what is happening at table five. He only listens to his
own table. When his customers stand up and leave, he wipes the table clean and waits for Arjun
to bring him the next group.

One evening a second cook tries to open a stall at number forty-two as well. The painter refuses.
One number, one place. And when a customer turns up at nine at night after the sign has been
flipped to closed, nobody answers the knock. She stands outside for a moment, then walks away.
Nothing bad happens. There was simply nobody there to open the door.

## 3. The idea in plain English

The street number is the **address**: an IP address and a port together, such as
`127.0.0.1:9000`. Giving your socket that address is `bind`. Only one program can bind a given
port at a time, which is why the second cook was refused.

Flipping the sign is `listen`. It tells the operating system: keep a queue of people who knock,
I will get to them. It does not talk to anyone.

Arjun at the door is `accept`. Every call to `accept` blocks until someone connects, and then
hands you back **a brand new socket** for that one client. This is the step people get wrong.
The listening socket never carries data. It only produces connected sockets, one per client,
and goes straight back to waiting.

The waiter is the code that reads from the connected socket and writes to it. Reading is
`recv`, which gives you some bytes — maybe fewer than you asked for, never more. Writing is
`sendall`, which keeps sending until every byte has gone. When the client hangs up, `recv`
returns an empty `bytes` object, and that is how the waiter knows the table is empty.

One waiter per table is one thread per connection. If Arjun took orders himself, the second
family would wait on the pavement. If the accepting loop served the client itself, the second
client would sit in the queue until the first one left.

## 4. The picture

```text
   server                                         client
   ------                                         ------
   socket()      make the object
   bind(127.0.0.1:9000)   claim the address
   listen()      open sign, queue starts
   accept()  <--- blocks ---------------------- connect(127.0.0.1:9000)
      |
      v  returns (conn, addr)  ---- new thread ----+
   accept()  waits for the next client            |
                                                  v
                                            conn.recv()  <--- "hello\n" ---- sendall
                                            conn.sendall("hello\n") ------> recv
                                            conn.recv() returns b""  <----- close
                                            conn.close()
```

Notice that `accept` appears twice. It runs in a loop, and it never touches the bytes. All the
bytes flow through `conn`, the second socket, on the right-hand column.

## 5. The code, built step by step

Start with the waiter, because it is the part with the bytes in it.

```python
def serve_one(conn: socket.socket, addr: tuple[str, int]) -> None:
    print(f"connected: {addr[0]}:{addr[1]}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    print(f"closed: {addr[0]}:{addr[1]}")
```

`recv(1024)` means "give me up to 1024 bytes". It waits until at least one byte has arrived. An
empty result means the client closed its end, so the loop breaks and `with conn:` closes ours.
`sendall` is used rather than `send` because `send` may write only part of the data and return
how much it managed; `sendall` does the whole job.

Now the door.

```python
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("127.0.0.1", 9000))
listener.listen()
```

`AF_INET` means IPv4 and `SOCK_STREAM` means TCP. `SO_REUSEADDR` lets you restart the server
straight after killing it; without it, the operating system holds the port for a minute and
your second run fails to bind. `bind` takes a tuple of host and port. `listen` opens the sign.

Then the loop that seats the guests.

```python
while True:
    conn, addr = listener.accept()
    worker = threading.Thread(target=serve_one, args=(conn, addr), daemon=True)
    worker.start()
```

`accept` blocks, returns the new socket and the client's address, and the very next thing we do
is hand both to a thread and go back to `accept`. `daemon=True` means the threads die with the
program when you press Ctrl-C, instead of keeping it alive.

Save the server as `echo_server.py`. Then a client, `echo_client.py`, so you can test it without any other tool:

```python
import socket

with socket.create_connection(("127.0.0.1", 9000)) as sock:
    for line in ["hello", "one more"]:
        sock.sendall(line.encode() + b"\n")
        print("got back:", sock.recv(1024).decode().rstrip())
```

`create_connection` does the client's three steps — make a socket, connect, return it — in one
call. Sockets carry bytes, not text, so the client encodes on the way out and decodes on the
way back; that is the [day 39](../day-039-difference-arrays/README.md) distinction between
`str` and `bytes` showing up on the wire.

Run the server in one terminal:

```bash
python echo_server.py
```

and the client in a second terminal:

```bash
python echo_client.py
```

The client prints:

```text
got back: hello
got back: one more
```

The server's terminal prints:

```text
listening on 127.0.0.1:9000
connected: 127.0.0.1:63582
closed: 127.0.0.1:63582
```

The number after the colon is the client's port. The operating system picked it; it will be
different every run.

Here is the whole server again in one piece, `echo_server.py`, so you can copy it as it stands:

```python
import socket
import threading


def serve_one(conn: socket.socket, addr: tuple[str, int]) -> None:
    print(f"connected: {addr[0]}:{addr[1]}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    print(f"closed: {addr[0]}:{addr[1]}")


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("127.0.0.1", 9000))
        listener.listen()
        print("listening on 127.0.0.1:9000")
        while True:
            conn, addr = listener.accept()
            worker = threading.Thread(target=serve_one, args=(conn, addr), daemon=True)
            worker.start()


if __name__ == "__main__":
    main()
```

## 6. How the other two languages do it

**Go**

```go
listener, err := net.Listen("tcp", "127.0.0.1:9000")
for {
    conn, err := listener.Accept()
    go func() { defer conn.Close(); io.Copy(conn, conn) }()
}
```

`net.Listen` does socket, bind and listen in one call. The whole waiter is `io.Copy(conn, conn)`
because a `net.Conn` is both an `io.Reader` and an `io.Writer`, and a goroutine per connection
costs a few kilobytes rather than a full thread.

**C++**

```cpp
int fd = socket(AF_INET, SOCK_STREAM, 0);
bind(fd, reinterpret_cast<sockaddr*>(&addr), sizeof addr);
listen(fd, SOMAXCONN);
int conn = accept(fd, nullptr, nullptr);
std::thread(serve_one, conn).detach();
```

The same four names, but a socket is a plain `int` — a file descriptor — and every call returns
`-1` on failure with the reason in `errno`. Nothing closes it for you; you call `close(conn)`
or a thread leaks a descriptor.

**The difference that matters:** Python and C++ make you write `bind` and `listen` yourself
and give you a thread per client; Go folds the setup into `net.Listen` and gives you a
goroutine per client, which is why Go servers routinely hold ten thousand open connections and
a threaded Python server is sweating at a few hundred.

## 7. The traps

**The near-miss.** This looks like a server and it even works with one client:

```python
while True:
    conn, addr = listener.accept()
    serve_one(conn, addr)
```

Run two clients. The second one connects — TCP completes the handshake and puts it in the
listen queue — and then sits there, silent, until the first client closes. No error, no log
line, nothing. The interviewer's question is precisely about this: "what happens when a
*second* client connects while you are busy?" Your answer must contain the word "queue" and the
word "thread" (or "goroutine", or "event loop").

**Restarting too fast.** Kill the server and start it again within a minute without
`SO_REUSEADDR`, or start it while another copy is still running, and `bind` refuses:

```text
OSError: [Errno 98] Address already in use
```

On Windows the same failure reads:

```text
OSError: [WinError 10048] Only one usage of each socket address (protocol/network address/port) is normally permitted
```

**Nobody home.** Run the client with no server running:

```text
ConnectionRefusedError: [Errno 111] Connection refused
```

The operating system on the far side answered the knock with "nothing is listening on 9000".
That is a fast, clean failure. A firewall that silently drops the packet gives you the slow,
ugly one instead: `TimeoutError: [Errno 110] Connection timed out`, after a wait you did not
choose.

**Treating `recv` as a message.** `recv(1024)` returns *some* bytes. If the client sends
`"hello\n"` and `"one more\n"` back to back, one `recv` may return both, or half of one. TCP is
a stream of bytes with no message boundaries. The echo server does not care, because it echoes
whatever it gets. Every real protocol has to care: HTTP, which starts tomorrow on
[day 47](../day-047-minimise-the-maximum/README.md), marks the end of its headers with a blank
line and states the body's length up front, precisely so the reader knows where one message
ends.

## 8. Say it out loud

**How it gets asked**

- What happens when a client connects to your server?
- Walk me through bind, listen and accept.
- Why is there a second socket after `accept`?
- Your server handles one client at a time. What do you change?

**The ninety-second script**

The server makes a socket, binds it to an address and port so clients can find it, and calls
listen, which tells the operating system to queue incoming connections. Then it loops on
accept. When a client connects, TCP finishes the handshake in the kernel and accept returns a
new socket for that one client, plus the client's address. The listening socket carries no data
at all; it only produces connected sockets. I hand the connected socket to a thread, and the
main loop goes straight back to accept. The thread reads with recv, which returns some bytes or
an empty result when the client closes, and writes back with sendall, which keeps going until
everything has gone. When recv returns empty, the thread closes its socket and ends.

**The follow-ups**

- **Why a thread per connection and not just a loop?** *Because accept and recv both block. If
  the accept loop served clients itself, every other client would sit in the listen queue until
  the current one hung up. A thread lets the door stay open.*
- **What is the cost of a thread per connection?** *Each thread has its own stack, typically
  megabytes, so ten thousand connections means ten thousand stacks and the operating system
  scheduling all of them. Past a few thousand you move to an event loop, `asyncio` in Python,
  or to a language where the cheap unit is a goroutine.*
- **What does `recv` returning empty mean, and what does it not mean?** *It means the client
  closed its sending side. It does not mean "no data right now"; that case blocks. And a
  non-empty result is not a message, it is whatever bytes have arrived, so a real protocol needs
  a delimiter or a length prefix.*

**A model answer**

"When a client connects, the kernel completes the TCP handshake and places the connection in
the listen queue I asked for with `listen`. My `accept` call wakes up and returns a new socket
that is bound to that one client. I start a thread with that socket and go back to `accept`
immediately, so the queue never backs up. The thread loops on `recv`; it echoes each chunk
with `sendall` and stops when `recv` returns empty, which is the client hanging up. The trap is
that `recv` gives me a chunk of a stream, not a message, and that the listening socket and the
connected socket are two different objects with two different jobs."

## 9. Recall card

- `socket` → `bind(addr)` → `listen()` → loop on `accept()`.
- `accept` returns a **new** socket per client; the listener never carries data.
- `recv(n)` gives up to `n` bytes; empty means the client closed. Use `sendall`, not `send`.
- One thread per connection keeps `accept` free; blocking in the accept loop stalls every other client.
- `Address already in use` means bind lost; `Connection refused` means nobody is listening.
