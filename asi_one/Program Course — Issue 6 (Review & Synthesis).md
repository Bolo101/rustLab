# Issue 6: Review & Synthesis — Cycle 2 Recap

**Cycle 2 · Week C.** Three issues, four tools, one level up from Cycle 1: Python collections & files + NixOS services & flakes (Issue 4), Rust collections & error handling + Debian users, cron & hardening (Issue 5). Today: flashcards to test recall, mixed cross-tool exercises, and the updated bridges table. No new syntax — just consolidation. The harder material from Issues 4–5 deserves a second pass.

---

## Progress

| Week | Topics | Status |
|---|---|---|
| Issue 4 (Week A) | Python collections/files + NixOS services/flakes | ✅ Done |
| Issue 5 (Week B) | Rust collections/Result + Debian users/cron/hardening | ✅ Done |
| **Issue 6 (Week C)** | **Review & Synthesis (Cycle 2 recap)** | 📍 You are here |
| Issue 7 (Week A, Cycle 3) | Python classes & modules + NixOS networking & secrets | Next cycle |

---

# Part 1 — Flashcards (12 Q&A)

Cover the answer, answer out loud, then check. Target: 9/12 before moving on.

**Card 1.** Python: what does `counts[word] = counts.get(word, 0) + 1` do, and why not just `counts[word] += 1`?

<details><summary>Answer</summary>

It's the counting pattern: `get(word, 0)` returns the current count or 0 if the key doesn't exist yet, so the first occurrence works. `counts[word] += 1` raises `KeyError` on a missing key.

</details>

**Card 2.** NixOS: what does `services.openssh.settings.PasswordAuthentication = false;` in `configuration.nix` actually produce?

<details><summary>Answer</summary>

The NixOS sshd module generates the corresponding `sshd_config` directive, sets up the systemd unit, and activates it on `nixos-rebuild switch`. You never edit the generated config by hand — the option is the source of truth.

</details>

**Card 3.** Rust: what is the type and meaning of `v.get(5)` on a `Vec<i32>`?

<details><summary>Answer</summary>

`Option<&i32>` — either `Some(&value)` or `None`. Unlike indexing `v[5]` (which panics on out-of-bounds), `get` makes the "might not exist" case part of the type.

</details>

**Card 4.** Debian: why is `usermod -aG sudo alice` written with `-a`?

<details><summary>Answer</summary>

`-a` (append) preserves alice's existing groups. Without it, `-G` *replaces* her entire group list with just `sudo` — a classic footgun that silently strips memberships.

</details>

**Card 5.** Python: why iterate over a file object (`for line in f`) instead of `f.read()`?

<details><summary>Answer</summary>

Iterating reads line by line — constant memory. `f.read()` loads the entire file into RAM, which fails on large logs (a 10 GB file becomes a 10 GB string).

</details>

**Card 6.** NixOS: what does `Persistent = true` on a `systemd.timers.*` do?

<details><summary>Answer</summary>

If the machine was off or asleep when the timer should have fired, the missed run executes at the next boot/wake. Without it, missed runs are simply skipped.

</details>

**Card 7.** Rust: what does `?` do in `let n: i32 = s.parse()?;`?

<details><summary>Answer</summary>

If the expression is `Ok(v)`, unwrap to `v` and continue. If it's `Err(e)`, return early from the function with `Err(e)` — propagating the error upward. The function must return a compatible `Result`.

</details>

**Card 8.** Debian: what does the crontab line `>> /var/log/backup.log 2>&1` accomplish?

<details><summary>Answer</summary>

Appends stdout to the log file, and `2>&1` redirects stderr into the same stream. Without it, cron discards output and failures become invisible.

</details>

**Card 9.** NixOS: what two files make a system reproducible, and what does each contain?

<details><summary>Answer</summary>

`flake.nix` (declares inputs and how to build the system) and `flake.lock` (pins every input to an exact revision with a hash). Rebuilds with `--flake .` use the locked versions, so any machine at any time produces the same system.

</details>

**Card 10.** Rust: in the counting pattern `*counts.entry(word).or_insert(0) += 1;`, why the `*`?

<details><summary>Answer</summary>

`entry().or_insert(0)` returns a mutable reference (`&mut V`) to the value. You must dereference with `*` to modify the pointed-to value, not the reference itself.

</details>

**Card 11.** Debian: what's the first command to run when assessing a machine's network exposure, and what do you look for?

<details><summary>Answer</summary>

`ss -tlnp` — list all listening TCP ports with their owning processes. Anything listening on `0.0.0.0` that you can't identify or don't need is a candidate to stop or block with `ufw`.

</details>

**Card 12.** Python vs Rust: how does each express "read a file, or handle its absence"?

<details><summary>Answer</summary>

Python: runtime exceptions — `with open(...) as f:` inside a `try/except FileNotFoundError`. Rust: compile-time values — `fs::read_to_string(path)?` returns `Result<String, io::Error>`, and the function signature advertises the possibility of failure. Both work; Rust's version is checked before the program ever runs.

</details>

---

# Part 2 — Mixed Cross-Tool Exercises

Two tools cooperating per exercise. Budget: 10–15 minutes each.

**Ex 1 — Python analytics, served by NixOS.** Take a word-frequency style script and make it a nightly NixOS timer that appends its top-3 output to a log file.

<details><summary>Answer</summary>

```nix
systemd.services.wordfreq = {
  serviceConfig = {
    Type = "oneshot";
    ExecStart = "${pkgs.python3}/bin/python3 /home/mister/wordfreq.py /home/mister/notes.txt";
    StandardOutput = "append:/home/mister/wordfreq.log";
  };
};
systemd.timers.wordfreq = {
  wantedBy = [ "timers.target" ];
  timerConfig = { OnCalendar = "*-*-* 03:00:00"; Persistent = true; };
};
```

