# Issue 2: Rust Basics + Debian Essentials

**Cycle 1 · Week B.** Last week you wrote your first Python functions and rebuilt your first NixOS generations. This week we switch sides of the aisle: **Rust** (a compiled systems language) and **Debian** (the classic Linux distribution NixOS does things very differently from). New concepts only — nothing repeated from Issue 1.

---

## Progress

| Week | Topics | Status |
|---|---|---|
| Issue 1 (Week A) | Python basics + NixOS config/generations | ✅ Done |
| **Issue 2 (Week B)** | **Rust basics + Debian essentials** | 📍 You are here |
| Issue 3 (Week C) | Review & Synthesis (flashcards, mixed exercises) | Up next |

---

# Part 1 — Rust

## Core Concepts

Rust is a **compiled** language: you turn source code into a fast, standalone binary before running it. Where Python says "we'll check that at runtime," Rust says "prove it to me at compile time." That's why Rust is used for CLIs, servers, embedded systems, and anywhere a crash at 3 AM is unacceptable. This week: variables, functions, and your first compiled program.

## E-Learning Knowledge

### Step 1 — Install the toolchain and say hello

```bash
# Install rustup, the official Rust installer (Linux/macOS)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# Restart your shell, then verify
rustc --version   # compiler version
cargo --version   # Cargo = build tool + package manager in one
```

```bash
# Create and run your first project
cargo new hello_rust
cd hello_rust
cargo run         # compiles src/main.rs and executes it
```

### Step 2 — Variables, types, and mutability

```rust
fn main() {
    let x = 5;          // immutable by default — cannot be reassigned
    let mut y = 10;     // `mut` opts into mutation
    y += 1;
    println!("x = {x}, y = {y}");  // {x} inlines variables (like f-strings!)

    let pi: f64 = 3.14159;         // explicit type annotation
    let is_ready: bool = true;
    println!("pi={pi}, ready={is_ready}");
}
```

Key difference from Python: types are fixed at compile time. `y = "text";` after `let mut y = 10` is a compile error, not a runtime surprise.

### Step 3 — Functions and return values

```rust
fn add(a: i32, b: i32) -> i32 {  // types are mandatory: params and return
    a + b                        // last expression = implicit return (no semicolon!)
}

fn main() {
    let sum = add(2, 3);
    println!("2 + 3 = {sum}");
}
```

Note the missing semicolon on `a + b`: an expression *with* a semicolon becomes a statement (returns nothing). This is the #1 beginner gotcha.

### Step 4 — Control flow

```rust
fn main() {
    let n = 7;
    // `if` is an expression — it produces a value
    let parity = if n % 2 == 0 { "even" } else { "odd" };
    println!("{n} is {parity}");

    // loop over a range
    for i in 1..=3 {          // 1..=3 includes 3
        println!("iteration {i}");
    }
}
```

### Step 5 — Your first taste of ownership (preview for a later issue)

```rust
fn main() {
    let s = String::from("hello");
    let t = s;                  // ownership MOVES from s to t
    // println!("{s}");         // ← compile error: s no longer owns the data
    println!("{t}");            // this is fine
}
```

Rust doesn't garbage-collect. Each value has exactly one owner; assigning a heap value hands ownership over. The compiler enforces this so memory bugs become compile errors. We'll go deeper in a later issue.

## Quick Exercises

**Ex 1 — Greeting CLI.** Modify `hello_rust` to print a personalized greeting using a variable.

<details><summary>Answer</summary>

```rust
fn main() {
    let name = "Mister paper";
    println!("Hello, {name}! Welcome to Rust.");
}
```
Run with `cargo run`.

</details>

**Ex 2 — Temperature converter.** Write a function `celsius_to_fahrenheit(c: f64) -> f64` and print 25°C in °F.

<details><summary>Answer</summary>

```rust
fn celsius_to_fahrenheit(c: f64) -> f64 {
    c * 9.0 / 5.0 + 32.0
}

fn main() {
    let f = celsius_to_fahrenheit(25.0);
    println!("25°C = {f}°F");   // prints 77
}
```
Types are `f64` so the division is floating-point, not integer.

</details>

**Ex 3 — FizzBuzz, Rust edition.** Print 1–15; multiples of 3 → "Fizz", of 5 → "Buzz", both → "FizzBuzz".

<details><summary>Answer</summary>

```rust
fn main() {
    for n in 1..=15 {
        let out = if n % 15 == 0 { "FizzBuzz" }
                  else if n % 3 == 0 { "Fizz" }
                  else if n % 5 == 0 { "Buzz" }
                  else { "" };
        if out.is_empty() { println!("{n}") } else { println!("{out}") }
    }
}
```

</details>

**Ex 4 — Break the move rule on purpose.** Write `let a = String::from("hi"); let b = a;` then try to print `a`. Read the compiler error.

<details><summary>Answer</summary>

The compiler says: `borrow of moved value: 'a'` and suggests `clone()`. Fix: `let b = a.clone();` — that makes a deep copy, so both variables stay valid. Reading compiler errors carefully is the core Rust skill.

</details>

**Ex 5 — Build a release binary.** Compile your project in release mode and find the binary.

<details><summary>Answer</summary>

