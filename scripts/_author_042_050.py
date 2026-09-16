from pathlib import Path
import re
from curriculum import load
from build_skeleton import LANG_SECTIONS, lang_lesson_name

ROOT = Path(__file__).resolve().parent.parent
DATA = {}

def day(n, story, idea, picture, interview, followups, model, recall, exercises, questions):
    DATA[n] = dict(story=story, idea=idea, picture=picture, interview=interview,
                   followups=followups, model=model, recall=recall,
                   exercises=exercises, questions=questions, langs={})

def lang(n, name, intro, steps, code, run, output, traps, source):
    DATA[n]['langs'][name] = dict(intro=intro, steps=steps, code=code,
                                run=run, output=output, traps=traps, source=source)

day(42, """Anya is looking through the family chat for the day her cousin arrives. There
are photographs, greetings, and long arguments about who will collect him. She
does not read every message with equal care. She looks for four digits, a dash,
two digits, another dash, and two more digits. That is how her cousin usually
writes the day of a journey.

She finds 2026-09-16 in a sentence about a train. She also finds 2026-99-40 in a
message where her uncle has made a joke. Both have the arrangement she was
looking for. Only one can name a real day. Her way of spotting likely dates has
saved her some reading, but it has not settled which ones to trust.

Her mother asks her to find the cousin's email address too. Anya looks for a
short stretch without spaces, then an at sign, then another stretch containing
a dot. She finds an address in a message and copies it. Her mother asks whether
that means the address still works. Anya shakes her head. The cousin might have
stopped using it years ago. They will have to send a message and hear back.

Before she closes the chat, Anya checks the train booking itself. The shapes
helped her find candidates. The booking and a reply supply the facts she actually
needs. She keeps those two jobs separate the next time she searches.""",
"""A regular expression, or regex, describes a text shape. `[0-9]` accepts one
ASCII digit; `{4}` repeats the preceding piece four times. Parentheses capture
part of a match so you can retrieve the year separately. `+` means one or more,
and `.` normally accepts almost any character; write `\.` for a literal dot.

Searching asks whether the shape occurs anywhere. Whole-input matching asks
whether every character belongs to the shape. Neither validates a calendar or
proves ownership of a mailbox. Use a date parser after extraction and a
confirmation message when ownership matters. Prefer a literal substring search
when you have no variable shape to describe.""",
"text:  arrive 2026-09-16 please\n              |year| mm dd\n+search --------------------> candidate\n+date parser ----------------> real calendar date?",
"""I first clarify whether you want extraction or validation. To extract a date,
I can search for four ASCII digits, a dash, two digits, a dash, and two digits,
with boundaries appropriate to the input format. Capturing groups return its
pieces. To validate a whole field I require the entire input to match and then
ask a date parser to check month lengths and leap years. For email I would call
a small pattern a product input rule, not a complete definition of valid email.
It cannot tell me whether an inbox exists. I also ask about untrusted input:
pattern syntax and worst-case matching cost depend on the engine.""",
[("Why compile a pattern once?", "It separates pattern construction from repeated matching and makes reuse explicit."),
 ("Why not parse JSON with regex?", "Nested structure and escapes belong to a JSON parser; regex is useful for bounded flat fields."),
 ("Does a matching email exist?", "No. Syntax, deliverability, and ownership are separate checks.")],
"""For an agreed simple ASCII field I might start with
`[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` and require a whole-input match.
It still accepts consecutive dots and other invalid arrangements and rejects
some legitimate address forms. I would state those limitations, apply the
product's documented policy, and confirm ownership separately. I would not
claim that adding more punctuation to the pattern makes it an email parser.""",
["Choose search or whole-input matching deliberately.", "Capture parentheses return pieces, not semantic validity.",
 "Use ASCII ranges when the contract says ASCII.", "Compile reusable patterns once; understand the engine's cost.", "Parse dates; confirm email ownership."],
[("Extract both dates from `a 2026-09-16 b 2026-99-40`; print year, month, day.", "Captures and the difference between shape and calendar validity."),
 ("Apply the simple email policy to `a@b.in`, `a..b@c.in`, and `prefix a@b.in suffix`.", "Whole-input matching and explicit counterexamples."),
 ("Extract dates, parse them, and report accepted/rejected counts without stopping at the first bad date.", "Separate extraction, validation, and per-record failure handling.")],
["Why does a regex accepting a date not prove that the date exists?", "Which engine can promise linear matching for a fixed pattern, and what syntax does it give up?"])

lang(42, 'python', """Python's `re` module searches, captures, and replaces text described by a
pattern. `search` looks anywhere; `match` starts at the beginning; `fullmatch`
requires the whole input. You use these operations to extract fields from logs
without confusing a successful search with valid input.""",
[(r'date = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})")',
  "A raw literal preserves backslashes for the regex parser. Compiling returns a reusable pattern object."),
 ('found = date.search("arrive 2026-09-16")\nif found is not None:\n    print(found.group(1))',
  "Check for absence first. Group zero is the entire match; groups one through three are the pieces.")],
'''import re

def main() -> None:
    date = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})")
    text = "arrive 2026-09-16; leave 2026-09-18"
    found = date.search(text)
    if found is not None:
        print("year", found.group(1))
    print("start", date.match(text) is not None)
    print("whole", date.fullmatch("2026-09-16x") is not None)
    print("parts", date.findall(text))
    try:
        re.compile("[")
    except re.error as exc:
        print("invalid:", exc)

if __name__ == "__main__":
    main()
''', 'Save as `main.py`; run `python main.py`.',
"year 2026\nstart False\nwhole False\nparts [('2026', '09', '16'), ('2026', '09', '18')]\ninvalid: unterminated character set at position 0",
"""**Near-miss:** `re.match(r"[0-9]+", "12cats")` succeeds. Use `fullmatch` for
a numeric field. `findall` returns tuples when there are several capturing
groups; use `finditer` if you need full match objects and positions.

**Real error:** the complete program catches the invalid pattern `[` and prints
`invalid: unterminated character set at position 0`. Catch `re.error` on Python
3.12; newer Python also names this exception `PatternError`.

Python's engine can backtrack: it revisits earlier choices. Nested ambiguous
repetition such as `(a+)+$` can become very expensive on a long almost-match.
Compiling does not remove this risk. Avoid such patterns on untrusted input;
bound input length and choose a suitable engine when predictable cost matters.""",
'[Python re reference](https://docs.python.org/3/library/re.html)')

lang(42, 'go', """Go's `regexp` package matches text with RE2-style syntax and guarantees
matching time linear in input length for a fixed pattern. It leaves out
backreferences and lookaround. That trade-off matters when a user can send a
long input that nearly matches your rule.""",
[(r'pattern, err := regexp.Compile(`([0-9]{4})-([0-9]{2})-([0-9]{2})`)',
  "Use Compile for a pattern that can fail and handle its error. MustCompile is appropriate only for a trusted program constant whose failure is a programming mistake."),
 ('parts := pattern.FindStringSubmatch(text)\nif parts != nil {\n\tfmt.Println(parts[1])\n}',
  "Element zero is the full match, followed by captures. No match returns nil, so checking length or nil must precede indexing.")],
'''package main

import (
	"fmt"
	"regexp"
)

func main() {
	pattern, err := regexp.Compile(`([0-9]{4})-([0-9]{2})-([0-9]{2})`)
	if err != nil {
		fmt.Println(err)
		return
	}
	text := "arrive 2026-09-16; leave 2026-09-18"
	for _, parts := range pattern.FindAllStringSubmatch(text, -1) {
		fmt.Println(parts[1], parts[2], parts[3])
	}
	whole := regexp.MustCompile(`\A[0-9]{4}-[0-9]{2}-[0-9]{2}\z`)
	fmt.Println("whole", whole.MatchString("2026-09-16x"))
	if _, err := regexp.Compile(`[`); err != nil {
		fmt.Println("invalid:", err)
	}
}
''', 'Save as `main.go`; run `go run main.go` with Go 1.23+.',
'2026 09 16\n2026 09 18\nwhole false\ninvalid: error parsing regexp: missing closing ]: `[`',
"""**Near-miss:** `MatchString` searches; it does not require a whole-input
match. The unanchored date pattern accepts `2026-09-16x`. Use `\\A` and `\\z`
when you need absolute start and end, as in the program.

**Real error:** compiling `[` prints
`invalid: error parsing regexp: missing closing ]: ` followed by the pattern in
backticks, exactly as shown in the output. Do not index a nil submatch result.

Lookahead such as `(?=x)` and a backreference such as `\\1` are unsupported.
Move those checks into ordinary Go code. Linear matching is not free matching:
pattern size, capture allocation, and the number of returned matches still
consume resources. Compile outside the record-processing loop.""",
'[Go regexp reference](https://pkg.go.dev/regexp)')

lang(42, 'cpp', """`std::regex` is the C++ standard library's text-pattern facility.
`regex_search` finds a substring, while `regex_match` requires the whole input.
It is convenient for small tools, but the standard facility does not promise
RE2's linear-time behaviour.""",
[(r'const std::regex date(R"(([0-9]{4})-([0-9]{2})-([0-9]{2}))");',
  "A raw C++ literal avoids doubling regex backslashes. The default grammar is ECMAScript, not Python's entire syntax."),
 ('std::smatch found;\nif (std::regex_search(text, found, date)) {\n    std::cout << found[1].str();\n}',
  "smatch holds matches into a std::string. Keep the searched string alive while using those results.")],
'''#include <iostream>
#include <regex>
#include <string>

int main() {
    const std::regex date(R"(([0-9]{4})-([0-9]{2})-([0-9]{2}))");
    const std::string text = "arrive 2026-09-16; leave 2026-09-18";
    for (std::sregex_iterator it(text.begin(), text.end(), date), end;
         it != end; ++it) {
        std::cout << (*it)[1] << ' ' << (*it)[2] << ' ' << (*it)[3] << '\\n';
    }
    const std::string bad = "2026-09-16x";
    std::cout << "whole " << std::boolalpha << std::regex_match(bad, date) << '\\n';
    try {
        const std::regex invalid("[");
    } catch (const std::regex_error& exc) {
        if (exc.code() == std::regex_constants::error_brack) {
            std::cout << "invalid: unmatched bracket\\n";
        } else {
            throw;
        }
    }
}
''', 'Save as `main.cpp`; run `g++ -Wall -Wextra -std=c++20 main.cpp -o main`, then `./main` (`.\\main.exe` on Windows).',
'2026 09 16\n2026 09 18\nwhole false\ninvalid: unmatched bracket',
"""**Near-miss:** `regex_search` accepts the date inside `2026-09-16x`.
`regex_match` rejects it. A capture is a view into the searched text, so copying
`found[1].str()` is useful when the source will go away.

**Real error:** constructing `std::regex("[")` throws `std::regex_error`.
The program translates `error_brack` to the stable diagnostic
`invalid: unmatched bracket`; this is our output, not portable `what()` text.
The implementation's own `what()` wording varies by standard library.

Choose RE2 when a fixed pattern needs predictable linear matching on hostile
text and its restricted syntax is sufficient. CTRE moves pattern processing
to compile time for literal patterns and can avoid runtime construction; that
alone is not RE2's complexity guarantee. Both add a dependency. Measure your
workload before claiming either is always faster than `std::regex`.""",
'[RE2 design](https://github.com/google/re2) and [CTRE usage](https://github.com/hanickadot/compile-time-regular-expressions)')

day(43, """Ravi is helping his family prepare for a weekend away. His sister sends him
a photograph of each packed bag. He opens the first photograph and names what
he can see: a blue coat, a pair of shoes, and a small pouch. He can describe the
contents even though he did not pack the bag himself.

His mother asks him to put a spare key into the pouch. Ravi cannot do that by
touching the photograph. He needs the actual bag. Once his sister brings it to
him, he opens the pouch, adds the key, and closes it again. Seeing what something
contains and being able to change it are different kinds of access.

The family has three identical grey bags. Their father once sewed a small name
inside each one so that the children could tell them apart. Those names are
extra information about the bags; they do not change what the bags can carry.
Ravi reads the names before deciding which bag belongs by which bedroom door.

For his own bag he needs none of this checking. He knows exactly where he put
the coat and the pouch. Opening every pocket just to discover them again would
be wasted effort. But the photographs are helpful for bags other people packed.
He decides to ask for that extra information only when he needs it, and to ask
for the real bag whenever the job involves changing what is inside.""",
"""Reflection means inspecting a program's values and types while it runs.
Names, tags, and annotations are metadata: information describing the data.
Reading metadata is different from having permission to modify a value.
Python can look up a named attribute; Go can inspect an exported struct field.
C++20 does not provide general runtime enumeration of a struct's field names:
templates and type traits answer compile-time questions instead.

A JSON library may use runtime inspection, generated code, or explicit field
registration. It does not magically know every representation. Use ordinary
field access when the shape is already known; reserve general inspection for
boundaries that genuinely accept several shapes.""",
"known object ---- direct field access\nunknown supported shape ---- metadata ---- checked access\nC++20 template ---- compile-time condition ---- chosen code",
"""I ask what metadata the language makes available. In Python I can look up
attributes by name, although that lookup may execute a property. In Go I can
walk exported struct fields and read their tags using reflect. Updating a field
requires a settable value of the right kind. In C++20 I cannot enumerate arbitrary
member names at runtime; a serializer needs explicit mappings, generated code,
or another supported mechanism. Compile-time traits help select implementations,
but are not the same as runtime reflection. For a known application type I
prefer explicit code because its failures are easier to find and its accepted
fields are easier to review.""",
[("Is reflection free?", "No. Runtime lookup and checks add work and move some mistakes out of compile-time checking."),
 ("Should a request choose any field to set?", "No. Validate against an allowlist and preserve the object's invariants."),
 ("What replaces reflection for a fixed schema?", "Explicit adapters or generated code can make the mapping visible and checked.")],
"""A serializer learns names from metadata or from mappings supplied by its
author. I would not build a general serializer just to avoid writing three
field assignments. If the input chooses a field, I first restrict the allowed
names and validate its value. Inspection can tell me a member exists; it cannot
tell me that changing it is a valid business operation. That is why I keep
domain updates behind methods even when the language permits dynamic access.""",
["Reflection inspects running values; templates operate during compilation.", "Metadata describes data, not permission to edit it.",
 "Check existence, kind, and mutability before dynamic writes.", "C++20 needs explicit mappings to enumerate member names.", "Prefer direct access for known shapes."],
[("Describe a two-field Person; print its supported field names and values.", "Runtime metadata in Python/Go versus explicit C++20 mappings."),
 ("Allow updates only to `name`; reject `balance` and unknown names without mutation.", "An allowlist is a domain boundary, not just a lookup."),
 ("Create an explicit JSON-name mapping and compare it with dynamic inspection on 10,000 records.", "Correctness first; measure runtime work without assuming a winner.")],
["Why can inspecting a value succeed while modifying it fails?", "What can C++20 type traits tell you that runtime field-name reflection cannot?"])

lang(43, 'python', """`getattr` reads an attribute whose name is supplied as text, and `setattr`
writes one. An ordinary instance often stores attributes in `__dict__`, but
slots and properties mean this is not a universal field catalogue. These tools
help adapters; they should not bypass your object's update rules.""",
[( 'name = getattr(person, "name", "unknown")', "The third argument supplies a default for a missing attribute; without it, absence raises AttributeError."),
 ('if field != "name":\n    raise ValueError("field not writable")\nsetattr(person, field, value)', "Restrict the operation before the write. setattr can otherwise create a misspelled attribute on an ordinary instance.")],
'''class Person:
    def __init__(self, name: str) -> None:
        self.name = name

def rename(person: Person, field: str, value: str) -> None:
    if field != "name":
        raise ValueError("field not writable")
    setattr(person, field, value)

def main() -> None:
    person = Person("Anya")
    print(getattr(person, "name"))
    rename(person, "name", "Ravi")
    print(person.__dict__)
    try:
        rename(person, "balance", "999")
    except ValueError as exc:
        print(type(exc).__name__ + ": " + str(exc))

if __name__ == "__main__":
    main()
''', 'Save as `main.py`; run `python main.py`.',
"Anya\n{'name': 'Ravi'}\nValueError: field not writable",
"""**Near-miss:** `setattr(person, "naem", "Ravi")` creates a new attribute
instead of renaming `name`. The allowlist in `rename` rejects that typo.

**Real error:** `rename(person, "balance", "999")` prints
`ValueError: field not writable`. The original state remains unchanged.
`getattr` can execute properties and `__getattr__`; it is not necessarily a
passive dictionary read. `vars(obj)` requires an instance dictionary.

A metaclass is the class of a class: normally `type`. Its construction hooks
can validate or register newly defined classes. A class decorator often achieves
simple registration with less machinery. Neither a metaclass nor a `__dict__`
walk substitutes for a deliberately designed external schema.""",
'[Python data model](https://docs.python.org/3/reference/datamodel.html)')

