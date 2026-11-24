# Issue 5: Rust Collections & Error Handling + Debian Users, Cron & Hardening

**Cycle 2 · Week B.** Issue 4 gave Python its collections and `try/except`, and NixOS its services and flakes. This week the Week B pair goes one level deeper in perfect symmetry: Rust's collections and its `Result`-based error handling (the compile-time mirror of Python's exceptions), and Debian's user model, scheduled jobs, and first security hardening. Nothing repeats Issue 2 — that was toolchain, variables, functions, apt, permissions, and systemd basics.

---

## Progress

| Week | Topics | Status |
|---|---|---|
| Issue 4 (Week A) | Python collections/files + NixOS services/flakes | ✅ Done |
| **Issue 5 (Week B)** | **Rust collections/Result + Debian users/cron/hardening** | 📍 You are here |
| Issue 6 (Week C) | Review & Synthesis — Cycle 2 recap | Up next |

---

# Part 1 — Rust: Collections & Error Handling

## Core Concepts

Python programs crash gracefully at runtime; Rust programs *refuse to compile* if you forgot to handle failure. This is done with `Result<T, E>` — a value that is either `Ok(data)` or `Err(reason)` — and the compiler forces you to choose what to do with it. Combined with collections (`Vec`, `HashMap`) and iterators, this is the core of writing real Rust: parsing files, aggregating data, handling missing things. Use cases: CLIs that process files, config parsers, anything that touches the outside world.

## E-Learning Knowledge

### Step 1 — Vec: the growable list

```rust
fn main() {
    let mut v: Vec<i32> = Vec::new();
    v.push(1);
    v.push(2);
    v.push(3);

    // literal syntax — the common way
    let v2 = vec![10, 20, 30];

    // indexing vs get: one panics, one returns an Option
    println!("{}", v2[1]);            // 20 — panics if out of bounds
    println!("{:?}", v2.get(5));      // None — safe access
    println!("{:?}", v2.get(1));      // Some(20)

    // iterate ( borrowing, not moving — important!)
    for x in &v2 {
        println!("got {x}");
    }
    println!("still usable: {:?}", v2);   // works because we borrowed with &
}
```

`Vec` is Rust's Python list. The difference to internalize: without `&`, a `for x in v2` loop would *move* the vector and you couldn't use it afterwards.

### Step 2 — HashMap: the dictionary

```rust
use std::collections::HashMap;

fn main() {
    let mut scores: HashMap<String, i32> = HashMap::new();
    scores.insert("alice".to_string(), 90);
    scores.insert("bob".to_string(), 75);

    // safe read via get → Option
    if let Some(score) = scores.get("alice") {
        println!("alice: {score}");
    }

    // the counting pattern (compare Python's counts.get(w, 0) + 1)
    let text = "the cat and the hat";
    let mut counts: HashMap<&str, i32> = HashMap::new();
    for word in text.split_whitespace() {
        *counts.entry(word).or_insert(0) += 1;
    }
    println!("{:?}", counts);   // {"the": 2, "cat": 1, "and": 1, "hat": 1}
}
```

`entry().or_insert(0)` is the idiomatic "get or create with default" — one line instead of Python's get-and-reassign.

### Step 3 — Result: errors as values

```rust
use std::fs;

fn main() {
    // parse a string → Result. 8/2 fits, "x"/0 doesn't
    let n: Result<i32, _> = "42".parse();
    match n {
        Ok(value) => println!("parsed: {value}"),
        Err(e) => println!("failed: {e}"),
    }

    // reading a file returns Result too
    match fs::read_to_string("notes.txt") {
        Ok(content) => println!("{} bytes", content.len()),
        Err(e) => println!("could not read: {e}"),
    }
}
```

There is no exception here: the error is an ordinary value in the return type, and the compiler refuses to let you ignore it silently (unwarned code that drops a `Result` produces a warning).

### Step 4 — match, unwrap, and the ? operator

Three levels of ergonomics, from manual to idiomatic:

