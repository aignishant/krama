---
day: 59
track: lang-python
title: "A slim Python image with uv and a non-root user"
theme: "Docker for each language"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 059 · Python — A slim Python image with uv and a non-root user

**Today's theme:** Docker for each language

**After today you can:** You can containerise a service in each language and say why the images are 1 GB, 10 MB, and 20 MB.

**The interviewer asks it as:** *Why is your Docker image so large, and how would you shrink it?*

---

## 1. What this is, and why it matters

A Docker **image** is a frozen filesystem plus a command: everything your service needs to run,
packed so it runs the same on your laptop and on a server. On [day 13](../day-013-reverse-and-rotate/README.md)
you met the idea; today you write the `Dockerfile` that builds one for a Python service. The
Python version has a particular shape: a **slim** base, so you ship an interpreter and not a
whole operating system; **uv** installing dependencies from the lock file into a virtual
environment, in a layer that is rebuilt only when the lock file changes; and a **non-root user**,
so a bug in your service cannot become a bug in the host.

At work you will write, or inherit, one of these for every service, and the most common review
comment on them is "why is this a gigabyte". In interviews the question is exactly that, and
the answer has three parts: the base image, the build tools you left in, and the layers you
ordered wrong.

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

The full trunk is the image most people build first: `FROM python:3.12` is a whole Debian
operating system with compilers, documentation, and every library anyone might ever need, about
a gigabyte before your code goes in. The small bag is `python:3.12-slim`: the interpreter and
what it needs to run, about 130 MB. Same Python. The difference is everything you were never
going to use.

The sewing machine staying at home is the **build stage**. Installing dependencies needs uv,
and sometimes a compiler; running the service needs neither. A **multi-stage** Dockerfile has a
first `FROM` where the installing happens and a second `FROM` that copies in only the result,
the `.venv` directory. The tools never reach the final image.

The key ring is **root**. A container runs as root by default, and root inside a container is
close to root outside it if anything goes wrong. `useradd` plus `USER app` hands the service one
room key. If an attacker gets in through your service, they get a user that can read `/app` and
write nowhere.

Packing the clothes already altered is **layer order**. Each Dockerfile line makes a layer,
cached until its inputs change. Copy `pyproject.toml` and `uv.lock` first and install; copy the
code after. Then editing your code rebuilds only the last layer, and dependency installation is
reused from the cache; get the order wrong and every edit reinstalls everything.

## 4. The picture

```text
  stage 1: builder (python:3.12-slim + uv)        stage 2: runtime (python:3.12-slim)
  +---------------------------------------+       +-----------------------------------+
  | /bin/uv                 (tool)        |       | /usr/local/bin/python3.12         |
  | /app/pyproject.toml, uv.lock          |       | /app/.venv/    <-- copied         |
  | /app/.venv/  <- uv sync --frozen      | ----> | /app/app.py    <-- copied         |
  | /root/.cache/uv (build cache)         |       | USER app  (uid 1000, no shell)    |
  | /app/app.py                           |       | CMD uvicorn app:app               |
  +---------------------------------------+       +-----------------------------------+
        thrown away after the build                    ~180 MB, what actually ships
```

Notice that the only arrow is the `COPY --from=builder`. `uv` itself, and the cache it used,
never cross it. And notice `USER app` is below the copy: the files are copied as root and then
owned by `app`, so the service can read them and cannot change them.

## 5. The code, built step by step

The service is the day 48 one, cut to a health route so the image is the lesson, not the code.
`app.py`:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

Its dependencies, declared with uv from [day 14](../day-014-single-pass-habit/README.md):

```bash
uv init --name pricer --no-readme
uv add fastapi "uvicorn[standard]"
```

That leaves `pyproject.toml` and `uv.lock`, and the lock file is the important one: it pins every
package to an exact version, so the image built next month is the same as the one built today.

Now the `Dockerfile`, top down. The builder stage starts from slim and copies the uv binary in
from its own image; that line is how you get uv without `pip install`.

```dockerfile
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
```

`UV_COMPILE_BYTECODE` precompiles `.pyc` files so start-up is faster; `UV_LINK_MODE=copy` stops
uv trying to hard-link out of a cache mount, which it cannot do across layers. Pin the uv tag to
a version in real work; `latest` is here so the line works the day you read it.

Dependencies first, code second. This is the layer-order rule.

