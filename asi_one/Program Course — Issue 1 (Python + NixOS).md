# Program Course — Issue 1: Python + NixOS

**Cycle 1 · Week 1 · Restart from zero · Beginner → Intermediate**

> Full original format: for each technology — Core Concepts, step-by-step knowledge, and quick exercises with full answers. Cycle 1: Week 1 = Python + NixOS, Week 2 = Rust + Debian, Week 3 = Review.

---

## 🐍 Python — the first building blocks

*Variables and types, f-strings, conditions, loops, and functions: the foundation everything else rests on.*

### Core Concepts

Python is the reference language for automation, data science, and system scripting. Its strengths: readable syntax close to pseudocode, a giant ecosystem, and an interpreter that lets you test ideas instantly. In this series it becomes also the natural scripting tool for your NixOS and Debian machines — from parsing config files to automating package checks.

### E-Learning Knowledge

**Step 1 — Variables and types.** A variable is a name attached to an object; the type is inferred at runtime (dynamic typing). The four you'll use daily:

```python
age = 30            # int
price = 9.99        # float
name = "Alice"      # str
active = True       # bool (capital T!)
print(type(age))    # <class 'int'>
```

Useful conversions: `int("42")`, `float(3)`, `str(99)`. Golden rule: `input()` **always** returns a `str` — convert with `int(input())`, or `"5" + 1` crashes.

**Step 2 — Strings and f-strings.** An f-string embeds variables and expressions directly in text, with format specs:

```python
name = "Alice"; price = 9.5
print(f"{name} pays {price:.2f} €")   # .2f = exactly 2 decimals → 9.50
print(f"{name:>10}")                  # right-aligned in 10 chars
print(f"{2 + 3}")                     # any expression works → 5
```

**Step 3 — Conditions.** Indentation (4 spaces) *is* the structure of Python code — get it wrong and the program means something else:

```python
if age >= 18:
    print("adult")
elif age >= 13:
    print("teen")
else:
    print("child")
```

Comparisons `== != < > <= >=`, combined with `and`, `or`, `not`. Classic trap: `=` assigns, `==` compares.

**Step 4 — Loops.** `for` iterates over a sequence; `range(a, b)` yields integers from a to b-1 (exclusive end); `while` repeats while a condition holds; `break`/`continue` control the flow:

```python
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

n = 0
while n < 3:
    n += 1               # no n++ in Python
```

**Step 5 — Functions.** Define once, reuse everywhere. Parameters can have defaults; `return` sends a value back:

```python
def greet(name, punct="!"):        # default value
    return f"Hello, {name}{punct}"

print(greet("Alice"))              # Hello, Alice!
print(greet("Bob", punct="?"))     # Hello, Bob?
```

Run scripts with `python3 script.py`. Errors are your friends: read the last line of a traceback first — it names the problem.

> 💡 **Common beginner traps:** mixing tabs and spaces (pick 4 spaces, always), forgetting the colon `:` after `if`/`for`/`def`, and using `=` where `==` is meant. The interpreter flags all three precisely.

### Quick Exercises

**EX 1 —** Ask the user for their birth year, compute their age in 2030, and print it with an f-string.

<details><summary>Answer — EX 1</summary>

```python
year = int(input("Birth year: "))   # str → int conversion
print(f"In 2030 you'll be {2030 - year}")
```
</details>

**EX 2 —** Print the 7-times table from 7×1 to 7×10, formatted as `7 x 4 = 28`, one per line.

<details><summary>Answer — EX 2</summary>

```python
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")
```
</details>

**EX 3 —** Write `is_even(n)` that returns `True` or `False`, then test it on 4, 7, and 0.

<details><summary>Answer — EX 3</summary>

```python
def is_even(n):
    return n % 2 == 0        # % is the remainder

print(is_even(4), is_even(7), is_even(0))   # True False True
```
</details>

**EX 4 —** Keep asking for a password until the user types `nixos`, then print "Access granted".

<details><summary>Answer — EX 4</summary>

```python
while input("Password: ") != "nixos":
    print("Wrong, try again")
print("Access granted")
```
</details>

**EX 5 —** Write `temp(c)` converting Celsius to Fahrenheit (F = C × 9/5 + 32), with the result formatted to 1 decimal via f-string.

<details><summary>Answer — EX 5</summary>

```python
def temp(c):
    return c * 9 / 5 + 32

print(f"25°C = {temp(25):.1f}°F")   # 25°C = 77.0°F
```
</details>

---

## ❄️ NixOS — your system as code

*The declarative config file, rebuild, generations, the store, and finding packages.*

### Core Concepts

NixOS rebuilds the idea of a Linux distribution: instead of installing packages and editing config files scattered across `/etc`, you describe your **entire system in one file** — `/etc/nixos/configuration.nix` — and a single command makes reality match it. The payoff: a change that breaks something is always one command away from being undone, and the whole machine is reproducible on any other computer from that one file. It's version control for your operating system.