```rust
use std::fs;

// 1. unwrap: "crash if wrong" — fine for examples, never for production
let content = fs::read_to_string("notes.txt").unwrap();

// 2. match: full control
let content = match fs::read_to_string("notes.txt") {
    Ok(c) => c,
    Err(e) => {
        eprintln!("fatal: {e}");
        std::process::exit(1);
    }
};

// 3. ? : propagate the error upward — the workhorse
fn read_len(path: &str) -> Result<usize, std::io::Error> {
    let content = fs::read_to_string(path)?;   // on Err, return early with it
    Ok(content.len())
}

fn main() {
    match read_len("notes.txt") {
        Ok(n) => println!("{n} bytes"),
        Err(e) => eprintln!("error: {e}"),
    }
}
```

`?` is Rust's answer to `try/except`-with-rethrow: handle locally with `match`, or pass the problem up with `?`. Function signatures tell the truth about what can fail.

### Step 5 — Iterators: map/filter/collect

```rust
fn main() {
    let nums = vec![1, 2, 3, 4, 5, 6];

    // the comprehension equivalent: iterator chain → collect
    let squares: Vec<i32> = nums.iter().map(|n| n * n).collect();
    let evens: Vec<&i32> = nums.iter().filter(|n| n % 2 == 0).collect();
    let sum: i32 = nums.iter().sum();
    let total_sq: i32 = nums.iter().map(|n| n * n).sum();

    println!("{squares:?}");   // [1, 4, 9, 16, 25, 36]
    println!("{evens:?}");     // [2, 4, 6]
    println!("{sum}, {total_sq}");   // 21, 91

    // collect into other types too: collect::<HashSet<_>>() etc.
}
```

Same shape as Python comprehensions (`[n*n for n in nums]`), but lazy and checked at compile time. `.iter()` borrows; `.into_iter()` consumes.

## Quick Exercises

**Ex 1 — Safe word counter.** Port Python's counting pattern: read the program argument as a filename, count word frequencies, print the top 3. Use `entry().or_insert(0)`.

<details><summary>Answer</summary>

```rust
use std::collections::HashMap;
use std::env;
use std::fs;

fn main() {
    let path = env::args().nth(1).expect("usage: wordfreq <file>");
    let content = fs::read_to_string(&path).expect("cannot read file");

    let mut counts: HashMap<&str, usize> = HashMap::new();
    for word in content.split_whitespace() {
        *counts.entry(word).or_insert(0) += 1;
    }

    let mut v: Vec<_> = counts.into_iter().collect();
    v.sort_by(|a, b| b.1.cmp(&a.1));
    for (word, n) in v.iter().take(3) {
        println!("{n:5}  {word}");
    }
}
```
`env::args().nth(1)` returns an `Option` — `expect` is our friendly crash for a missing argument. `sort_by` with `b.1.cmp(&a.1)` sorts descending by count.

</details>

**Ex 2 — match vs ?.** Write `fn double(s: &str) -> Result<i32, std::num::ParseIntError>` that parses and doubles a number. Call it three ways: `match`, `.unwrap_or(0)`, and `?` from another function.

<details><summary>Answer</summary>

```rust
fn double(s: &str) -> Result<i32, std::num::ParseIntError> {
    let n: i32 = s.parse()?;
    Ok(n * 2)
}

fn main() {
    // 1. match
    match double("21") {
        Ok(v) => println!("match: {v}"),
        Err(e) => println!("match error: {e}"),
    }
    // 2. default on error
    println!("default: {}", double("x").unwrap_or(0));
    // 3. ? (implicitly demonstrated: double itself uses ? on parse)
}
```
`unwrap_or(0)` = Python's `dict.get(key, default)` spirit: substitute instead of crashing.

</details>

**Ex 3 — Iterator chain gauntlet.** Given `let nums = vec![3, 1, 4, 1, 5, 9, 2, 6];` produce in iterator chains: (a) the squares of the even numbers, (b) the largest value, (c) the values sorted descending.

<details><summary>Answer</summary>

