---
day: 59
track: lang-go
title: "A multi-stage build to a scratch image"
theme: "Docker for each language"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 059 · Go — A multi-stage build to a scratch image

**Today's theme:** Docker for each language

**After today you can:** You can containerise a service in each language and say why the images are 1 GB, 10 MB, and 20 MB.

**The interviewer asks it as:** *Why is your Docker image so large, and how would you shrink it?*

---

## 1. What this is, and why it matters

A Go service compiles to one **static binary**: a single file with no interpreter and, with
`CGO_ENABLED=0`, no dependence on the C library of whatever machine runs it. That makes the Go
Dockerfile the simplest of the three. A **builder stage** on the `golang` image compiles the
binary; a **runtime stage** starting `FROM scratch`, an image with literally nothing in it,
copies the binary across. The result is about 10 MB, has no shell, no package manager, and no
files an attacker could use, and it starts in milliseconds.

At work this is the shape of nearly every Go service image you will meet, and the two things
that go wrong with it, a binary that needs a dynamic linker `scratch` does not have and a TLS
call that fails because there are no root certificates, are the two things this lesson shows
you breaking. In interviews, "why is your image so large" for a Go service has a crisp answer,
"it is not, it is the binary", and the interviewer will then ask you what `scratch` costs you.

## 2. The story

Meena's daughter Tara is leaving for hostel on Sunday. The trunk is on the bed, and Meena is
packing it the way she packs for a family trip: everything. Both quilts. The sewing machine,
because Tara's kurtas always need taking in. The iron. Six pairs of shoes. The big steel tiffin
set. By four o'clock the trunk will not close, and the taxi driver, when he sees it, says he
will need to make two trips and charge for both.

Tara sits down next to it and starts taking things out. "I need the kurtas. I do not need the
sewing machine. Take them in tonight, here, with your machine, and I take only the kurtas." The
iron goes back; the hostel has one on every floor. Four pairs of shoes go back. The tiffin set
goes back; there is a mess hall. What is left is a small bag: the clothes, already altered, a
pair of shoes, a phone charger, a towel.

Meena has one more thing. She reaches into her handbag for the key ring with every key on it,
the flat, the scooter, the storeroom, her mother's house, and starts to hand it over. Tara
laughs and takes just the one key, the one for her hostel room. "If I lose this, I have lost a
room. If I lose that, you have lost everything."

On Sunday the taxi takes one trip. The bag fits under the seat. Tara texts from the hostel that
evening: the room has a bed, a desk, and a plug socket, and that is all it has, and it is enough.
Meena keeps the sewing machine. It was always going to stay with her; it was the thing that
made the clothes fit, not the thing Tara needed to wear them.

## 3. The idea in plain English

The sewing machine is the Go toolchain. `golang:1.23` is about 800 MB: the compiler, the
standard library source, git, and a full Debian underneath. You need every bit of it to build
the binary and none of it to run the binary. So the build happens in a first stage on that
image, and only the output crosses to the second stage.

The bag that fits under the seat is `FROM scratch`. Scratch is not a small operating system; it
is an empty directory. No `/bin/sh`, no `ls`, no `/etc/passwd`, no C library. The only thing in
the final image is what you `COPY` into it, and for Go that can be one file, because
`CGO_ENABLED=0 go build` produces a binary that carries its own runtime and makes system calls
directly. On [day 44](../day-044-first-and-last-occurrence/README.md) you built such a binary;
today you find out what it is for.

The room with a bed and a socket is what the service finds at run time. Two things are missing
that it might need. Root certificates, `/etc/ssl/certs/ca-certificates.crt`, if it makes any
HTTPS call; copy them from the builder. And time zone data, if it formats times in a zone;
either copy `/usr/share/zoneinfo` or import `time/tzdata` so the binary carries its own.

The single key is `USER 65534:65534`. Scratch has no `/etc/passwd`, so you cannot `useradd`; you
give a numeric id, and 65534 is the conventional "nobody". Every process in the container then
runs without root, in an image where there is nothing to be root of anyway.

## 4. The picture

```text
  stage 1: builder (golang:1.23, ~800 MB)          stage 2: runtime (scratch, 0 bytes)
  +----------------------------------------+       +----------------------------------+
  | /usr/local/go/   compiler, stdlib src  |       | /server            (~9 MB)       |
  | /go/pkg/mod/     downloaded modules    |       | /etc/ssl/certs/ca-certificates.crt
  | /src/            your code             | ----> |                   (~200 KB)      |
  | /out/server  <- CGO_ENABLED=0 go build |       | USER 65534:65534                 |
  | /etc/ssl/certs/ca-certificates.crt     |       | ENTRYPOINT ["/server"]           |
  +----------------------------------------+       +----------------------------------+
        thrown away after the build                   ~9 MB, no shell, no libc
```

