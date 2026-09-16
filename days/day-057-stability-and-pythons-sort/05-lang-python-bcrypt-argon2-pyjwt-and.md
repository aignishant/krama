---
day: 57
track: lang-python
title: "bcrypt/argon2, PyJWT, and a login flow"
theme: "Authentication: hashing and tokens"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 057 · Python — bcrypt/argon2, PyJWT, and a login flow

**Today's theme:** Authentication: hashing and tokens

**After today you can:** You can store a password correctly and issue a signed token in each language.

**The interviewer asks it as:** *How do you store a password?*

---

## 1. What this is, and why it matters

Authentication is proving who a caller is. It has two halves. Storing a password so that even
someone who steals your whole database cannot learn it: you store a slow, salted **hash**, never
the password, and `bcrypt` or `argon2` is the library that makes the hash. And letting a caller
prove, on every later request, that they logged in, without sending the password again: you give
them a signed **token**, a JWT, and `PyJWT` is the library that signs and verifies it.

At work, this is the code you are least allowed to get wrong, because a mistake is a breach that
makes the news. In interviews, "how do you store a password" is asked in almost every backend
round, and it is a filter: the answer "hashed" is not enough, the answer "salted and slow-hashed
with bcrypt or argon2, never encrypted, never the plain password" is the one they are listening
for.

## 2. The story

Farah runs a members' club. To become a member you come in once and sign the register in your own
hand. But the club does not keep your signature. That would be dangerous: a thief who broke in and
photographed the register could forge any member's signature forever. Instead, the moment you
sign, a clerk studies the signature closely, notes down a long list of its particular quirks, the
curl on the F, the pressure on the downstroke, and files that description. Your actual signature
is destroyed. Nobody at the club can reproduce your signature from the description; they can only
check a new signature against it.

When you come back, you sign again. The clerk compares your new signature to the filed
description. If they match, you are in. Two things make this safe. The clerk deliberately takes a
slow, careful minute over each comparison, so a thief who somehow got the descriptions and wanted
to try a million forged signatures against them would need a million slow minutes. And every
member's description is salted with a random word the clerk picked when they joined, written
beside it, so that two members who happen to sign alike still have completely different
descriptions on file, and a thief cannot prepare forgeries in advance.

Signing in full every time you want a drink would be tedious, so once you are in for the evening,
Farah gives you a wristband. It says who you are and the time it was issued, and it is stamped
with the club's embossing seal, which only Farah has. At the bar, the barman does not check the
register again; he glances at the wristband, runs a thumb over the seal to feel it is genuine,
and pours. The wristband expires at midnight. If you try to alter the name on it, the seal no
longer matches the band and the barman refuses. And a wristband from the club down the road,
with a different seal, is refused at a glance.

## 3. The idea in plain English

Destroying the signature and keeping only a description is **hashing**. A hash is a one-way
function: from the password you can compute the hash, but from the hash you cannot get the
password back. You store the hash. When someone logs in, you hash what they typed and compare it
to the stored hash. `bcrypt.hashpw(password, salt)` computes it; `bcrypt.checkpw(password,
stored)` does the comparison.

The clerk's deliberate slowness is the **work factor**. A general-purpose hash like SHA-256 is
fast, which is bad here, because fast means a thief can try billions of guesses a second. bcrypt
is designed to be slow, and its cost is tunable: the `12` in a bcrypt hash means 2 to the power
12 rounds. Slow for one login is nothing; slow times a billion guesses is centuries.

The random word beside each description is the **salt**: random bytes mixed into each hash so
that two identical passwords produce different hashes. `bcrypt.gensalt()` makes one, and bcrypt
stores it inside the hash string, so you do not manage it separately. The salt is why a stolen
database cannot be cracked with a precomputed table, because the attacker would need a table per
salt.

The wristband is a **JWT**, a JSON Web Token: a small piece of JSON, `{"sub": "meera", "exp":
...}`, that the server signs. `sub` is the subject, who it is for; `exp` is the expiry. The
embossing seal is the **signature**, computed from the JSON and a **secret** only the server
knows. `jwt.encode(payload, secret, algorithm="HS256")` makes the token; `jwt.decode(token,
secret, algorithms=["HS256"])` checks the seal and the expiry and returns the JSON, or raises.