```bash
sudo nixos-rebuild switch
systemctl list-timers wordfreq.timer
journalctl -u wordfreq -e      # last run's output
```
The Nix `${pkgs.python3}` interpolation pins the interpreter path — the service can't break because PATH changed.

</details>

**Ex 2 — Rust log analyzer on Debian.** Write a tiny Rust program that counts failed SSH logins per source IP from `lastb`-style input piped to stdin (simplification: each line's third field is the IP), then run it against real `lastb` output.

<details><summary>Answer</summary>

```rust
use std::collections::HashMap;
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut counts: HashMap<String, usize> = HashMap::new();
    for line in stdin.lock().lines() {
        let line = line.unwrap();
        let fields: Vec<&str> = line.split_whitespace().collect();
        if fields.len() >= 3 {
            *counts.entry(fields[2].to_string()).or_insert(0) += 1;
        }
    }
    let mut v: Vec<_> = counts.into_iter().collect();
    v.sort_by(|a, b| b.1.cmp(&a.1));
    for (ip, n) in v.iter().take(3) {
        println!("{n:5}  {ip}");
    }
}
```

```bash
cargo build --release
sudo lastb | ./target/release/release/logcount
```
Rust (collections, stdin iteration) + Debian (`lastb`) — the shell-pipeline equivalent of Issue 5's awk one-liner.

</details>

**Ex 3 — Hardening audit, two systems.** On Debian, run `ss -tlnp` and `sudo ufw status`. Then on NixOS, name the declarative equivalent of "open port 22": which option exposes a port, and why does the NixOS version survive a reinstall?

<details><summary>Answer</summary>

Debian: `ss -tlnp` shows listeners; `ufw status` shows rules — both are *runtime* state you must recreate by hand on a new box.
NixOS: `networking.firewall.allowedTCPPorts = [ 22 ];` in `configuration.nix`. It survives reinstall because it lives in the config file, and every rebuild regenerates the firewall rules from it — declarative vs imperative, in one concrete example.

</details>

**Ex 4 — Error handling Rosetta.** The same task three ways: read `notes.txt` and print its line count. Write the Python version (`try/except`) and the Rust version (`Result` + `?`), then state in one sentence where the difference actually shows up.

<details><summary>Answer</summary>

```python
try:
    with open("notes.txt") as f:
        print(len(f.readlines()))
except FileNotFoundError:
    print("file missing")
```

```rust
use std::fs;

fn line_count(path: &str) -> Result<usize, std::io::Error> {
    let c = fs::read_to_string(path)?;
    Ok(c.lines().count())
}

fn main() {
    match line_count("notes.txt") {
        Ok(n) => println!("{n} lines"),
        Err(e) => println!("error: {e}"),
    }
}
```

Difference: in Rust the possibility of failure is in the *function signature* and checked before running; in Python it only appears at runtime.

</details>

**Ex 5 — Cron vs Nix timer, measured.** Schedule the same trivial job (`date >> ~/tick.txt`) twice: once with cron on Debian, once with a systemd timer on NixOS. Then get each one's last run: `cat ~/tick.txt` vs `journalctl -u tick -e`. Which told you more, and how much setup did each take?

<details><summary>Answer</summary>

Cron: one line in `crontab -e` — instant, but `~/tick.txt` is your only evidence; no built-in logging, no metadata.
NixOS timer: ~10 lines of Nix + rebuild, but `journalctl -u tick -e` gives timestamps, exit codes, and full output — and `Persistent=true` catches missed runs. Trade-off confirmed in practice: cron is zero-setup and universal; timers cost config but give observability for free.

</details>

---

# Part 3 — Bridges: Updated Mental Model

| Concern | Python | Rust | Debian | NixOS |
|---|---|---|---|---|
| **Handle "missing"** | `dict.get(k, d)`, `try/except FileNotFoundError` | `Option` / `Result`, `?` propagates | `apt remove` vs `purge` (state leftovers) | generations make "missing" reversible (`--rollback`) |
| **Collections / aggregation** | dicts, sets, comprehensions | `Vec`, `HashMap`, iterator chains | `sort \| uniq -c \| sort -rn` pipeline | — |
| **Schedule work** | — | — | cron (5 fields, manual logs) | `systemd.timers.*` (journalctl logs, `Persistent`) |
| **Expose a port** | — | — | install + start service, `ufw allow` | `networking.firewall.allowedTCPPorts` + service option, one file |
| **Trust boundary** | — | compiler checks types & error handling | users, groups, sudo policy, ufw, fail2ban | config file IS the boundary — regenerate it anywhere |

**The two axes, one level deeper:** Cycle 1 framed dynamic-vs-static and imperative-vs-declarative. Cycle 2 sharpened both: Rust's `Result` shows static typing extending to *error handling*, not just types; NixOS flakes show declarative extending to *version pinning and reproducibility*, not just packages. Error handling and reproducibility are the same idea in different clothes: push uncertainty to a place where it's checked — compile time or a lock file — instead of a place where it's discovered.

---

# Cycle 2 Complete 🎓

You can now: count, aggregate, and transform data in Python and Rust; read and write files safely in both languages; schedule work on both Debian and NixOS; declare services and firewalls so they survive reinstalls; and harden a box against the automated internet. That's a genuine mid-level toolbelt.

**Next issue — Issue 7 (Cycle 3, Week A):** Python classes, modules & virtual environments (structuring real projects, `pip` + `requirements.txt`) + NixOS networking, users & secrets management (declarative networking, `sops-nix`-style secret handling, multi-machine configs). See you next Monday! 🚀