```dockerfile
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev
COPY app.py ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
```

`--frozen` refuses to touch the lock file; if `pyproject.toml` and `uv.lock` disagree, the build
fails rather than silently resolving something new. `--no-dev` leaves pytest and respx out; the
image does not run tests. `--mount=type=cache` keeps uv's download cache between builds without
it landing in any layer.

The runtime stage. Fresh slim base, a user with a home and no password, the built `.venv` copied
across, and the switch to that user.

```dockerfile
FROM python:3.12-slim
RUN useradd --create-home --uid 1000 --shell /usr/sbin/nologin app
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
USER app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

`--chown=app:app` sets ownership during the copy, so there is no separate `chown` layer that
would double the size. `PATH` puts the virtual environment's `uvicorn` first, so no activation
is needed. `0.0.0.0`, not `127.0.0.1`: inside a container, loopback is the container's own, and
a server bound to it is unreachable from outside.

Build it, and look at the size:

```bash
docker build -t pricer-py .
docker images pricer-py
```

```text
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
pricer-py    latest    4c1e8f2a9b3d   12 seconds ago   183MB
```

Run it and call it:

```bash
docker run --rm -p 8000:8000 pricer-py
curl -s http://127.0.0.1:8000/health
```

```text
INFO:     Started server process [1]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
{"status":"ok"}
```

And confirm who it runs as:

```bash
docker run --rm pricer-py id
```

```text
uid=1000(app) gid=1000(app) groups=1000(app)
```

For the comparison, build the same service on the full base with everything in one stage as
root, the trunk version, and look:

```text
REPOSITORY    TAG       IMAGE ID       CREATED          SIZE
pricer-fat    latest    9a7d3c1e5f20   8 seconds ago    1.09GB
```

Same code, same behaviour, six times the size, running as root. Here is the whole `Dockerfile`:

```dockerfile
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev
COPY app.py ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.12-slim
RUN useradd --create-home --uid 1000 --shell /usr/sbin/nologin app
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
USER app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 6. How the other two languages do it

**Go**

```dockerfile
FROM golang:1.23 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /out/server .

FROM scratch
COPY --from=builder /out/server /server
USER 65534:65534
ENTRYPOINT ["/server"]
```

Go compiles to one static binary, so the runtime stage is `scratch`, an empty filesystem, and
the image is the binary: about 10 MB. There is no interpreter to ship.

**C++**

```dockerfile
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends g++ cmake ninja-build git ca-certificates
COPY . /src
RUN cmake -S /src -B /build -G Ninja -DCMAKE_BUILD_TYPE=Release && cmake --build /build

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /build/server /server
ENTRYPOINT ["/server"]
```

C++ also ships a binary, but one that needs the C and C++ runtime libraries, so the runtime stage
is `distroless/cc`: those libraries and nothing else, no shell, no package manager, about 20 MB
with the binary.

**The difference that matters:** Python cannot be shipped as a binary, so its runtime stage must
contain the interpreter and every installed package, and the smallest honest Python image is an
order of magnitude bigger than the Go or C++ one. That is not a mistake you can fix with a flag;
it is the cost of the language, and the interviewer wants to hear you know which of the three
sizes is the floor and why.

## 7. The traps

**The near-miss: code before dependencies.**

```dockerfile
COPY . .
RUN uv sync --frozen --no-dev
```

It builds, and it is correct. But `COPY . .` changes on every edit to `app.py`, so the `RUN`
below it is never cached, and every build reinstalls every package. Dependencies first, code
after, always. The lesson's Dockerfile does exactly this and the second build of it, after an
edit, takes a second.

**`COPY . .` with no `.dockerignore`.** The `.venv` you made locally, `.git`, `__pycache__`, and
the test database all go into the build context and often into the image. Write the ignore file
before the first build:

```text
.venv
.git
__pycache__
*.db
```

**Binding to loopback.** `CMD ["uvicorn", "app:app", "--host", "127.0.0.1"]` starts fine and logs
`Uvicorn running on http://127.0.0.1:8000`, and then:

```text
curl: (56) Recv failure: Connection reset by peer
```

Inside the container `127.0.0.1` is the container's own loopback; the port mapping delivers to
the container's outer interface. `0.0.0.0` inside the container, and the host's firewall
outside it.