```bash
cargo build --release
ls target/release/        # the executable is named after your project
./target/release/hello_rust
```
Release mode enables optimizations — much faster, slower to compile.

</details>

---

# Part 2 — Debian

## Core Concepts

Debian is the granddaddy of stable Linux distributions: what NixOS does with generations and a store, Debian does with a mature package index and disciplined releases. Knowing Debian matters because it powers most servers, and because understanding its *imperative* model (install/change things in place) sharpens your appreciation of NixOS's *declarative* model. This week: package management, moving around the filesystem, permissions, and services.

## E-Learning Knowledge

### Step 1 — apt: the package lifecycle

```bash
sudo apt update               # refresh the package index (metadata only)
apt search nginx              # find packages
apt show nginx                # details: version, deps, size
sudo apt install nginx        # install
sudo apt upgrade              # upgrade all installed packages
sudo apt remove nginx         # uninstall (keeps config files)
sudo apt purge nginx          # uninstall + delete config files
sudo apt autoremove           # clean orphaned dependencies
```

`apt update` ≠ `apt upgrade`: the first refreshes the *list* of available versions, the second actually installs them.

### Step 2 — Navigate the filesystem like a native

```bash
pwd                  # where am I
ls -lah              # list with sizes, hidden files, human-readable
cd /etc/nginx        # absolute path
cd .. && cd ~        # up one level / home
cat /etc/os-release  # confirm it's Debian
less /var/log/syslog # page through a long file (q to quit)
find /etc -name "*.conf" 2>/dev/null   # find config files
```

Key locations: `/etc` (configs), `/var/log` (logs), `/home` (users), `/usr/bin` (programs), `/opt` (your own software).

### Step 3 — Permissions and ownership

```bash
ls -l script.sh
# -rwxr-xr-- 1 alice dev 220 Nov 7 10:00 script.sh
#  ^ owner: rwx   group: r-x   others: r--
chmod +x script.sh            # make executable
chmod 640 script.sh           # owner rw-, group r--, others nothing
sudo chown alice:dev script.sh  # change owner and group
```

Rule of thumb: give the minimum rights needed. A web server should read its config, not own it.

### Step 4 — systemd: services in Debian

```bash
systemctl status nginx        # is it running? enabled at boot?
sudo systemctl start nginx    # start now
sudo systemctl enable nginx   # start automatically at boot
sudo systemctl restart nginx  # restart after config change
journalctl -u nginx -e        # recent logs for this unit
```

systemd is Debian's init system: PID 1, parent of all services. Unit files live in `/etc/systemd/system/` and `/lib/systemd/system/`.

### Step 5 — SSH: the remote-admin essentials

```bash
sudo apt install openssh-server
systemctl status ssh

# Generate your own key pair (accept the defaults, add a passphrase)
ssh-keygen -t ed25519
# connect from another machine:
ssh alice@192.168.1.50
# copy your public key for passwordless login:
ssh-copy-id alice@192.168.1.50
```

## Quick Exercises

**Ex 1 — Index vs upgrade.** Run `sudo apt update`, then `apt list --upgradable`. How many packages could be upgraded? Now decide: upgrade now or later?

<details><summary>Answer</summary>

```bash
sudo apt update
apt list --upgradable
```
`update` only refreshes metadata; `apt list --upgradable` reads it. Upgrading is your call — on a stable server, review the list first (`sudo apt upgrade` shows sizes and asks for confirmation).

</details>

**Ex 2 — Permission surgery.** Create a file, then make it readable/writable by you only, and verify with `ls -l`.

<details><summary>Answer</summary>

```bash
touch secret.txt
chmod 600 secret.txt
ls -l secret.txt    # -rw------- : only the owner can read/write
```

</details>

**Ex 3 — Service detective.** Install `nginx` (or check any installed service), confirm it's running, find its boot status, and read its last 10 log lines.

<details><summary>Answer</summary>

```bash
sudo apt install nginx
systemctl status nginx        # active (running)?
systemctl is-enabled nginx    # enabled at boot?
journalctl -u nginx -n 10     # last 10 log lines
```

</details>

**Ex 4 — Find the biggest log.** In `/var/log`, find the largest file and report its size in human-readable form.

<details><summary>Answer</summary>

```bash
sudo du -ah /var/log 2>/dev/null | sort -rh | head -5
```
`du -ah` lists all files with sizes, `sort -rh` sorts human-readable descending, `head -5` shows the biggest five.

</details>

**Ex 5 — Contrast drill.** Install `htop` on Debian with apt. Without touching anything on NixOS, write one sentence: what would be the NixOS way, and what's the key difference?

<details><summary>Answer</summary>

Debian: `sudo apt install htop` — an imperative change applied to the running system immediately.
NixOS: add `pkgs.htop` to `environment.systemPackages` in `configuration.nix`, then `sudo nixos-rebuild switch` — a declarative change that produces a new generation. Debian mutates state in place; NixOS declares desired state and derives it atomically.

</details>

---

## Next Issue Preview

**Issue 3 (Week C) — Review & Synthesis:** flashcards over Issues 1–2, mixed cross-tool exercises (Rust + Debian together, Python + NixOS together), bridges between all four tools, and the Cycle 1 progress table. See you next week! 🚀
