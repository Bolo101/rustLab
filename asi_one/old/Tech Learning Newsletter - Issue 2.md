# 🚀 Tech Learning Newsletter - Issue 2
### Leveling Up: Rust, Python, Debian & NixOS
*Building on Issue 1 — this week we go one step deeper, from basics toward intermediate territory.*

---

## 🦀 Rust: Ownership, Borrowing & Structs

### Core Concepts
Last week you learned variables, functions, and loops. This week we tackle the feature that makes Rust *Rust*: **ownership**. It's how Rust guarantees memory safety at compile time — no garbage collector, no manual `free()`. Understanding ownership unlocks everything else in the language.

**Why this matters:**
- **Ownership** is the compiler's rulebook for who is responsible for a value in memory
- **Borrowing** lets you use data without taking control of it
- **Structs** let you model real-world things (a `User`, a `Book`, a `Point`) as custom types
- These concepts are why Rust programs rarely crash from memory bugs

### E-Learning Knowledge - Week 2: The Ownership Model

#### 1. Ownership Rules
Rust has exactly three rules. Memorize them:
```rust
fn main() {
    // RULE 1: Each value has ONE owner.
    let s1 = String::from("hello");

    // RULE 2: When the owner goes out of scope, the value is dropped (freed).
    {
        let s2 = String::from("temporary");
        println!("{}", s2);
    } // s2 is dropped here — memory freed automatically.

    // RULE 3: You can MOVE ownership, but only one variable can own at a time.
    let s3 = s1; // s1 is MOVED into s3.
    // println!("{}", s1); // ❌ COMPILE ERROR: s1 no longer owns the data.
    println!("{}", s3);   // ✅ s3 is the owner now.

    // Copy types (integers, floats, bools, chars) are copied, not moved:
    let a = 5;
    let b = a; // a is COPIED into b — both still valid!
    println!("{} and {}", a, b);
}
```

#### 2. Borrowing: References
Instead of moving values, *borrow* them with `&`:
```rust
fn count_length(text: &str) -> usize {
    text.len() // We only LOOK at the data; we don't own it.
}

fn main() {
    let message = String::from("Hello, Rust!");

    // Immutable borrow: read-only access, any number allowed.
    let len = count_length(&message);
    println!("'{}' has {} characters", message, len); // ✅ message still valid!

    // Mutable borrow: exactly ONE at a time, nothing else can read while active.
    let mut counter = String::from("count: ");
    add_exclamation(&mut counter);
    println!("{}", counter); // "count: !"
}

fn add_exclamation(text: &mut String) {
    text.push('!');
}
```

**The golden rule:** at any given time you may have *either* many immutable references (`&T`) *or* one mutable reference (`&mut T`) — never both. The compiler enforces this to prevent data races.

#### 3. Structs: Your Own Data Types
```rust
// Define a struct — a blueprint for related data.
struct Book {
    title: String,
    author: String,
    pages: u32,
}

// Implement methods on the struct.
impl Book {
    // Associated function (like a constructor) — no self parameter.
    fn new(title: &str, author: &str, pages: u32) -> Book {
        Book {
            title: title.to_string(),
            author: author.to_string(),
            pages,
        }
    }

    // Method — takes &self (a read-only borrow of the instance).
    fn summary(&self) -> String {
        format!("'{}' by {} ({} pages)", self.title, self.author, self.pages)
    }

    // Method that mutates — takes &mut self.
    fn add_pages(&mut self, extra: u32) {
        self.pages += extra;
    }
}

fn main() {
    let mut my_book = Book::new("The Rust Book", "Community", 500);
    println!("{}", my_book.summary());

    my_book.add_pages(50);
    println!("After expansion: {} pages", my_book.pages);
}
```

#### 4. Enums and match (a taste of intermediate Rust)
```rust
enum Shape {
    Circle(f64),          // Variant carrying data
    Rectangle(f64, f64),
}

fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle(radius) => 3.14159 * radius * radius,
        Shape::Rectangle(w, h) => w * h,
    }
}

fn main() {
    let c = Shape::Circle(2.0);
    let r = Shape::Rectangle(3.0, 4.0);
    println!("Circle area: {:.2}", area(&c));     // 12.57
    println!("Rectangle area: {:.2}", area(&r));  // 12.00
}
```
`match` must cover *every* possibility — the compiler won't let you forget a case. This is why Rust code handles errors so thoroughly.

