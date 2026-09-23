# 🚀 Tech Learning Newsletter - Issue 3
### Getting Solid: Rust, Python, Debian & NixOS
*Issue 3 — collections, classes, hardening, and flakes. This week is firmly intermediate.*

---

## 🦀 Rust: Collections, Result & Error Handling

### Core Concepts
You now own the ownership model. This week we put it to work with Rust's two workhorse collections — `Vec` and `HashMap` — and tackle **`Result`**, Rust's way of handling errors. In Rust, errors aren't exceptions: they're *values* the compiler forces you to deal with.

**Why this matters:**
- **`Vec<T>`** is a growable list — the collection you'll use most
- **`HashMap<K, V>`** is a key-value store — lookups by key, fast
- **`Result<T, E>`** makes failure explicit: functions that can fail return a value you *must* handle
- Mastering these three is the bridge from "I know Rust syntax" to "I can write real Rust programs"

### E-Learning Knowledge - Week 3: Collections & Errors

#### 1. Vec: The Growable List
```rust
fn main() {
    // Creating vectors
    let mut numbers: Vec<i32> = Vec::new();
    numbers.push(10);
    numbers.push(20);
    numbers.push(30);

    let pre_filled = vec![1, 2, 3]; // macro shorthand

    // Accessing elements — two ways, two philosophies:
    let third = &numbers[2];        // panics (crashes) if out of bounds
    println!("third = {}", third);

    match numbers.get(5) {          // returns Option: None instead of crashing
        Some(value) => println!("found {}", value),
        None => println!("no element at index 5"),
    }

    // Iterating
    for n in &numbers {             // borrow: read each element
        println!("{}", n);
    }

    for n in &mut numbers {         // mutable borrow: modify each element
        *n *= 2;                    // double every value
    }
    println!("{:?}", numbers);      // [20, 40, 60]

    // Common operations
    println!("len = {}", numbers.len());
    println!("contains 40? {}", numbers.contains(&40));
    let last = numbers.pop();       // removes & returns the last (an Option)
    println!("popped {:?}", last);

    // Strings are kind of Vec<u8> under the hood — same ownership ideas apply.
    let mut s = String::from("ab");
    s.push('c');
    s.push_str("def");
    println!("{}", s);              // abcdef
}
```

#### 2. HashMap: Key-Value Power
```rust
use std::collections::HashMap;

fn main() {
    let mut scores: HashMap<String, i32> = HashMap::new();

    // Insert
    scores.insert(String::from("Alice"), 95);
    scores.insert(String::from("Bo"), 87);

    // Access — get returns an Option<&V>
    if let Some(score) = scores.get("Alice") {
        println!("Alice: {}", score);
    }

    // entry(): insert only if absent — a classic pattern
    scores.entry(String::from("Cy")).or_insert(72);
    scores.entry(String::from("Alice")).or_insert(0); // Alice keeps 95

    // Update based on the old value
    if let Some(score) = scores.get_mut("Bo") {
        *score += 5; // Bo: 92
    }

    // Counting word occurrences — THE HashMap exercise
    let text = "the quick the lazy the dog";
    let mut counts: HashMap<&str, i32> = HashMap::new();
    for word in text.split_whitespace() {
        *counts.entry(word).or_insert(0) += 1;
    }
    println!("{:?}", counts); // {"the": 3, "quick": 1, "lazy": 1, "dog": 1}

    // Iterating
    for (name, score) in &scores {
        println!("{} -> {}", name, score);
    }
}
```

#### 3. Result: Errors as Values
```rust
// A function that can FAIL returns Result<T, E>.
// Ok(value) = success, Err(reason) = failure.
fn parse_age(text: &str) -> Result<u32, String> {
    match text.trim().parse::<u32>() {
        Ok(age) if age <= 130 => Ok(age),
        Ok(_) => Err(String::from("unrealistic age")),
        Err(_) => Err(format!("'{}' is not a number", text)),
    }
}

fn main() {
    // Handling with match — the explicit way:
    match parse_age("42") {
        Ok(age) => println!("Age is {}", age),
        Err(e) => println!("Error: {}", e),
    }

    // Handling with if let — when you only care about success:
    if let Ok(age) = parse_age("30") {
        println!("Valid age: {}", age);
    }

    // unwrap() = "crash on error" — fine for quick tests, avoid in real code:
    let age = parse_age("25").unwrap();

    // expect() = unwrap with a custom panic message:
    let _ = parse_age("60").expect("age should parse in tests");

    // unwrap_or(default) — provide a fallback:
    let age = parse_age("abc").unwrap_or(0);
    println!("fallback age: {}", age);

    // The ? operator — propagate errors upward, the idiomatic way:
    match try_example() {
        Ok(v) => println!("got {}", v),
        Err(e) => println!("stopped early: {}", e),
    }
}

// '?' instantly returns the Err from this function if parse_age fails.
fn try_example() -> Result<u32, String> {
    let age = parse_age("40")?;   // if Err, return it NOW; if Ok, unwrap it
    let doubled = parse_age(&age.to_string())?;
    Ok(doubled * 2)
}
```

