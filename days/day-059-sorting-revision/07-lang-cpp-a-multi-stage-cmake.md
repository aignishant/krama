---
day: 59
track: lang-cpp
title: "A multi-stage CMake build to a distroless image"
theme: "Docker for each language"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 059 · C++ — A multi-stage CMake build to a distroless image

**Today's theme:** Docker for each language

**After today you can:** You can containerise a service in each language and say why the images are 1 GB, 10 MB, and 20 MB.

**The interviewer asks it as:** *Why is your Docker image so large, and how would you shrink it?*

---

## 1. What this is, and why it matters

A C++ service compiles to a binary, but unless you go out of your way it is a **dynamically
linked** binary: it expects to find `libstdc++`, `libgcc`, and the C library on the machine at
run time. So the C++ image has the same two-stage shape as Go's, a builder with the compiler and
CMake, and a runtime with only the output, but the runtime cannot be empty. It is
**distroless/cc**: an image containing exactly those three runtime libraries and a set of
certificates, with no shell, no package manager, and a non-root user already defined. The
binary plus that base is about 20 MB.

At work, C++ services in containers are common in trading, telecoms, games, and anywhere latency
is the product, and the image is where the "works on my machine" problems concentrate, because
the builder and the runtime must agree on the C library version. In interviews, "why is your
image so large" for C++ leads straight to "what is in your image that is not your binary", and
the answer is a short list you should be able to recite.

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

The sewing machine is `g++`, CMake, Ninja, and git. Together with the Debian they sit on, the
builder stage is about 600 MB, and every byte of it is needed to compile and none to run. The
first `FROM` installs them and builds; the second `FROM` never sees them.

The iron on every floor is the runtime library. Tara does not pack an iron because the hostel
provides one; your binary does not carry `libstdc++.so.6` because the runtime image provides
it. That is what **distroless/cc** is: a base with `libc`, `libstdc++`, `libgcc`, a certificate
bundle, and a time zone database, and nothing else. No shell, no `apt`, no `ls`. The `cc` in
the name means "C and C++ runtime".

The catch is that the iron has to fit the plug. A binary built against one version of the C
library asks for symbols by version, and a runtime image with an older library refuses it. So
the builder is `debian:bookworm-slim` and the runtime is `distroless/cc-debian12`, and those
are the same Debian, twelve, by two names. Change one without the other and the binary will
not start.

The single key is the `:nonroot` tag. Distroless images ship with a user named `nonroot`, uid
65532, and the `nonroot` variant of the tag makes it the default. No `useradd`, because there is
no `useradd`; the user is baked in.

The clothes already altered are the CMake layers: `CMakeLists.txt` and the dependency fetch
first, your sources after, so an edit to `main.cpp` does not re-download cpp-httplib.

## 4. The picture

```text
  stage 1: builder (debian:bookworm-slim + g++, cmake)     stage 2: runtime (distroless/cc-debian12:nonroot)
  +------------------------------------------------+       +----------------------------------------+
  | /usr/bin/g++, cmake, ninja, git   (~500 MB)    |       | /lib/x86_64-linux-gnu/libc.so.6        |
  | /src/CMakeLists.txt, src/main.cpp              |       | /usr/lib/x86_64-linux-gnu/libstdc++.so.6
  | /build/_deps/  fetched cpp-httplib, json       | ----> | /lib/x86_64-linux-gnu/libgcc_s.so.1    |
  | /build/server  <- cmake --build (Release)      |       | /etc/ssl/certs/, /usr/share/zoneinfo   |
  | /lib/x86_64-linux-gnu/libc.so.6  (glibc 2.36)  |       | /server  (~2 MB)   USER nonroot (65532)|
  +------------------------------------------------+       +----------------------------------------+
        thrown away after the build                            ~22 MB, no shell, same glibc 2.36
```

Notice `libc.so.6` appears on both sides with the same version. That equality is the contract
between the stages, and it is why the two `FROM` lines name the same Debian. The binary itself is
the small thing; the libraries it borrows are most of the twenty megabytes.

## 5. The code, built step by step

The service, `src/main.cpp`, the day 48 server cut to a health route:

```cpp
#include <httplib.h>

int main() {
    httplib::Server svr;
    svr.Get("/health", [](const httplib::Request&, httplib::Response& res) {
        res.set_content(R"({"status":"ok"})", "application/json");
    });
    return svr.listen("0.0.0.0", 8000) ? 0 : 1;
}
```

`0.0.0.0` so the port mapping can reach it; loopback inside a container is the container's own.

`CMakeLists.txt`, fetching cpp-httplib the way [day 48](../day-048-binary-search-on-floats/README.md)
did:

```cmake
cmake_minimum_required(VERSION 3.20)
project(server CXX)
set(CMAKE_CXX_STANDARD 20)
include(FetchContent)
FetchContent_Declare(httplib GIT_REPOSITORY https://github.com/yhirose/cpp-httplib GIT_TAG v0.18.3)
FetchContent_MakeAvailable(httplib)
add_executable(server src/main.cpp)
target_link_libraries(server PRIVATE httplib::httplib)
```

Now the `Dockerfile`. The builder installs the tools in one `RUN`, with the apt cache cleaned in
the same line so it never lands in a layer.

```dockerfile
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        g++ cmake ninja-build git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
```

`ca-certificates` is there for git to fetch cpp-httplib over HTTPS, not for the service.

Configure before copying sources. The configure step is what runs `FetchContent`, so with
`CMakeLists.txt` copied alone first, the download is cached until that file changes.

```dockerfile
COPY CMakeLists.txt ./
RUN mkdir -p src && echo 'int main(){}' > src/main.cpp \
    && cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
COPY src ./src
RUN cmake --build build
```

The placeholder `main.cpp` exists only so configure succeeds; the real one replaces it on the
next line. `Release` turns on optimisation and turns off the asserts and debug information that
make a binary large.

The runtime stage: distroless, the binary, done.

```dockerfile
FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /src/build/server /server
EXPOSE 8000
ENTRYPOINT ["/server"]
```

No `USER` line, because `:nonroot` already set it. JSON-form `ENTRYPOINT`, because there is no
shell.

Build and inspect:

```bash
docker build -t pricer-cpp .
docker images pricer-cpp
```

```text
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
pricer-cpp   latest    2e8a6c4d0f91   14 seconds ago   22.7MB
```

Run it, call it, and check the user:

```bash
docker run --rm -p 8000:8000 pricer-cpp
curl -s http://127.0.0.1:8000/health
docker inspect pricer-cpp --format '{{.Config.User}}'
```

```text
{"status":"ok"}
nonroot
```

To see where the twenty megabytes go, build only the first stage with `--target` and ask it what
the binary needs:

```bash
docker build --target builder -t pricer-cpp-builder .
docker run --rm pricer-cpp-builder ldd /src/build/server
```

```text
        linux-vdso.so.1 (0x00007ffd3b5f2000)
        libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f2c1a400000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f2c1a8d3000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f2c1a21f000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f2c1a140000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f2c1a90c000)
```

Every line there is a file distroless/cc provides and scratch would not. Here is the whole
`Dockerfile`:

```dockerfile
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        g++ cmake ninja-build git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY CMakeLists.txt ./
RUN mkdir -p src && echo 'int main(){}' > src/main.cpp \
    && cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
COPY src ./src
RUN cmake --build build

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /src/build/server /server
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

Python's runtime stage must hold the interpreter and every package, so its floor is about
130 MB before the code; the tools stay behind but the language cannot.

**Go**

```dockerfile
FROM golang:1.23 AS builder
COPY . /src
RUN cd /src && CGO_ENABLED=0 go build -ldflags="-s -w" -o /out/server .

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /out/server /server
USER 65534:65534
ENTRYPOINT ["/server"]
```

Go's binary is static, so its runtime is empty: no libraries to provide, no version to match,
and even the certificates have to be copied by hand.

**The difference that matters:** C++ is the one where the two stages must agree on the C
library. Go sidesteps it with a static binary, and Python's interpreter and packages come from
one image so they agree by construction; C++ builds on one Debian and runs on a distroless of
the same Debian, and the day someone bumps the builder to a newer release without bumping the
runtime, the binary stops at start-up with a `GLIBC_2.38 not found`. That pairing is the thing
to say out loud.

## 7. The traps

**The near-miss: `distroless/static` instead of `distroless/cc`.** It is smaller and it is what
the Go lesson would use. The build succeeds; the run does not:

```text
/server: error while loading shared libraries: libstdc++.so.6: cannot open shared object file: No such file or directory
```

The `static` variant has no C++ runtime. Either use `cc`, or link the runtime in with
`-static-libstdc++ -static-libgcc` and accept a larger binary.

**A builder newer than the runtime.** Change the builder to `debian:trixie-slim` and keep
`cc-debian12`:

```text
/server: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.38' not found (required by /server)
```

The binary asks for a symbol version the older library does not have. Same Debian on both
lines, always. The other direction, an older builder and a newer runtime, works, because
glibc is backwards compatible; it is only the forward direction that fails.

**Forgetting `--no-install-recommends`.** `apt-get install g++ cmake` without it pulls in
documentation and suggested packages, and the builder grows by hundreds of megabytes. It does
not change the final image, but it makes every cold build slower, and someone will eventually
copy the pattern into a runtime stage.

**Debug build in the image.** Leave out `-DCMAKE_BUILD_TYPE=Release` and the binary is built
without optimisation and with full debug information; ten times slower and several times
larger. Release in the Dockerfile, Debug on your machine.

**Trying to shell in.** `docker exec -it <id> sh` on distroless:

```text
OCI runtime exec failed: exec failed: unable to start container process: exec: "sh": executable file not found in $PATH: unknown
```

Use the `:debug` tag of distroless in staging, which adds busybox, or `docker cp` and inspect
from outside. Do not add a shell to production for convenience.

**The service writing to disk.** As `nonroot`, `std::ofstream("data.txt")` in `/` fails
silently unless you check `is_open()`. Write to a directory you created and `chown`ed in the
Dockerfile, or to a mounted volume, and check the stream.

## 8. Say it out loud

**How it gets asked**

- Why is your Docker image so large, and how would you shrink it?
- What is a distroless image, and why not just use scratch for C++?
- Why do the builder and runtime stages need the same base?
- What is actually in your final image besides your binary?

**The ninety-second script**

The compile toolchain is most of a C++ image if you let it in, so I use a multi-stage build.
The builder is `debian:bookworm-slim` with `g++`, CMake, Ninja, and git installed in one `RUN`
with `--no-install-recommends` and the apt lists removed. I copy `CMakeLists.txt` and configure
first, so the `FetchContent` download is cached, then copy the sources and build in Release.
The runtime is `gcr.io/distroless/cc-debian12:nonroot`: `libc`, `libstdc++`, `libgcc`,
certificates, time zone data, a non-root user, and nothing else, because the binary is
dynamically linked and needs those three libraries; `scratch` would fail with `libstdc++.so.6
not found`. The two stages are both Debian 12 on purpose: the binary asks for glibc symbols by
version, and a newer builder than runtime fails at start-up with `GLIBC_2.38 not found`. The
image is the binary plus about twenty megabytes of runtime, no shell, running as uid 65532.

**The follow-ups**

- **Could you make it static and use scratch like Go?** *Yes, `-static` on the link, and then
  scratch works. The costs are a bigger binary, glibc's own warnings about static linking of
  name resolution, and losing security updates to the runtime libraries, which in distroless
  arrive by rebuilding on a newer base. For most services, `cc` is the better trade.*
- **Where do the certificates come from if the service calls HTTPS?** *Distroless includes a
  certificate bundle at `/etc/ssl/certs/ca-certificates.crt`, unlike scratch, so an HTTPS client
  in the binary verifies without any extra copy.*
- **How do you keep the layer cache useful with FetchContent?** *Configure with only
  `CMakeLists.txt` copied, using a placeholder source so configure succeeds; the fetch happens
  there and is cached until the CMake file changes. Sources are copied after, so an edit only
  re-runs the build step.*

**A model answer**

"Two stages on the same Debian. Builder: `debian:bookworm-slim`, install `g++ cmake ninja-build
git` with `--no-install-recommends`, copy `CMakeLists.txt`, configure so FetchContent is cached,
copy `src`, build Release. Runtime: `gcr.io/distroless/cc-debian12:nonroot`, copy the binary,
JSON-form `ENTRYPOINT`. About 22 MB, of which the binary is two; the rest is `libc`,
`libstdc++`, `libgcc`, and certificates, which is what `ldd` on the binary lists. Not `scratch`,
because the binary is dynamic; not a different Debian, because glibc symbol versions must
match; and no shell, which is the point."

## 9. Recall card

- Builder `debian:bookworm-slim` + `g++ cmake ninja-build git ca-certificates` with `--no-install-recommends` and `rm -rf /var/lib/apt/lists/*` in the same `RUN`.
- Copy `CMakeLists.txt`, configure with a placeholder source so FetchContent is cached, then copy `src` and `cmake --build build`; always `-DCMAKE_BUILD_TYPE=Release`.
- Runtime `gcr.io/distroless/cc-debian12:nonroot`: libc, libstdc++, libgcc, certs, zoneinfo, uid 65532, no shell; JSON-form `ENTRYPOINT ["/server"]`.
- Same Debian on both `FROM` lines or the binary fails at start with ``version `GLIBC_2.38' not found``; `distroless/static` or `scratch` fails with `libstdc++.so.6: cannot open shared object file`.
- `ldd server` in the builder lists exactly what the runtime must provide; the image is the binary plus those, ~20 MB.
