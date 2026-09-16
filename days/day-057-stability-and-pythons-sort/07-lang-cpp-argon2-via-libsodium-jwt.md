---
day: 57
track: lang-cpp
title: "Argon2 via libsodium, jwt-cpp, and a login flow"
theme: "Authentication: hashing and tokens"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 057 · C++ — Argon2 via libsodium, jwt-cpp, and a login flow

**Today's theme:** Authentication: hashing and tokens

**After today you can:** You can store a password correctly and issue a signed token in each language.

**The interviewer asks it as:** *How do you store a password?*

---

## 1. What this is, and why it matters

Authentication has two halves, and in C++ you reach for two well-audited libraries. libsodium's
`crypto_pwhash_str` stores a password as a slow, salted **argon2** hash, the current
first-recommended algorithm, so a stolen database reveals no passwords. `jwt-cpp`, a header-only
library, signs and verifies a **JWT**, the token a caller presents on every later request. You do
not write the cryptography; you call libraries that do, because hand-rolled crypto is the classic
way to ship a hole.

At work this is the code you are least allowed to get wrong, and in C++ "least allowed to get
wrong" and "easy to get wrong" meet, which is exactly why you use libsodium and jwt-cpp rather
than OpenSSL primitives directly. In interviews, "how do you store a password" is in nearly every
backend round; the C++ answer is the same as everywhere, with the added point that you lean on
audited libraries rather than assembling it from parts.

## 2. The story

Farah runs a members' club. To become a member you come in once and sign the register in your own
hand. But the club does not keep your signature. That would be dangerous: a thief who broke in and
photographed the register could forge any member's signature forever. Instead, the moment you
sign, a clerk studies the signature closely, notes down a long list of its particular quirks, and
files that description. Your actual signature is destroyed. Nobody at the club can reproduce your
signature from the description; they can only check a new signature against it.

When you come back, you sign again. The clerk compares your new signature to the filed
description. Two things make this safe. The clerk deliberately takes a slow, careful minute over
each comparison, so a thief who somehow got the descriptions and wanted to try a million forged
signatures would need a million slow minutes. And every member's description is salted with a
random word the clerk picked when they joined, so two members who sign alike still have different
descriptions on file.

Signing in full every time you want a drink would be tedious, so once you are in for the evening,
Farah gives you a wristband, stamped with the club's embossing seal, which only Farah has. At the
bar, the barman feels the seal is genuine and pours. The band expires at midnight, and altering
the name breaks the seal.

Farah does not make the seals or the special ink herself. Years ago the club tried, mixing its
own ink and cutting its own stamp, and a forger reproduced it in a week because the recipe was
amateur. Now the seal and the ink come from a specialist supplier who does nothing else and has
been doing it for decades. Farah's staff apply the seal; they do not invent it. The one rule that
survived from the amateur days is the barman's: always check for the one real seal, never the kind
of seal a band claims for itself.

## 3. The idea in plain English

Destroying the signature and keeping a description is **hashing**: a one-way function from
password to hash. libsodium's `crypto_pwhash_str(out, password, len, opslimit, memlimit)` computes
an argon2 hash, salt and parameters baked into the output string;
`crypto_pwhash_str_verify(stored, password, len)` checks a login, returning 0 for a match. You
store the hash, never the password.

The clerk's slowness is the **work parameters**, `opslimit` and `memlimit`: how much computation
and how much memory each hash costs. argon2 is memory-hard, meaning it deliberately uses a lot of
memory, which defeats the custom hardware attackers use against simpler hashes. libsodium ships
sensible constants, `crypto_pwhash_OPSLIMIT_INTERACTIVE` and `MEMLIMIT_INTERACTIVE`, for a login.
The salt is random per hash and stored inside the output, so identical passwords hash
differently.

The wristband is a **JWT**: JSON claims, `sub` and `exp`, signed with a **secret** only the
server holds, HS256. `jwt::create().set_subject(...).set_expires_at(...).sign(jwt::algorithm::hs256{secret})`
makes it; a verifier checks it.

The specialist supplier, not the amateur mix, is the point about using **audited libraries**:
libsodium and jwt-cpp are written and reviewed by people who do only this. You do not implement
argon2 or HMAC yourself, exactly as Farah does not mix her own ink.

The barman's surviving rule is the **algorithm allow-list**. A jwt-cpp verifier is built with
`allow_algorithm(jwt::algorithm::hs256{secret})`, which says "only accept HS256, with this
secret". A token that names a different algorithm, or `none`, is refused, because the verifier was
told the one seal to accept. Omitting this, or building a verifier that trusts the token's own
algorithm, is the `alg: none` hole, the same one as in the other two languages.