```rust
let nums = vec![3, 1, 4, 1, 5, 9, 2, 6];

let a: Vec<i32> = nums.iter().filter(|n| n % 2 == 0).map(|n| n * n).collect();
let b = nums.iter().max();                      // Option<&i32> — Some(9)
let mut c = nums.clone();
c.sort();                                       // sort ascending
c.reverse();                                    // descending
// or: c.sort_by(|x, y| y.cmp(x));

println!("{a:?}, {b:?}, {c:?}");
```
`max()` returns an `Option` — Rust never hands you a "no answer" as a silent zero.

</details>

**Ex 4 — Robust file reader.** Write a function `count_lines(path: &str) -> Result<usize, std::io::Error>` using `?`, and a `main` that prints a friendly message instead of panicking when the file is missing. Test with a nonexistent path.

<details><summary>Answer</summary>

```rust
use std::fs;

fn count_lines(path: &str) -> Result<usize, std::io::Error> {
    let content = fs::read_to_string(path)?;
    Ok(content.lines().count())
}

fn main() {
    match count_lines("does_not_exist.txt") {
        Ok(n) => println!("{n} lines"),
        Err(e) => eprintln!("could not read file: {e}"),
    }
}
```
Output is a clean `could not read file: No such file or directory` — no traceback-style panic, because we chose to handle the error instead of `unwrap()`.

</details>

**Ex 5 — The compiler teaches.** In Ex 1, remove the `&` from `for (word, n) in v.iter()...` by writing `for (word, n) in v` and then trying to use `v` afterwards. Read the error, then fix it either with `&v` or by restructuring.

<details><summary>Answer</summary>

Error: `value borrowed here after move` (or `borrow of moved value: 'v'`). Iterating `for x in v` *consumes* the vector; afterwards it no longer exists. Fixes:
- `for (word, n) in &v { ... }` — borrow, keep ownership;
- or accept the move and simply not use `v` afterwards (as in Ex 1, where `into_iter()` consumed it deliberately).
Same lesson as Issue 2's move preview — now applied to collections.

</details>

---

# Part 2 — Debian: Users, Cron & Hardening

## Core Concepts

Issue 2 treated Debian as a single-admin box. Real machines are shared and exposed: multiple users with different powers, jobs that must run unattended, and a network that probes every open port. Debian's answers are its user/group model, `sudo` policy, cron and systemd timers for scheduling, and a short list of high-value hardening moves. These skills transfer to every Debian-based server you'll ever touch.

## E-Learning Knowledge

### Step 1 — Users and groups: the foundations

```bash
sudo adduser alice            # interactive: creates user, home, password
sudo usermod -aG sudo alice   # grant sudo (append -a is critical, -G alone REPLACES groups)
groups alice                  # verify membership
sudo deluser --remove-home bob  # remove user + home directory

id                            # your own uid, gid, groups
cat /etc/passwd | tail -5     # user database (one line per user)
cat /etc/group | grep sudo    # group database
```

The `-aG` flag is the classic footgun: `usermod -G sudo alice` (without `-a`) would strip alice of *all* other groups.

### Step 2 — sudo policy: who may do what

```bash
sudo visudo                   # NEVER edit /etc/sudoers directly; visudo checks syntax
```

```
# give a group full sudo
%sudo ALL=(ALL:ALL) ALL

# or a single command with no password — e.g. for a backup script
backup ALL=(root) NOPASSWD: /usr/bin/rsync
```

Principle: grant the narrowest sudo that works. A service account that only needs `rsync` should not have full root.

### Step 3 — Cron: scheduled jobs, the classic way

```bash
crontab -e                    # edit YOUR cron table
crontab -l                    # list it
sudo crontab -e               # root's cron table
```

```cron
# ┌─ minute (0-59)
# │ ┌─ hour (0-23)
# │ │ ┌─ day of month (1-31)
# │ │ │ ┌─ month (1-12)
# │ │ │ │ ┌─ day of week (0-6, 0=Sunday)
# │ │ │ │ │
  30 3  * * *   /home/mister/scripts/backup.sh >> /var/log/backup.log 2>&1
  0  *  * * *   /usr/bin/apt-get update -qq          # hourly index refresh
```

Five time fields, then the command. `>> file 2>&1` captures both stdout and stderr — cron discards output otherwise, which makes failures invisible. Debian also ships `systemd timers` (you met them on NixOS in Issue 4): cron for quick personal jobs, timers when you want journalctl logging and dependencies.