lang(43, 'go', """Go's `reflect.Type` describes a type; `reflect.Value` describes a value.
Struct tags are text attached to fields, such as the JSON name `name`.
Reflection is useful for reusable encoders, but ordinary struct access gives
simpler checks when you already know the shape.""",
[( 't := reflect.TypeOf(person)\nfield := t.Field(0)\nfmt.Println(field.Tag.Get("json"))', "Field metadata supplies the exported Go name and its optional external tag."),
 ('value := reflect.ValueOf(&person).Elem().FieldByName("Name")\nif value.CanSet() && value.Kind() == reflect.String {\n\tvalue.SetString("Ravi")\n}', "A pointer followed by Elem exposes the original struct. A copied non-addressable value is not settable.")],
'''package main

import (
	"fmt"
	"reflect"
)

type Person struct {
	Name string `json:"name"`
}

func main() {
	person := Person{Name: "Anya"}
	field := reflect.TypeOf(person).Field(0)
	fmt.Println(field.Name, field.Tag.Get("json"))
	value := reflect.ValueOf(&person).Elem().FieldByName("Name")
	if value.IsValid() && value.CanSet() && value.Kind() == reflect.String {
		value.SetString("Ravi")
	}
	fmt.Println(person.Name)
	copyValue := reflect.ValueOf(person).Field(0)
	if !copyValue.CanSet() {
		fmt.Println("invalid: field is not settable")
	}
}
''', 'Save as `main.go`; run `go run main.go`.',
'Name name\nRavi\ninvalid: field is not settable',
"""**Near-miss:** `reflect.ValueOf(person)` describes a copy. It can be
inspected but cannot be set. `ValueOf(&person).Elem()` reaches the original.
Check `IsValid` before operating on a field returned by `FieldByName`.

**Real error:** the program prints `invalid: field is not settable` before
attempting the forbidden operation. Removing the guard and calling
`copyValue.SetString("X")` panics with
`reflect: reflect.Value.SetString using unaddressable value`.

Unexported fields are not a supported reflective write path. A `json` tag is a
convention interpreted by the encoder; reflection does not rename the Go field
or validate the tag's business meaning. Avoid reflective traversal in a hot
loop unless measurement justifies its flexibility.""",
'[Go reflect reference](https://pkg.go.dev/reflect)')

lang(43, 'cpp', """C++20 type traits answer compile-time questions about types.
`if constexpr` chooses a branch during template instantiation, allowing the
other branch to use operations that the chosen type does not support.
This is compile-time metaprogramming, not general runtime member reflection.""",
[( 'template <typename T>\nstd::string describe(const T& value) {\n    if constexpr (std::is_integral_v<T>) {\n        return std::to_string(value);\n    } else {\n        return value;\n    }\n}', "For an integer instantiation only the numeric branch is used. A normal if would still require both branches to be well-formed for that T.")],
'''#include <iostream>
#include <stdexcept>
#include <string>
#include <type_traits>

template <typename T>
std::string describe(const T& value) {
    if constexpr (std::is_integral_v<T>) {
        return std::to_string(value);
    } else {
        static_assert(std::is_same_v<T, std::string>, "unsupported type");
        return value;
    }
}

int main() {
    std::cout << describe(42) << '\\n';
    std::cout << describe(std::string("Anya")) << '\\n';
    try {
        throw std::invalid_argument("unknown field: balance");
    } catch (const std::invalid_argument& exc) {
        std::cout << "invalid: " << exc.what() << '\\n';
    }
}
''', 'Save as `main.cpp`; run `g++ -Wall -Wextra -std=c++20 main.cpp -o main`, then `./main`.',
'42\nAnya\ninvalid: unknown field: balance',
"""**Near-miss:** replace `if constexpr` with `if`. Instantiating the template
with `std::string` now tries to compile `std::to_string(value)` too. Runtime
branch selection cannot make that expression valid.

**Real error:** the deliberately rejected field in the complete program prints
`invalid: unknown field: balance`. It demonstrates an adapter's explicit failure
path. Separately, `describe(3.5)` fails the `static_assert` with the diagnostic
message `unsupported type` (the surrounding compiler text varies).

`typeid(T).name()` is implementation-defined text, not a stable schema and not
a list of member names. For a C++20 Person serializer, explicitly map `name` to
`person.name` or use a library's documented registration facility. Do not claim
that this template discovers that mapping on its own.""",
'[C++ working draft: constexpr if](https://eel.is/c++draft/stmt.if)')

day(44, """Leela has made a cake for her aunt. At home she has a large oven, a mixer,
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
checking that the thing survives where it is actually going.""",
"""A build turns source into an artifact you can distribute. Packaging says
what files and dependencies travel with it. The target is the operating system
and processor architecture where it will run, not necessarily your laptop.

A Python wheel installs a package into a Python environment. A frozen application
bundles an interpreter and supporting files. A Go executable often carries its
Go dependencies, while cgo can add native library requirements. A C++ executable
may load shared libraries at runtime. A static library is an archive used during
linking; it is not itself a runnable program.

Build in a clean environment, record versions and the target, then smoke-test on
that target. A smoke test is a small real execution proving the artifact can
start and perform its basic job without your development checkout.""",
"source + build metadata -> build tool -> artifact\nartifact + runtime requirements -> target machine -> smoke test\nrecipe                    cake         can it be served here?",
"""I first name the target OS and architecture and whether an interpreter or
native libraries can be installed there. For Python users with Python, I ship
a wheel with dependency metadata. For users without Python, I can build a frozen
application for that platform. With Go I build the target executable and check
whether cgo introduces external requirements. With C++ I use a Release build
and verify the runtime libraries rather than assuming one file means no
dependencies. I test the artifact outside the source directory on a clean target,
including its version command and a failing invocation. I retain enough build
metadata to reproduce it and enough diagnostic information to debug a crash.""",
[("Is a wheel a standalone executable?", "No. It is an installable Python distribution and normally needs a compatible interpreter."),
 ("Can one binary run on every machine?", "No. OS, architecture, ABI, and native dependencies constrain compatibility."),
 ("Why test outside the checkout?", "The checkout can accidentally supply files or imports missing from the package.")],
"""I would deliver a tested artifact plus its runtime requirements and version.
For an internal Python tool, a wheel may be the simplest contract if Python is
already managed on the target. For a desktop user without Python, a platform
build with PyInstaller may be appropriate. For Go or C++, I check the binary's
actual dependencies. I would demonstrate the shipped artifact starting on the
target, not merely show that the compiler returned success on my laptop.""",
["Name the target OS and architecture before building.", "A wheel needs Python; a frozen app bundles a runtime.",
 "Static libraries are link inputs, not executables.", "Record versions and check native dependencies.", "Smoke-test the artifact outside the checkout."],
[("Ship a CLI that prints `krama 1.0` and rejects an unknown option.", "A reproducible entry point and a deliberate failure path."),
 ("Build a wheel and frozen Python app, a Go executable, and a CMake Release executable.", "The artifact and its runtime requirements differ by language."),
 ("Copy only the distributable files into a fresh directory and run the smoke test; record OS and architecture.", "Finding accidental dependencies on the development checkout.")],
["What still needs installing on the destination machine?", "Why can a successful cross-build still produce an unusable artifact?"])

lang(44,'python',"""`pyproject.toml` declares how a Python package is built and what it needs.
A wheel is an installable distribution; PyInstaller builds a platform-specific
application containing a Python runtime. Choose based on who will run the tool
and what they already have installed.""",
[( '[build-system]\nrequires = ["setuptools>=68"]\nbuild-backend = "setuptools.build_meta"', "Save this in pyproject.toml. The build frontend creates an isolated environment and calls the declared backend."),
 ('[project]\nname = "krama-demo"\nversion = "1.0.0"\nrequires-python = ">=3.12"\n[project.scripts]\nkrama-demo = "krama_demo:main"\n[tool.setuptools]\npy-modules = ["krama_demo"]', "Append this to the same file. The script entry names an importable callable; the module declaration includes the single source file.")],
'''import sys

def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1:] != ["--version"]:
        print("invalid: unknown option", file=sys.stderr)
        raise SystemExit(2)
    print("krama 1.0")

if __name__ == "__main__":
    main()
''', """Save the program as `krama_demo.py` beside the complete `pyproject.toml`
formed from the two fragments. Run `python krama_demo.py --version`.

For a wheel: `python -m pip install build`, then `python -m build --wheel`.
In a fresh virtual environment, install `dist/krama_demo-1.0.0-py3-none-any.whl`
with `python -m pip install` followed by that path, then run
`krama-demo --version`. A `py3-none-any` wheel contains no platform-specific
extension in this example; wheels with native extensions have narrower tags.

For an app: `python -m pip install pyinstaller`, then
`python -m PyInstaller --onefile --name krama-demo krama_demo.py`.
Run `dist/krama-demo --version` (Windows: `.\\dist\\krama-demo.exe --version`).
Build the frozen app on each supported target platform. Build-tool progress
and artifact paths vary; the application's output below does not.""",
'krama 1.0',
"""**Near-miss:** sending the `.whl` file to someone without Python does not
give them a runnable desktop program. Conversely, PyInstaller is not a general
cross-compiler: build and test per target platform.

**Real error:** run `python krama_demo.py --unknown`; stderr is
`invalid: unknown option` and the exit status is 2. Repeat that test on the
installed entry point and on the frozen executable.

Data files and dynamically discovered imports may need explicit packaging
configuration. Test outside the repository so the current directory cannot
hide missing files. A one-file app may unpack supporting files at startup;
one file does not mean your code was translated to native machine instructions.""",
'[Packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) and [PyInstaller operation](https://pyinstaller.org/en/stable/operating-mode.html)')

lang(44,'go',"""`go build` produces an executable for a selected OS and architecture.
Build flags can embed a version or remove local paths. A pure-Go build can
often travel as one executable, but cgo and platform resources require a more
careful runtime inventory.""",
[( 'go build -trimpath -ldflags="-X main.version=1.0" -o krama-demo .', "Run in a module created with go mod init example.com/krama-demo. -X sets an eligible string variable at link time; it cannot rewrite a constant."),
 ('$env:CGO_ENABLED = "0"\n$env:GOOS = "linux"\n$env:GOARCH = "amd64"\ngo build -trimpath -o krama-demo-linux .', "These are PowerShell commands for a pure-Go Linux build. Use a fresh terminal afterwards or restore these task-specific build settings before building for your host.")],
'''package main

import (
	"fmt"
	"os"
)

var version = "dev"

func main() {
	if len(os.Args) > 1 && !(len(os.Args) == 2 && os.Args[1] == "--version") {
		fmt.Fprintln(os.Stderr, "invalid: unknown option")
		os.Exit(2)
	}
	fmt.Println("krama", version)
}
''', """Save as `main.go`. In that directory run
`go mod init example.com/krama-demo`, then
`go build -trimpath -ldflags="-X main.version=1.0" -o krama-demo .`.
Run `./krama-demo --version`; on Windows name the output `krama-demo.exe`
and run `.\\krama-demo.exe --version`. The cross-build fragment is separate:
run its result on Linux amd64, not on Windows.""",
'krama 1.0',
"""**Near-miss:** changing `var version` to `const version` defeats the `-X`
assignment. Running `go run main.go` also prints `dev` because it did not use
the version-setting build command.

**Real error:** the built program with `--unknown` prints
`invalid: unknown option` on stderr and exits 2.

`CGO_ENABLED=0` disables cgo; it does not make a cgo-dependent package work.
Cross-compilation with cgo may require a target C compiler and native libraries.
Even a statically linked tool may need CA certificates or time-zone data at
runtime. `-ldflags="-s -w"` removes symbol/debug information; decide how you will
diagnose production failures before discarding it.""",
'[Go build command](https://pkg.go.dev/cmd/go)')

lang(44,'cpp',"""CMake describes build targets and their dependencies, then generates work
for a compiler and linker. A Release configuration enables the toolchain's
release settings. Static and shared libraries affect what gets linked now and
what must be present when the application starts.""",
[( 'cmake_minimum_required(VERSION 3.20)\nproject(krama_demo LANGUAGES CXX)\nadd_executable(krama-demo main.cpp)\ntarget_compile_features(krama-demo PRIVATE cxx_std_20)\nif(MSVC)\n  target_compile_options(krama-demo PRIVATE /W4)\nelse()\n  target_compile_options(krama-demo PRIVATE -Wall -Wextra)\nendif()', "Save as CMakeLists.txt. Requirements belong to the target so they follow it through the build graph."),
 ('cmake -S . -B build -DCMAKE_BUILD_TYPE=Release\ncmake --build build --config Release', "Single-configuration generators use CMAKE_BUILD_TYPE; multi-configuration generators such as Visual Studio select Release at build time.")],
'''#include <iostream>
#include <string_view>

int main(int argc, char* argv[]) {
    if (argc > 1 && !(argc == 2 && std::string_view(argv[1]) == "--version")) {
        std::cerr << "invalid: unknown option\\n";
        return 2;
    }
    std::cout << "krama 1.0\\n";
}
''', """Save as `main.cpp` beside `CMakeLists.txt` and run the two CMake commands.
Run `./build/krama-demo --version` for a Unix single-configuration build or
`.\\build\\Release\\krama-demo.exe --version` for Visual Studio.
For a direct GNU build, use
`g++ -Wall -Wextra -std=c++20 -O2 main.cpp -o krama-demo`.""",
'krama 1.0',
"""**Near-miss:** building a static library with `add_library(core STATIC ...)`
does not create an executable. Link it to an executable using
`target_link_libraries(krama-demo PRIVATE core)`. A `SHARED` library normally
must be found by the loader on the target machine.

**Real error:** `krama-demo --unknown` prints `invalid: unknown option` and
returns 2. Test this on the shipped executable too.

A Release build is not automatically fully static. The C++ runtime and other
libraries may remain dynamic. Install/copy the required runtime components,
check target ABI compatibility, and keep an unstripped diagnostic artifact
when you distribute stripped binaries. A successful link on the development
machine cannot prove that the destination's loader will find its libraries.""",
'[CMake tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)')