#### 4. Option vs Result — Know the Difference
```rust
// Option<T> = a value that might be ABSENT (no error reason).
//   Use for: .get() on a Vec/HashMap, .pop(), .first()
// Result<T, E> = an operation that might FAIL (with an explanation).
//   Use for: parsing, file I/O, network calls

fn first_char(s: &str) -> Option<char> {
    s.chars().next() // empty string → None
}

fn main() {
    println!("{:?}", first_char("hello")); // Some('h')
    println!("{:?}", first_char(""));      // None
}
```

### Quick Exercises

#### Exercise 1: Vec Statistics
**Task**: Write a function `stats(v: &Vec<i32>) -> Option<(i32, i32)>` returning `(max, min)` as a tuple, or `None` if the vec is empty. Don't crash on an empty input!

#### Exercise 2: Phone Book
**Task**: Build a `HashMap<String, String>` mapping names to phone numbers. Insert two entries, look up one with `.get()`, and print a "not found" message for a missing name.

#### Exercise 3: Safe Parser
**Task**: Write `parse_even(text: &str) -> Result<i32, String>` that parses the text as a number *and* errors with a message if the number is odd.

#### Exercise 4: Word Frequency
**Task**: Use the `entry().or_insert()` pattern to count character frequencies in the string `"mississippi"` and print the map.

#### Exercise 5: The ? Chain
**Task**: Write `double_parsed(text: &str) -> Result<i32, String>` that parses an integer and returns it doubled, using the `?` operator (not `unwrap`). Then explain in one sentence what `?` did.

### Exercise Answers

```rust
// Exercise 1 Answer
fn stats(v: &Vec<i32>) -> Option<(i32, i32)> {
    if v.is_empty() {
        return None;
    }
    let max = *v.iter().max().unwrap();
    let min = *v.iter().min().unwrap();
    Some((max, min))
}
// stats(&vec![3, 9, 1]) -> Some((9, 1)); stats(&vec![]) -> None

// Exercise 2 Answer
use std::collections::HashMap;
fn main() {
    let mut phone_book: HashMap<String, String> = HashMap::new();
    phone_book.insert("Alice".to_string(), "555-0101".to_string());
    phone_book.insert("Bo".to_string(), "555-0202".to_string());

    match phone_book.get("Alice") {
        Some(number) => println!("Alice: {}", number),
        None => println!("not found"),
    }
    match phone_book.get("Cy") {
        Some(number) => println!("Cy: {}", number),
        None => println!("Cy: not found"), // this branch runs
    }
}

// Exercise 3 Answer
fn parse_even(text: &str) -> Result<i32, String> {
    let n: i32 = text.trim().parse().map_err(|_| "not a number".to_string())?;
    if n % 2 == 0 {
        Ok(n)
    } else {
        Err(format!("{} is odd", n))
    }
}

// Exercise 4 Answer
use std::collections::HashMap;
fn main() {
    let mut counts: HashMap<char, i32> = HashMap::new();
    for c in "mississippi".chars() {
        *counts.entry(c).or_insert(0) += 1;
    }
    println!("{:?}", counts);
    // {'m': 1, 'i': 4, 's': 4, 'p': 2}
}

// Exercise 5 Answer
fn double_parsed(text: &str) -> Result<i32, String> {
    let n = text.trim().parse::<i32>().map_err(|e| e.to_string())?;
    Ok(n * 2)
}
// '?' explanation: if the parse returns Err, `?` returns that Err from
// double_parsed immediately; if it returns Ok, `?` extracts the inner value
// and the function continues.
```

---

## 🐍 Python: Classes & Object-Oriented Programming

