# Issue 3: Review & Synthesis — Cycle 1 Recap

**Cycle 1 · Week C.** Two weeks, four tools: Python + NixOS (Week A), Rust + Debian (Week B). Today is consolidation day: flashcards to test recall, mixed exercises that force the tools to work *together*, and the bridges that tie the whole picture into one mental model. No new syntax — just connections.

---

## Progress

| Week | Topics | Status |
|---|---|---|
| Issue 1 (Week A) | Python basics + NixOS config/generations | ✅ Done |
| Issue 2 (Week B) | Rust basics + Debian essentials | ✅ Done |
| **Issue 3 (Week C)** | **Review & Synthesis (Cycle 1 recap)** | 📍 You are here |
| Issue 4 (Week A, Cycle 2) | Python collections/files + NixOS services/flakes | Next cycle |

---

# Part 1 — Flashcards (12 Q&A)

Cover the answer, answer out loud, then check. Aim for 9/12 before moving on.

**Card 1.** In Python, what is an f-string and what does `f"n={n}"` do?

<details><summary>Answer</summary>

A formatted string literal: prefix the string with `f` and any `{expression}` inside is evaluated and inserted into the text. `f"n={n}"` substitutes the current value of `n`.

</details>

**Card 2.** What does `sudo nixos-rebuild switch` do, and how is it different from `sudo nixos-rebuild test`?

<details><summary>Answer</summary>

It evaluates `configuration.nix`, builds the declared system, and *switches* to it — also making it the boot default. `test` activates the new configuration in the running system but does NOT update the default boot entry.

</details>

**Card 3.** In Rust, what does the compiler say when you use a variable after its value was moved?

<details><summary>Answer</summary>

`borrow of moved value: 'x'` (error [E0382]). Each heap value has exactly one owner; the assignment handed ownership away, so the old name is no longer usable. Fix with `.clone()` if a copy is really needed.

</details>

**Card 4.** Difference between `apt update` and `apt upgrade`?

<details><summary>Answer</summary>

`apt update` refreshes the package *index* (metadata about available versions) — installs nothing. `apt upgrade` downloads and installs the newer versions of packages already installed.

</details>

**Card 5.** What is a NixOS generation and how do you roll back?

<details><summary>Answer</summary>

A complete, immutable snapshot of the system configuration produced by each rebuild. Roll back with `sudo nixos-rebuild switch --rollback` or by selecting the previous entry in the boot menu.

</details>

**Card 6.** What does `chmod 640` mean numerically?

<details><summary>Answer</summary>

6 = owner `rw-` (4+2), 4 = group `r--`, 0 = others `---`. Digits are octal sums: read=4, write=2, execute=1.

</details>

**Card 7.** In Rust, why does `a + b` as the last line of a function return a value, but `a + b;` return nothing?

<details><summary>Answer</summary>

The semicolon turns an expression into a statement, discarding its value. A function's implicit return is its last *expression*; a statement evaluates to `()` (unit).

</details>

**Card 8.** Where do unit files live in Debian, and which command shows the last 10 log lines of a service?

<details><summary>Answer</summary>

`/etc/systemd/system/` (admin-created) and `/lib/systemd/system/` (shipped by packages). Logs: `journalctl -u <service> -n 10`.

</details>

**Card 9.** NixOS: where do installed packages physically live, and why does that enable atomic upgrades?

<details><summary>Answer</summary>

In `/nix/store`, each package in a content-addressed path like `/nix/store/abc123...-htop-3.3.0`. New builds never touch old paths, so switching generations is a symlink change — atomic and reversible.

</details>

**Card 10.** Python: what's the difference between a list and a tuple?

<details><summary>Answer</summary>

A list (`[1, 2]`) is mutable — you can append, remove, reorder. A tuple (`(1, 2)`) is immutable — fixed at creation, hashable, usable as a dict key.

</details>

**Card 11.** Debian: what's the difference between `apt remove` and `apt purge`?

<details><summary>Answer</summary>

`remove` uninstalls the binaries but keeps config files under `/etc`; `purge` also deletes those config files.

</details>

**Card 12.** Rust: why is `let mut y = 10; y = "text";` an error while Python happily rebinds?

<details><summary>Answer</summary>

Rust is statically typed: `y`'s type (`i32`) is fixed at compile time and `mut` only permits changing the *value*, not the type. Python is dynamically typed — names just point to whatever object you bind them to.

</details>

---

# Part 2 — Mixed Cross-Tool Exercises

These require two tools cooperating. Budget: 10–15 minutes each.

**Ex 1 — Ship a Python script on Debian.** Write a Python script that prints the 5 largest files in `/var/log`, make it executable, and run it on Debian.