Because the server can verify the seal without looking anything up, a JWT is **stateless**: the
barman needs no register, only the seal. Altering the name breaks the seal, so `decode` raises;
an expired band is refused by the `exp` check; a band from another club, signed with a different
secret, fails the seal. The one rule that makes it safe is that the secret never leaves the
server, which is [day 51](../day-051-why-sorting-matters/README.md)'s lesson about secrets,
applied here.

## 4. The picture

```text
  register (once)                         login (each time)

  password "hunter2"                      password "hunter2"
      |  bcrypt.hashpw (slow, salted)         |  bcrypt.checkpw against the stored hash
      v                                        v
  $2b$12$ebZr8KTSeQjJ...   <- stored       match? yes -> issue a token
  the password itself is gone

  token (the wristband)
  {"sub":"meera","exp":...}  +  HMAC-SHA256(payload, SECRET)  =  eyJhbGci...
                                          ^ only the server has SECRET
  every later request: jwt.decode(token, SECRET) -> checks seal + exp -> "meera", or raises
```

Notice the password never appears on the right after registration: login hashes the attempt and
compares, and the stored hash is never turned back into a password because it cannot be.

## 5. The code, built step by step

Install the libraries:

```bash
python -m pip install bcrypt pyjwt
```

Registering: hash and store, never the password.

```python
USERS: dict[str, bytes] = {}


def register(username: str, password: str) -> None:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    USERS[username] = hashed
```

`password.encode()` turns the string into bytes, which bcrypt needs. `bcrypt.gensalt()` makes a
random salt with the default work factor of 12. `hashpw` returns a hash string that contains the
algorithm, the work factor, the salt, and the hash, all in one, so you store that one value and
nothing else. The plain password is never stored and never leaves the function.

Checking a password.

```python
def check_password(username: str, password: str) -> bool:
    stored = USERS.get(username)
    if stored is None:
        return False
    return bcrypt.checkpw(password.encode(), stored)
```

`checkpw` reads the salt and work factor out of the stored hash, hashes the attempt the same way,
and compares, in constant time so the comparison itself leaks nothing about how much matched. You
never hash the attempt yourself and compare with `==`; `checkpw` is the whole comparison.

Issuing a token on a successful login.

```python
SECRET = os.environ["JWT_SECRET"]   # a long random string, from the environment


def issue_token(username: str) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    payload = {"sub": username, "iat": now, "exp": now + dt.timedelta(minutes=15)}
    return jwt.encode(payload, SECRET, algorithm="HS256")
```

`sub` is who the token is for, `iat` is issued-at, `exp` is when it expires, fifteen minutes
here. `HS256` is HMAC with SHA-256: the seal is computed from the payload and the secret.
The secret comes from the environment, because it is a secret, and it must be long, at least
32 bytes for HS256, or PyJWT warns you.

Verifying a token on every later request.

```python
def verify_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

`jwt.decode` checks the seal against the secret, checks `exp` has not passed, and returns the
payload, or raises. `algorithms=["HS256"]` is not optional and not decoration: it is the list of
algorithms you will accept, and leaving it out or trusting the token's own claim is the most
famous JWT vulnerability, in section 7. `ExpiredSignatureError` is the midnight wristband;
`InvalidTokenError`, its parent, covers a broken seal and a wrong secret.

Run it:

```bash
JWT_SECRET=a-long-random-secret-of-at-least-32-bytes python main.py
```

```text
hash stored: $2b$12$ebZr8KTSeQjJfF.M98CDBe ...
same password twice, different hash: True
right password: True
wrong password: False
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ ...
verified as: meera
tampered -> None
expired -> None
wrong secret -> None
```

The stored hash starts with `$2b$12$`: bcrypt, work factor 12, then the salt. The same password
hashed twice gives two different hashes, because the salt differs, which is the line that proves
salting works. The token verifies as `meera`; a tampered token, an expired token, and a token
signed with a different secret all fail, each caught and returned as `None`.

Here is the whole program in one piece, `main.py`:

```python
import datetime as dt
import os

import bcrypt
import jwt

SECRET = os.environ["JWT_SECRET"]
USERS: dict[str, bytes] = {}


def register(username: str, password: str) -> None:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    USERS[username] = hashed


def check_password(username: str, password: str) -> bool:
    stored = USERS.get(username)
    if stored is None:
        return False
    return bcrypt.checkpw(password.encode(), stored)


