---
day: 46
track: lang-cpp
title: "POSIX sockets, or Boost.Asio, and one thread per connection"
theme: "TCP sockets: an echo server"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 046 · C++ — POSIX sockets, or Boost.Asio, and one thread per connection

**Today's theme:** TCP sockets: an echo server

**After today you can:** You can write a server that accepts a connection and echoes bytes back, in each language, and test it with a client.

**The interviewer asks it as:** *What happens when a client connects to your server?*

---

## 1. What this is, and why it matters

C++ has no networking in its standard library, so on Linux and macOS you call the operating
system directly through the POSIX socket functions: `socket`, `bind`, `listen`, `accept`,
`read`, `write`, `close`. A socket is an `int`, a file descriptor, the same kind of number the
operating system uses for open files. An echo server makes one, binds it to a port, accepts
clients, and gives each one a thread that writes back whatever it reads.

Python's `socket` module and Go's `net` package are thin wrappers over these exact calls, so
this lesson is where you see what they were hiding. Interviewers who ask "what happens when a
client connects" are pleased when the answer includes the words "file descriptor" and "listen
queue", because those are the operating system's words. Boost.Asio is the library most real C++
services use instead of raw POSIX; the lesson shows the raw calls first, because Asio only makes
sense once you know what it is wrapping.

## 2. The story

Meera opens a small eatery on the corner of a busy road. Before anyone can visit, she needs
one thing: a street number. She fills in the council's form, and the clerk gives her a
numbered ticket for the building. From now on every request about the place goes through that
ticket number. Painting the number above the door is a second form. Flipping the sign to open
is a third. Nothing here happens by itself, and every form can come back stamped refused, with
a reason scrawled in the margin.

Her cousin Arjun stands at the door. When a family arrives, he does not take their order. He
walks them to an empty table, and the council gives that table its own ticket number too, and
he goes straight back to the door, because there is already a second group behind them.

Each table gets its own waiter. The waiter does something slightly odd. Whatever the customer
says, the waiter says back, word for word. "Two plates of rice." "Two plates of rice." The
customers hear at once if something was misheard.

Here is the part Meera learns the hard way. When a family leaves, the waiter has to hand the
table's ticket back to the council. If he forgets, the council believes the table is still in
use, and after a busy month the council tells Meera she has used up her allowance of tickets
and refuses to give her any more. Nothing has gone wrong at any single table. Every one of them
was simply never handed back.

One evening a second cook tries to open a stall at number forty-two as well. His form comes
back stamped refused, address already in use. And when a customer knocks at nine at night after
the sign has been flipped to closed, nobody answers. She waits a moment, then walks away.

## 3. The idea in plain English

The council ticket is a **file descriptor**: a small `int` that the operating system hands you
and that you pass back to it on every later call. `socket(AF_INET, SOCK_STREAM, 0)` gets one.
`AF_INET` is IPv4 and `SOCK_STREAM` is TCP.

Every form is a call that returns `-1` on failure and puts the reason in a global called
`errno`. `perror("bind")` prints that reason as text. There are no exceptions here; this is C's
error style, older than the `std::expected` you met on
[day 9](../day-009-what-an-array-is/README.md), and you must check every return value
yourself.

`bind` attaches the address to the descriptor. The address lives in a `sockaddr_in` struct that
you fill in by hand: the family, the port, and the IP. Two of those need converting to network
byte order with `htons` and `inet_pton`, because the network agreed long ago on big-endian and
your CPU probably did not.

`listen` opens the sign and sets the queue length. `accept` blocks until a client has finished
the TCP handshake and returns **a second descriptor**, the table's own ticket, for that client
alone. The listening descriptor never carries data.

The waiter is a thread that loops on `read` and `write`. `read` returns how many bytes it got,
`0` when the client closed, and `-1` on error. Handing the ticket back is `close(fd)`. Nothing
does it for you: no destructor, no `with`, no `defer`. Forget it and the process runs out of
descriptors, which is the story's allowance.

## 4. The picture