<details><summary>Answer</summary>

```python
# biggest.py
import os
logs = "/var/log"
files = []
for root, _, names in os.walk(logs):
    for n in names:
        p = os.path.join(root, n)
        try:
            files.append((os.path.getsize(p), p))
        except OSError:
            pass
for size, path in sorted(files, reverse=True)[:5]:
    print(f"{size:>12}  {path}")
```

```bash
chmod +x biggest.py        # Debian permission from Issue 2
./biggest.py               # run it
```
Python (Issue 1) + filesystem/permissions (Issue 2) working together.

</details>

**Ex 2 — Parse a journal log with Python.** Take `journalctl -u nginx` output (or any service) and count how many lines contain the word "error" (case-insensitive).

<details><summary>Answer</summary>

```bash
journalctl -u nginx --no-pager | python3 -c "
import sys
lines = sys.stdin.readlines()
errors = [l for l in lines if 'error' in l.lower()]
print(f'{len(errors)} error lines out of {len(lines)}')
for l in errors[:5]:
    print(l.strip())
"
```
`--no-pager` is essential when piping; `python3 -c` runs inline code.

</details>

**Ex 3 — Rust exercise runner on NixOS.** On a NixOS machine, you need `cargo` but it's not installed. What are your two declarative options, and which is lighter?

<details><summary>Answer</summary>

1) System-wide: add `pkgs.cargo` (or `pkgs.rustup`) to `environment.systemPackages` in `configuration.nix`, then `sudo nixos-rebuild switch`.
2) Ephemeral per-shell: `nix-shell -p cargo` (or `nix develop`) — no config change, disappears on exit. The ephemeral shell is lighter for one-off work; the config change is right for a permanent toolchain.

</details>

**Ex 4 — Permission audit script.** On Debian, write and run a one-liner (shell or Python) listing files under your home directory that are executable by *others* — a common security smell.

<details><summary>Answer</summary>

```bash
find ~ -type f -perm -o+x 2>/dev/null
```
Python version:

```bash
python3 -c "
import os, stat
for root, _, names in os.walk(os.path.expanduser('~')):
    for n in names:
        p = os.path.join(root, n)
        try:
            if os.stat(p).st_mode & stat.S_IXOTH:
                print(p)
        except OSError:
            pass
"
```
`S_IXOTH` = "execute by others" bit. Fix findings with `chmod o-x <file>`.

</details>

**Ex 5 — FizzBuzz, three ways.** You wrote FizzBuzz in Rust (Issue 2). Rewrite it in Python in under 5 minutes, then state one concrete difference you noticed between the two languages.

<details><summary>Answer</summary>

```python
for n in range(1, 16):
    out = "Fizz"*(n % 3 == 0) + "Buzz"*(n % 5 == 0)
    print(out or n)
```

Differences you might have noticed (any one is fine): Python has no mandatory types or `fn main`; `bool` is an `int` so `"Fizz"*(True)` works; Python is interpreted (`python file.py`) vs Rust's `cargo build` step; strings don't need a `String`/`&str` distinction in Python.

</details>

---

# Part 3 — Bridges: One Mental Model, Four Tools

| Concern | Python | Rust | Debian | NixOS |
|---|---|---|---|---|
| **Get software** | `pip install` (per-project, venv) | `cargo add` / crates.io | `apt install` (system-wide, curated) | declare in `configuration.nix` or `nix-shell -p` |
| **Declare deps** | `requirements.txt` | `Cargo.toml` | `debian/control` (for packaging) | `configuration.nix` / `flake.nix` |
| **Type checking** | runtime (duck typing) | compile time (enforced) | — | — |
| **Mutation of state** | variables rebinding freely | owner must say `mut` | system mutated in place | system never mutated — new generation |
| **Undo** | reassign | `clone()` / restructure | `apt purge` + manual fixes | `--rollback` (built in) |

**The big picture:** Debian and NixOS answer the same question ("what software runs on this machine?") with opposite philosophies — *imperative in-place* vs *declarative immutable*. Python and Rust answer "how do I express computation?" the same way: dynamic/runtime vs static/compile-time. Every tool you learned this cycle is one point on those two axes. Cycle 2 will go deeper along each.

---

# Cycle 1 Complete 🎓

You can now: write and run Python and Rust programs, manage packages on two philosophically opposite Linux systems, control services with systemd, reason about permissions and ownership (of files *and* of memory), and roll back a NixOS system like it's nothing.

**Next issue — Issue 4 (Cycle 2, Week A):** Python collections & file I/O (lists/dicts mastery, reading/writing files, error handling with `try/except`) + NixOS services & flakes (declaring a custom service, `flake.nix` and reproducible systems). See you Monday! 🚀