**The non-root user writing where it cannot.** Add `Path("data").mkdir()` to the service and:

```text
PermissionError: [Errno 13] Permission denied: 'data'
```

`/app` is owned by `app` only because of `--chown`; the rest of the filesystem is root's. A
service that writes needs a directory it owns, created in the Dockerfile, or better, a mounted
volume. The error is the user doing its job.

**`uv sync` without `--frozen`.** If someone edited `pyproject.toml` and forgot to run `uv lock`,
a plain `uv sync` quietly re-resolves and the image gets versions nobody reviewed. `--frozen`
fails instead:

```text
error: The lockfile at `uv.lock` needs to be updated, but `--frozen` was provided.
```

That is the build refusing to guess, which is what you want.

**`python:3.12-alpine` to save another 80 MB.** Alpine uses a different C library, so packages
with compiled parts, which includes much of the data science and database world, either have
no prebuilt wheel or misbehave. Slim is the Debian-based small image, and it is the default
answer; Alpine is a decision to make with a reason.

## 8. Say it out loud

**How it gets asked**

- Why is your Docker image so large, and how would you shrink it?
- Why run a container as a non-root user?
- What is a multi-stage build for?
- Why does the order of lines in a Dockerfile matter?

**The ninety-second script**

The image is large for one of three reasons. The base: `python:3.12` is a full Debian with
compilers and docs, about a gigabyte, and `python:3.12-slim` is the same interpreter at about
130 MB, so I start there. The build tools: installing dependencies needs uv and sometimes a
compiler, running does not, so I use a multi-stage build, install into a `.venv` in the first
stage, and copy only that directory into a fresh slim base. And the layers: `COPY` of the
dependency files and the install come before `COPY` of the code, so an edit to the code reuses
the cached install instead of reinstalling. With that the image is under 200 MB and I would say
that is close to the floor for Python, because unlike Go or C++ it cannot be a single binary.
The other thing I always do is `useradd` and `USER app`, so the service holds one key, not the
key ring: a compromise of the process cannot write outside its own directory. And `--frozen` on
the install, so the image gets exactly the versions in the lock file or fails.

**The follow-ups**

- **Why not Alpine for an even smaller image?** *Different C library, so compiled packages
  often have no wheel and build from source, slowly, or behave differently. Slim is the safe
  small default; Alpine is a choice with a cost.*
- **Where does the cache mount go, and is it in the image?** *`--mount=type=cache` lives on the
  build host, outside every layer; it speeds up rebuilds and ships nothing. Without it, uv's
  cache would either be in a layer or re-downloaded every build.*
- **How would you ship secrets into this container?** *Never in the image; environment
  variables at run time or a mounted secrets file, exactly as on
  [day 51](../day-051-why-sorting-matters/README.md). An image is copied and cached everywhere; a
  secret in a layer is a secret in every registry it passes through.*

**A model answer**

"Three causes, three fixes. Base: start from `python:3.12-slim`, not `python:3.12`, which alone
is a gigabyte. Tools: multi-stage, with uv installing into `.venv` in a builder stage and only
`.venv` and the code copied into the runtime stage. Layers: dependency files and `uv sync
--frozen` before the code copy, so edits do not reinstall. Result under 200 MB, which is about
the floor for Python since it needs the interpreter. Then `useradd` and `USER app` with
`--chown` on the copy, so it runs as uid 1000 and cannot write outside `/app`, and `--host
0.0.0.0` so the port mapping reaches it."

## 9. Recall card

- `python:3.12` is ~1 GB, `python:3.12-slim` is ~130 MB, same interpreter; start slim. Alpine is a decision, not a default.
- Multi-stage: `FROM python:3.12-slim AS builder`, copy uv from `ghcr.io/astral-sh/uv`, `uv sync --frozen --no-dev` into `/app/.venv`; then a fresh `FROM python:3.12-slim` and `COPY --from=builder --chown=app:app /app /app`.
- Layer order: `COPY pyproject.toml uv.lock` and the install before `COPY app.py`; edits then reuse the cached install. `.dockerignore` before the first build.
- `useradd --create-home --uid 1000 --shell /usr/sbin/nologin app` then `USER app`; the service can read `/app` and write nowhere else, and `PermissionError` is the user working.
- `CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]`; loopback inside a container is unreachable from outside. Secrets at run time, never in a layer.