Notice there are two arrows this time. The binary is obvious; the certificates are the thing
people forget until the first HTTPS call fails in production. And notice what is not on the
right: no `/lib`, because `CGO_ENABLED=0` means the binary asks for no shared library.

## 5. The code, built step by step

The service, `main.go`, cut to a health route and one outbound HTTPS call so the certificate
point is demonstrable:

```go
package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, `{"status":"ok"}`)
	})
```

The outbound route calls a real HTTPS address and reports the status, which is what will break
without certificates.

```go
	mux.HandleFunc("GET /outbound", func(w http.ResponseWriter, r *http.Request) {
		resp, err := http.Get("https://example.com/")
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadGateway)
			return
		}
		defer resp.Body.Close()
		fmt.Fprintf(w, `{"upstream":%d}`+"\n", resp.StatusCode)
	})
	log.Fatal(http.ListenAndServe("0.0.0.0:8000", mux))
}
```

`0.0.0.0`, not `127.0.0.1`: inside a container, loopback is the container's own, and the port
mapping cannot reach a server bound to it.

Now the `Dockerfile`. The builder stage, with the module files copied first so `go mod download`
is cached until they change.

```dockerfile
FROM golang:1.23 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
```

The build line. `CGO_ENABLED=0` is the whole point; `-ldflags="-s -w"` strips the symbol table
and debug information, which is a third of the size for free.

```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /out/server .
```

The runtime stage. Scratch, the certificates, the binary, the numeric user, and the entrypoint.

```dockerfile
FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /out/server /server
USER 65534:65534
EXPOSE 8000
ENTRYPOINT ["/server"]
```

`ENTRYPOINT` in the JSON form, because there is no shell in scratch to parse a string form.

Build it:

```bash
docker build -t pricer-go .
docker images pricer-go
```

```text
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
pricer-go    latest    7b2d9e4f1a6c   9 seconds ago    9.41MB
```

Run it, and call both routes:

```bash
docker run --rm -p 8000:8000 pricer-go
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/outbound
```

```text
{"status":"ok"}
{"upstream":200}
```

Try to open a shell in it, to see what scratch means:

```bash
docker run --rm -it pricer-go /bin/sh
```

```text
docker: Error response from daemon: failed to create task for container: failed to create shim
task: OCI runtime create failed: runc create failed: unable to start container process: exec:
"/bin/sh": stat /bin/sh: no such file or directory: unknown.
```

There is no shell. That is the security property, and also the debugging cost; §7 has the
trade. Here is the whole `Dockerfile`:

```dockerfile
FROM golang:1.23 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /out/server .

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /out/server /server
USER 65534:65534
EXPOSE 8000
ENTRYPOINT ["/server"]
```

## 6. How the other two languages do it

**Python**