### Core Concepts
You can write functions, use modules, and handle exceptions. This week: **classes** — grouping data and the functions that operate on it into a single object. Almost every Python library you'll touch (requests, pandas, Django) is built from classes, so reading and writing them is essential.

**Why this matters:**
- **Classes** bundle state (attributes) and behavior (methods) together
- **`__init__`** and **`self`** are the two concepts that unlock reading any Python codebase
- **Dunder methods** (`__str__`, `__len__`, `__eq__`) let your objects behave like built-in types
- **Inheritance** lets you extend existing classes without rewriting them

### E-Learning Knowledge - Week 3: Object-Oriented Python

#### 1. Your First Class
```python
class Dog:
    # __init__ runs when you create an instance (the "constructor").
    # self = the instance being created. Always the first parameter.
    def __init__(self, name, age):
        self.name = name      # attribute: stored ON the instance
        self.age = age

    # A method — a function that belongs to the class.
    def bark(self):
        return f"{self.name} says WOOF!"

    def birthday(self):
        self.age += 1         # methods can modify the instance's attributes

# Creating instances:
rex = Dog("Rex", 3)
bella = Dog("Bella", 5)

print(rex.name)        # Rex
print(rex.bark())      # Rex says WOOF!
rex.birthday()
print(rex.age)         # 4
```

#### 2. Dunder (Magic) Methods
```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    # __str__: what print() shows — make it human-friendly.
    def __str__(self):
        return f"'{self.title}' ({self.pages} pages)"

    # __len__: enables len(book)
    def __len__(self):
        return self.pages

    # __eq__: enables book1 == book2
    def __eq__(self, other):
        return self.title == other.title and self.pages == other.pages

    # __add__: enables book1 + book2
    def __add__(self, other):
        return Book(f"{self.title} & {other.title}", self.pages + other.pages)

book1 = Book("Learning Python", 300)
book2 = Book("Learning Rust", 450)

print(book1)             # 'Learning Python' (300 pages)
print(len(book1))        # 300
print(book1 == Book("Learning Python", 300))  # True
print(book1 + book2)     # 'Learning Python & Learning Rust' (750 pages)
```

#### 3. Class vs Instance: Properties and Class Methods
```python
class BankAccount:
    interest_rate = 0.02   # CLASS attribute — shared by all accounts

    def __init__(self, owner, balance=0):
        self.owner = owner       # instance attributes — unique per account
        self._balance = balance  # single underscore = "internal, please"

    # @property: access a method like an attribute.
    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    # @classmethod: works on the class itself, gets cls instead of self.
    @classmethod
    def set_rate(cls, rate):
        cls.interest_rate = rate

acct = BankAccount("Mister paper", 100)
acct.deposit(50)
print(acct.balance)          # 150 — note: no parentheses, it's a property
# acct.deposit(-5)           # raises ValueError
BankAccount.set_rate(0.03)   # changes the rate for ALL accounts
```

#### 4. Inheritance: Building on What Exists
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("subclasses must implement speak")

class Cat(Animal):           # Cat inherits from Animal
    def speak(self):
        return f"{self.name}: meow"

class Duck(Animal):
    def speak(self):
        return f"{self.name}: quack"

# Polymorphism: same call, different behavior per class.
animals = [Cat("Felix"), Duck("Donald")]
for animal in animals:
    print(animal.speak())
# Felix: meow
# Donald: quack

# super(): call the parent's version — common in __init__.
class Kitten(Cat):
    def __init__(self, name):
        super().__init__(name)   # reuse Cat's setup
        self.cute = True
```

### Quick Exercises

#### Exercise 1: Temperature Class
**Task**: Create a `Temperature` class with a `celsius` attribute, a method `to_fahrenheit()` returning `(celsius * 9/5) + 32`, and a `__str__` that prints like `"25.0°C"`.

#### Exercise 2: Shopping Cart
**Task**: Create a `Cart` class where `__init__` starts an empty `items` list. Add `add(item)` and a `__len__` so `len(cart)` returns the item count.

#### Exercise 3: Rectangle OOP
**Task**: Recreate last Rust exercise in Python: a `Rectangle` class with `width`, `height`, an `area()` method, and an `__eq__` that considers two rectangles equal if their *areas* match (not their dimensions).

#### Exercise 4: Class Attribute Detective
**Task**: Predict the output before running:
```python
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1