```text
   descriptor table of the server process

   fd  what it is
   --  --------------------------------
    0  stdin
    1  stdout
    2  stderr
    3  listening socket   <- socket(); bind(); listen()
    4  client A           <- accept() returned this, thread 1 owns it
    5  client B           <- accept() returned this, thread 2 owns it
    6  client C           <- accept() returned this, thread 3 owns it
   ...
 1023  (limit: after this, accept() fails with EMFILE)
```

Notice that the listening socket is one row and never changes; every client is a new row.
`close(fd)` frees the row. A thread that returns without `close` leaves the row occupied for
the life of the process.

## 5. The code, built step by step

The includes, and the waiter.

```cpp
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <thread>
```

`<sys/socket.h>` has `socket`, `bind`, `listen`, `accept`. `<arpa/inet.h>` has `htons` and
`inet_pton`. `<unistd.h>` has `read`, `write`, `close`. These are C headers from the operating
system, not from C++, which is why they have no `std::`.

```cpp
void serve_one(int client) {
    char buffer[1024];
    while (true) {
        ssize_t got = read(client, buffer, sizeof buffer);
        if (got <= 0) break;
        write(client, buffer, got);
    }
    close(client);
}
```

`read` fills up to 1024 bytes of the buffer and returns how many. Zero means the client closed;
negative means an error; both end the loop. `write` sends back exactly `got` bytes, not the
whole buffer. Then `close`, the line this lesson exists for.

Now the descriptor and the address.

```cpp
int listener = socket(AF_INET, SOCK_STREAM, 0);
int yes = 1;
setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof yes);

sockaddr_in addr{};
addr.sin_family = AF_INET;
addr.sin_port = htons(9000);
inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
```

`sockaddr_in addr{}` zeroes the struct first, which matters because it has padding fields.
`htons` converts the port to network byte order. `inet_pton` turns the dotted text into the
four bytes of the IP. `SO_REUSEADDR` lets you restart the server straight after killing it.

The three forms, each checked.

```cpp
if (bind(listener, reinterpret_cast<sockaddr*>(&addr), sizeof addr) == -1) {
    perror("bind");
    return 1;
}
if (listen(listener, SOMAXCONN) == -1) {
    perror("listen");
    return 1;
}
```

`bind` wants a pointer to the generic `sockaddr`, and `sockaddr_in` is the IPv4-specific one, so
the cast is required; it is the one place in this file where C++ has to talk C's dialect.
`SOMAXCONN` asks for the largest listen queue the system allows.

Then the loop that seats the guests.

```cpp
while (true) {
    int client = accept(listener, nullptr, nullptr);
    if (client == -1) {
        perror("accept");
        continue;
    }
    std::thread(serve_one, client).detach();
}
```

The two `nullptr`s mean "I do not need the client's address". `std::thread(...).detach()`
starts the waiter and lets it run on its own; the loop goes straight back to `accept`. A
`std::jthread` from [day 31](../day-031-fixed-window/README.md) would be wrong here, and §7
says why.

Save this as `echo_server.cpp`:

```cpp
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <thread>

void serve_one(int client) {
    std::cout << "connected: fd " << client << "\n";
    char buffer[1024];
    while (true) {
        ssize_t got = read(client, buffer, sizeof buffer);
        if (got <= 0) break;
        write(client, buffer, got);
    }
    close(client);
    std::cout << "closed: fd " << client << "\n";
}

int main() {
    int listener = socket(AF_INET, SOCK_STREAM, 0);
    if (listener == -1) {
        perror("socket");
        return 1;
    }
    int yes = 1;
    setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof yes);

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(9000);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);

    if (bind(listener, reinterpret_cast<sockaddr*>(&addr), sizeof addr) == -1) {
        perror("bind");
        return 1;
    }
    if (listen(listener, SOMAXCONN) == -1) {
        perror("listen");
        return 1;
    }
    std::cout << "listening on 127.0.0.1:9000\n";

    while (true) {
        int client = accept(listener, nullptr, nullptr);
        if (client == -1) {
            perror("accept");
            continue;
        }
        std::thread(serve_one, client).detach();
    }
}
```