### Step 4 — Firewalls and open ports: know your exposure

```bash
sudo apt install ufw          # Uncomplicated Firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh            # or: allow 22/tcp
sudo ufw enable
sudo ufw status verbose

ss -tlnp                      # what is LISTENING on which port — run this first!
sudo apt install nmap && nmap localhost   # outside view of your own box
```

The workflow: `ss -tlnp` shows what's listening → anything unnecessary gets stopped → `ufw` blocks what must stay local. An open port is a standing invitation.

### Step 5 — Hardening checklist: five high-value moves

```bash
# 1. Key-only SSH (you set the NixOS version in Issue 4; here's the Debian way):
sudo nano /etc/ssh/sshd_config
#   PasswordAuthentication no
#   PermitRootLogin no
sudo systemctl restart ssh

# 2. Automatic security updates:
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# 3. Fail2ban: ban IPs that brute-force SSH
sudo apt install fail2ban
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd     # see banned IPs

# 4. Audit who logged in:
last -20                             # recent logins
sudo lastb                           # failed login attempts

# 5. Check pending security fixes:
sudo apt update && apt list --upgradable | grep -i secur
```

None of these makes you unhackable; together they eliminate the attacks that are automated, constant, and opportunistic.

## Quick Exercises

**Ex 1 — User lifecycle.** Create a user `tester`, put them in the `sudo` group, verify with `groups`, then delete them with their home directory.

<details><summary>Answer</summary>

```bash
sudo adduser tester
sudo usermod -aG sudo tester
groups tester                  # tester : tester sudo
sudo deluser --remove-home tester
```

</details>

**Ex 2 — Cron drill.** Schedule a job that appends the current date to `~/cronlog.txt` every minute. Watch it for two minutes, then remove the job.

<details><summary>Answer</summary>

```bash
crontab -e
# add:
* * * * * date >> /home/mister/cronlog.txt
```
```bash
cat ~/cronlog.txt              # one line per minute
crontab -e                     # delete the line
```
Every-minute jobs are the standard way to prove cron is alive before trusting it with something real.

</details>

**Ex 3 — Port census.** Run `ss -tlnp`. List every listening service, and for each decide: keep, or stop and block. Then enable ufw with deny-incoming and allow-ssh.

<details><summary>Answer</summary>

```bash
ss -tlnp
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
sudo ufw status verbose
```
A typical minimal box listens on `:22` (keep, firewalled) and a local resolver on `127.0.0.1` (keep — loopback only, unreachable from outside). Anything on `0.0.0.0` that you don't recognize is the item to investigate.

</details>

**Ex 4 — Log analysis, Debian edition.** Count failed SSH logins of the last session with `lastb`, and identify the top 3 source IPs.

<details><summary>Answer</summary>

```bash
sudo lastb | head -20          # eyeball it
sudo lastb | awk '{print $3}' | sort | uniq -c | sort -rn | head -3
```
`awk '{print $3}'` extracts the host column, `sort | uniq -c | sort -rn` is the classic count-and-rank pipeline (the shell cousin of Python's counting dict).

</details>

**Ex 5 — Cross-week contrast.** You scheduled a backup with a NixOS systemd timer in Issue 4 and with cron here. Write two sentences: which gives better logging, and which is available on *every* Debian/Unix machine regardless of config management?

<details><summary>Answer</summary>

systemd timers win on logging (stdout/stderr go to the journal automatically — `journalctl -u <name>` — plus `Persistent=true` catches missed runs after downtime). Cron wins on universality: it exists on essentially every Unix-like system with zero configuration machinery, so it's the portable choice for quick personal jobs. Rule of thumb: services you administer → timers; quick user-level scripts → cron.

</details>

---

## Next Issue Preview

**Issue 6 (Week C) — Review & Synthesis, Cycle 2 recap:** flashcards over Issues 4–5, mixed cross-tool exercises (Rust + Debian, Python + NixOS together), the updated bridges table, and the cumulative Cycle 2 progress table. See you next Monday! 🚀