### Quick Exercises

#### Exercise 1: Fix the Move
**Task**: This code fails to compile. Fix it with a borrow instead of a move.
```rust
fn print_twice(s: String) {
    println!("{}", s);
}

fn main() {
    let greeting = String::from("hi");
    print_twice(greeting);
    print_twice(greeting); // ❌ error!
}
```

#### Exercise 2: Rectangle Struct
**Task**: Create a `Rectangle` struct with `width` and `height` fields, a `new` constructor, and an `area` method that returns `width * height` as `u32`.

#### Exercise 3: Mutable Counter
**Task**: Write a function `bump(n: &mut i32)` that adds 1 to the value it borrows. In `main`, call it three times on a variable starting at 0 and print the result (expect `3`).

#### Exercise 4: Shape Matcher
**Task**: Extend the `Shape` enum from the lesson with a `Triangle(f64, f64)` variant (base, height) and update `area` so triangles return `base * height / 2.0`.

#### Exercise 5: Borrow Checker Detective
**Task**: Will this compile? Say yes or no, and explain why — *before* running it.
```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let first = &v[0];
    v.push(4);
    println!("{}", first);
}
```

### Exercise Answers

```rust
// Exercise 1 Answer — take a reference (&str) instead of owning String:
fn print_twice(s: &str) {
    println!("{}", s);
}
fn main() {
    let greeting = String::from("hi");
    print_twice(&greeting); // borrow, don't move
    print_twice(&greeting); // ✅ works now
}

// Exercise 2 Answer
struct Rectangle {
    width: u32,
    height: u32,
}
impl Rectangle {
    fn new(width: u32, height: u32) -> Rectangle {
        Rectangle { width, height }
    }
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

// Exercise 3 Answer
fn bump(n: &mut i32) {
    *n += 1; // dereference the mutable borrow to change the value
}
fn main() {
    let mut count = 0;
    bump(&mut count);
    bump(&mut count);
    bump(&mut count);
    println!("{}", count); // 3
}

// Exercise 4 Answer
enum Shape {
    Circle(f64),
    Rectangle(f64, f64),
    Triangle(f64, f64),
}
fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle(radius) => 3.14159 * radius * radius,
        Shape::Rectangle(w, h) => w * h,
        Shape::Triangle(base, height) => base * height / 2.0,
    }
}

// Exercise 5 Answer: ❌ NO, it does not compile.
// `first` is an immutable borrow of `v`. Calling `v.push(4)` needs a
// mutable borrow, and the borrow checker forbids a mutable borrow while
// an immutable one is still alive (it's used in the println! after the push).
// Fix: move `println!("{}", first);` BEFORE `v.push(4);`.
```

---

## 🐍 Python: Functions Deep-Dive, Modules & Error Handling

### Core Concepts
You wrote your first functions last week. This week we go deeper: Python's flexible function arguments, how to organize code into **modules**, and how to handle things going wrong gracefully with **exceptions**. These three skills are what separate "I can run scripts" from "I can write real programs."

**Why this matters:**
- **Flexible arguments** (`*args`, `**args`, keyword defaults) power almost every library API you'll ever use
- **Modules** keep projects organized — no more one giant 500-line file
- **Exception handling** means your programs recover from bad input instead of crashing

### E-Learning Knowledge - Week 2: Functions, Modules & Errors

#### 1. Flexible Function Arguments
```python
# Default arguments — callers can omit them.
def make_coffee(size="medium", milk=True):
    milk_str = "with milk" if milk else "black"
    return f"A {size} coffee, {milk_str}"

print(make_coffee())                      # A medium coffee, with milk
print(make_coffee(size="large"))          # A large coffee, with milk
print(make_coffee("small", milk=False))   # A small coffee, black

# *args — collect any number of positional arguments into a tuple.
def total(*numbers):
    return sum(numbers)

print(total(1, 2))          # 3
print(total(1, 2, 3, 4, 5)) # 15

# **kwargs — collect any keyword arguments into a dict.
def describe_person(**details):
    for key, value in details.items():
        print(f"  {key}: {value}")

describe_person(name="Mister paper", city="Dieppe", hobby="sailing")

# Combining them (order matters: positional, *args, default, **kwargs).
def flexible(a, b=2, *args, **kwargs):
    return (a, b, args, kwargs)

print(flexible(1, 3, 4, 5, extra="hi"))
# (1, 3, (4, 5), {'extra': 'hi'})
```