```dockerfile
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY app.py ./

FROM python:3.12-slim
RUN useradd --create-home --uid 1000 app
COPY --from=builder --chown=app:app /app /app
USER app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

Python cannot be one file. The runtime stage must contain the interpreter and every installed
package, so the floor is `python:3.12-slim` at about 130 MB, and the user is made with `useradd`
because the image has an `/etc/passwd` to add to.

**C++**

```dockerfile
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends g++ cmake ninja-build git
COPY . /src
RUN cmake -S /src -B /build -DCMAKE_BUILD_TYPE=Release && cmake --build /build

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /build/server /server
ENTRYPOINT ["/server"]
```

C++ is a binary too, but a dynamically linked one that needs `libstdc++` and `libc`. So the
runtime is `distroless/cc`, which is scratch plus exactly those libraries, and the builder and
runtime must be the same Debian so the library versions match.

**The difference that matters:** Go is the only one of the three that can run in a truly empty
image, because `CGO_ENABLED=0` makes the binary independent of any C library. Python needs an
interpreter and C++ needs a runtime library, and both therefore need a base image, a package
manager somewhere in the chain, and a matching version story. Go's image is the binary plus
whatever data files you remember to copy, and the two you forget are certificates and time zones.

## 7. The traps

**The near-miss: forgetting `CGO_ENABLED=0`.** The Dockerfile builds. The image is the right
size. Then:

```bash
docker run --rm -p 8000:8000 pricer-go
```

```text
exec /server: no such file or directory
```

The file is there. What is missing is `/lib64/ld-linux-x86-64.so.2`, the dynamic linker the
binary was built to ask for, because with cgo on, `net` and `os/user` link against libc. This
error message is famous for being wrong about what is missing. `CGO_ENABLED=0`, and check with
`ldd server` in the builder, which should say `not a dynamic executable`.

**No certificates.** Leave out the `ca-certificates.crt` copy and `/health` works, `/outbound`
does not:

```text
Get "https://example.com/": tls: failed to verify certificate: x509: certificate signed by unknown authority
```

There are no root certificates in scratch, so no HTTPS server can be verified. Copy the bundle
from the builder, as the lesson does.

**No time zone data.** `time.LoadLocation("Asia/Kolkata")` in scratch:

```text
unknown time zone Asia/Kolkata
```

Either `COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo` or add
`import _ "time/tzdata"` to the binary, which embeds the data at a cost of about 450 KB.

**A string-form `ENTRYPOINT`.** `ENTRYPOINT /server` is run as `/bin/sh -c "/server"`, and there
is no `/bin/sh`:

```text
docker: Error response from daemon: ... exec: "/bin/sh": stat /bin/sh: no such file or directory
```

Always the JSON array form in scratch.

**Debugging a container with no shell.** You cannot `docker exec -it ... sh` into scratch. The
answers are: `docker cp` files out; `docker run --rm -it --pid container:<id> busybox` to look
at it from a sidecar; or use `gcr.io/distroless/static:debug`, which is scratch plus busybox,
for the staging environment only. Do not put a shell in the production image to make debugging
easier; that is the trade you chose scratch for.

**`COPY . .` with `.git` and the local binary in it.** The builder stage's `COPY . .` sends your
whole directory as the build context, and a stale locally built `server` or a large `.git` makes
every build slow. A `.dockerignore` with `.git`, `*.exe`, and the output name, before the first
build.

## 8. Say it out loud

**How it gets asked**

- Why is your Docker image so large, and how would you shrink it?
- What is `FROM scratch`, and what does it not contain?
- Why do you set `CGO_ENABLED=0` when building for a container?
- What breaks when you move a Go service into a scratch image?

**The ninety-second script**

A Go service image should be about the size of the binary, and mine is: a multi-stage build,
`golang:1.23` as the builder stage where I `go mod download` with the module files copied first
so it caches, then `CGO_ENABLED=0 go build -ldflags="-s -w"` for a static, stripped binary,
and then `FROM scratch` with the binary copied in, which is an empty image with nothing but
what I copy. That is nine or ten megabytes. `CGO_ENABLED=0` is the line that matters: with cgo
on, the binary asks for the C library's dynamic linker, scratch has none, and the container dies
with a misleading "no such file or directory". The two things scratch does not give you are
root certificates, which I copy from the builder so HTTPS calls verify, and time zone data,
which I embed with `time/tzdata`. I run as `USER 65534:65534`, numeric because there is no
`/etc/passwd`, and the entrypoint is the JSON form because there is no shell to parse a string.
The cost is that there is no shell to debug with either, which is a feature in production and a
nuisance in staging, where I use the distroless debug variant.

**The follow-ups**

- **Why not `alpine` instead of `scratch`?** *Alpine gives you a shell and a package manager for
  about 5 MB, which is convenient and is also an attack surface. If the binary is static, scratch
  or distroless/static is the smaller and safer choice; alpine when you genuinely need `sh` in
  the image.*
- **What is `-s -w`?** *`-s` omits the symbol table and `-w` omits DWARF debug information. Stack
  traces still work, because they use the runtime's own tables; only debuggers lose out. About a
  third off the binary.*
- **How do you get the SQLite service from day 53 into scratch?** *The driver there was
  `modernc.org/sqlite`, pure Go, so `CGO_ENABLED=0` works. A cgo driver such as `mattn/go-sqlite3`
  would force cgo on, and then you need distroless/cc or a base with libc, like the C++ image.*

**A model answer**

"It is not large; it is the binary. Two stages: `golang:1.23` builds with `CGO_ENABLED=0` and
`-ldflags='-s -w'`, and `FROM scratch` copies in `/server` and `/etc/ssl/certs/ca-certificates.crt`.
Under ten megabytes, no shell, no libc, `USER 65534:65534`, JSON-form `ENTRYPOINT`. The three
things that break moving into scratch are cgo, which I turn off; HTTPS verification, which I fix
by copying the certificate bundle; and time zones, which I embed with `time/tzdata`. If I ever
need a cgo dependency, I move to distroless/cc and accept twenty megabytes."

## 9. Recall card

- Builder `golang:1.23`: `COPY go.mod go.sum` then `go mod download` before `COPY . .`; build with `CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /out/server .`
- Runtime `FROM scratch`: empty, no shell, no libc, no `/etc/passwd`. Copy `/server`, use `USER 65534:65534`, and the JSON-form `ENTRYPOINT ["/server"]`.
- `exec /server: no such file or directory` with the file present means cgo was on and the dynamic linker is missing; `ldd` should say `not a dynamic executable`.
- Copy `/etc/ssl/certs/ca-certificates.crt` from the builder or HTTPS fails with `x509: certificate signed by unknown authority`; embed `time/tzdata` or `LoadLocation` fails.
- Image is ~9 MB; about 800 MB of toolchain stays in the builder. A cgo dependency forces distroless/cc instead of scratch.