day(45, """Mina is helping four friends carry shopping upstairs after a family outing.
There are twenty bags in the car. At first everyone reaches into the boot at
once, and two people grab the same handle. Mina asks them to take one bag each,
close the boot while they walk away, and return for another only when their
hands are free.

Now four bags are moving at a time. The remaining bags wait safely in the car.
Mina keeps a count on her phone as each friend comes back. After five trips each,
the car should be empty. But one bag has a torn handle. Her brother sets it down,
finds another bag to put around it, and tries again. Nobody sends all four
friends to rescue that one bag; the others continue with the remaining shopping.

It starts to rain. Mina tells everyone that if the stairs become slippery they
will stop and leave the rest in the locked car until the rain passes. Finishing
everything is less important than knowing where every bag is and making sure
no one is still struggling alone on the stairs.

At the end she checks the car and the kitchen. Nineteen bags are upstairs, and
the last one is with her brother, who is replacing its torn handle. She does
not announce that all twenty are home just because all twenty have been picked
up once. Her count means delivered, and the last trip must finish before the
job is done.""",
"""Bounded concurrency means only a fixed number of downloads run at once.
Four workers repeatedly take the next URL. A timeout limits an attempt; a retry
budget limits how often a failure is tried again. Backoff inserts a delay between
attempts so a struggling destination is not hammered immediately.

Each URL owns one numbered output file. Write to a temporary `.part` file and
publish the final filename only after the response succeeds. A progress count
means completed jobs, including reported failures; it does not mean every job
succeeded. The final summary distinguishes those outcomes.

The programs use GET, retry transport failures and 5xx responses at most three
times, and bound each file to 1 MiB. They do not retry arbitrary mutations.
The fixture below serves local content so you can test without relying on a
public website. Run in a fresh output directory for each language.""",
"200 URLs -> next-job assignment -> 4 workers -> .part files\n                                      |             |\n                               bounded retry     success only\n                                      |             v\n                                failed result    final .bin\nall completed results -----------------------> summary",
"""I separate how many jobs exist from how many requests may be active. I use
a fixed worker count and reuse HTTP clients where the library supports it.
Every attempt has a timeout, and every job has a finite retry budget. A retry
starts a fresh temporary file so partial bytes cannot be mistaken for a complete
download. I classify failures: a 404 is usually final; selected 5xx responses
may justify backoff. I bound body sizes and keep final output names unique.
When cancellation is requested I stop admitting new work and ensure current
operations finish or hit a deadline. I report successes and failures separately
and tune concurrency using measured throughput and the destination's limits.""",
[("Why not 200 workers?", "The limit protects connections, memory, disk, and the remote service; more waiting tasks do not guarantee more throughput."),
 ("What can be retried?", "These GETs are safe to repeat; other operations require an idempotency contract."),
 ("What happens to a partial file?", "It keeps a temporary name and is removed on failure; only a successful attempt becomes the final file.")],
"""I would begin with four workers, per-attempt deadlines, three total attempts,
and a summary that identifies each failed URL. I would measure before raising
the limit. For a service I would also enforce a total operation deadline, honour
Retry-After where applicable, and consider a separate per-host limit. I would
test a timeout, a 404, a transient 500, and cancellation against a local fixture.
A run is complete only after the workers stop and every admitted job has an
accounted-for result.""",
["Bound active work independently of the URL count.", "Timeout each attempt and cap total attempts.",
 "Retry safe operations with backoff, not every failure.", "Publish a final filename only after success.", "Join workers and report failures as well as successes."],
[("Download one local `/ok` URL and publish `000.bin` only after success.", "Response checks, size bounds, and temporary file ownership."),
 ("Download 200 local URLs with exactly four workers and progress every 50 completions.", "Bounded work, unique outputs, and honest progress."),
 ("Inject 404, 500, and delay cases; cancel a run and record files and results.", "Finite retries, bounded shutdown, and no partial file presented as complete.")],
["Why do partial files need different names from successful downloads?", "What stops a retry loop or cancellation from leaving workers running forever?"])

DATA[45]['deliverable'] = '''### Project deliverable

Use `python/main.py`, `go/main.go`, and `cpp/main.cpp` in your own project
directory, with separate working directories for their outputs. Keep `urls.txt`,
an output folder, and a README recording dependency versions, commands, and the
measured maximum active requests. The complete lessons generate 200 identical
fixture URLs to make the first run reproducible; extend them to read one URL per
line from `urls.txt` without changing the worker limit.

Save the following shared fixture as `fixture.py` and run `python fixture.py`
in a separate terminal. It serves HTTP on loopback only; stop it with Ctrl+C.

```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import time

class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/slow":
            time.sleep(3)
        status = 500 if self.path == "/fail" else 404 if self.path == "/missing" else 200
        body = b"hello" if status == 200 else b"failed"
        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass  # A timed-out client may have closed its connection.

    def log_message(self, format: str, *args: object) -> None:
        pass

if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8090), Handler).serve_forever()
```

With `/ok`, expect 200 files, each containing the five bytes `hello`, no `.part`
files, and a final `success 200 failed 0`. With `/missing`, every job must fail
after one attempt. With `/fail`, every job must stop after three attempts.
For `/slow`, first test one URL; the two-second attempt limit should fail it.
Add a fixture counter so a `/flaky` URL returns 500 once and then 200; prove the
second attempt succeeds. Record that request count rather than guessing from
the progress display.

For cancellation, extend the Python entry point to expose an event, the Go
entry point to accept a signal-derived context, and C++ to stop assigning jobs
through a stop flag. The Python and Go examples already propagate cancellation;
the synchronous C++ example bounds each in-flight attempt with libcurl's timeout.
Require the cancelled run to stop admitting work, join its workers, remove
temporary files, and print an accurate partial summary. Do not call a run complete
just because all jobs were placed in a queue.

Done means all three implementations pass the same fixture cases, with at most
four active requests, finite retries, distinct final and partial filenames, and
a README explaining the remaining limitations (including body limits and the
absence of cross-process resume support).
'''

lang(45,'python',"""An `httpx.AsyncClient` reuses connections while `asyncio` workers wait for
network I/O without dedicating an OS thread to each request. Four worker tasks
consume the jobs. Their number, rather than the number of URLs, sets the active
download limit.""",
[( 'async with client.stream("GET", url) as response:\n    response.raise_for_status()', "The context closes the response on success or failure. Check status before writing a body to its destination."),
 ('async with asyncio.TaskGroup() as group:\n    for _ in range(4):\n        group.create_task(worker())', "TaskGroup waits for all workers and propagates cancellation. Network calls yield; the small local file writes below are synchronous.")],
'''import asyncio
from pathlib import Path
import httpx

async def fetch(client: httpx.AsyncClient, url: str, dest: Path) -> bool:
    part = dest.with_suffix(".part")
    try:
        for attempt in range(3):
            try:
                async with asyncio.timeout(2):
                    async with client.stream("GET", url) as response:
                        if 400 <= response.status_code < 500:
                            return False
                        response.raise_for_status()
                        total = 0
                        with part.open("wb") as output:
                            async for chunk in response.aiter_bytes():
                                total += len(chunk)
                                if total > 1024 * 1024:
                                    return False
                                output.write(chunk)
                part.replace(dest)
                return True
            except (httpx.HTTPError, TimeoutError):
                if attempt < 2:
                    await asyncio.sleep(0.1 * 2**attempt)
            except OSError:
                return False
        return False
    finally:
        part.unlink(missing_ok=True)

async def main() -> None:
    out = Path("downloads-python")
    out.mkdir(exist_ok=True)
    jobs = iter(enumerate(["http://127.0.0.1:8090/ok"] * 200))
    results: list[bool] = []
    async with httpx.AsyncClient(timeout=2, follow_redirects=False) as client:
        async def worker() -> None:
            for number, url in jobs:
                ok = await fetch(client, url, out / f"{number:03}.bin")
                results.append(ok)
                if len(results) % 50 == 0:
                    print(f"completed {len(results)}/200")
        async with asyncio.TaskGroup() as group:
            for _ in range(4):
                group.create_task(worker())
    print("success", sum(results), "failed", len(results) - sum(results))

if __name__ == "__main__":
    asyncio.run(main())
''', 'Start the fixture from [the shared practice](03-practice.md). Install with `python -m pip install httpx`. Save as `main.py`; run `python main.py` in a fresh working directory.',
'completed 50/200\ncompleted 100/200\ncompleted 150/200\ncompleted 200/200\nsuccess 200 failed 0',
"""**Near-miss:** `gather(*(fetch(...) for url in urls))` schedules one task
per URL without a worker bound. A semaphore bounds active calls but still
creates all those tasks; four consumers make the ownership easier to see.

**Real failure:** replace `/ok` with `/missing`; the application ends with
`success 0 failed 200` and no final files in a fresh output directory. No
exception is silently converted to success.

Do not swallow `CancelledError`; cleanup belongs in `finally`, as above.
`asyncio.timeout` covers the attempt, while HTTPX's timeout also limits network
wait phases. Synchronous disk writes can delay the event loop on a slow disk;
a production large-file downloader needs bounded offloading or an appropriate
asynchronous file strategy. This example deliberately caps each response.""",
'[HTTPX async support](https://www.python-httpx.org/async/) and [asyncio task groups](https://docs.python.org/3/library/asyncio-task.html)')

lang(45,'go',"""A Go worker pool sends job numbers through a channel to four goroutines.
A shared `http.Client` reuses its transport safely. Request contexts carry
cancellation and deadlines through the HTTP operation; result collection waits
until every worker has stopped.""",
[( 'attemptCtx, cancel := context.WithTimeout(ctx, 2*time.Second)\nreq, err := http.NewRequestWithContext(attemptCtx, http.MethodGet, url, nil)', "Cancel each attempt's context when the attempt finishes. Handle request construction errors before using req."),
 ('for i := 0; i < 4; i++ {\n\twg.Add(1)\n\tgo func() {\n\t\tdefer wg.Done()\n\t\tfor number := range jobs { results <- download(number) }\n\t}()\n}', "Workers own one job at a time. Close results only after Wait returns, never while a worker can still send.")],
'''package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"
)

func attempt(ctx context.Context, client *http.Client, url, part string) (bool, bool) {
	ctx, cancel := context.WithTimeout(ctx, 2*time.Second)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil { return false, false }
	resp, err := client.Do(req)
	if err != nil { return false, true }
	defer resp.Body.Close()
	if resp.StatusCode >= 500 { return false, true }
	if resp.StatusCode != 200 { return false, false }
	file, err := os.Create(part)
	if err != nil { return false, false }
	n, copyErr := io.Copy(file, io.LimitReader(resp.Body, 1024*1024+1))
	closeErr := file.Close()
	if n > 1024*1024 || closeErr != nil { return false, false }
	return copyErr == nil, copyErr != nil
}

func fetch(ctx context.Context, client *http.Client, url, dest string) bool {
	part := dest + ".part"
	defer func() {
		if err := os.Remove(part); err != nil && !os.IsNotExist(err) { fmt.Fprintln(os.Stderr, err) }
	}()
	for tries := 0; tries < 3; tries++ {
		if ctx.Err() != nil { return false }
		ok, retry := attempt(ctx, client, url, part)
		if ok {
			if err := os.Rename(part, dest); err != nil { return false }
			return true
		}
		if !retry || tries == 2 { return false }
		select {
		case <-ctx.Done(): return false
		case <-time.After(time.Duration(100*(1<<tries)) * time.Millisecond):
		}
	}
	return false
}

func main() {
	if err := os.MkdirAll("downloads-go", 0755); err != nil { fmt.Println(err); return }
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	client := &http.Client{Timeout: 2*time.Second, CheckRedirect: func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse }}
	defer client.CloseIdleConnections()
	jobs := make(chan int)
	results := make(chan bool)
	var wg sync.WaitGroup
	for i := 0; i < 4; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for number := range jobs {
				dest := filepath.Join("downloads-go", fmt.Sprintf("%03d.bin", number))
				results <- fetch(ctx, client, "http://127.0.0.1:8090/ok", dest)
			}
		}()
	}
	go func() { defer close(jobs); for i := 0; i < 200; i++ { jobs <- i } }()
	go func() { wg.Wait(); close(results) }()
	done, success := 0, 0
	for ok := range results {
		done++
		if ok { success++ }
		if done%50 == 0 { fmt.Printf("completed %d/200\\n", done) }
	}
	fmt.Println("success", success, "failed", done-success)
}
''', 'Start the fixture in [the shared practice](03-practice.md). Save as `main.go`; run `gofmt -w main.go`, then `go run main.go` in a fresh directory.',
'completed 50/200\ncompleted 100/200\ncompleted 150/200\ncompleted 200/200\nsuccess 200 failed 0',
"""**Near-miss:** deferring every response close inside a long worker loop
keeps bodies open until the worker returns. The attempt helper gives each
response and context a short scope. Reading through EOF on success enables
connection reuse; closing a rejected unread body may sacrifice reuse, not
correctness.

**Real failure:** changing the fixture URL to `/missing` yields
`success 0 failed 200`. These HTTP responses are failures even though `Do`
returned no transport error.

The total context is 30 seconds; after expiry, pending jobs are accounted for
as failures without new HTTP calls. The current producer still assigns those
numbers so the summary covers all 200. For a very large input, stop the producer
on cancellation and report unstarted jobs separately. A context does not cancel
arbitrary disk I/O; keep filesystem assumptions explicit.""",
'[Go HTTP client](https://pkg.go.dev/net/http) and [Go context](https://pkg.go.dev/context)')

lang(45,'cpp',"""A fixed group of C++ threads can download concurrently with libcurl.
Each worker owns its own easy handle; sharing one handle concurrently is not
allowed. Initialise libcurl before starting workers and clean it up only after
they have all joined.""",
[( 'curl_easy_setopt(handle, CURLOPT_TIMEOUT_MS, 2000L);\ncurl_easy_setopt(handle, CURLOPT_NOSIGNAL, 1L);', "A total transfer timeout bounds each attempt. NOSIGNAL is the documented setting for threaded applications; resolver capabilities affect timeout details."),
 ('std::atomic<int> next{0};\nint number = next.fetch_add(1);', "An atomic counter assigns each number once. The program's mutex separately serialises progress output and completed-result counters.")],
'''#include <curl/curl.h>
#include <atomic>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

struct Sink { std::ofstream file; std::size_t bytes = 0; };

std::size_t write_body(char* data, std::size_t size, std::size_t count, void* user) {
    auto& sink = *static_cast<Sink*>(user);
    const auto n = size * count;
    if (n > 1024 * 1024 - sink.bytes) return 0;
    sink.file.write(data, static_cast<std::streamsize>(n));
    if (!sink.file) return 0;
    sink.bytes += n;
    return n;
}

bool fetch(const std::string& url, const std::filesystem::path& dest) {
    const auto part = std::filesystem::path(dest.string() + ".part");
    for (int attempt = 0; attempt < 3; ++attempt) {
        std::unique_ptr<CURL, decltype(&curl_easy_cleanup)> handle(curl_easy_init(), curl_easy_cleanup);
        if (!handle) return false;
        Sink sink{std::ofstream(part, std::ios::binary), 0};
        if (!sink.file) return false;
        CURL* h = handle.get();
        const bool configured =
            curl_easy_setopt(h, CURLOPT_URL, url.c_str()) == CURLE_OK &&
            curl_easy_setopt(h, CURLOPT_TIMEOUT_MS, 2000L) == CURLE_OK &&
            curl_easy_setopt(h, CURLOPT_NOSIGNAL, 1L) == CURLE_OK &&
            curl_easy_setopt(h, CURLOPT_WRITEFUNCTION, write_body) == CURLE_OK &&
            curl_easy_setopt(h, CURLOPT_WRITEDATA, &sink) == CURLE_OK;
        const CURLcode result = configured ? curl_easy_perform(h) : CURLE_FAILED_INIT;
        long status = 0;
        const auto info = curl_easy_getinfo(h, CURLINFO_RESPONSE_CODE, &status);
        sink.file.close();
        std::error_code ec;
        if (result == CURLE_OK && info == CURLE_OK && status == 200 && sink.file) {
            std::filesystem::rename(part, dest, ec);
            if (!ec) return true;
        }
        std::filesystem::remove(part, ec);
        if (ec) return false;
        if (!configured || result == CURLE_WRITE_ERROR || (result == CURLE_OK && status < 500)) return false;
        if (attempt < 2) std::this_thread::sleep_for(std::chrono::milliseconds(100 * (1 << attempt)));
    }
    return false;
}

int main() {
    std::error_code ec;
    std::filesystem::create_directories("downloads-cpp", ec);
    if (ec) { std::cerr << ec.message() << '\\n'; return 1; }
    if (curl_global_init(CURL_GLOBAL_DEFAULT) != CURLE_OK) return 1;
    std::atomic<int> next{0};
    std::mutex mutex;
    int done = 0, success = 0;
    {
        std::vector<std::jthread> workers;
        for (int i = 0; i < 4; ++i) workers.emplace_back([&] {
            for (;;) {
                const int number = next.fetch_add(1);
                if (number >= 200) break;
                const auto digits = std::to_string(1000 + number).substr(1);
                const bool ok = fetch("http://127.0.0.1:8090/ok", "downloads-cpp/" + digits + ".bin");
                std::lock_guard lock(mutex);
                ++done;
                success += ok;
                if (done % 50 == 0) std::cout << "completed " << done << "/200\\n";
            }
        });
    }
    curl_global_cleanup();
    std::cout << "success " << success << " failed " << done - success << '\\n';
}
''', """Start the fixture in [the shared practice](03-practice.md). Save as `main.cpp`.
On Linux with a C++20 compiler and libcurl development headers installed, run
`g++ -Wall -Wextra -std=c++20 -pthread main.cpp -lcurl -o downloader`, then
`./downloader`. A Windows build needs a matching libcurl development package
and its documented include/library paths; the Unix command is not a Windows
dependency installer.""",
'completed 50/200\ncompleted 100/200\ncompleted 150/200\ncompleted 200/200\nsuccess 200 failed 0',
"""**Near-miss:** using one easy handle from all four workers is not made
safe by libcurl being usable in threaded programs. Each attempt here owns its
handle. Reusing a handle sequentially within a worker can improve connection
reuse; this teaching version constructs one per attempt.

**Real failure:** `/missing` produces `success 0 failed 200`, even though
libcurl can successfully transfer the 404 body. HTTP status and transfer status
are distinct. A callback returning zero aborts a body that exceeds the size
limit or cannot be written.

`jthread` joins on destruction but does not magically interrupt a synchronous
libcurl call. This version has a finite per-attempt deadline and retry budget;
add an explicit stop flag/progress callback for user-driven cancellation.
Filesystem exceptions and allocation failures need a worker-level exception
boundary in a production version. Do not let unexpected exceptions escape a
thread and terminate the process without recording failed work.""",
'[libcurl thread safety](https://curl.se/libcurl/c/threadsafe.html) and [easy interface](https://curl.se/libcurl/c/libcurl-easy.html)')