#### 2. Modules: Organizing Your Code
```python
# --- Save this as mymath.py ---
def double(x):
    return x * 2

PI = 3.14159

# --- In another file (or the same session) ---
import mymath
print(mymath.double(21))   # 42
print(mymath.PI)           # 3.14159

# Import just one thing:
from mymath import double
print(double(8))           # 16

# Rename on import:
import mymath as mm
print(mm.PI)

# Python's standard library is full of ready-made modules:
import math
print(math.sqrt(144))      # 12.0

import random
print(random.randint(1, 6))   # a dice roll: 1-6

from datetime import date
print(date.today())        # today's date
```

#### 3. Exception Handling
```python
# try / except: catch an error and keep going.
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero!"
    except TypeError:
        return "Please use numbers only."

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # Cannot divide by zero!
print(safe_divide(10, "x")) # Please use numbers only.

# else runs if NO exception occurred; finally always runs.
def read_config(filename):
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:
        return None
    finally:
        print("(read attempt finished)")

# Raising your own exceptions:
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age

# set_age(-5)  # would raise: ValueError: Age cannot be negative
```

#### 4. List & Dict Methods You'll Use Daily
```python
# Sorting
scores = [88, 42, 95, 67]
print(sorted(scores))            # [42, 67, 88, 95] (new list)
scores.sort(reverse=True)        # sorts in place: [95, 88, 67, 42]

# enumerate: index + value together
for i, fruit in enumerate(["apple", "kiwi", "plum"], start=1):
    print(f"{i}. {fruit}")

# zip: walk two lists in parallel
names = ["Ana", "Bo", "Cy"]
ages = [31, 25, 44]
for name, age in zip(names, ages):
    print(f"{name} is {age}")

# min / max / any / all
print(max(scores), min(scores))  # 95 42
print(all(s > 40 for s in scores))  # True
```

### Quick Exercises

#### Exercise 1: Flexible Greeter
**Task**: Write `greet(*names, punctuation="!")` that returns one greeting line per name, e.g. `greet("Ana", "Bo")` → `"Hello Ana!\nHello Bo!"`, and `greet("Cy", punctuation="?")` → `"Hello Cy?"`.

#### Exercise 2: Dice Simulator
**Task**: Using `random.randint`, write `roll_dice(sides=6, times=1)` that returns a list of rolls. `roll_dice(sides=20, times=3)` should give 3 numbers between 1 and 20.

#### Exercise 3: Safe Converter
**Task**: Write `to_int(text)` that returns the integer value of `text`, or `None` if the text isn't a valid number — using `try/except ValueError`. Test with `"42"`, `"3.5"`, and `"hello"`.

#### Exercise 4: Module Practice
**Task**: Create a file `stringtools.py` with a function `shout(text)` returning the uppercase text plus `"!!!"`. Import it from another file and call `shout("learning python")`.

#### Exercise 5: Zip Detective
**Task**: Predict the output of this code, then run it to check:
```python
a = [1, 2, 3]
b = ["x", "y"]
print(dict(zip(a, b)))
```

### Exercise Answers

```python
# Exercise 1 Answer
def greet(*names, punctuation="!"):
    return "\n".join(f"Hello {name}{punctuation}" for name in names)

# Exercise 2 Answer
import random
def roll_dice(sides=6, times=1):
    return [random.randint(1, sides) for _ in range(times)]

# Exercise 3 Answer
def to_int(text):
    try:
        return int(text)
    except ValueError:
        return None
# to_int("42") -> 42, to_int("3.5") -> None, to_int("hello") -> None

# Exercise 4 Answer
# stringtools.py:
def shout(text):
    return text.upper() + "!!!"
# main file:
from stringtools import shout
print(shout("learning python"))  # LEARNING PYTHON!!!

# Exercise 5 Answer: {'1': 'x', '2': 'y'}
# zip stops at the SHORTER list, so the 3 in `a` is dropped.
# dict() pairs each key with its value — keys become strings "1" and "2".
```