a = Counter()
b = Counter()
c = Counter()
print(Counter.count)
print(a.count)
```

#### Exercise 5: Inherit & Extend
**Task**: Given the `Dog` class from the lesson, create a `Puppy(Dog)` subclass that overrides `bark()` to return a high-pitched `"yip!"` version, still using `self.name`.

### Exercise Answers

```python
# Exercise 1 Answer
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    def to_fahrenheit(self):
        return (self.celsius * 9/5) + 32
    def __str__(self):
        return f"{self.celsius}°C"

# Exercise 2 Answer
class Cart:
    def __init__(self):
        self.items = []
    def add(self, item):
        self.items.append(item)
    def __len__(self):
        return len(self.items)

# Exercise 3 Answer
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height
    def __eq__(self, other):
        return self.area() == other.area()
# Rectangle(2, 8) == Rectangle(4, 4) → True (both 16)

# Exercise 4 Answer: 3, then 3.
# `count` is a CLASS attribute shared by all instances. Each __init__ call
# increments the same Counter.count. a.count finds no instance attribute,
# so Python falls back to the class attribute — which is 3.

# Exercise 5 Answer
class Puppy(Dog):
    def bark(self):
        return f"{self.name} says yip! yip!"
```

---

## 🐧 Debian: Firewalls, Users & System Hardening

### Core Concepts
You can manage services and read logs. This week: protecting the machine. A Debian server on the internet is probed by bots within minutes of booting, so a **firewall**, sensible **user accounts**, and a few hardening habits are not optional — they're the baseline of professional Linux administration.

**Why this matters:**
- **UFW** (Uncomplicated Firewall) makes iptables usable by humans — default deny, allow only what's needed
- **Users, groups, and sudo** determine who can do what — the principle of least privilege
- **Automatic security updates** close vulnerabilities before you even read about them

### E-Learning Knowledge - Week 3: Hardening the Machine

#### 1. UFW: Firewall Basics
```bash
# Install the simple firewall frontend
sudo apt install ufw

# THE golden rule: set defaults BEFORE enabling, or you can lock yourself out!
sudo ufw default deny incoming    # block everything coming in...
sudo ufw default allow outgoing   # ...but let everything go out

# Allow ONLY the services you actually need:
sudo ufw allow ssh                # or: sudo ufw allow 22/tcp
sudo ufw allow 80,443/tcp         # web server ports

# Turn it on (safe now — SSH is allowed)
sudo ufw enable

# Check status with rule numbers (needed for deleting):
sudo ufw status verbose
sudo ufw status numbered

# Delete a rule by number:
sudo ufw delete 2

# Deny a specific address:
sudo ufw deny from 203.0.113.50
```

#### 2. Users, Groups & Least Privilege
```bash
# Create a user with a home directory
sudo adduser developer

# Groups: permissions travel with groups, not individuals
sudo groupadd webteam
sudo usermod -aG webteam developer   # -a = append, -G = groups
groups developer                     # verify membership

# File permissions for collaboration (review from Issue 1, now with purpose):
# 660 = owner+group read/write, others nothing — good for shared files
chmod 660 shared.txt
chown alice:webteam shared.txt

# sudo: grant admin rights ONLY to trusted accounts
sudo usermod -aG sudo developer
# Audit who has sudo:
grep 'sudo' /etc/group

# See who has logged in recently:
last | head -10
```

#### 3. SSH Hardening
```bash
# Edit the SSH server configuration:
sudo nano /etc/ssh/sshd_config

# The three changes worth making:
# PermitRootLogin no          ← bots hammer root@ constantly; disable it
# PasswordAuthentication no   ← keys only (after ssh-copy-id works!)
# Port 2222                   ← optional: move off the default port

# Apply the change:
sudo systemctl restart ssh

# BEFORE closing your current session, verify a new login still works!
# (Getting locked out of a remote server is a rite of passage — avoid it.)

# Watch live login attempts:
sudo journalctl -u ssh -f
```

#### 4. Automatic Security Updates & Audits
```bash
# Install unattended-upgrades (often preinstalled on Debian):
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades   # choose "yes"

# Verify it's active:
systemctl status unattended-upgrades
cat /etc/apt/apt.conf.d/20auto-upgrades