day(46, """Arun and his cousin are speaking through an open doorway while moving into
a new flat. His cousin asks him to repeat every number she says so she knows he
heard it correctly. She says the first few numbers slowly. Arun repeats them,
and she nods before continuing.

Then a lorry passes outside. She pauses halfway through a longer number and
finishes it after the noise fades. Arun has heard all the sounds in the right
order, but the pause did not tell him whether she had finished the number.
They agree that she will say 'done' after each complete number. Now the pauses
can be as long or as short as needed without changing where one number ends.

Another cousin arrives at the door and starts asking about a box. Arun cannot
keep both conversations straight if he stops listening to the first person
halfway through. He asks his brother to help the newcomer while he finishes
with the first cousin. Each conversation now has someone responsible for it.

Before lunch, his cousin says she has no more numbers to read. Arun repeats the
last one and leaves the doorway. His brother is still talking about the box,
so that conversation continues. The front door remains open for other people
arriving at the flat. Ending one conversation is different from closing the
door to everyone. By lunchtime they have a way to begin, continue, and finish
each exchange without mixing up the people or the numbers.""",
"""A listening socket accepts new TCP connections. Each accepted socket is
a separate byte stream connected to one client. `bind` chooses a local address,
`listen` enables acceptance, and `accept` returns a connected socket. Go and
Boost.Asio package some of those steps together.

TCP preserves byte order, not the boundaries of your writes. One receive may
return part of a send or combine several sends. An echo service needs no message
parser: it writes each received chunk back unchanged. A request protocol needs
framing, such as a length prefix or a delimiter.

These examples accept two clients, start one worker per connection, then join
both workers and exit. That finite limit makes the demonstration easy to stop;
a long-running service needs admission limits, deadlines, and a shutdown policy.
The client closes its sending half after `hello` and reads until the echo ends.""",
"listening socket :8081\n        | accept #1 -> connected socket A -> worker A\n        | accept #2 -> connected socket B -> worker B\nclient send: [he][llo]    receives may be: [hello] or [h][ello]\nbytes stay ordered; chunk boundaries do not",
"""The operating system completes the TCP handshake and queues a connection
for the listening socket. Accept gives my program a new connected socket; it
does not replace the listener. I hand that socket to a worker with clear
ownership. The worker reads bytes until EOF or an error and writes the actual
received count back, handling partial writes. I do not assume that one read is
one request. If this were a real protocol I would define framing and a maximum
message size. I would bound active connections and set deadlines so an idle
client cannot retain a worker forever. On shutdown I stop accepting, then
close or drain active connections and join their workers.""",
[("Does listen's backlog bound all clients?", "No. It concerns pending connections; active connection limits are an application policy."),
 ("What does EOF mean?", "The peer has ended its sending direction. You may still have bytes to send back."),
 ("Why can a single read be short?", "TCP delivers available bytes without preserving the sender's write boundaries.")],
"""I would show two sockets in the design: a listener and one accepted socket
per client. Each worker owns and closes its accepted socket. The echo loop
returns precisely the bytes received; it is not a text-line parser. For a
production server I would add an active-connection limit and deadlines rather
than create an unlimited number of threads. I would test a split send, an empty
connection, and two overlapping clients to show that framing and ownership are
understood, not just that a single happy-path message happens to work.""",
["The listener accepts; the connected socket carries one conversation.", "TCP preserves byte order, not message boundaries.",
 "Write all received bytes, including after a short read.", "EOF ends one sending direction.", "Bound connections and define shutdown ownership."],
[("Echo `hello` and an empty connection; compare received bytes exactly.", "EOF, zero-length input, and socket ownership."),
 ("Send 100,000 bytes in varying chunk sizes and read until EOF.", "Short reads and writes cannot truncate the stream."),
 ("Connect two clients concurrently; add idle deadlines and an active-connection cap.", "A slow connection must not monopolise acceptance or resources.")],
["Why is one send not guaranteed to produce one receive?", "Who closes the listening socket and each accepted socket during shutdown?"])

DATA[46]['deliverable'] = '''Use the complete server from each language lesson. Start one server at a
time. In another terminal run this client twice; the server intentionally stops
after two connections. Save it as `client.py` and run `python client.py`.

```python
import socket

with socket.create_connection(("127.0.0.1", 8081), timeout=3) as connection:
    connection.sendall(b"hello")
    connection.shutdown(socket.SHUT_WR)
    received = bytearray()
    while chunk := connection.recv(4096):
        received.extend(chunk)
    print(received.decode("ascii"))
```

Expected output on each run is `hello`. For the empty case, omit `sendall`
and expect an empty line. For the large case, collect the bytes and compare
them directly instead of decoding or printing the whole body. The Python/Go
servers use timeouts; the blocking Boost.Asio example requires cooperative
clients and explains the deadline extension. State that difference in your
comparison rather than claiming identical shutdown guarantees.
'''

lang(46,'python',"""Python's `socket` module exposes the TCP listener and connected sockets
directly. A `threading.Thread` lets a second connection proceed while the first
waits for bytes. Context managers close each socket when its owner finishes.""",
[( 'listener.bind(("127.0.0.1", 8081))\nlistener.listen(2)\nconnection, address = listener.accept()', "Bind to loopback for this local exercise. accept returns a new socket plus the peer address; the listener remains available."),
 ('while chunk := connection.recv(4096):\n    connection.sendall(chunk)', "recv returns at most the requested amount. Empty bytes mean EOF; sendall handles sending the whole chunk or raises an error.")],
'''import socket
import threading

def echo(connection: socket.socket) -> None:
    with connection:
        connection.settimeout(5)
        try:
            while chunk := connection.recv(4096):
                connection.sendall(chunk)
        except OSError as exc:
            print("connection failed:", exc)

def main() -> None:
    workers: list[threading.Thread] = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", 8081))
            listener.listen(2)
            listener.settimeout(30)
            print("listening 8081", flush=True)
            for _ in range(2):
                connection, _address = listener.accept()
                worker = threading.Thread(target=echo, args=(connection,))
                worker.start()
                workers.append(worker)
    except OSError as exc:
        print("listener failed:", exc)
    finally:
        for worker in workers:
            worker.join()

if __name__ == "__main__":
    main()
''', 'Save as `main.py`; run `python main.py`. Run the [shared practice client](03-practice.md) twice in a second terminal. Each client prints `hello`; the server prints the line below.',
'listening 8081',
"""**Near-miss:** `connection.send(chunk)` can send fewer bytes than requested.
Discarding its return value loses the unsent suffix. Use `sendall` here.
Decoding each receive separately can also split a multi-byte character; echo
bytes without decoding.

**Real error:** leave an accepted client idle for five seconds. The caught
socket timeout prints `connection failed: timed out`. The listener's 30-second
timeout bounds waiting for a missing second client separately.

Threads help overlapping I/O waits; they are not permission to create one
unbounded worker for every incoming client. The GIL does not turn CPU-heavy
Python parsing into parallel CPU work. A production accept loop needs a cap,
and an overall connection deadline differs from this per-operation timeout.""",
'[Python socket reference](https://docs.python.org/3/library/socket.html)')

lang(46,'go',"""`net.Listen` creates a TCP listener, and `Accept` returns a `net.Conn`.
One goroutine can own each connection while the listener accepts the next.
Deadlines and explicit closes keep blocked I/O from becoming indefinite work.""",
[( 'listener, err := net.Listen("tcp", "127.0.0.1:8081")', "Listen packages socket setup, binding, and listening. Return on failure before trying to call methods on the listener."),
 ('if err := connection.SetDeadline(time.Now().Add(5 * time.Second)); err != nil {\n\tfmt.Println(err)\n\treturn\n}\nif _, err := io.Copy(connection, connection); err != nil {\n\tfmt.Println("connection failed:", err)\n}', "io.Copy handles the stream transfer. This absolute deadline bounds the connection's reads and writes, not just one wait.")],
'''package main

import (
	"fmt"
	"io"
	"net"
	"sync"
	"time"
)

func echo(connection net.Conn) {
	defer connection.Close()
	if err := connection.SetDeadline(time.Now().Add(5 * time.Second)); err != nil {
		fmt.Println("deadline failed:", err)
		return
	}
	if _, err := io.Copy(connection, connection); err != nil {
		fmt.Println("connection failed:", err)
	}
}

func main() {
	listener, err := net.Listen("tcp", "127.0.0.1:8081")
	if err != nil { fmt.Println(err); return }
	defer listener.Close()
	fmt.Println("listening 8081")
	var workers sync.WaitGroup
	defer workers.Wait()
	for i := 0; i < 2; i++ {
		connection, err := listener.Accept()
		if err != nil { fmt.Println(err); return }
		workers.Add(1)
		go func() { defer workers.Done(); echo(connection) }()
	}
}
''', 'Save as `main.go`; run `gofmt -w main.go`, then `go run main.go`. Run the [shared client](03-practice.md) twice; each client prints `hello`.',
'listening 8081',
"""**Near-miss:** putting `echo(connection)` directly in the accept loop
serialises clients. Starting the goroutine allows the second Accept while the
first connection is waiting. The goroutine owns the connection close.

**Real error:** reading from a connection after explicitly closing it returns
an error containing `use of closed network connection`; the surrounding
operation and endpoint addresses vary. An idle client's deadline instead yields
`i/o timeout` in the wrapped network error.

This finite example still waits indefinitely in Accept if the second client
never connects. Close the listener from a shutdown coordinator, or use a
TCPListener deadline, to bound that wait. The connection deadline does not
apply to the listener. A goroutine is lightweight, but its socket and buffers
still consume resources, so a long-lived service needs an active limit.""",
'[Go net reference](https://pkg.go.dev/net)')

lang(46,'cpp',"""Boost.Asio wraps platform sockets in owning C++ objects and provides
portable read/write operations. This lesson uses its synchronous interface
with one thread per accepted connection. `boost::asio::write` completes the
whole supplied buffer or reports an error.""",
[( 'tcp::acceptor listener(context, tcp::endpoint(boost::asio::ip::make_address("127.0.0.1"), 8081));\ntcp::socket connection = listener.accept();', "The acceptor owns the listener; the socket owns one connection. Boost.Asio hides the POSIX versus Windows setup details."),
 ('std::size_t n = connection.read_some(boost::asio::buffer(buffer), error);\nif (n != 0) boost::asio::write(connection, boost::asio::buffer(buffer.data(), n));', "read_some may return fewer bytes than the buffer capacity. Pass the actual count to write, never the whole unused buffer.")],
'''#include <boost/asio.hpp>
#include <array>
#include <iostream>
#include <thread>
#include <utility>
#include <vector>

using boost::asio::ip::tcp;

void echo(tcp::socket connection) {
    try {
        std::array<char, 4096> buffer{};
        for (;;) {
            boost::system::error_code error;
            const auto n = connection.read_some(boost::asio::buffer(buffer), error);
            if (n != 0) boost::asio::write(connection, boost::asio::buffer(buffer.data(), n));
            if (error == boost::asio::error::eof) break;
            if (error) throw boost::system::system_error(error);
        }
    } catch (const std::exception& exc) {
        std::cerr << "connection failed: " << exc.what() << '\\n';
    }
}

int main() {
    try {
        boost::asio::io_context context;
        tcp::acceptor listener(context, tcp::endpoint(boost::asio::ip::make_address("127.0.0.1"), 8081));
        std::cout << "listening 8081" << std::endl;
        std::vector<std::jthread> workers;
        for (int i = 0; i < 2; ++i) {
            workers.emplace_back(echo, listener.accept());
        }
    } catch (const std::exception& exc) {
        std::cerr << "listener failed: " << exc.what() << '\\n';
        return 1;
    }
}
''', """Install Boost development headers and libraries for your compiler. Save as
`main.cpp`. On Linux, run
`g++ -Wall -Wextra -std=c++20 -pthread main.cpp -lboost_system -o echo`, then
`./echo`. A Windows build requires the matching Boost package and Winsock
linkage (normally handled by its toolchain configuration). Run the
[shared client](03-practice.md) twice; each prints `hello`.""",
'listening 8081',
"""**Near-miss:** writing `buffer.size()` after receiving three bytes echoes
unused bytes too. Use `n`. Moving the socket into its worker makes ownership
clear; capturing a short-lived local socket by reference does not.

**Real error:** an operation on a closed socket reports `Bad file descriptor`
on common Unix builds; the full exception text and Windows diagnostic differ.
The program labels such failures `connection failed:` rather than hiding them.

These synchronous reads have no timer. An idle client can keep a worker and
its join blocked indefinitely; run the cooperative fixture for this version.
For bounded shutdown, build the next version with asynchronous reads and a
`steady_timer` that closes the socket on the same executor when the deadline
expires. A stop token alone cannot interrupt the blocking read. C++ RAII
closes owned sockets, but it does not invent a cancellation policy.""",
'[Boost.Asio tutorials](https://www.boost.org/doc/libs/latest/doc/html/boost_asio/tutorial.html)')

day(47, """Nisha phones a bakery to order tea and snacks for a meeting. The first
time she calls, she gives her name, explains where the office is, and asks what
is available. The person at the bakery answers, then waits while she checks
with her colleagues.

She could hang up and call again for each question. Instead, she keeps the
conversation open while she confirms the quantity and asks about delivery.
She does not have to introduce herself three times, and the person helping her
does not have to find the same order again after each call.

The bakery says they have run out of one snack. Nisha heard the answer clearly;
the call itself worked. That is different from hearing nothing because the
phone line went silent. For the missing snack she chooses another item. For a
silent line she might call back, but first she checks whether the order was
already accepted. She does not want two deliveries just because she missed the
last few words.

Her meeting begins in ten minutes. She tells the bakery she can wait for a
reply for another minute, then she needs to decide. She also repeats the
delivery address to make sure the answer concerns the right office. Before
ending the call, she listens to the final total and confirms the order number.
Keeping a conversation open saved effort, but she still had to check what the
answer meant and finish the exchange properly.""",
"""An HTTP client sends a method, URL, headers, and sometimes a body, then
receives a status, headers, and body. A connection pool keeps reusable
connections instead of establishing a new TCP/TLS connection for every call.
A transport error means the exchange could not be completed; a 500 response
means the server replied with a failure status.

JSON decoding is a separate step that can fail even after status 200. Set
timeouts, check status, then decode the expected body shape. Reuse a client or
session and close responses according to the library's ownership rules.
Headers describe the representation: `Content-Type` says what you sent and
`Accept` says what you want back.

Retrying GET and retrying a payment POST are different decisions. If the reply
is lost after a POST is processed, an automatic retry may duplicate the action.
Use the operation's idempotency contract rather than retrying every timeout.""",
"request -> reusable client -> pooled connection -> server\n                |                                  |\n        transport failure? <-----------------------+\n                | response\n          status acceptable? -> JSON valid? -> domain result",
"""I keep a client for the lifetime of the component making calls, because
its transport can reuse connections. I set explicit timeouts rather than let a
slow destination retain resources forever. I distinguish failure to receive a
response from receiving a 500, and I treat invalid JSON as another failure.
I read or close the response as the library requires so pooled connections are
not stranded. I send Content-Type for a JSON body and check the returned data
before passing it into my application. I only retry operations whose semantics
permit repetition; for a mutation I need an idempotency key or another explicit
contract. Connection reuse improves repeated calls but does not replace those
correctness checks.""",
[("Is HTTP 500 a network exception?", "Not necessarily. Go and cpr return a response; Python raises a status exception only when requested."),
 ("Why close a body?", "It releases resources; consuming to EOF often permits connection reuse."),
 ("Does a timeout prove the server did nothing?", "No. The action might have completed before its reply was lost.")],
"""Creating a client per request discards connection-pool reuse and can add
DNS, TCP, and TLS work to repeated calls. I would share a supported client,
configure deadlines and pool limits, and scope each response carefully. I
would test a 200 with valid JSON, a 500 with an error body, invalid JSON, and a
delayed response. For POST I would not infer failure of the business operation
from a timeout alone. The retry policy belongs to the operation's semantics,
not to a blanket catch-and-repeat helper.""",
["Reuse the client or session, not an open response body.", "Transport success and HTTP success are different.",
 "Set timeouts and check JSON separately.", "Read/close responses to release resources.", "A timed-out mutation may already have happened."],
[("GET `/ok`, parse JSON, and print the boolean field.", "Headers, status, and decoding are separate checks."),
 ("POST a JSON item through the same session; check 201 and the returned id.", "Body encoding and connection reuse."),
 ("Handle `/fail`, malformed JSON, and a delayed fixture without retrying POST automatically.", "Transport, HTTP, and representation failures need different decisions.")],
["Why can a 200 response still be unusable?", "When can retrying a timed-out POST create a duplicate?"])