---

## 🐧 Debian: Services, systemd & Networking Basics

### Core Concepts
Last week you navigated files, packages, and permissions. This week we look at what makes a Debian machine a *server* (or a well-behaved desktop): **services** managed by `systemd`, and the basics of **networking**. Almost everything running in the background on Linux — web servers, SSH, timers — is a systemd service.

**Why this matters:**
- **systemd** is the engine that starts, stops, and supervises every service on boot
- **SSH** is how you'll connect to any remote Linux machine in your career
- Understanding **logs with journalctl** is the #1 debugging skill on any Linux system

### E-Learning Knowledge - Week 2: Services & Networking

#### 1. systemd: Managing Services
```bash
# Check the status of a service (e.g. the SSH server)
systemctl status ssh

# Start, stop, restart a service
sudo systemctl start ssh
sudo systemctl stop ssh
sudo systemctl restart ssh

# Enable = start automatically at boot; disable = don't
sudo systemctl enable ssh
sudo systemctl disable ssh

# List all services and whether they're running
systemctl list-units --type=service

# See only the failing ones (super useful!)
systemctl --failed
```

#### 2. journalctl: Reading Logs Like a Pro
```bash
# All logs from one service
journalctl -u ssh

# Follow logs live (like tail -f, but for everything)
journalctl -f

# Logs since the last boot
journalctl -b

# Filter by time
journalctl --since "1 hour ago"
journalctl --since "2026-09-13" --until "2026-09-14"

# Show only errors and worse
journalctl -p err -b
```

#### 3. Networking Fundamentals
```bash
# Your IP addresses
ip a                 # all interfaces
ip route             # routing table (default gateway lives here)

# Test connectivity
ping -c 4 debian.org # 4 packets, then stop

# DNS lookup
resolvectl query debian.org

# See which ports are listening (what your machine exposes)
ss -tlnp
# t=tcp, l=listening, n=numeric ports, p=processes

# Download a file from the web
curl -O https://example.com/index.html
wget https://example.com/index.html
```

#### 4. SSH: Your Remote Superpower
```bash
# Connect to a remote machine (asks for that machine's password)
ssh user@192.168.1.50

# Generate your own key pair (accept the defaults, add a passphrase)
ssh-keygen -t ed25519

# Copy your public key to a server → passwordless login afterwards
ssh-copy-id user@192.168.1.50

# Run a single command remotely without an interactive session
ssh user@192.168.1.50 "uptime"

# Copy files to/from a remote machine
scp myfile.txt user@192.168.1.50:~/
scp user@192.168.1.50:~/results.txt ./
```

#### 5. Cron: Scheduling Tasks
```bash
# Edit your personal schedule
crontab -e

# Format: minute hour day-of-month month day-of-week command
# Examples:
# 30 8 * * *     /home/me/backup.sh      → every day at 08:30
# 0 */6 * * *    /home/me/sync.sh        → every 6 hours
# 15 2 * * 1     /home/me/report.sh      → Mondays at 02:15

# List your scheduled jobs
crontab -l
```

### Quick Exercises

#### Exercise 1: Service Status Report
**Task**: Run `systemctl list-units --type=service --state=running | head -15` and write down three services you recognize. Then check `systemctl --failed` — ideally it says "0 loaded units listed".

#### Exercise 2: Log Detective
**Task**: Run `journalctl -p err -b --no-pager | tail -20`. Pick one error line and try to understand it: which program produced it, and what is it complaining about?

#### Exercise 3: Port Scan Your Own Machine
**Task**: Run `ss -tlnp`. List every listening port and which process owns it. Is anything listening that surprises you?

#### Exercise 4: Schedule a Hello
**Task**: Add a cron job with `crontab -e`:
```
* * * * * date >> /tmp/cron_hello.txt
```
Wait 2 minutes, then check `cat /tmp/cron_hello.txt`. Remove the job afterwards (it runs every minute!).