And a client, `echo_client.cpp`:

```cpp
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <string>

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(9000);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
    if (connect(sock, reinterpret_cast<sockaddr*>(&addr), sizeof addr) == -1) {
        perror("connect");
        return 1;
    }
    for (std::string line : {"hello\n", "one more\n"}) {
        write(sock, line.data(), line.size());
        char buffer[1024];
        ssize_t got = read(sock, buffer, sizeof buffer);
        std::cout << "got back: " << std::string(buffer, got);
    }
    close(sock);
}
```

The client fills in the same `sockaddr_in` and calls `connect` where the server called `bind`.
Compile and run the server in one terminal, on Linux or macOS:

```bash
g++ -std=c++20 -pthread echo_server.cpp -o echo_server
./echo_server
```

and the client in a second terminal:

```bash
g++ -std=c++20 echo_client.cpp -o echo_client
./echo_client
```

The client prints:

```text
got back: hello
got back: one more
```

The server's terminal prints:

```text
listening on 127.0.0.1:9000
connected: fd 4
closed: fd 4
```

Run the client again and the server prints `fd 4` again: the number was handed back by
`close`, so the operating system reuses it. That is the visible proof that the waiter returned
the ticket.

**If you would rather use Boost.Asio.** The same server in Asio hides the struct-filling and
the byte-order calls, and gives you objects that close themselves:

```cpp
boost::asio::io_context io;
boost::asio::ip::tcp::acceptor acceptor(io, {boost::asio::ip::tcp::v4(), 9000});
while (true) {
    boost::asio::ip::tcp::socket client = acceptor.accept();
    std::thread([s = std::move(client)]() mutable {
        boost::system::error_code ec;
        char buffer[1024];
        while (std::size_t got = s.read_some(boost::asio::buffer(buffer), ec))
            boost::asio::write(s, boost::asio::buffer(buffer, got));
    }).detach();
}
```

The `acceptor` is the listening socket, and `accept()` returns a `tcp::socket` whose
destructor calls `close` for you. The reason to learn the POSIX version first is that every
name in this snippet — acceptor, accept, socket, read, write — is the POSIX call with a
class around it.

## 6. How the other two languages do it

**Python**

```python
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("127.0.0.1", 9000))
listener.listen()
while True:
    conn, addr = listener.accept()
    threading.Thread(target=serve_one, args=(conn, addr), daemon=True).start()
```

The same names, one for one: `AF_INET` and `SOCK_STREAM` are the same constants, `bind` takes a
tuple instead of a struct, and a failure raises `OSError` instead of returning `-1`. `with conn:`
closes the socket when the block ends.

**Go**

```go
listener, err := net.Listen("tcp", "127.0.0.1:9000")
for {
    conn, err := listener.Accept()
    go func() { defer conn.Close(); io.Copy(conn, conn) }()
}
```

Socket, bind and listen collapse into `net.Listen`. The conn is an object with a `Close` method,
`defer` guarantees it runs, and the waiter is a goroutine rather than an operating-system
thread.

**The difference that matters:** In C++ the connected socket is a bare `int` and nothing
closes it for you, so a thread that returns without `close(client)` leaks a descriptor
silently; Python's `with` and Go's `defer` make the close a habit the language enforces, and
Asio gives C++ the same habit through a destructor.

## 7. The traps

**The near-miss: `std::jthread`.** Day 31 taught you that `jthread` is the safe one because it
joins in its destructor. So you write:

```cpp
std::jthread(serve_one, client);
```

It compiles and the first client works. The temporary `jthread` is destroyed at the end of that
statement, its destructor joins, and the accept loop is now stuck inside `serve_one` until the
first client hangs up. The second client sits in the listen queue, silent. The safe default is
wrong here precisely because you want the thread to outlive the line that started it, which is
what `detach` means.

**Forgetting the cast.** Pass `&addr` to `bind` directly:

```text
echo_server.cpp:29:24: error: cannot convert 'sockaddr_in*' to 'const sockaddr*'
   29 |     if (bind(listener, &addr, sizeof addr) == -1) {
      |                        ^~~~~
      |                        |
      |                        sockaddr_in*
```

The C interface takes the generic type, and C++ will not convert between struct pointers on its
own. The `reinterpret_cast` is the honest way to say "I know these have the same first bytes".

**Forgetting `<unistd.h>`.**

```text
echo_server.cpp:17:9: error: 'close' was not declared in this scope
   17 |         close(client);
      |         ^~~~~
```

`read`, `write` and `close` live there, not in `<sys/socket.h>`, and the compiler does not
guess.

**Port already taken.** Start the server twice:

```text
bind: Address already in use
```

That is `perror` at work: your label, a colon, then `strerror(errno)`.

**Nobody home.** Run the client with no server:

```text
connect: Connection refused
```

**Forgetting `close(client)`.** The server keeps working. Then, some thousands of clients later:

```text
accept: Too many open files
```

Every leaked descriptor occupies a row in the table from §4, and the default limit on Linux is
1024. This bug never shows up in testing with one client, which is why the interview follow-up
about it is a good one.

## 8. Say it out loud

**How it gets asked**

- What happens when a client connects to your server?
- What is a file descriptor, and why does `accept` return a new one?
- Why is the socket an `int` and not an object?
- Your server dies after a day with "too many open files". What happened?

**The ninety-second script**

I call `socket` and get a file descriptor, a small integer the kernel uses to name the socket.
I fill in a `sockaddr_in` with the family, the port in network byte order, and the IP, and call
`bind` to attach it. `listen` puts the socket in the listening state with a queue. Then I loop
on `accept`, which blocks until a client has completed the TCP handshake and returns a second
descriptor for that client alone. I start a detached thread with that descriptor and go
straight back to `accept`. The thread loops on `read`, which returns the byte count, zero when
the client closes, or minus one on error, and writes each chunk back with `write`. When `read`
returns zero it calls `close` on the descriptor, and that is the line that matters, because
nothing else will do it.

**The follow-ups**

- **Why `detach` and not `join`?** *A join would block the accept loop until that client
  finished, so every other client would wait in the listen queue. Detach lets the thread
  outlive the statement that created it. A `jthread` joins in its destructor and so has the
  same bug as an explicit join.*
- **What is the cost of a thread per client?** *Each thread gets its own stack, eight
  megabytes by default on Linux, and the kernel schedules all of them. A few thousand is fine;
  tens of thousands is not, and that is when you move to Asio's asynchronous mode or `epoll`,
  where one thread waits on many descriptors at once.*
- **What does "too many open files" have to do with sockets?** *Sockets are file descriptors
  and share the same per-process limit as open files. A thread that returns without `close`
  leaks one per client, and the leak surfaces as `accept` failing with `EMFILE`, hours after
  the bug ran.*

**A model answer**

"When a client connects, the kernel completes the handshake and queues the connection on the
listening descriptor. My `accept` returns a fresh descriptor for that client; the listening one
never carries data. I hand the new descriptor to a detached thread and return to `accept`
immediately. The thread reads and writes on its descriptor until `read` returns zero, then
closes it. Two things I always check: every call's `-1` return with `perror`, and that every
path out of the handler closes the descriptor, because a socket is an `int` with no
destructor. In production I would use Boost.Asio, which wraps exactly these calls in objects
that close themselves and can multiplex many connections on one thread."

## 9. Recall card

- A socket is an `int` file descriptor; every call returns `-1` on failure and sets `errno`. Check it.
- `socket` → fill `sockaddr_in` with `htons` and `inet_pton` → `bind` (with the `sockaddr*` cast) → `listen` → loop `accept`.
- `accept` returns a new descriptor per client; the listener never carries data.
- `std::thread(serve_one, client).detach()`; a `jthread` here joins and stalls the accept loop.
- `read` returns 0 on hang-up; then `close(client)`, or the leak ends in `accept: Too many open files`.