DATA[47]['deliverable'] = '''Save this fixture as `fixture.py`, run `python fixture.py` in a separate
terminal, and stop it with Ctrl+C when done. It accepts the three calls in each
lesson. Add malformed-JSON and delayed routes for exercise 3.

```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def reply(self, status: int, body: dict[str, object]) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/ok":
            self.reply(200, {"ok": True})
        else:
            self.reply(500, {"error": {"code": "unavailable"}})

    def do_POST(self) -> None:
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        try:
            item = json.loads(body)
        except (ValueError, UnicodeError):
            self.reply(400, {"error": {"code": "bad_json"}})
            return
        if self.path != "/items" or not isinstance(item, dict) or item.get("name") != "tea":
            self.reply(400, {"error": {"code": "invalid_item"}})
            return
        self.reply(201, {"id": 1, "name": "tea"})

    def log_message(self, format: str, *args: object) -> None:
        pass

if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8091), Handler).serve_forever()
```

Record the three statuses (200, 201, 500), the parsed success values, and a
separate transport failure with the fixture stopped. A 500 body is not a
successful item response. Keep the JSON representation and expected status
checks the same in all three implementations.
'''

lang(47,'python',"""HTTPX provides synchronous and asynchronous clients; Requests provides
a familiar synchronous Session. Both can reuse connections through an owned
client/session. JSON helpers encode bodies and decode responses, but you still
choose timeouts and decide which HTTP statuses are acceptable.""",
[( 'with httpx.Client(timeout=2, headers={"Accept": "application/json"}) as client:\n    response = client.get("http://127.0.0.1:8091/ok")\n    response.raise_for_status()', "The client owns its pool. raise_for_status separates an HTTP failure response from the decoded success path."),
 ('with requests.Session() as session:\n    response = session.post(url, json={"name": "tea"}, timeout=(1, 2))\n    response.raise_for_status()', "The Requests alternative takes connect/read timeouts here. Neither Requests' tuple nor HTTPX's phase timeouts should be described as an overall workflow deadline.")],
'''import httpx

def main() -> None:
    base = "http://127.0.0.1:8091"
    try:
        with httpx.Client(timeout=2, headers={"Accept": "application/json"}) as client:
            response = client.get(base + "/ok")
            response.raise_for_status()
            if response.json().get("ok") is not True:
                raise ValueError("missing ok field")
            print("GET", response.status_code)
            response = client.post(base + "/items", json={"name": "tea"})
            response.raise_for_status()
            if response.status_code != 201:
                raise ValueError("expected 201")
            print("POST", response.status_code, response.json()["name"])
            response = client.get(base + "/fail")
            if response.status_code >= 400:
                print("HTTP", response.status_code)
    except httpx.RequestError:
        print("transport failed")
    except httpx.HTTPStatusError as exc:
        print("HTTP", exc.response.status_code)
    except (ValueError, KeyError, AttributeError, TypeError):
        print("invalid response")

if __name__ == "__main__":
    main()
''', 'Run the fixture from [the shared practice](03-practice.md). Install `httpx` with `python -m pip install httpx`. Save as `main.py`; run `python main.py`. The comparison snippet additionally needs `requests`.',
'GET 200\nPOST 201 tea\nHTTP 500',
"""**Near-miss:** `client.post(url, data={"name": "tea"})` sends form data,
not the JSON body expected by this fixture. Use `json=`. A 200 with an HTML
body still fails JSON decoding.

**Real error:** stop the fixture and rerun the program. It catches the
connection failure and prints `transport failed`. With the fixture running,
the deliberate failed route prints `HTTP 500` instead.

Creating an AsyncClient inside every iteration defeats pooling too. Keep its
scope around the whole workload. When streaming, close the stream even if you
stop reading early. Do not log authorization headers or entire response bodies
just to diagnose a status failure; record bounded, relevant context.""",
'[HTTPX clients](https://www.python-httpx.org/advanced/clients/) and [Requests sessions](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects)')

lang(47,'go',"""Go's `http.Client` owns request behaviour and uses a Transport for
connections. A shared client is safe for concurrent use. `Do` returns HTTP
error statuses as ordinary responses, so checking only `err` is insufficient.""",
[( 'client := &http.Client{Timeout: 2 * time.Second}\nreq, err := http.NewRequest(http.MethodGet, url, nil)', "Client.Timeout includes connection setup, redirects, and reading the response body. Per-request contexts can impose a tighter bound."),
 ('resp, err := client.Do(req)\nif err != nil { return err }\ndefer resp.Body.Close()', "Scope the body close to one call. Consume the expected response before making a pooled connection available for reuse.")],
'''package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

func call(client *http.Client, method, path string, body []byte) (int, map[string]any, error) {
	req, err := http.NewRequest(method, "http://127.0.0.1:8091"+path, bytes.NewReader(body))
	if err != nil { return 0, nil, err }
	req.Header.Set("Accept", "application/json")
	if body != nil { req.Header.Set("Content-Type", "application/json") }
	resp, err := client.Do(req)
	if err != nil { return 0, nil, err }
	defer resp.Body.Close()
	data, err := io.ReadAll(io.LimitReader(resp.Body, 1024*1024+1))
	if err != nil { return resp.StatusCode, nil, err }
	if len(data) > 1024*1024 { return resp.StatusCode, nil, fmt.Errorf("body too large") }
	if resp.StatusCode >= 400 { return resp.StatusCode, nil, nil }
	var result map[string]any
	if err := json.Unmarshal(data, &result); err != nil { return resp.StatusCode, nil, err }
	return resp.StatusCode, result, nil
}

func main() {
	client := &http.Client{Timeout: 2 * time.Second}
	defer client.CloseIdleConnections()
	status, body, err := call(client, http.MethodGet, "/ok", nil)
	if err != nil { fmt.Println("request failed:", err); return }
	if status != 200 || body["ok"] != true { fmt.Println("invalid response"); return }
	fmt.Println("GET", status)
	status, body, err = call(client, http.MethodPost, "/items", []byte(`{"name":"tea"}`))
	if err != nil { fmt.Println("request failed:", err); return }
	if status != 201 || body["name"] != "tea" { fmt.Println("invalid response"); return }
	fmt.Println("POST", status, body["name"])
	status, _, err = call(client, http.MethodGet, "/fail", nil)
	if err != nil { fmt.Println("request failed:", err); return }
	fmt.Println("HTTP", status)
}
''', 'Start the [practice fixture](03-practice.md). Save as `main.go`; run `gofmt -w main.go`, then `go run main.go`.',
'GET 200\nPOST 201 tea\nHTTP 500',
"""**Near-miss:** `err == nil` after `client.Do` does not mean status 200.
The `/fail` request completes normally and prints `HTTP 500`.

**Real error:** change the JSON request to the bytes `not-json`. The fixture
returns 400 and the program prints `invalid response` at its expected-201
check. With the fixture stopped, it prints `request failed:` followed by the
platform's connection diagnostic.

The default zero Timeout is not an application deadline. Set one or supply
a bounded request context. Reuse the Transport, not a single mutable Request
across concurrent operations. Reading a bounded body here permits complete
JSON validation; for large responses stream intentionally and account for
early-close effects on connection reuse.""",
'[Go net/http reference](https://pkg.go.dev/net/http)')

lang(47,'cpp',"""cpr wraps libcurl with C++ request and response objects. A `cpr::Session`
can reuse connection state across calls; `cpr::Response` exposes transfer
errors separately from HTTP status. Use a JSON library to encode and decode
bodies instead of building JSON with string concatenation.""",
[( 'cpr::Session session;\nsession.SetTimeout(cpr::Timeout{2000});\nsession.SetHeader(cpr::Header{{"Accept", "application/json"}});', "Session owns the reusable request machinery. Configure the timeout in milliseconds and do not share a mutable session concurrently."),
 ('session.SetBody(cpr::Body{nlohmann::json{{"name", "tea"}}.dump()});\nsession.SetHeader(cpr::Header{{"Content-Type", "application/json"}});\nauto response = session.Post();', "Serialise JSON and label it correctly. Changing the request method does not itself clear every other persistent session setting.")],
'''#include <cpr/cpr.h>
#include <nlohmann/json.hpp>
#include <iostream>
#include <stdexcept>

void require(const cpr::Response& response, long expected) {
    if (response.error.code != cpr::ErrorCode::OK) throw std::runtime_error("transport failed");
    if (response.status_code != expected) throw std::runtime_error("unexpected HTTP status");
}

int main() {
    try {
        cpr::Session session;
        session.SetTimeout(cpr::Timeout{2000});
        session.SetHeader(cpr::Header{{"Accept", "application/json"}});
        session.SetUrl(cpr::Url{"http://127.0.0.1:8091/ok"});
        auto response = session.Get();
        require(response, 200);
        if (!nlohmann::json::parse(response.text).at("ok").get<bool>()) throw std::runtime_error("invalid response");
        std::cout << "GET " << response.status_code << '\\n';
        session.SetUrl(cpr::Url{"http://127.0.0.1:8091/items"});
        session.SetHeader(cpr::Header{{"Accept", "application/json"}, {"Content-Type", "application/json"}});
        session.SetBody(cpr::Body{nlohmann::json{{"name", "tea"}}.dump()});
        response = session.Post();
        require(response, 201);
        std::cout << "POST " << response.status_code << ' '
                  << nlohmann::json::parse(response.text).at("name").get<std::string>() << '\\n';
        session.SetBody(cpr::Body{""});
        session.SetUrl(cpr::Url{"http://127.0.0.1:8091/fail"});
        response = session.Get();
        require(response, 500);
        std::cout << "HTTP " << response.status_code << '\\n';
    } catch (const std::exception& exc) {
        std::cerr << exc.what() << '\\n';
        return 1;
    }
}
''', """Start the [practice fixture](03-practice.md). Save as `main.cpp` and use
this `CMakeLists.txt` (CMake, Git, and a C++20 toolchain are prerequisites):

```cmake
cmake_minimum_required(VERSION 3.20)
project(client LANGUAGES CXX)
include(FetchContent)
FetchContent_Declare(cpr GIT_REPOSITORY https://github.com/libcpr/cpr.git GIT_TAG 1.11.2)
FetchContent_Declare(json GIT_REPOSITORY https://github.com/nlohmann/json.git GIT_TAG v3.11.3)
FetchContent_MakeAvailable(cpr json)
add_executable(client main.cpp)
target_compile_features(client PRIVATE cxx_std_20)
target_link_libraries(client PRIVATE cpr::cpr nlohmann_json::nlohmann_json)
if(MSVC)
  target_compile_options(client PRIVATE /W4)
else()
  target_compile_options(client PRIVATE -Wall -Wextra)
endif()
```

Run `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release`, then
`cmake --build build --config Release`. Run `./build/client` on a Unix
single-configuration build or `.\\build\\Release\\client.exe` with Visual
Studio. Configuration downloads the pinned example dependencies and may
require platform TLS development libraries; follow cpr's build requirements.""",
'GET 200\nPOST 201 tea\nHTTP 500',
"""**Near-miss:** checking only `response.error.code` accepts an HTTP 500 as
an application success. The complete program explicitly expects 500 only for
its failure demonstration.

**Real error:** stop the fixture; the program emits `transport failed` and
returns 1. Give it malformed JSON with status 200 and JSON parsing throws a
separate exception. Those are different failures.

A session carries state: headers, bodies, cookies, and connection settings.
Reset per-request values when switching operations. Do not disable certificate
verification to work around a production HTTPS failure; configure the correct
trust store. This loopback HTTP fixture isolates request behaviour from TLS
setup, which is a separate deployment requirement.""",
'[cpr source and build guide](https://github.com/libcpr/cpr) and [JSON parsing](https://json.nlohmann.me/api/basic_json/parse/)')

CPP_HTTP_BUILD = '''Save the program as `main.cpp` and use this `CMakeLists.txt`. Install
CMake, Git, and a C++20 compiler first. Configuration fetches the example's
pinned dependency versions; retain those versions when comparing runs.

```cmake
cmake_minimum_required(VERSION 3.20)
project(server LANGUAGES CXX)
include(FetchContent)
FetchContent_Declare(httplib GIT_REPOSITORY https://github.com/yhirose/cpp-httplib.git GIT_TAG v0.18.1)
FetchContent_Declare(json GIT_REPOSITORY https://github.com/nlohmann/json.git GIT_TAG v3.11.3)
FetchContent_MakeAvailable(httplib json)
add_executable(server main.cpp)
target_compile_features(server PRIVATE cxx_std_20)
target_link_libraries(server PRIVATE httplib::httplib nlohmann_json::nlohmann_json)
if(MSVC)
  target_compile_options(server PRIVATE /W4)
else()
  target_compile_options(server PRIVATE -Wall -Wextra)
endif()
```

Run `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release`, then
`cmake --build build --config Release`. Start `./build/server` on Unix with
a single-configuration generator or `.\\build\\Release\\server.exe` for
Visual Studio. Run the requests from [the shared practice](03-practice.md)
in another terminal, then stop the server with Ctrl+C. On a GNU toolchain
the target uses `-Wall -Wextra` and C++20 through the CMake configuration.
'''

day(48, """Farah is helping at a neighbourhood lunch. People come to the serving
table with different requests. Some want to know whether tea is ready. Others
want a plate prepared. Farah puts the tea question at one end of the table and
asks her brother to handle plates at the other end.

A guest asks for a plate but does not say how many people it is for. Her
brother asks for the missing number before starting. Another guest asks for a
negative number of plates as a joke. He refuses that request too. Having heard
the words clearly does not make the request sensible.

Farah tells everyone that a ready plate will contain rice, vegetables, and a
spoon. Her brother checks those three things before handing one over. A guest
should not have to guess whether a missing spoon is deliberate or whether the
helpers forgot it. The expected request and the expected reply are both clear.

During the busiest part of lunch, Farah hears someone ask for directions to
the bus stop. Nobody at the table is assigned that job. She says so politely
instead of handing over a plate and hoping that was what the guest meant.
Later she notices that the tea helper is also chopping vegetables, so people
asking simple tea questions have to wait. She separates those jobs again. A
clear place for each request only helps when the person answering it can
actually do the work and return the promised reply.""",
"""An HTTP server accepts a request and chooses a handler using its method
and path. The handler validates input, performs work, and creates a response.
A request model describes accepted fields; a response model describes promised
output. Frameworks differ in how much validation they perform automatically.

The examples expose `GET /health` and `POST /echo`. Health returns
`{"ok":true}`. Echo accepts a JSON object with one nonempty `name`, then returns
that name. An absent route must not accidentally run a different handler.

Set response headers before writing the body. In Go and many other servers,
writing body bytes commits a default success status if none was set. Starting
the listener blocks until the server stops; test requests from another terminal.
These local examples focus on handling one request, not deployment or TLS.""",
"HTTP method + path -> router -> input validation -> handler\n                                     |                |\n                                  rejection      response model\n                                     |                |\n                                     +---- status + JSON ----> client",
"""I follow a request through the layers. The listener accepts a connection,
the HTTP implementation parses the request, and the router chooses a handler
from the method and path. Input decoding checks representation; validation
checks allowed values. The handler performs the operation and produces a
response with a deliberate status and content type. I distinguish unknown
routes from invalid input and from internal failures. I do not expose exception
traces as a public response. I also check the framework's execution model:
blocking work inside an async route can stall other requests, and shared state
inside concurrent handlers needs protection. I prove the boundary with a valid
request and at least one malformed and one semantically invalid request.""",
[("Does valid JSON imply valid input?", "No. An object with an empty name is syntactically valid but violates this endpoint's rule."),
 ("Why set headers first?", "The first body write may commit the status and headers, after which changing them is too late."),
 ("Is an async handler automatically nonblocking?", "No. A blocking call inside it still blocks its execution thread.")],
"""For POST /echo I require a JSON object, validate the name, and return a
documented JSON response. FastAPI supplies model validation; Go and cpp-httplib
need explicit decoding and checks in this example. I keep domain work separate
from the HTTP adapter so tests can distinguish invalid input from broken
business logic. Before calling the endpoint finished I test wrong methods,
unknown paths, malformed JSON, and an empty name. A working browser GET alone
does not prove a request-body endpoint behaves correctly.""",
["Route by method and path.", "Decode the representation, then validate values.",
 "Set status and content type before the body.", "A response model is an output contract.", "Test rejection paths as well as the success path."],
[("Serve GET `/health` with 200 and JSON `ok: true`.", "Listener, route selection, and response content type."),
 ("Serve POST `/echo` with a required nonempty name and a documented response.", "Request/response models versus manual validation."),
 ("Send malformed JSON, an empty name, an unknown field, and the wrong method.", "Identify exactly which layer rejects each input and which status it uses.")],
["What changes when validation is automatic rather than handwritten?", "Why can writing the response body before its status create a bug?"])