#### Exercise 5: Local SSH Loop
**Task**: If SSH server is installed, connect to your own machine: `ssh localhost`. If it fails, read the error — is the service stopped? Start it with `sudo systemctl start ssh` and try again.

### Exercise Answers

```bash
# Exercise 1 Answer — example of what you might find:
# ssh          → remote login server
# cron         → scheduled task runner
# NetworkManager → manages your network connections
# If --failed shows units, investigate with: systemctl status <name>

# Exercise 2 Answer — how to read a log line:
# "Sep 13 08:31:02 myhost kernel: usb 1-2: unable to enumerate USB device"
# → produced by the kernel, about a USB device that failed to initialize.
# Not every error is urgent — context matters.

# Exercise 3 Answer — typical output on a fresh Debian:
# :22   sshd        (SSH server)
# :631  cupsd       (printing, if enabled)
# :25   (often NOT listening — good, mail should be off)
# Anything listening on 0.0.0.0 is reachable from your network.

# Exercise 4 Answer — verification:
# cat /tmp/cron_hello.txt   → one timestamp line per minute
# crontab -e → delete the line to stop it
# This proves cron works; it's the foundation of all Linux automation.

# Exercise 5 Answer — the debugging loop:
# ssh localhost → "Connection refused" means sshd isn't running
# sudo systemctl start ssh → then ssh localhost succeeds
# exit → leave the SSH session
```

---

## ❄️ NixOS: Home Manager & Dev Shells

### Core Concepts
Last week you edited `configuration.nix` and rebuilt. This week we explore two of Nix's most-loved features: **Home Manager** (declarative user-level config — dotfiles included!) and **dev shells** (a per-project, throwaway environment with exactly the tools that project needs).

**Why this matters:**
- **Home Manager** turns your `.bashrc`, `.gitconfig`, and editor config into versioned, reproducible code
- **Dev shells** mean "it works on my machine" becomes "it works on *every* machine" — just `nix-shell` and go
- Both work even on non-NixOS systems (Debian + Nix is a popular combo!)

### E-Learning Knowledge - Week 2: Reproducible Environments

#### 1. Dev Shells: Instant, Throwaway Toolchains
```bash
# Enter a shell with Python 3 — nothing else changes on your system.
nix-shell -p python3

# Inside, check it:
python3 --version
exit  # leave — the package vanishes from your PATH (but is cached).

# Multiple packages at once:
nix-shell -p python3 nodejs go

# Pin a specific version:
nix-shell -p python311

# The real magic: a shell.nix per project.
```

```nix
# --- Save as shell.nix in your project folder ---
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.requests
    git
  ];

  shellHook = ''
    echo "🛠️  Dev environment ready: Python + requests + git"
  '';
}
```
```bash
# Now any machine with Nix gets the identical environment:
nix-shell
```

#### 2. Home Manager: Your Dotfiles as Code
```nix
# --- ~/.config/home-manager/home.nix (simplified) ---
{ config, pkgs, ... }:

{
  home.username = "misterpaper";
  home.homeDirectory = "/home/misterpaper";
  home.stateVersion = "24.05";

  # User-level packages (no sudo needed to manage these!)
  home.packages = with pkgs; [
    htop
    tree
  ];

  # Declarative programs — Nix WRITES these config files for you.
  programs.git = {
    enable = true;
    userName = "Mister paper";
    userEmail = "mister@example.com";
  };

  programs.bash = {
    enable = true;
    shellAliases = {
      ll = "ls -la";
      update = "sudo nixos-rebuild switch";
    };
  };

  # Let Home Manager manage itself
  programs.home-manager.enable = true;
}
```
```bash
# Apply your user configuration:
home-manager switch
# Your git config and bash aliases now exist — reproducibly.
```

#### 3. Generations & Rollbacks, Part 2
```bash
# User-level generations (Home Manager keeps its own history):
home-manager generations

# Roll back your HOME environment:
home-manager switch --rollback

# System generations with boot entries — pick one at the GRUB menu!
# Every nixos-rebuild switch creates a boot entry; old ones stay available.

# Clean up old generations (keep the last 5):
sudo nix-collect-garbage --delete-older-than 5d
```

