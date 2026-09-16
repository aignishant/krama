---
day: 44
track: lang-python
title: "pyproject.toml, wheels, and PyInstaller"
theme: "Building and shipping"
phase: "Languages: advanced features"
status: written
---

# Day 044 · Python — pyproject.toml, wheels, and PyInstaller

**Today's theme:** Building and shipping

**After today you can:** You can produce a distributable artifact of a program in each language.

**The interviewer asks it as:** *How do you ship your program to a machine without the toolchain?*

---

## 1. What this is, and why it matters

`pyproject.toml` declares how a Python package is built and what it needs.
A wheel is an installable distribution; PyInstaller builds a platform-specific
application containing a Python runtime. Choose based on who will run the tool
and what they already have installed.

## 2. The story

Leela has made a cake for her aunt. At home she has a large oven, a mixer,
and every bowl she needs. Her aunt has none of those things. That does not matter
if Leela takes a finished cake. It matters a great deal if she sends only the
recipe and a bag of flour.

She puts the cake in a box and checks whether it will fit in the basket on her
bicycle. Her brother suggests taking the icing in a separate tub so it will not
be damaged on the way. That makes the box lighter, but now someone must remember
the tub and have a spoon at the other end. A finished cake with everything
already on it is simpler to hand over, though it takes more room.

Before leaving, Leela tries to lift the box with one hand. The bottom bends.
It looked fine while resting on the kitchen table, where she had made it. She
moves the cake into a stronger box and tries carrying it down the steps. This
time it holds.

Her aunt lives across town, where the afternoon is hotter. Leela adds a cool
bag and writes the ingredients in a message on her phone. She sends that before
setting off. Making something work in her own kitchen was only the first part.
The other part is choosing what to take, saying what is still needed, and
checking that the thing survives where it is actually going.

## 3. The idea in plain English

A build turns source into an artifact you can distribute. Packaging says
what files and dependencies travel with it. The target is the operating system
and processor architecture where it will run, not necessarily your laptop.

A Python wheel installs a package into a Python environment. A frozen application
bundles an interpreter and supporting files. A Go executable often carries its
Go dependencies, while cgo can add native library requirements. A C++ executable
may load shared libraries at runtime. A static library is an archive used during
linking; it is not itself a runnable program.

Build in a clean environment, record versions and the target, then smoke-test on
that target. A smoke test is a small real execution proving the artifact can
start and perform its basic job without your development checkout.

## 4. The picture

```text
source + build metadata -> build tool -> artifact
artifact + runtime requirements -> target machine -> smoke test
recipe                    cake         can it be served here?
```

Notice where the decision happens and what information it needs.

## 5. The code, built step by step

```python
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

Save this in pyproject.toml. The build frontend creates an isolated environment and calls the declared backend.

```python
[project]
name = "krama-demo"
version = "1.0.0"
requires-python = ">=3.12"
[project.scripts]
krama-demo = "krama_demo:main"
[tool.setuptools]
py-modules = ["krama_demo"]
```

Append this to the same file. The script entry names an importable callable; the module declaration includes the single source file.

Save the program as `krama_demo.py` beside the complete `pyproject.toml`
formed from the two fragments. Run `python krama_demo.py --version`.

For a wheel: `python -m pip install build`, then `python -m build --wheel`.
In a fresh virtual environment, install `dist/krama_demo-1.0.0-py3-none-any.whl`
with `python -m pip install` followed by that path, then run
`krama-demo --version`. A `py3-none-any` wheel contains no platform-specific
extension in this example; wheels with native extensions have narrower tags.

For an app: `python -m pip install pyinstaller`, then
`python -m PyInstaller --onefile --name krama-demo krama_demo.py`.
Run `dist/krama-demo --version` (Windows: `.\dist\krama-demo.exe --version`).
Build the frozen app on each supported target platform. Build-tool progress
and artifact paths vary; the application's output below does not.

Expected application output (framework access logs are omitted):

    krama 1.0

Complete program:

```python
import sys

def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1:] != ["--version"]:
        print("invalid: unknown option", file=sys.stderr)
        raise SystemExit(2)
    print("krama 1.0")

if __name__ == "__main__":
    main()
```

## 6. How the other two languages do it

**Go**

```go
go build -trimpath -ldflags="-X main.version=1.0" -o krama-demo .
```

Run in a module created with go mod init example.com/krama-demo. -X sets an eligible string variable at link time; it cannot rewrite a constant.

**Cpp**

```cpp
cmake_minimum_required(VERSION 3.20)
project(krama_demo LANGUAGES CXX)
add_executable(krama-demo main.cpp)
target_compile_features(krama-demo PRIVATE cxx_std_20)
if(MSVC)
  target_compile_options(krama-demo PRIVATE /W4)
else()
  target_compile_options(krama-demo PRIVATE -Wall -Wextra)
endif()
```

Save as CMakeLists.txt. Requirements belong to the target so they follow it through the build graph.

**The difference that matters:** Name the target OS and architecture before building.

## 7. The traps

**Near-miss:** sending the `.whl` file to someone without Python does not
give them a runnable desktop program. Conversely, PyInstaller is not a general
cross-compiler: build and test per target platform.

**Real error:** run `python krama_demo.py --unknown`; stderr is
`invalid: unknown option` and the exit status is 2. Repeat that test on the
installed entry point and on the frozen executable.

Data files and dynamically discovered imports may need explicit packaging
configuration. Test outside the repository so the current directory cannot
hide missing files. A one-file app may unpack supporting files at startup;
one file does not mean your code was translated to native machine instructions.

Reference: [Packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) and [PyInstaller operation](https://pyinstaller.org/en/stable/operating-mode.html).

## 8. Say it out loud

**How it gets asked**

- How do you ship your program to a machine without the toolchain?
- What still needs installing on the destination machine?
- Why can a successful cross-build still produce an unusable artifact?

**What to say out loud**

I first name the target OS and architecture and whether an interpreter or
native libraries can be installed there. For Python users with Python, I ship
a wheel with dependency metadata. For users without Python, I can build a frozen
application for that platform. With Go I build the target executable and check
whether cgo introduces external requirements. With C++ I use a Release build
and verify the runtime libraries rather than assuming one file means no
dependencies. I test the artifact outside the source directory on a clean target,
including its version command and a failing invocation. I retain enough build
metadata to reproduce it and enough diagnostic information to debug a crash.

**The follow-ups**

- **Is a wheel a standalone executable?** No. It is an installable Python distribution and normally needs a compatible interpreter.

- **Can one binary run on every machine?** No. OS, architecture, ABI, and native dependencies constrain compatibility.

- **Why test outside the checkout?** The checkout can accidentally supply files or imports missing from the package.

**A model answer**

I would deliver a tested artifact plus its runtime requirements and version.
For an internal Python tool, a wheel may be the simplest contract if Python is
already managed on the target. For a desktop user without Python, a platform
build with PyInstaller may be appropriate. For Go or C++, I check the binary's
actual dependencies. I would demonstrate the shipped artifact starting on the
target, not merely show that the compiler returned success on my laptop.

## 9. Recall card

- Name the target OS and architecture before building.
- A wheel needs Python; a frozen app bundles a runtime.
- Static libraries are link inputs, not executables.
- Record versions and check native dependencies.
- Smoke-test the artifact outside the checkout.