A JWT is **stateless**: the barman needs no register. Tampering breaks the seal, `exp` bounds its
life, and the secret staying on the server keeps the seal un-forgeable,
[day 51](../day-051-why-sorting-matters/README.md)'s rule.

## 4. The picture

```text
  register (once)                         login (each time)

  password "hunter2"                      password "hunter2"
      |  crypto_pwhash_str (slow, salted, memory-hard)   |  crypto_pwhash_str_verify(stored, ...)
      v                                                    v
  $argon2id$v=19$m=65536,t=2,p=1$...  <- stored        returns 0? yes -> issue a token

  token: {"sub":"meera","exp":...} + HMAC-SHA256(payload, SECRET) = eyJhbGci...
  verify: jwt::verify().allow_algorithm(hs256{SECRET}).verify(decode(token))  -> throws on failure
```

Notice the stored hash names the algorithm, `argon2id`, and its parameters, `m`, `t`, `p`,
memory, time, parallelism, so `verify` knows exactly how to re-hash the attempt.

## 5. The code, built step by step

The libraries: `libsodium-dev` on Debian and Ubuntu, `libsodium` on Homebrew and vcpkg; jwt-cpp
is header-only, `libjwt-cpp-dev` or a single header, and it needs an OpenSSL or a picojson
backend, which its docs cover.

Registering. libsodium must be initialised once.

```cpp
#include <sodium.h>

std::string hash_password(const std::string& password) {
    char hashed[crypto_pwhash_STRBYTES];
    if (crypto_pwhash_str(hashed, password.c_str(), password.size(),
                          crypto_pwhash_OPSLIMIT_INTERACTIVE,
                          crypto_pwhash_MEMLIMIT_INTERACTIVE) != 0) {
        throw std::runtime_error("out of memory hashing password");
    }
    return std::string(hashed);
}
```

`crypto_pwhash_str` writes a null-terminated string into `hashed`, containing the algorithm,
parameters, salt, and hash. It returns non-zero only if it could not get the memory it needs,
which is why it can throw. `crypto_pwhash_STRBYTES` is the buffer size the library defines. Store
the returned string.

Checking a password.

```cpp
bool check_password(const std::string& stored, const std::string& password) {
    return crypto_pwhash_str_verify(stored.c_str(), password.c_str(), password.size()) == 0;
}
```

`crypto_pwhash_str_verify` reads the parameters and salt from `stored`, re-hashes the attempt the
same way, and compares in constant time, returning 0 for a match. You never parse the hash
yourself.

Issuing a token.

```cpp
#include <jwt-cpp/jwt.h>

std::string issue_token(const std::string& username, const std::string& secret) {
    const auto now = std::chrono::system_clock::now();
    return jwt::create()
        .set_type("JWT")
        .set_subject(username)
        .set_issued_at(now)
        .set_expires_at(now + std::chrono::minutes(15))
        .sign(jwt::algorithm::hs256{secret});
}
```

The builder sets the claims and `sign` seals it with HS256 and the secret. `set_expires_at` is
`exp`; a token without it never expires.

Verifying, with the allow-list.

```cpp
std::optional<std::string> verify_token(const std::string& token, const std::string& secret) {
    try {
        const auto decoded = jwt::decode(token);
        jwt::verify()
            .allow_algorithm(jwt::algorithm::hs256{secret})
            .with_type("JWT")
            .verify(decoded);
        return decoded.get_subject();
    } catch (const std::exception& e) {
        std::cerr << "token rejected: " << e.what() << '\n';
        return std::nullopt;
    }
}
```

`jwt::decode` parses the token; `jwt::verify()...allow_algorithm(...)` builds a verifier that
accepts only HS256 with this secret, and `verify` throws if the signature, the algorithm, or the
expiry is wrong. The `allow_algorithm` line is the barman's rule; without it the verifier would
trust the token's own algorithm. The return is a `std::optional` from
[day 23](../day-023-palindromes/README.md), empty on any failure.

Build and run:

```bash
g++ -Wall -Wextra -std=c++20 main.cpp -lsodium -lssl -lcrypto -o app
JWT_SECRET=a-long-random-secret-of-at-least-32-bytes ./app
```

```text
hash stored: $argon2id$v=19$m=65536,t=2,p=1$...
right password: 1
wrong password: 0
verified as: meera
tampered -> token rejected: signature verification failed
expired -> token rejected: token expired
wrong secret -> token rejected: signature verification failed
alg none -> token rejected: algorithm 'none' is not allowed
```

The stored hash names `argon2id` and its parameters. The password check passes and fails, the
good token verifies, and a tampered, expired, wrong-secret, and forged `none` token all fail, the
last one caught by the allow-list.

Here is the whole program in one piece, `main.cpp`:

```cpp
#include <sodium.h>
#include <jwt-cpp/jwt.h>

#include <chrono>
#include <cstdlib>
#include <iostream>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>

std::string hash_password(const std::string& password) {
    char hashed[crypto_pwhash_STRBYTES];
    if (crypto_pwhash_str(hashed, password.c_str(), password.size(),
                          crypto_pwhash_OPSLIMIT_INTERACTIVE,
                          crypto_pwhash_MEMLIMIT_INTERACTIVE) != 0) {
        throw std::runtime_error("out of memory hashing password");
    }
    return std::string(hashed);
}

bool check_password(const std::string& stored, const std::string& password) {
    return crypto_pwhash_str_verify(stored.c_str(), password.c_str(), password.size()) == 0;
}

std::string issue_token(const std::string& username, const std::string& secret) {
    const auto now = std::chrono::system_clock::now();
    return jwt::create()
        .set_type("JWT")
        .set_subject(username)
        .set_issued_at(now)
        .set_expires_at(now + std::chrono::minutes(15))
        .sign(jwt::algorithm::hs256{secret});
}

std::optional<std::string> verify_token(const std::string& token, const std::string& secret) {
    try {
        const auto decoded = jwt::decode(token);
        jwt::verify()
            .allow_algorithm(jwt::algorithm::hs256{secret})
            .with_type("JWT")
            .verify(decoded);
        return decoded.get_subject();
    } catch (const std::exception& e) {
        std::cerr << "token rejected: " << e.what() << '\n';
        return std::nullopt;
    }
}

int main() {
    if (sodium_init() < 0) {
        std::cerr << "libsodium failed to initialise\n";
        return 1;
    }
    const char* env = std::getenv("JWT_SECRET");
    if (env == nullptr) {
        std::cerr << "JWT_SECRET is not set\n";
        return 1;
    }
    const std::string secret = env;

    std::map<std::string, std::string> users;
    users["meera"] = hash_password("hunter2");
    std::cout << "hash stored: " << users["meera"].substr(0, 32) << "...\n";
    std::cout << "right password: " << check_password(users["meera"], "hunter2") << '\n';
    std::cout << "wrong password: " << check_password(users["meera"], "wrong") << '\n';

    const std::string token = issue_token("meera", secret);
    if (auto sub = verify_token(token, secret)) std::cout << "verified as: " << *sub << '\n';

    const std::string tampered = token.substr(0, token.size() - 3) + "abc";
    std::cout << "tampered -> " << (verify_token(tampered, secret) ? "accepted" : "rejected") << '\n';

    const std::string expired = jwt::create().set_type("JWT").set_subject("meera")
        .set_expires_at(std::chrono::system_clock::now() - std::chrono::seconds(1))
        .sign(jwt::algorithm::hs256{secret});
    std::cout << "expired -> " << (verify_token(expired, secret) ? "accepted" : "rejected") << '\n';

    const std::string other = jwt::create().set_type("JWT").set_subject("meera")
        .sign(jwt::algorithm::hs256{"a-different-secret-of-at-least-32-bytes!"});
    std::cout << "wrong secret -> " << (verify_token(other, secret) ? "accepted" : "rejected") << '\n';

    const std::string none = jwt::create().set_type("JWT").set_subject("admin")
        .sign(jwt::algorithm::none{});
    std::cout << "alg none -> " << (verify_token(none, secret) ? "accepted" : "rejected") << '\n';
    return 0;
}
```

## 6. How the other two languages do it

**Python**

```python
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
bcrypt.checkpw(password.encode(), hashed)
jwt.decode(token, SECRET, algorithms=["HS256"])   # algorithms= is the allow-list
```

bcrypt for the hash (argon2 is a one-line swap with `argon2-cffi`), and PyJWT's `algorithms=`
argument is the allow-list, jwt-cpp's `allow_algorithm` by another name.

**Go**

```go
hash, _ := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
token, _ := jwt.Parse(str, func(t *jwt.Token) (any, error) {
    if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok { return nil, errUnexpected }
    return secret, nil
})
```

bcrypt again, and golang-jwt's key function asserting the method is the allow-list expressed as
code you write.

**The difference that matters:** C++ leans hardest on audited libraries, because the language
gives you the sharpest tools to build the primitives wrong. libsodium's argon2 and jwt-cpp's
verifier are the specialist's ink; the equivalent of writing your own is calling OpenSSL's
low-level HMAC and EVP functions by hand, which is where C++ crypto holes come from. The
allow-list defence is identical, `allow_algorithm` here, `algorithms=` in Python, the key
function in Go, and forgetting it is the same `alg: none` hole in all three.

## 7. The traps

**The near-miss: a fast hash.**

```cpp
// SHA-256 of the password, from OpenSSL or a hand-rolled loop
```