DATA[48]['deliverable'] = '''Start one language server at a time on 127.0.0.1:8080. For a shell-neutral
check, save this as `client.py` and run `python client.py` after installing
HTTPX with `python -m pip install httpx`:

```python
import httpx

with httpx.Client(base_url="http://127.0.0.1:8080", timeout=2) as client:
    for response in (
        client.get("/health"),
        client.post("/echo", json={"name": "tea"}),
        client.post("/echo", json={"name": ""}),
    ):
        print(response.status_code, response.json())
```

The first two statuses are 200 with `{"ok": true}` and `{"name": "tea"}`.
The empty-name request gets FastAPI's default 422, or the explicit 400 in Go
and C++. Record that difference; Day 050 defines a common custom error contract.
You can also run `curl.exe -i http://127.0.0.1:8080/health` on Windows or
`curl -i http://127.0.0.1:8080/health` on Unix. Do not compare header order or
framework access-log timestamps as if they were application output.
'''

lang(48,'python',"""FastAPI connects Python callables to HTTP routes and uses Pydantic models
to validate request bodies and describe responses. A route decorator binds a
method and path. A model annotation describes the expected data, not a promise
that arbitrary input will be accepted.""",
[( 'class EchoIn(BaseModel):\n    model_config = ConfigDict(extra="forbid")\n    name: str = Field(min_length=1, max_length=80)', "A nonempty string of at most 80 characters is the input policy. Rejecting extra fields catches misspelled client keys."),
 ('@app.post("/echo", response_model=EchoOut)\ndef echo(item: EchoIn) -> EchoOut:\n    return EchoOut(name=item.name)', "FastAPI decodes and validates the body before invoking this function. The response model states what can leave it.")],
'''from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()

class EchoIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=80)

class EchoOut(BaseModel):
    name: str

@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}

@app.post("/echo", response_model=EchoOut)
def echo(item: EchoIn) -> EchoOut:
    return EchoOut(name=item.name)
''', 'Install `fastapi` and `uvicorn` with `python -m pip install fastapi uvicorn`. Save as `main.py`; run `python -m uvicorn main:app --host 127.0.0.1 --port 8080`. Run the [shared client](03-practice.md). The valid response bodies are shown below; Uvicorn prints its own startup/access logs.',
'{"ok":true}\n{"name":"tea"}',
"""**Near-miss:** accepting `dict` without a model does not enforce this
name rule. A Pydantic field annotation makes the boundary explicit. Whitespace
is still nonempty here; Day 050 adds a stricter domain policy.

**Real error:** the body `{"name":""}` receives HTTP 422 with validation
type `string_too_short` and message `String should have at least 1 character`.
An omitted name produces type `missing` and message `Field required`.
The full error envelope includes its location and input.

`async def` is appropriate when the work awaits asynchronous operations.
Calling a blocking HTTP library or doing long CPU work directly inside it is
not made asynchronous by that spelling. These synchronous `def` endpoints are
run through the framework's thread-pool handling; their lack of shared mutable
state keeps this first example simple.""",
'[FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/) and [response models](https://fastapi.tiangolo.com/tutorial/response-model/)')

lang(48,'go',"""Go's ServeMux maps method/path patterns to handlers. A handler receives
an `http.ResponseWriter` and a request; it explicitly decodes input and writes
output. Go 1.23 includes the method-aware routing used here.""",
[( 'mux.HandleFunc("GET /health", health)\nmux.HandleFunc("POST /echo", echo)', "These patterns include the method, so the route table distinguishes GET from POST before entering your code."),
 ('decoder := json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096))\ndecoder.DisallowUnknownFields()', "Limit the body and reject unknown object fields. After the first decode, require EOF to reject a second JSON document.")],
'''package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"time"
	"unicode/utf8"
)

func reply(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(value); err != nil { fmt.Println("write failed:", err) }
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		reply(w, 200, map[string]bool{"ok": true})
	})
	mux.HandleFunc("POST /echo", func(w http.ResponseWriter, r *http.Request) {
		defer r.Body.Close()
		var item struct { Name string `json:"name"` }
		decoder := json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096))
		decoder.DisallowUnknownFields()
		if err := decoder.Decode(&item); err != nil { reply(w, 400, map[string]string{"error": "invalid body"}); return }
		if err := decoder.Decode(new(any)); !errors.Is(err, io.EOF) { reply(w, 400, map[string]string{"error": "one object required"}); return }
		if item.Name == "" || utf8.RuneCountInString(item.Name) > 80 { reply(w, 400, map[string]string{"error": "invalid name"}); return }
		reply(w, 200, item)
	})
	server := &http.Server{Addr: "127.0.0.1:8080", Handler: mux, ReadHeaderTimeout: 2*time.Second, ReadTimeout: 5*time.Second, WriteTimeout: 5*time.Second}
	fmt.Println("listening 8080")
	if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) { fmt.Println(err) }
}
''', 'Save as `main.go`; run `gofmt -w main.go`, then `go run main.go`. Run the [practice client](03-practice.md). The server starts with the line below; successful response bodies are `{"ok":true}` and `{"name":"tea"}` (with a trailing newline).',
'listening 8080',
"""**Near-miss:** decoding once accepts a second JSON value left unread in
the body. The explicit EOF check rejects `{"name":"tea"}{"name":"coffee"}`.

**Real error:** sending `{"name":""}` returns HTTP 400 with
`{"error":"invalid name"}`. Sending an unknown key triggers the earlier
`{"error":"invalid body"}` response.

Calling `Write` before `WriteHeader(400)` may already send status 200. The
reply helper orders these operations deliberately. Set server timeouts instead
of relying on a zero-value long-lived listener. Body-size rejection uses the
same 400 envelope in this first example; a public API may distinguish 413 and
also enforce media type, which the later API contract makes explicit.""",
'[Go ServeMux and Server](https://pkg.go.dev/net/http)')

lang(48,'cpp',"""cpp-httplib provides HTTP routes and response objects around a blocking
server interface. It does not turn a parsed JSON value into a validated domain
object for you. Use nlohmann/json to parse, then check shape and values before
reading fields.""",
[( 'server.Get("/health", [](const httplib::Request&, httplib::Response& response) {\n    response.set_content(R"({"ok":true})", "application/json");\n});', "The route attaches a handler to GET /health. set_content sets the body and representation type."),
 ('auto item = nlohmann::json::parse(request.body, nullptr, false);\nif (item.is_discarded() || !item.is_object()) {\n    response.status = 400;\n}', "The nonthrowing parse form reports syntax failure as a discarded value. Object validation remains a separate check.")],
'''#include <httplib.h>
#include <nlohmann/json.hpp>
#include <iostream>

int main() {
    httplib::Server server;
    server.set_payload_max_length(4096);
    server.set_read_timeout(5, 0);
    server.set_write_timeout(5, 0);
    server.Get("/health", [](const httplib::Request&, httplib::Response& response) {
        response.set_content(R"({"ok":true})", "application/json");
    });
    server.Post("/echo", [](const httplib::Request& request, httplib::Response& response) {
        const auto item = nlohmann::json::parse(request.body, nullptr, false);
        if (!item.is_object() || item.size() != 1 || !item.contains("name") || !item["name"].is_string()) {
            response.status = 400;
            response.set_content(R"({"error":"invalid body"})", "application/json");
            return;
        }
        const auto name = item["name"].get<std::string>();
        if (name.empty() || name.size() > 80) {
            response.status = 400;
            response.set_content(R"({"error":"invalid name"})", "application/json");
            return;
        }
        response.set_content(nlohmann::json{{"name", name}}.dump(), "application/json");
    });
    std::cout << "listening 8080" << std::endl;
    if (!server.listen("127.0.0.1", 8080)) {
        std::cerr << "listen failed\\n";
        return 1;
    }
}
''',CPP_HTTP_BUILD,
'listening 8080',
"""**Near-miss:** indexing `item["name"]` before proving the input is an
object with a string field can throw or create unintended values. Check the
shape first. A JSON string containing an object's spelling is not an object.

**Real error:** an empty name yields HTTP 400 and
`{"error":"invalid name"}`; malformed JSON yields
`{"error":"invalid body"}`. A failed bind prints `listen failed`.

`std::string::size()` counts bytes here, unlike Python's character count and
the Go rune count. The ASCII fixtures fit all three policies; define a common
Unicode policy before claiming identical behaviour for non-ASCII input.
Handlers may execute concurrently. Capturing a mutable map by reference will
require locking when you add state in Day 050.""",
'[cpp-httplib usage](https://github.com/yhirose/cpp-httplib) and [JSON parse](https://json.nlohmann.me/api/basic_json/parse/)')

day(49, """At the entrance to a school play, Imran checks each visitor's invitation
before sending them to a seat. The invitation says which row they should use.
He does not ask every person already sitting in the hall to check invitations
again. One check at the entrance is easier to remember and harder to miss.

His sister stands beside him with a counter on her phone. She counts everyone
who approaches, including people who discover they have come to the wrong
event. When someone is turned away, that still matters to her count. If she
only counted people after they sat down, she would miss the confusion building
outside the door.

A guest shows an invitation for row twelve. Imran checks the invitation first,
then points towards the right aisle. Another shows an invitation but says
'the row with my friends' instead of a number. Imran asks for a clear row before
sending them anywhere. Being allowed inside and knowing where to go are
separate questions.

Halfway through the evening, his sister takes over the entrance. The seating
helpers do not change their jobs. The rule remains in one place, and everyone
still passes through it. At the end they compare the number of visitors who
approached with the number admitted. They can explain the difference because
the count began before the invitation check, not after it. The position of a
shared step changes what it can see, even when the step itself stays the same.""",
"""A router chooses a handler; a path parameter extracts a value such as the
`7` in `/items/7`. Middleware wraps a request around shared behaviour such as
logging. A dependency supplies or validates something a group of handlers needs,
such as authentication.

Order is observable. If logging surrounds authentication, rejected requests
are logged. If logging runs only inside the authenticated route, they vanish
from that log. Authentication decides who may proceed; path validation decides
whether an identifier is well formed. Neither proves that an item exists.

The examples use a fixed demonstration bearer token, `demo`, to show control
flow on loopback. This is not a credential system. A deployed service needs
real credential verification, HTTPS, and a policy for secret storage. The log
records method and path, never the Authorization header.""",
"request -> logging begins -> authentication -> router/path check -> handler\n                   |                |                              |\n                   |             rejection                         |\n                   +----------- log completion <------------------+",
"""I make logging a wrapper around the request pipeline so it sees both
successful and rejected attempts. I keep authentication in a reusable boundary,
such as a router dependency or middleware, and put resource-specific permission
checks next to the operation. A route extracts the item id and validates its
format before the handler uses it. I test middleware order explicitly: a
missing token must be rejected and still appear in the completion log. I log
bounded request metadata and status rather than credentials. If the framework
provides a response object after the inner handler, I inspect that object;
if it writes directly, I use a response-writer wrapper carefully to capture
the committed status without changing response behaviour.""",
[("Does authentication belong in every handler?", "Shared identity checks belong in a reusable boundary; resource-specific authorisation remains explicit."),
 ("Which order logs rejected requests?", "Logging outside authentication sees the early rejection too."),
 ("Is a route parameter already a trusted id?", "No. Validate its shape/range and then perform existence and permission checks.")],
"""I would use one outer logging wrapper and one shared authentication step,
then routes for the operations. I would verify missing credentials, invalid
identifiers, and unknown paths because each may leave the pipeline at a
different point. A middleware wrapper is useful only if it preserves the
framework's response semantics. In Go, for example, a minimal ResponseWriter
wrapper can hide optional interfaces needed by streaming. I would use a
well-tested wrapper when those capabilities matter rather than silently breaking
them while adding a status field to a log.""",
["Routing selects work; middleware wraps shared behaviour.", "Logging outside authentication sees rejections.",
 "Validate path parameters before domain lookup.", "Authentication is not resource authorisation.", "Do not log credentials or break response capabilities."],
[("Add GET `/items/7` and extract the id; reject zero and nonnumeric input.", "Routing and parameter validation are distinct."),
 ("Require the demo bearer token for item routes through one shared boundary.", "No copied authentication checks in individual handlers."),
 ("Log every attempted request, including missing-token and invalid-id cases; swap wrapper order and explain the difference.", "Composition order changes observable behaviour.")],
["Which requests disappear from logs if logging is placed inside authentication?", "How do route parameters, authentication, and resource authorisation differ?"])

DATA[49]['deliverable'] = '''Start one implementation at a time, then run this `client.py` with HTTPX:

```python
import httpx

with httpx.Client(base_url="http://127.0.0.1:8080", timeout=2) as client:
    denied = client.get("/items/7")
    accepted = client.get("/items/7", headers={"Authorization": "Bearer demo"})
    invalid = client.get("/items/0", headers={"Authorization": "Bearer demo"})
    print(denied.status_code)
    print(accepted.status_code, accepted.json())
    print(invalid.status_code)
```

Expect 401, then 200 with `{"id":7}`, then FastAPI's default 422 or the explicit
400 in Go/C++. All three attempts must appear in the server's application log.
The C++ example logs method/path only; Python and Go also capture status.
Extend C++'s logger with response status as part of exercise 3. Add unknown
routes and wrong methods, record each framework's result, and say whether
authentication ran before routing for that case. The examples deliberately
show both router-scoped authentication (FastAPI) and an outer gate (Go/C++).
'''

lang(49,'python',"""FastAPI's APIRouter groups routes, path annotations validate parameters,
and dependencies can enforce a shared authentication rule. HTTP middleware
surrounds the route pipeline and can observe the returned response status.
These are complementary mechanisms rather than three names for one hook.""",
[( 'router = APIRouter(prefix="/items", dependencies=[Depends(authenticate)])', "Every route registered on this router inherits the dependency. Unrelated routes do not automatically require it."),
 ('@app.middleware("http")\nasync def log_request(request: Request, call_next):\n    response = await call_next(request)\n    print(request.method, request.url.path, response.status_code)\n    return response', "The wrapper sees normal error responses too. The complete version uses finally so an unexpected exception is logged with its initial 500 status.")],
'''from collections.abc import Awaitable, Callable
from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Path, Request
from starlette.responses import Response

app = FastAPI()

def authenticate(authorization: Annotated[str | None, Header()] = None) -> None:
    if authorization != "Bearer demo":
        raise HTTPException(status_code=401, detail="unauthorized", headers={"WWW-Authenticate": "Bearer"})

router = APIRouter(prefix="/items", dependencies=[Depends(authenticate)])

@router.get("/{item_id}")
def item(item_id: Annotated[int, Path(gt=0)]) -> dict[str, int]:
    return {"id": item_id}

@app.middleware("http")
async def log_request(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        print(request.method, request.url.path, status, flush=True)

app.include_router(router)
''', 'Install with `python -m pip install fastapi uvicorn`. Save as `main.py`; run `python -m uvicorn main:app --host 127.0.0.1 --port 8080 --no-access-log`. Run the [practice client](03-practice.md); application logs follow.',
'GET /items/7 401\nGET /items/7 200\nGET /items/0 422',
"""**Near-miss:** calling the logging helper only inside `item` misses the
unauthorised request because the dependency rejects it before the handler.

**Real error:** without Authorization, `/items/7` returns 401 and
`{"detail":"unauthorized"}` with a Bearer challenge. `/items/0` with the
demo token fails validation with type `greater_than` and message
`Input should be greater than 0`.

Router dependencies run for matched routes, not as a universal front-door
gate for every unknown path. Stacking multiple middleware layers changes
their order; test observed behaviour rather than relying on visual proximity
to a handler. A real token verifier should supply an identity to downstream
code; the demonstration equality check only illustrates rejection and scope.""",
'[FastAPI middleware](https://fastapi.tiangolo.com/tutorial/middleware/) and [router dependencies](https://fastapi.tiangolo.com/tutorial/bigger-applications/)')