#### 4. Reading Nix Expressions
Nix is a small functional language. The essentials:
```nix
# Values
let
  name = "misterpaper";      # string
  age = 30;                  # integer
  hobbies = [ "sailing" "coding" ];  # list
in
{
  # Attribute set — like a dict/struct. THE core NixOS structure.
  user = {
    inherit name age;        # shorthand for name = name; age = age;
    hobbies = hobbies;
  };

  # String interpolation:
  greeting = "Hello, ${name}!";   # → "Hello, misterpaper!"
}
```
Key vocabulary you'll see everywhere:
- **`with pkgs;`** — "bring all of pkgs into scope" so you can write `git` instead of `pkgs.git`
- **`mkOverride` / `mkForce`** — resolve conflicting option values
- **`//`** — merge two attribute sets: `{ a = 1; } // { b = 2; }`

### Quick Exercises

#### Exercise 1: Project Shell
**Task**: Create a folder `myproject/` with a `shell.nix` providing `python3` and `git`. Run `nix-shell` inside it, verify with `git --version`, then exit.

#### Exercise 2: Alias Factory
**Task**: Add a Home Manager (or configuration.nix) bash alias `sysinfo` that runs `df -h && free -h`. Rebuild, open a new shell, and test it.

#### Exercise 3: Rollback Drill
**Task**: Add a harmless package (e.g. `cowsay`) via Home Manager, run `home-manager switch`, verify `cowsay hello` works — then roll back and confirm it's gone.

#### Exercise 4: Nix Grammar Check
**Task**: What does this evaluate to? Answer before testing with `nix eval`:
```nix
let a = 5; b = 10; in { sum = a + b; label = "a+b=${toString (a + b)}"; }
```

#### Exercise 5: Garbage Audit
**Task**: Run `du -sh /nix/store` to see how much space Nix uses, then `nix-collect-garbage -d` and measure again. Report the difference.

### Exercise Answers

```nix
// Exercise 1 Answer
// myproject/shell.nix:
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [ python3 git ];
}
// Run: nix-shell → git --version works → exit

// Exercise 2 Answer
programs.bash.shellAliases = {
  sysinfo = "df -h && free -h";
};
// Then: sudo nixos-rebuild switch (or home-manager switch) → new shell → sysinfo

// Exercise 3 Answer
// 1. home.packages = with pkgs; [ cowsay ]; → home-manager switch
// 2. cowsay hello → works ✅
// 3. home-manager switch --rollback → cowsay: command not found ✅
// That's atomic, reversible package management in action.

// Exercise 4 Answer:
// { sum = 15; label = "a+b=15"; }
// toString converts the number so it can be embedded in the string.

// Exercise 5 Answer — you'll typically reclaim hundreds of MB to several GB
// after the first weeks of experimenting. The store only grows from builds;
// garbage collection removes paths no current generation references.
```

---

## 🎯 Issue 2 Wrap-Up

### What You Can Do Now (vs. Issue 1)
| Area | Issue 1 | Issue 2 (now) |
|---|---|---|
| Rust | Variables, functions, loops | Ownership, borrowing, structs, enums |
| Python | Variables, lists, dicts, basic functions | *args/**kwargs, modules, exceptions |
| Debian | Files, APT, permissions | systemd, journalctl, SSH, cron |
| NixOS | configuration.nix basics | Dev shells, Home Manager, Nix language basics |

### Practice Tips
1. **Break things on purpose**: write code the borrow checker rejects, then fix it — that's how ownership sticks
2. **One shell.nix per project**: start today; future-you will thank you
3. **Read one log line per day**: journalctl fluency compounds fast
4. **Rollback drills**: practice rollbacks *before* you need them in an emergency

### Coming in Issue 3
- **Rust**: Collections (Vec, HashMap) and error handling with `Result`
- **Python**: Classes and object-oriented programming
- **Debian**: Firewalls, users & groups, and hardening basics
- **NixOS**: Flakes — the modern, fully-pinned way to manage Nix projects

---

**Happy Learning! 📚💻**

*Ownership feels strange for about a week, then it feels like a superpower. Keep going — every compile error is the compiler protecting you, not fighting you.*