# Quick security audit checklist:
sudo ss -tlnp          # 1. What ports am I exposing? Fewer is better.
sudo ufw status        # 2. Is the firewall on?
last | head -10        # 3. Who has been logging in?
apt list --upgradable  # 4. Any pending updates?
```

### Quick Exercises

#### Exercise 1: Firewall Dry Run
**Task**: Install `ufw`, set both defaults (`deny incoming`, `allow outgoing`), allow SSH — but do **not** enable yet. Print `ufw status` and confirm it's inactive with your rules staged.

#### Exercise 2: User Lab
**Task**: Create a user `student`, create a group `classroom`, add `student` to it, and verify with `groups student`. Then delete the user cleanly: `sudo deluser --remove-home student`.

#### Exercise 3: Permission Puzzle
**Task**: Create a file `secret.txt`, then set permissions so ONLY the owner can read and write it (`chmod 600`). Verify with `ls -l` — the output should start with `-rw-------`.

#### Exercise 4: Exposure Audit
**Task**: Run `ss -tlnp` and list every listening port. For each, write whether you actually need it. Then run `apt list --upgradable` — how many updates are pending?

#### Exercise 5: SSH Log Reading
**Task**: Run `sudo journalctl -u ssh --since today --no-pager | tail -20`. Count how many login attempts (successful or failed) appear. On an internet-connected machine, you may be surprised.

### Exercise Answers

```bash
# Exercise 1 Answer — verification:
sudo ufw status
# Status: inactive
# (rules staged but not enforced — exactly what a dry run should show)

# Exercise 2 Answer — the full sequence:
sudo adduser student
sudo groupadd classroom
sudo usermod -aG classroom student
groups student        # student : student classroom
sudo deluser --remove-home student

# Exercise 3 Answer:
touch secret.txt
chmod 600 secret.txt
ls -l secret.txt      # -rw------- 1 you you 0 ... secret.txt

# Exercise 4 Answer — how to judge:
# :22 sshd       → needed (if you use SSH)
# :631 cupsd     → not needed on a server → sudo systemctl disable --now cups
# Pending updates count varies; anything listed as security should be
# applied promptly: sudo apt update && sudo apt upgrade

# Exercise 5 Answer — reading the log:
# Look for lines like "Failed password for root from x.x.x.x"
# or "Accepted publickey for user". Failed root attempts are automated
# bot noise — the reason PermitRootLogin no is step one of hardening.
```

---

## ❄️ NixOS: Flakes — Pinned, Modern, Reproducible

### Core Concepts
You know `configuration.nix`, dev shells, and Home Manager. This week: **flakes** — the modern Nix workflow that pins *exact* versions of everything in a lockfile, making your system and projects bit-for-bit reproducible on any machine, any date.

**Why this matters:**
- **`flake.lock`** pins the exact nixpkgs commit — "works today" becomes "works identically forever"
- **One flake** can define your whole system, dev shells for multiple projects, and packages
- Flakes are how modern Nix projects (and most of the Nix community) ship software

### E-Learning Knowledge - Week 3: The Flake Workflow

#### 1. Anatomy of a Flake
```nix
# --- flake.nix: every flake has this exact skeleton ---
{
  # Inputs: WHERE your dependencies come from (the "what").
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    home-manager = {
      url = "github:nix-community/home-manager/release-24.05";
      inputs.nixpkgs.follows = "nixpkgs";   # share ONE nixpkgs version
    };
  };

  # Outputs: WHAT you build from those inputs.
  outputs = { self, nixpkgs, home-manager, ... }: {
    # A complete system configuration, flake-style:
    nixosConfigurations.mynixos = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ./configuration.nix          # your existing config, reused!
        home-manager.nixosModules.home-manager
      ];
    };

    # A dev shell, flake-style:
    devShells.x86_64-linux.default =
      nixpkgs.legacyPackages.x86_64-linux.mkShell {
        buildInputs = with nixpkgs.legacyPackages.x86_64-linux; [ python3 git ];
      };
  };
}
```

#### 2. Flake Commands: The Daily Workflow
```bash
# Initialize a new flake in a project (creates flake.nix + flake.lock):
nix flake init
# Or from a template:
nix flake init -t templates#python

# Update the lockfile to newer (but still pinned!) versions:
nix flake update

# See what's pinned:
nix flake metadata
nix flake info

# Enter the project's pinned dev shell:
nix develop          # (instead of nix-shell)

# Build a flake's package or run its app:
nix build
nix run

# Rebuild your SYSTEM when configuration is flake-based:
sudo nixos-rebuild switch --flake .#mynixos
```

#### 3. Inside flake.lock
```bash
# Never edit flake.lock by hand — but DO learn to read it:
cat flake.lock | head -30