lang(49,'go',"""ServeMux method/path patterns can capture named segments, and
`Request.PathValue` retrieves them. Middleware is an ordinary function taking
an `http.Handler` and returning one. The order in the final expression defines
which wrapper gets the request first.""",
[( 'mux.HandleFunc("GET /items/{id}", item)\nhandler := logging(authenticate(mux))', "Logging is outermost, so it observes authentication failures before the router is reached."),
 ('id, err := strconv.Atoi(r.PathValue("id"))\nif err != nil || id <= 0 {\n\thttp.Error(w, "invalid id", http.StatusBadRequest)\n\treturn\n}', "A captured segment is text, not a validated integer. Check both conversion and the domain range.")],
'''package main

import (
	"errors"
	"fmt"
	"net/http"
	"strconv"
	"time"
)

type recorder struct { http.ResponseWriter; status int }
func (w *recorder) WriteHeader(status int) {
	if w.status == 0 { w.status = status; w.ResponseWriter.WriteHeader(status) }
}
func (w *recorder) Write(data []byte) (int, error) {
	if w.status == 0 { w.WriteHeader(200) }
	return w.ResponseWriter.Write(data)
}
func logging(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		recorded := &recorder{ResponseWriter: w}
		next.ServeHTTP(recorded, r)
		status := recorded.status
		if status == 0 { status = 200 }
		fmt.Println(r.Method, r.URL.Path, status)
	})
}
func authenticate(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("Authorization") != "Bearer demo" {
			w.Header().Set("WWW-Authenticate", "Bearer")
			http.Error(w, "unauthorized", 401)
			return
		}
		next.ServeHTTP(w, r)
	})
}
func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /items/{id}", func(w http.ResponseWriter, r *http.Request) {
		id, err := strconv.Atoi(r.PathValue("id"))
		if err != nil || id <= 0 { http.Error(w, "invalid id", 400); return }
		w.Header().Set("Content-Type", "application/json")
		if _, err := fmt.Fprintf(w, `{"id":%d}`, id); err != nil { fmt.Println("write failed:", err) }
	})
	server := &http.Server{Addr: "127.0.0.1:8080", Handler: logging(authenticate(mux)), ReadHeaderTimeout: 2*time.Second, WriteTimeout: 5*time.Second}
	if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) { fmt.Println(err) }
}
''','Save as `main.go`; run `gofmt -w main.go`, then `go run main.go` with Go 1.23+. Run the [practice client](03-practice.md).',
'GET /items/7 401\nGET /items/7 200\nGET /items/0 400',
"""**Near-miss:** `authenticate(logging(mux))` does not log rejected
credentials: the authentication wrapper returns before invoking logging.

**Real error:** the unauthorised response body is `unauthorized` followed by
a newline; status is 401. An invalid id gets `invalid id` with status 400.
These plain-text errors will become consistent JSON errors in Day 050.

The recorder is deliberately limited to ordinary nonstreaming responses. It
does not preserve every optional ResponseWriter interface, handle all 1xx
responses, or log a panic as a normal completion. For streaming, hijacking, or
production recovery use a tested wrapper with the required capabilities.
Go's `GET` pattern also matches HEAD; account for that in method tests.""",
'[Go routing and ResponseWriter](https://pkg.go.dev/net/http)')

lang(49,'cpp',"""cpp-httplib routes can use regular-expression captures, while a
pre-routing handler can accept or reject a request before route dispatch.
A logger observes completed exchanges. Keeping these roles separate prevents
every endpoint from copying the same credential check.""",
[( 'server.set_pre_routing_handler([](const httplib::Request& request, httplib::Response& response) {\n    if (request.get_header_value("Authorization") == "Bearer demo")\n        return httplib::Server::HandlerResponse::Unhandled;\n    response.status = 401;\n    response.set_content("unauthorized", "text/plain");\n    return httplib::Server::HandlerResponse::Handled;\n});', "Unhandled means continue normal dispatch; Handled means the hook produced the response. Reversing them defeats the gate."),
 ('server.Get(R"(/items/([^/]+))", handler);', "The first parenthesised capture is available as request.matches[1]. The handler still has to validate that captured text.")],
'''#include <httplib.h>
#include <charconv>
#include <iostream>
#include <mutex>
#include <string>

int main() {
    httplib::Server server;
    std::mutex log_mutex;
    server.set_read_timeout(5, 0);
    server.set_write_timeout(5, 0);
    server.set_pre_routing_handler([](const httplib::Request& request, httplib::Response& response) {
        if (request.get_header_value("Authorization") == "Bearer demo")
            return httplib::Server::HandlerResponse::Unhandled;
        response.status = 401;
        response.set_header("WWW-Authenticate", "Bearer");
        response.set_content("unauthorized", "text/plain");
        return httplib::Server::HandlerResponse::Handled;
    });
    server.Get(R"(/items/([^/]+))", [](const httplib::Request& request, httplib::Response& response) {
        const std::string text = request.matches[1].str();
        int id = 0;
        const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), id);
        if (error != std::errc{} || end != text.data() + text.size() || id <= 0) {
            response.status = 400;
            response.set_content("invalid id", "text/plain");
            return;
        }
        response.set_content("{\\"id\\":" + std::to_string(id) + "}", "application/json");
    });
    server.set_logger([&](const httplib::Request& request, const httplib::Response&) {
        std::lock_guard lock(log_mutex);
        std::cout << request.method << ' ' << request.path << std::endl;
    });
    if (!server.listen("127.0.0.1", 8080)) { std::cerr << "listen failed\\n"; return 1; }
}
''',CPP_HTTP_BUILD,
'GET /items/7\nGET /items/7\nGET /items/0',
"""**Near-miss:** `std::stoi("7oops")` can parse an initial integer unless
you check the consumed position. `from_chars` exposes the endpoint explicitly;
the complete program requires full consumption and checks overflow.

**Real error:** `/items/0` with the demo token returns 400 and `invalid id`.
Without the token the pre-routing hook returns 401 and `unauthorized` first.

This pre-routing gate applies more broadly than a FastAPI router dependency,
including paths that may later have no matching route. Be deliberate about
health checks and public routes. Log output is protected by a mutex so
concurrent lines do not interleave. In a production log, also bound and escape
untrusted path text; never add the raw credential just because it is available.""",
'[cpp-httplib routing hooks and logger](https://github.com/yhirose/cpp-httplib)')

day(50, """Dev is organising the snacks for a weekly club meeting. Members send him
requests on his phone. He gives each accepted request a number and repeats the
item name back to its owner. When someone asks what they ordered, they can give
the number instead of explaining the whole conversation again.

One member sends only an empty message. Dev asks for an item name. Another
asks to change order ninety, but there have only been six orders. Dev says he
cannot find that order. Those are different problems, and he wants his replies
to make that clear without making the member guess.

His sister helps him after lunch. They agree to use the same words for the
same problem. If an order cannot be found, both say so directly. They do not
let one person say 'try again' while the other says 'wrong name' for the same
missing order. The members should not need to know which helper answered.

A member cancels order four. Dev removes it and confirms that the cancellation
is finished. Later someone asks for order four again. He says it is no longer
there; he does not silently assign the number to a different snack.

Before going home, the helpers compare the current orders rather than every
message ever sent. Adding, reading, changing, and cancelling all refer to the
same numbered items. Clear numbers and consistent replies have made it possible
for two people to do the work without requiring every member to understand how
the helpers keep their list.""",
"""CRUD means create, read, update, and delete. A resource is the item these
operations address, such as `/items/1`. The API contract includes paths, methods,
accepted data, statuses, and error bodies. JSON syntax is only one part of it.

Today all three implementations use the same small contract: POST `/items`
creates with 201 and Location; GET `/items` lists; GET `/items/{id}` reads;
PUT `/items/{id}` replaces an existing item; DELETE returns 204 without a body.
Names contain 1–80 printable ASCII characters and must not be all spaces.
Unknown input fields are rejected. Integers used as ids must be positive.

Malformed or invalid input receives 400, missing items 404, and non-JSON
write requests 415. Application errors use `{"error":{"code":...,"message":...}}`.
These examples store state in memory with a lock: restarting loses it and
multiple processes would have different stores. That is a teaching constraint,
not a persistence design.""",
"POST /items -> validate -> lock/create -> 201 + Location\nGET /items/1 -------------------------> 200 or 404\nPUT /items/1 -> validate -> lock/replace -> 200 or 404\nDELETE /items/1 ---------> lock/remove -> 204 or 404\ninvalid input -> one error envelope; never a successful-looking result",
"""I define a stable machine-readable code and a human-readable message in
the error envelope. Clients branch on the code, not wording that may change.
I choose statuses deliberately: a created resource gets 201 and a Location;
a completed deletion gets 204 with no body; an unknown item gets 404. I validate
types and domain rules before changing state. The read-check-write sequence
for an update must be protected as one operation. I keep framework exceptions
behind the API boundary so callers do not receive stack traces or inconsistent
shapes. I also state limits: this sample's memory store is process-local, ids
are server-assigned, and a retried create can duplicate an item unless I add
an idempotency contract.""",
[("400 or 422?", "Both appear in API designs; this contract chooses 400 for input rejection and translates FastAPI's default 422."),
 ("Why does 204 have no JSON body?", "It is a no-content response. Clients should not try to decode JSON from it."),
 ("Does a mutex make the store durable?", "No. It coordinates threads in one process, not restarts or other processes.")],
"""A 400 response could be `{"error":{"code":"invalid_input","message":
"name must be 1-80 printable ASCII characters"}}`. The code is the stable
contract; the message helps the caller fix the request. I would not include a
traceback, SQL text, or secrets. I test that rejected writes leave the stored
item unchanged. I also test create, read, replace, delete, and a second read of
the deleted id. Those checks prove the resource lifecycle and its errors agree
across implementations, rather than merely proving each route exists.""",
["CRUD describes one resource lifecycle.", "Validate before mutation; protect compound updates.",
 "Use deliberate statuses: 201 create, 204 delete, 404 missing.", "Give errors stable codes and useful messages.", "A process-local lock is not persistence or cross-process coordination."],
[("Implement create/list/read with 201, Location, stable ids, and 404 for absence.", "A consistent resource representation and lifecycle."),
 ("Add full replacement and deletion; reject invalid writes without changing stored state.", "Atomic updates and a bodyless 204."),
 ("Run the shared lifecycle client against all three servers, then test malformed JSON and wrong media types.", "The same observable contract across framework boundaries.")],
["Why should clients branch on an error code rather than its message?", "What breaks if this in-memory server runs in two processes?"])

DATA[50]['deliverable'] = '''### One API contract, three implementations

| Operation | Request | Successful result | Rejection |
|---|---|---|---|
| Create | POST `/items`, JSON name | 201, item, Location | 400 invalid input; 415 media type |
| List | GET `/items` | 200, items in id order | — |
| Read | GET `/items/{id}` | 200, item | 400 invalid id; 404 missing |
| Replace | PUT `/items/{id}`, JSON name | 200, replacement | 400 invalid input; 404 missing; 415 media type |
| Delete | DELETE `/items/{id}` | 204, empty body | 400 invalid id; 404 missing |

Save this as `client.py`. Install HTTPX, start a fresh server on loopback, and
run `python client.py`. Repeat with each language, restarting between runs.

```python
import httpx

with httpx.Client(base_url="http://127.0.0.1:8080", timeout=2) as client:
    created = client.post("/items", json={"name": "tea"})
    assert created.status_code == 201
    path = created.headers["Location"]
    assert created.json()["name"] == "tea"
    assert client.get(path).json() == created.json()
    assert client.get("/items").json() == [created.json()]
    invalid = client.put(path, json={"name": ""})
    assert invalid.status_code == 400
    assert invalid.json()["error"]["code"] == "invalid_input"
    assert client.get(path).json()["name"] == "tea"
    updated = client.put(path, json={"name": "coffee"})
    assert updated.status_code == 200 and updated.json()["name"] == "coffee"
    deleted = client.delete(path)
    assert deleted.status_code == 204 and deleted.content == b""
    missing = client.get(path)
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "not_found"
    assert client.get("/items").json() == []
    print("CRUD contract passed")
```

Add cases for missing, null, numeric, all-space, non-ASCII and oversized names;
unknown fields; malformed JSON; two concatenated JSON documents; zero or
nonnumeric ids; and `text/plain` write bodies. For each rejected write, prove
the existing item remains unchanged. Error field order is irrelevant; status,
code, shape, and absence of mutation matter. Framework-level errors for unknown
routes or wrong methods should also use JSON; do not assume a default HTML/text
page satisfies the contract. Bodies rejected before your framework reaches a
handler (for example by a reverse proxy) need that deployment layer's policy.

The examples omit authentication to isolate CRUD. Combine Day 049's real
authentication boundary with these operations only after the lifecycle passes.
Do not expose the in-memory demonstration as a production service.
'''

lang(50,'python',"""Pydantic models validate API inputs; FastAPI serialises model responses
and routes exceptions through handlers. A deliberate error adapter keeps the
public contract stable instead of exposing the framework's default validation
envelope. The store below uses one lock around each state operation.""",
[( 'class ItemIn(BaseModel):\n    model_config = ConfigDict(extra="forbid")\n    name: str = Field(strict=True, min_length=1, max_length=80)', "This rejects absent names, nulls, numbers, and extra fields. A field validator adds the printable-ASCII rule."),
 ('@app.exception_handler(RequestValidationError)\nasync def invalid(request: Request, exc: RequestValidationError) -> JSONResponse:\n    return error(400, "invalid_input", "invalid request")', "This API intentionally maps FastAPI's validation rejection to 400 with the same envelope as other input errors.")],
'''from threading import Lock
from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()
items: dict[int, str] = {}
mutex = Lock()
next_id = 1
PositiveId = Annotated[int, Path(gt=0)]

class ItemIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(strict=True, min_length=1, max_length=80)

    @field_validator("name")
    @classmethod
    def valid_name(cls, value: str) -> str:
        if not value.strip(" ") or any(not 32 <= ord(char) <= 126 for char in value):
            raise ValueError("printable ASCII name required")
        return value

class ItemOut(BaseModel):
    id: int
    name: str

def error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})

@app.exception_handler(RequestValidationError)
async def invalid(request: Request, exc: RequestValidationError) -> JSONResponse:
    return error(400, "invalid_input", "invalid request")

@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = {404: "not_found", 405: "method_not_allowed", 415: "unsupported_media_type"}.get(exc.status_code, "request_failed")
    response = error(exc.status_code, code, str(exc.detail))
    if exc.headers:
        response.headers.update(exc.headers)
    return response

@app.middleware("http")
async def require_json(request: Request, call_next):
    if request.method in {"POST", "PUT"}:
        media = request.headers.get("content-type", "").split(";", 1)[0].strip().lower()
        if media != "application/json":
            return error(415, "unsupported_media_type", "application/json required")
    return await call_next(request)

@app.post("/items", status_code=201, response_model=ItemOut)
def create(item: ItemIn, response: Response) -> ItemOut:
    global next_id
    with mutex:
        item_id = next_id
        next_id += 1
        items[item_id] = item.name
    response.headers["Location"] = f"/items/{item_id}"
    return ItemOut(id=item_id, name=item.name)

@app.get("/items", response_model=list[ItemOut])
def list_items() -> list[ItemOut]:
    with mutex:
        return [ItemOut(id=i, name=name) for i, name in sorted(items.items())]

@app.get("/items/{item_id}", response_model=ItemOut)
def read(item_id: PositiveId) -> ItemOut:
    with mutex:
        if item_id not in items:
            raise HTTPException(404, "item not found")
        return ItemOut(id=item_id, name=items[item_id])

@app.put("/items/{item_id}", response_model=ItemOut)
def replace(item_id: PositiveId, item: ItemIn) -> ItemOut:
    with mutex:
        if item_id not in items:
            raise HTTPException(404, "item not found")
        items[item_id] = item.name
    return ItemOut(id=item_id, name=item.name)

@app.delete("/items/{item_id}", status_code=204)
def delete(item_id: PositiveId) -> Response:
    with mutex:
        if item_id not in items:
            raise HTTPException(404, "item not found")
        del items[item_id]
    return Response(status_code=204)
''', 'Install with `python -m pip install fastapi uvicorn`. Save as `main.py`; run `python -m uvicorn main:app --host 127.0.0.1 --port 8080`. Run the [lifecycle client](03-practice.md), which prints the line below. Use one server process for this in-memory exercise.',
'CRUD contract passed',
"""**Near-miss:** returning a dictionary containing `status: 400` still
creates HTTP 200 unless you set the actual response status. The error helper
does both deliberately.

**Real error:** PUT with `{"name":""}` receives 400 and
`{"error":{"code":"invalid_input","message":"invalid request"}}`.
The stored name remains unchanged. DELETE returns no JSON at all; trying to
decode its empty body is a client mistake.

Validation exceptions and HTTP exceptions are translated separately. Unexpected
exceptions still need a production-safe 500 handler and internal logging; do
not enable debug traceback responses publicly. Add request-size limits at the
server/proxy boundary before accepting arbitrary bodies. Running `--workers 2`
would create two independent dictionaries, not a larger shared store.""",
'[FastAPI error handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/) and [Pydantic validators](https://docs.pydantic.dev/latest/concepts/validators/)')