def issue_token(username: str) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    payload = {"sub": username, "iat": now, "exp": now + dt.timedelta(minutes=15)}
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verify_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def main() -> None:
    register("meera", "hunter2")
    print("hash stored:", USERS["meera"][:29].decode(), "...")
    print("same password twice, different hash:",
          bcrypt.hashpw(b"hunter2", bcrypt.gensalt()) != bcrypt.hashpw(b"hunter2", bcrypt.gensalt()))
    print("right password:", check_password("meera", "hunter2"))
    print("wrong password:", check_password("meera", "wrong"))

    token = issue_token("meera")
    print("token:", token[:40], "...")
    print("verified as:", verify_token(token))

    print("tampered ->", verify_token(token[:-3] + "abc"))

    expired = jwt.encode(
        {"sub": "meera", "exp": dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=1)},
        SECRET, algorithm="HS256")
    print("expired ->", verify_token(expired))

    other = jwt.encode({"sub": "meera"}, "a-different-secret-of-at-least-32-bytes!", algorithm="HS256")
    print("wrong secret ->", verify_token(other))


if __name__ == "__main__":
    main()
```

For the argon2 alternative, `pip install argon2-cffi`, then `PasswordHasher().hash(password)` and
`.verify(stored, password)`. Argon2 won the Password Hashing Competition and is the current
first recommendation; bcrypt is the well-worn one that is everywhere. Both are slow and salted;
the choice between them is not the thing an interview turns on, and using either instead of a
fast hash is.

## 6. How the other two languages do it

**Go**

```go
hash, _ := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
err := bcrypt.CompareHashAndPassword(stored, []byte(password))   // nil means match