Fast and, done by hand, usually unsalted. A stolen database is cracked at billions of guesses a
second. Use `crypto_pwhash_str`; it is argon2, slow, salted, and memory-hard, and you did not
write it.

**A verifier without the allow-list.**

```cpp
jwt::verify().verify(jwt::decode(token));   // no allow_algorithm
```

```text
token rejected: no algorithms specified
```

jwt-cpp refuses to verify with no algorithm allowed, which is the library protecting you; the
danger is a verifier that allows the wrong thing, or code that reads the algorithm from the token
and allows that. Always name the one algorithm you accept.

**Not calling `sodium_init()`.** libsodium requires initialisation before any call; skipping it is
undefined behaviour, sometimes working, sometimes a crash, sometimes weak randomness. `if
(sodium_init() < 0) return;` at the top of `main`, always.

**A buffer too small for the hash.** Using anything smaller than `crypto_pwhash_STRBYTES` for the
output overflows:

```text
*** buffer overflow detected ***: terminated
```

Always size the buffer with the library's constant, never a guess.

**Secrets in the token.** A JWT is signed, not encrypted; the payload is base64, readable by
anyone who has the token. Decode `eyJ...` and the claims are plain. No password, card number, or
private data in it.

**No expiry.** Omit `set_expires_at` and the token never dies, so a stolen one is a permanent
key. Always set it, short.

**Logging the token or password.** Both are on [day 52](../day-052-quadratic-sorts/README.md)'s
never-log list; a token in a log is a live credential.

## 8. Say it out loud

**How it gets asked**

- How do you store a password?
- Why use libsodium and jwt-cpp instead of OpenSSL directly?
- What is the allow-list on a JWT verifier for?
- What is the `alg: none` attack?

**The ninety-second script**

Never store the password; store a slow, salted hash with libsodium's `crypto_pwhash_str`, which is
argon2, and check on login with `crypto_pwhash_str_verify`, which reads the salt and parameters
from the stored hash and compares in constant time. argon2 is slow and memory-hard, which defeats
both brute force and the custom hardware attackers use, and the salt inside the hash means
identical passwords hash differently. Never encrypt a password, because that is reversible. For
sessions I issue a JWT with jwt-cpp: subject and a short expiry, signed HS256 with a secret only
the server holds. Verifying is built with `allow_algorithm(hs256{secret})`, which is the
allow-list: it accepts only that one algorithm, so a token naming a different algorithm or `none`
is refused. In C++ especially I use audited libraries, libsodium and jwt-cpp, rather than
assembling this from OpenSSL primitives, because hand-rolled crypto is how holes ship. The secret
is long and from the environment, expiry is always set, and nothing secret goes in the token
because it is signed, not encrypted.

**The follow-ups**

- **Why argon2 over bcrypt?** *argon2 is memory-hard, so it resists GPU and custom-hardware
  cracking better than bcrypt, and it won the Password Hashing Competition. bcrypt is fine and
  ubiquitous; argon2 is the current first recommendation. Either beats a fast hash, which is the
  only answer that fails the interview.*
- **Where does verification live in a service?** *The auth hook from
  [day 49](../day-049-peak-finding/README.md): read the `Authorization: Bearer <token>` header,
  `verify_token`, and set the subject, or answer 401.*
- **How do you revoke a JWT?** *Not directly; that is the cost of stateless. Short expiries so a
  stolen token dies soon, plus a server-side deny-list for immediate revocation, which trades back
  some statelessness.*

**A model answer**

"Store a slow, salted, memory-hard hash with libsodium's `crypto_pwhash_str`, argon2; verify with
`crypto_pwhash_str_verify`, constant-time, salt read from the hash. Slow and memory-hard beat
brute force and custom hardware; salt beats rainbow tables; never encryption. Sessions are a JWT
via jwt-cpp: subject, short expiry, HS256 signed with an environment secret. The verifier is built
with `allow_algorithm(hs256{secret})`, the allow-list, or the `alg: none` forgery works. And I use
audited libraries, not OpenSSL primitives, because hand-rolled crypto is where the holes are."

## 9. Recall card

- Never store the password: `crypto_pwhash_str` (argon2, slow, salted, memory-hard); check with `crypto_pwhash_str_verify(...) == 0`, constant-time. Never a fast hash, never encryption.
- Call `sodium_init()` once before any libsodium call; size the output buffer with `crypto_pwhash_STRBYTES`.
- JWT via jwt-cpp: `jwt::create().set_subject(...).set_expires_at(...).sign(jwt::algorithm::hs256{secret})`.
- Verify with `jwt::verify().allow_algorithm(jwt::algorithm::hs256{secret})` — the allow-list is mandatory, or `alg: none` gets in.
- Signed, not encrypted: no secrets in the payload; always set expiry; secret is long and from the environment; use audited libraries.