### E-Learning Knowledge

**Step 1 — The one file that matters.** Everything lives in `/etc/nixos/configuration.nix`, a Nix expression — attribute assignments between braces:

```nix
{ config, pkgs, ... }:

{
  # comments start with #
  time.timeZone = "Europe/Paris";
  users.users.alice = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];   # wheel = sudo rights
  };
}
```

Syntax essentials: `key = value;` (semicolon mandatory), lists in `[ ]`, nested sets in `{ }`, strings in double quotes, booleans lowercase `true`/`false`.

**Step 2 — The rebuild command.** One command applies the file:

```bash
sudo nano /etc/nixos/configuration.nix
sudo nixos-rebuild switch
```

`switch` builds the new system and activates it immediately. If you made a syntax error, the build fails *with the line number* and your running system is untouched — that's the safety net.

**Step 3 — Generations: undo as a feature.** Every successful rebuild creates a numbered *generation* — a complete bootable snapshot. Broke Wi-Fi with the last change?

```bash
sudo nixos-rebuild switch --rollback   # back to the previous generation, instantly
nixos-rebuild list-generations         # see the history
```

Old generations also appear in the boot menu, so you can boot into yesterday's system even if today's won't start.

**Step 4 — The /nix/store magic.** Every package lives in `/nix/store/<hash>-<name>-<version>`, e.g. `/nix/store/x2j9…-python3-3.11.9/`. The hash makes every version a unique path — different versions coexist without collision, nothing is ever overwritten in place, and "dependency hell" is structurally impossible. You rarely touch this directory; understanding *why* it never conflicts is what matters.

**Step 5 — Finding and adding packages.** Search at **search.nixos.org** (or `nix search nixpkgs firefox`), then declare them:

```nix
environment.systemPackages = with pkgs; [
  vim
  git
  firefox
  htop
];
```

Rebuild once, and all four are installed system-wide. Remove a line, rebuild — it's gone. Your package list is now readable, versionable text.

> 💡 **Bridge to next weeks:** on Debian (Week 2) you'll manage packages imperatively with `apt` — one command at a time, mutating live state. Same goal, opposite philosophy: mutation vs declaration.

### Quick Exercises

**EX 1 —** Open `configuration.nix`, find `time.timeZone`, and confirm it matches your timezone.

<details><summary>Answer — EX 1</summary>

```bash
grep timeZone /etc/nixos/configuration.nix
# expect: time.timeZone = "Europe/Paris";
```
</details>

**EX 2 —** Add `htop` to `environment.systemPackages`, rebuild, and verify it runs.

<details><summary>Answer — EX 2</summary>

```bash
sudo nano /etc/nixos/configuration.nix   # add htop to the list
sudo nixos-rebuild switch
htop                                     # press q to quit
```
</details>

**EX 3 —** List your system generations and note how many exist.

<details><summary>Answer — EX 3</summary>

```bash
nixos-rebuild list-generations
# or: ls -l /nix/var/nix/profiles/system-*-link
```
</details>

**EX 4 —** Introduce a deliberate syntax error (delete a semicolon), run the rebuild, and read the error message. What line does it point to? Then fix it.

<details><summary>Answer — EX 4</summary>

```bash
sudo nixos-rebuild switch
# error: syntax error, unexpected '}', expecting ';' at /etc/nixos/configuration.nix:23:5
```

The message names the file, line and column — and your running system was never at risk. Restore the semicolon and rebuild.
</details>

**EX 5 —** Look up `ripgrep` on search.nixos.org, add it, rebuild, then try `rg "timeZone" /etc/nixos/configuration.nix`.

<details><summary>Answer — EX 5</summary>

```nix
environment.systemPackages = with pkgs; [ ripgrep ];
```

```bash
sudo nixos-rebuild switch
rg timeZone /etc/nixos/configuration.nix
```

Congratulations — you just did the full NixOS loop: search → declare → rebuild → use.
</details>

---

## 📈 Series progress — Cycle 1 (restart)

| Week | Topics | Status |
|------|--------|--------|
| W1 | Python (variables, f-strings, conditions, loops, functions) + NixOS (config file, rebuild, generations, /nix/store, packages) | ● This issue |
| W2 | Rust (cargo, variables/mut, functions, control flow, ownership) + Debian (navigation, apt, permissions, systemd, sudo) | Next Monday |
| W3 | Review & Synthesis — flashcards, mixed exercises, bridges | Week after |

**Next issue (Week B):** Rust — install with rustup, immutable-by-default variables, functions, control flow, and your first taste of ownership — plus Debian — filesystem navigation, apt, permissions, and systemd services.

---
*Program Course · Issue 1 · Cycle 1 restart · Python + NixOS*