token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{"sub": name, "exp": exp})
signed, _ := token.SignedString(secret)
```

`golang.org/x/crypto/bcrypt` and `golang-jwt`. `CompareHashAndPassword` returns `nil` for a
match and an error otherwise, so the check is `err == nil`. Verifying supplies a key function
that must assert the algorithm.

**C++**

```cpp
std::string hash = argon2::hash(password);              // libsodium: crypto_pwhash_str
bool ok = argon2::verify(hash, password);               // crypto_pwhash_str_verify
auto token = jwt::create().set_subject(name).set_expires_at(exp).sign(jwt::algorithm::hs256{secret});
auto verifier = jwt::verify().allow_algorithm(jwt::algorithm::hs256{secret});
verifier.verify(jwt::decode(token));                    // throws on failure
```

libsodium's `crypto_pwhash_str` is argon2 with the salt and parameters baked into the string, and
`jwt-cpp` is header-only. `allow_algorithm` is the algorithm allow-list, the same guard as
Python's `algorithms=`.

**The difference that matters:** all three store a slow salted hash and sign a token, and all
three make you name the algorithm you will accept when verifying. The danger is identical in
each: verifying without pinning the algorithm lets an attacker choose it. Python's
`algorithms=["HS256"]`, Go's key function checking `token.Method`, and C++'s `allow_algorithm`
are the same defence spelled three ways, and omitting it is the same hole three ways.

## 7. The traps

**The near-miss: a fast hash.**

```python
import hashlib
USERS[username] = hashlib.sha256(password.encode()).hexdigest()
```

It "hashes" the password, and it is broken. SHA-256 is built to be fast, so a stolen database is
cracked at billions of guesses a second, and with no salt, identical passwords have identical
hashes and a precomputed table cracks them instantly. A password hash must be slow and salted;
that is bcrypt and argon2, not the `hashlib` family.

**Verifying without pinning the algorithm.** The most famous JWT attack. An attacker takes a
token, changes its header to say `"alg": "none"`, and removes the signature:

```python
forged = jwt.encode({"sub": "admin"}, key="", algorithm="none")
```

A verifier that does not restrict algorithms, or trusts the token's own header, accepts it. PyJWT
refuses, because you passed `algorithms=["HS256"]`:

```text
jwt.exceptions.InvalidAlgorithmError: The specified alg value is not allowed
```

Never omit `algorithms=`, never derive it from the token.

**A short secret.**

```text
InsecureKeyLengthWarning: The HMAC key is 20 bytes long, which is below the minimum recommended length of 32 bytes for SHA256.
```

HS256 is only as strong as the secret; a short or guessable one is a seal anyone can forge. At
least 32 random bytes, from the environment, never in the code.

**Comparing hashes with `==`.**

```python
if bcrypt.hashpw(attempt.encode(), stored) == stored:
```

Two mistakes. You cannot re-hash with `gensalt()` and match; you must use the stored hash's salt,
which is exactly what `checkpw` does. And a plain `==` on secret-derived bytes can leak timing.
`bcrypt.checkpw` handles the salt and compares in constant time.

**Putting secrets in the token.** A JWT is signed, not encrypted: anyone can read the payload,
because it is base64, not ciphertext. Decode `eyJ...` at jwt.io and you see the JSON. So a token
holds an id and an expiry, never a password, a card number, or anything private.

**A token that never expires.** Omit `exp` and the wristband works forever, so a stolen token is
a permanent key. Always set `exp`, short for access tokens, and use a separate refresh mechanism
for staying logged in, which the practice sheet explores.

**Logging the token or the password.** From [day 52](../day-052-quadratic-sorts/README.md): the
password and the token are both on the never-log list. A token in a log is a live credential for
as long as it is valid.

## 8. Say it out loud

**How it gets asked**

- How do you store a password?
- What is a salt, and what is a work factor?
- What is in a JWT, and what keeps it from being forged?
- What is the `alg: none` attack?

**The ninety-second script**

You never store the password. You store a slow, salted hash of it, made with bcrypt or argon2,
and on login you hash the attempt with the stored salt and compare in constant time; the library
does both. Slow matters because a fast hash like SHA-256 lets a stolen database be cracked at
billions of guesses a second, and bcrypt's work factor makes each guess deliberately expensive.
The salt, random per user and stored inside the hash, means two identical passwords hash
differently, so a precomputed table cannot crack the database. You never encrypt a password,
because encryption is reversible and the point is that it cannot be reversed. For staying logged
in, you issue a JWT: a small JSON payload with the subject and an expiry, signed with a secret
only the server holds, so the server can verify it on every request without a database lookup.
Tampering breaks the signature, expiry is checked from the payload, and the one rule that makes
it safe is pinning the algorithm on verify, `algorithms=["HS256"]`, because a verifier that lets
the token choose its own algorithm can be fed an unsigned `alg: none` token. The secret is long
and from the environment, and the token holds no secrets because it is signed, not encrypted.

**The follow-ups**

- **Why not encrypt the password instead of hashing?** *Encryption is reversible: whoever has the
  key can get the password back, so a breach of the key is a breach of every password. Hashing is
  one-way; there is no key that turns the hash back, so even a total breach cannot reveal the
  passwords, only let the attacker guess against slow hashes.*
- **Where do you check the token in a real service?** *In the auth middleware or dependency from
  [day 49](../day-049-peak-finding/README.md): read the `Authorization: Bearer <token>` header,
  `verify_token`, and put the subject on the request, or return 401. Every protected route gets
  it without repeating the check.*
- **How do you log someone out of a stateless token?** *You cannot revoke a JWT directly, which
  is the cost of stateless. You keep access tokens short, minutes, so a stolen one dies soon, and
  keep a server-side deny-list or a refresh-token store for immediate revocation when it matters.
  That is the trade: stateless and fast, versus revocable.*

**A model answer**

"Never store the password. Store a slow salted hash, bcrypt or argon2, and compare on login with
the library's constant-time check. Slow defeats brute force on a stolen database; the salt
defeats precomputed tables. Never encrypt it, because that is reversible. For sessions, a JWT: a
signed JSON payload with a subject and a short expiry, verified with a secret the server holds,
so no lookup per request. Pin the algorithm on verify or you are open to the `alg: none` forgery,
keep the secret long and in the environment, and put nothing secret in the token because it is
signed, not encrypted."

## 9. Recall card

- Never store the password: store a slow, salted hash (`bcrypt.hashpw`/`checkpw`, or argon2). Never a fast hash like SHA-256, never encryption.
- The salt (random per user, inside the hash) defeats precomputed tables; the work factor makes each guess slow. `checkpw` compares in constant time.
- A JWT is JSON + a signature from a server-only secret: `sub`, `exp`, `jwt.encode(payload, SECRET, algorithm="HS256")`.
- `jwt.decode(token, SECRET, algorithms=["HS256"])` — pinning `algorithms=` is mandatory, or the `alg: none` forgery works.
- A JWT is signed, not encrypted: readable by anyone, so no secrets in it; always set `exp`; the secret is long and from the environment.