# Key things to notice:
# - "rev": the exact git commit of nixpkgs being used
# - "date": when that revision was captured
# - Every input has a hash — tamper-evident by design

# See which revision is pinned, in one line:
nix flake metadata | grep -E 'Revision|Last modified'
```

#### 4. Sharing Environments with `nix profile` (goodbye, global installs)
```bash
# Per-user declarative-ish package profiles:
nix profile install nixpkgs#htop
nix profile list          # what's in your profile
nix profile remove htop
nix profile upgrade       # update everything in the profile

# Run a package WITHOUT installing (like nix-shell, but direct):
nix run nixpkgs#cowsay -- hello
nix shell nixpkgs#python311   # drops you in a shell with it
```

### Quick Exercises

#### Exercise 1: First Flake
**Task**: In a fresh folder, run `nix flake init` and open `flake.nix`. Identify the two top-level sections (`inputs` and `outputs`) and say in one sentence what each is for.

#### Exercise 2: Locked Dev Shell
**Task**: Create a flake whose output is a dev shell with `python3` and `nodejs`. Verify `flake.lock` was created, then enter it with `nix develop` and check both tools' versions.

#### Exercise 3: Reproducibility Proof
**Task**: Run `nix flake metadata` in your project. Note the pinned nixpkgs revision. Now run `nix flake update` and observe the revision change (or stay the same if already current) — that's your lockfile at work.

#### Exercise 4: Run Without Install
**Task**: Use `nix run nixpkgs#cowsay -- "flakes rock"` to run a program you never installed. Then run `which cowsay` *outside* the nix run environment — confirm it's not installed anywhere.

#### Exercise 5: Lock Detective
**Task**: Open `flake.lock` and find the `"rev"` field for `nixpkgs`. Paste that commit hash into `github.com/NixOS/nixpkgs/commit/<hash>` in a browser — you're looking at the exact source your system builds from.

### Exercise Answers

```nix
// Exercise 1 Answer:
// inputs = what your flake depends on and from where (with versions).
// outputs = what your flake produces: systems, dev shells, packages, apps.

// Exercise 2 Answer
{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  outputs = { self, nixpkgs }: let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
      buildInputs = [ pkgs.python3 pkgs.nodejs ];
    };
  };
}
// nix develop → python3 --version && node --version

// Exercise 3 Answer:
// nix flake metadata shows "Revision: <hash>" and "Last modified: <date>".
// After `nix flake update` the revision moves to a newer commit — but it
// stays PINNED. Everyone using this lockfile gets the identical revision.

// Exercise 4 Answer:
// nix run nixpkgs#cowsay -- "flakes rock"   → the cow speaks
// which cowsay → returns nothing / not found
// nix run downloads, runs, and discards — your PATH stays clean.

// Exercise 5 Answer:
// The rev field is a 40-character git hash. Viewing it on GitHub shows the
// precise nixpkgs tree — the essence of bit-for-bit reproducibility.
```

---

## 🎯 Issue 3 Wrap-Up

### Your Progress So Far
| Area | Issue 1 | Issue 2 | Issue 3 (now) |
|---|---|---|---|
| Rust | Basics | Ownership, structs | Vec, HashMap, Result, `?` |
| Python | Basics | Functions, modules | Classes, OOP, dunders |
| Debian | Files, packages | Services, SSH | Firewall, users, hardening |
| NixOS | configuration.nix | Shells, Home Manager | Flakes, lockfiles, profiles |

### Practice Tips
1. **Refactor an old exercise**: take an Issue 1 exercise and rewrite it with structs/classes — feel the difference
2. **Harden something real**: put UFW on a machine (virtual machine counts!) and audit its ports
3. **Flake everything**: convert one `shell.nix` to a flake — commit both `flake.nix` and `flake.lock`
4. **Read library source**: open a small Python library on GitHub and find its classes — you can read them now

### Coming in Issue 4
- **Rust**: Traits and generics — Rust's answer to interfaces
- **Python**: Working with files, JSON, and the `pathlib` module
- **Debian**: Backups, disks, and `rsync` — don't lose your work
- **NixOS**: Overlays and building your own packages

---

**Happy Learning! 📚💻**

*You're past the steep part of the curve now. Rust's `?` operator, Python's `self`, UFW's default-deny, and one lockfile — these four ideas are doing a lot of work in the professional world. See you in Issue 4!*