lang(50,'go',"""Go's JSON decoder can reject unknown fields, but you write the domain
validation and error adapter. A pointer input field distinguishes a missing or
null name from a valid string. Each state operation takes a mutex; response
encoding happens after releasing it.""",
[( 'type input struct { Name *string `json:"name"` }\ndecoder := json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096))\ndecoder.DisallowUnknownFields()', "The pointer is nil for missing/null input. A second Decode must reach EOF so trailing JSON cannot be ignored."),
 ('w.Header().Set("Location", fmt.Sprintf("/items/%d", item.ID))\nreply(w, http.StatusCreated, item)', "Location identifies the newly created resource. The JSON representation uses the same server-assigned id.")],
'''package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"mime"
	"net/http"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

type Item struct { ID int `json:"id"`; Name string `json:"name"` }

func reply(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(value); err != nil { fmt.Println("write failed:", err) }
}
func fail(w http.ResponseWriter, status int, code, message string) {
	reply(w, status, map[string]any{"error": map[string]string{"code": code, "message": message}})
}
func decode(w http.ResponseWriter, r *http.Request) (string, bool) {
	defer r.Body.Close()
	media, err := mime.ParseMediaType(r.Header.Get("Content-Type"))
	if err != nil || media != "application/json" { fail(w, 415, "unsupported_media_type", "application/json required"); return "", false }
	var input struct { Name *string `json:"name"` }
	decoder := json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096))
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&input); err != nil { fail(w, 400, "invalid_input", "invalid request"); return "", false }
	if err := decoder.Decode(new(any)); !errors.Is(err, io.EOF) { fail(w, 400, "invalid_input", "one object required"); return "", false }
	if input.Name == nil { fail(w, 400, "invalid_input", "name required"); return "", false }
	name := *input.Name
	valid := len(name) >= 1 && len(name) <= 80 && strings.Trim(name, " ") != ""
	for _, char := range name { if char < 32 || char > 126 { valid = false } }
	if !valid { fail(w, 400, "invalid_input", "printable ASCII name required"); return "", false }
	return name, true
}

func main() {
	items := make(map[int]Item)
	nextID := 1
	var mutex sync.Mutex
	mux := http.NewServeMux()
	mux.HandleFunc("/items", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			mutex.Lock()
			list := make([]Item, 0, len(items))
			for _, item := range items { list = append(list, item) }
			mutex.Unlock()
			sort.Slice(list, func(i, j int) bool { return list[i].ID < list[j].ID })
			reply(w, 200, list)
		case http.MethodPost:
			name, ok := decode(w, r)
			if !ok { return }
			mutex.Lock()
			item := Item{ID: nextID, Name: name}
			nextID++
			items[item.ID] = item
			mutex.Unlock()
			w.Header().Set("Location", fmt.Sprintf("/items/%d", item.ID))
			reply(w, 201, item)
		default:
			w.Header().Set("Allow", "GET, POST")
			fail(w, 405, "method_not_allowed", "method not allowed")
		}
	})
	mux.HandleFunc("/items/{id}", func(w http.ResponseWriter, r *http.Request) {
		id, err := strconv.Atoi(r.PathValue("id"))
		if err != nil || id <= 0 { fail(w, 400, "invalid_input", "positive id required"); return }
		if r.Method != http.MethodGet && r.Method != http.MethodPut && r.Method != http.MethodDelete {
			w.Header().Set("Allow", "GET, PUT, DELETE")
			fail(w, 405, "method_not_allowed", "method not allowed")
			return
		}
		var name string
		if r.Method == http.MethodPut {
			var ok bool
			name, ok = decode(w, r)
			if !ok { return }
		}
		mutex.Lock()
		item, found := items[id]
		if found && r.Method == http.MethodPut { item.Name = name; items[id] = item }
		if found && r.Method == http.MethodDelete { delete(items, id) }
		mutex.Unlock()
		if !found { fail(w, 404, "not_found", "item not found"); return }
		if r.Method == http.MethodDelete { w.WriteHeader(204); return }
		reply(w, 200, item)
	})
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) { fail(w, 404, "not_found", "route not found") })
	server := &http.Server{Addr: "127.0.0.1:8080", Handler: mux, ReadHeaderTimeout: 2*time.Second, ReadTimeout: 5*time.Second, WriteTimeout: 5*time.Second}
	if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) { fmt.Println(err) }
}
''','Save as `main.go`; run `gofmt -w main.go`, then `go run main.go`. Run the [shared lifecycle client](03-practice.md); its output follows. This program requires Go 1.23+ and no third-party packages.',
'CRUD contract passed',
"""**Near-miss:** checking `items[id]` before locking, then updating under
the lock, leaves a race between the check and the mutation. The example makes
lookup and replacement/deletion one critical section.

**Real error:** a missing name returns HTTP 400 and the JSON envelope with
code `invalid_input` and message `name required`. A missing id returns 404
with code `not_found`. Rejected input is decoded before mutation.

JSON object decoding into a struct uses case-insensitive field matching, so
`Name` may be accepted as `name`; strict public schemas need an exact-key check
before typed decoding. This lesson adds that check below before publication.
Duplicate keys normally keep the last value; decide a stricter policy if your
boundary requires one. The memory map is not durable, and the mutex does not
coordinate a second server process.""",
'[Go encoding/json](https://pkg.go.dev/encoding/json) and [Go net/http](https://pkg.go.dev/net/http)')

lang(50,'cpp',"""C++ API handlers need explicit JSON shape checks and consistent response
helpers. A mutex protects the resource store because cpp-httplib dispatches
concurrent requests. Copy the response data while locked, then serialise and
send it after releasing the lock.""",
[( 'void fail(httplib::Response& response, int status, const std::string& code) {\n    response.status = status;\n    response.set_content(json{{"error", {{"code", code}, {"message", code}}}}.dump(), "application/json");\n}', "One helper controls the error envelope. The complete version takes a separate human-readable message."),
 ('{\n    std::lock_guard lock(mutex);\n    auto found = items.find(id);\n    if (found != items.end()) copy = found->second;\n}', "A locked lookup avoids races. Copying the item prevents the response from referring to an entry another request can erase.")],
'''#include <httplib.h>
#include <nlohmann/json.hpp>
#include <charconv>
#include <iostream>
#include <map>
#include <mutex>
#include <string>

using json = nlohmann::json;

void reply(httplib::Response& response, int status, const json& body) {
    response.status = status;
    response.set_content(body.dump(), "application/json");
}
void fail(httplib::Response& response, int status, const std::string& code, const std::string& message) {
    reply(response, status, json{{"error", {{"code", code}, {"message", message}}}});
}
bool decode(const httplib::Request& request, httplib::Response& response, std::string& name) {
    auto media = request.get_header_value("Content-Type");
    media = media.substr(0, media.find(';'));
    while (!media.empty() && media.back() == ' ') media.pop_back();
    for (char& c : media) if (c >= 'A' && c <= 'Z') c = static_cast<char>(c - 'A' + 'a');
    if (media != "application/json") { fail(response, 415, "unsupported_media_type", "application/json required"); return false; }
    const auto body = json::parse(request.body, nullptr, false);
    if (!body.is_object() || body.size() != 1 || !body.contains("name") || !body["name"].is_string()) {
        fail(response, 400, "invalid_input", "one string name required"); return false;
    }
    name = body["name"].get<std::string>();
    bool valid = !name.empty() && name.size() <= 80 && name.find_first_not_of(' ') != std::string::npos;
    for (unsigned char c : name) if (c < 32 || c > 126) valid = false;
    if (!valid) { fail(response, 400, "invalid_input", "printable ASCII name required"); return false; }
    return true;
}

int main() {
    httplib::Server server;
    server.set_payload_max_length(4096);
    server.set_read_timeout(5, 0);
    server.set_write_timeout(5, 0);
    std::map<int, std::string> items;
    int next_id = 1;
    std::mutex mutex;
    server.Post("/items", [&](const httplib::Request& request, httplib::Response& response) {
        std::string name;
        if (!decode(request, response, name)) return;
        int id;
        { std::lock_guard lock(mutex); id = next_id++; items[id] = name; }
        response.set_header("Location", "/items/" + std::to_string(id));
        reply(response, 201, json{{"id", id}, {"name", name}});
    });
    server.Get("/items", [&](const httplib::Request&, httplib::Response& response) {
        json list = json::array();
        { std::lock_guard lock(mutex); for (const auto& [id, name] : items) list.push_back(json{{"id", id}, {"name", name}}); }
        reply(response, 200, list);
    });
    const auto one = [&](const httplib::Request& request, httplib::Response& response) {
        const auto text = request.matches[1].str();
        int id = 0;
        const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), id);
        if (error != std::errc{} || end != text.data() + text.size() || id <= 0) {
            fail(response, 400, "invalid_input", "positive id required"); return;
        }
        std::string name;
        if (request.method == "PUT" && !decode(request, response, name)) return;
        bool found = false;
        {
            std::lock_guard lock(mutex);
            auto it = items.find(id);
            if (it != items.end()) {
                found = true;
                if (request.method == "PUT") it->second = name;
                name = it->second;
                if (request.method == "DELETE") items.erase(it);
            }
        }
        if (!found) { fail(response, 404, "not_found", "item not found"); return; }
        if (request.method == "DELETE") { response.status = 204; return; }
        reply(response, 200, json{{"id", id}, {"name", name}});
    };
    server.Get(R"(/items/([^/]+))", one);
    server.Put(R"(/items/([^/]+))", one);
    server.Delete(R"(/items/([^/]+))", one);
    server.set_error_handler([](const httplib::Request&, httplib::Response& response) {
        if (response.body.empty()) {
            const std::string code = response.status == 404 ? "not_found" : "request_failed";
            fail(response, response.status, code, "request could not be handled");
        }
    });
    if (!server.listen("127.0.0.1", 8080)) { std::cerr << "listen failed\\n"; return 1; }
}
''', CPP_HTTP_BUILD+'\nThe shared lifecycle client prints the line below; the server does not print each successful request.',
'CRUD contract passed',
"""**Near-miss:** returning an iterator or reference into the map after
unlocking allows another request to erase it. The handler copies the name
while locked and builds its response from that copy.

**Real error:** posting `{"name":17}` gets HTTP 400 with code
`invalid_input` and message `one string name required`. An empty name gets
`printable ASCII name required`. Neither creates an item.

`operator[]` on a map can insert a missing entry. Use `find` for existence
checks so a failed read cannot create a resource. An unexpected exception
also needs a safe 500 adapter in a deployed service. The payload limit may be
enforced before route code, so test the library's error hook as well as your
helpers. No lock makes this process-local store persistent or shared across
multiple server instances.""",
'[cpp-httplib error handling](https://github.com/yhirose/cpp-httplib) and [nlohmann/json parsing](https://json.nlohmann.me/api/basic_json/parse/)')

def render():
    for d in load():
        if d.n not in DATA:
            continue
        info = DATA[d.n]
        folder = ROOT / 'days' / d.folder
        for lesson in d.langs.lessons:
            key = lesson.track.removeprefix('lang-')
            spec = info['langs'][key]
            path = folder / lang_lesson_name(lesson)
            old = path.read_text(encoding='utf-8')
            header = old.split('> Not written yet.')[0].replace('status: empty', 'status: written').rstrip()
            if '## 1.' in header:
                header = header.split('## 1.')[0].rstrip()
            blocks = []
            for fragment, explanation in spec['steps']:
                blocks.append(f'```{key}\n{fragment}\n```\n\n{explanation}')
            code_section = '\n\n'.join(blocks) + '\n\n' + spec['run']
            code_section += '\n\nExpected application output (framework access logs are omitted):\n\n' + '\n'.join('    ' + x for x in spec['output'].splitlines())
            code_section += f'\n\nComplete program:\n\n```{key}\n{spec["code"].strip()}\n```'
            comparisons = []
            for other, other_spec in info['langs'].items():
                if other != key:
                    fragment, explanation = other_spec['steps'][0]
                    comparisons.append(f'**{other.title()}**\n\n```{other}\n{fragment}\n```\n\n{explanation}')
            comparisons.append('**The difference that matters:** ' + info.get('difference', info['recall'][0]))
            interview = '**How it gets asked**\n\n' + '\n'.join('- ' + q for q in [d.langs.ask, *info['questions']])
            interview += '\n\n**What to say out loud**\n\n' + info['interview']
            interview += '\n\n**The follow-ups**\n\n' + '\n\n'.join(f'- **{q}** {a}' for q,a in info['followups'])
            interview += '\n\n**A model answer**\n\n' + info['model']
            bodies = [spec['intro'], info['story'], info['idea'], '```text\n'+info['picture']+'\n```\n\n'+info.get('caption', 'Notice where the decision happens and what information it needs.'), code_section,
                      '\n\n'.join(comparisons), spec['traps'], interview, '\n'.join('- '+x for x in info['recall'])]
            bodies[6] += '\n\nReference: ' + spec['source'] + '.'
            path.write_text(header+'\n\n'+'\n\n'.join(f'## {i}. {heading}\n\n{body}' for i,((heading,_),body) in enumerate(zip(LANG_SECTIONS,bodies),1))+'\n',encoding='utf-8')
        p = folder/'03-practice.md'
        text = p.read_text(encoding='utf-8').replace('status: draft','status: written')
        build = '## Build these, in all three languages\n\nComplete each exercise in Python, Go, and C++. Keep the same inputs and compare the results.\n\n| # | Exercise | What it is really testing |\n|---|---|---|\n'
        build += '\n'.join(f'| {i} | {a} | {b} |' for i,(a,b) in enumerate(info['exercises'],1))
        build += '\n\n' + info.get('deliverable','For each exercise, include a successful case, an absent or empty case, and a rejected input. State the expected result before running it. Preserve valid results when a different record fails.')
        build += '\n\n## Compare\n\nWrite one sentence per language explaining its mechanism and one concrete trade-off you observed.\n\n'
        build += '\n'.join(f'- **{name.title()}** — {spec["intro"].split(". ")[0].replace(chr(10), " ")}.' for name,spec in info['langs'].items())
        text = re.sub(r'## Build these, in all three languages.*?(?=## Say these out loud)', lambda _:build+'\n\n',text,flags=re.S)
        questions = [d.langs.ask,*info['questions']]
        oral = '### Languages\n\nAnswer each in two minutes without notes. Give a concrete input or failure case.\n\n'+'\n'.join(f'{i}. {q}' for i,q in enumerate(questions,1))+'\n\n'
        text = re.sub(r'### Languages.*?(?=## Before you move on)',lambda _:oral,text,flags=re.S)
        text += '\n- [ ] I completed all three language exercises in all three languages, including their failure cases.\n'
        p.write_text(text,encoding='utf-8')

if __name__ == '__main__':
    render()
