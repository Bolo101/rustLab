# Issue 4: Python Collections & Files + NixOS Services & Flakes

**Cycle 2 · Week A.** Cycle 1 gave you the foundations; Cycle 2 makes you productive. On the Python side: the collection types professionals actually use all day (dicts, sets, comprehensions) plus real file I/O and error handling. On the NixOS side: the leap from "installing packages" to "declaring services," and reproducible systems with flakes. Nothing here repeats Issue 1 — that was variables, loops, functions, and one `configuration.nix` rebuild.

---

## Progress

| Week | Topics | Status |
|---|---|---|
| Issue 3 (Week C) | Review & Synthesis — Cycle 1 recap | ✅ Done |
| **Issue 4 (Week A, Cycle 2)** | **Python collections/files + NixOS services/flakes** | 📍 You are here |
| Issue 5 (Week B) | Rust collections, Result/error handling + Debian users, cron, security hardening | Up next |

---

# Part 1 — Python: Collections, Files & Errors

## Core Concepts

Real programs don't juggle a handful of variables — they manage *lots* of data: a thousand log lines, a config file, an address book. Python's collections (dict, set, tuple) and its file model exist for exactly that. Master them and you can write useful scripts: log analyzers, CSV processors, config generators. And because real data is messy (missing files, bad lines), `try/except` is not optional decoration — it's the difference between a script that dies at 3 AM and one that logs and continues.

## E-Learning Knowledge

### Step 1 — Dictionaries: the workhorse

A dict maps keys to values. Lookup is instant regardless of size.

```python
user = {"name": "Mister paper", "level": "beginner+", "langs": ["python"]}
print(user["name"])            # direct access — KeyError if missing
print(user.get("email"))       # None instead of crash when missing
print(user.get("email", "n/a"))# with a default

user["level"] = "intermediate" # add or overwrite
for key, value in user.items():   # iterate pairs
    print(f"{key}: {value}")

# counting pattern — the most useful dict trick there is
counts = {}
for word in "the cat and the hat".split():
    counts[word] = counts.get(word, 0) + 1
print(counts)   # {'the': 2, 'cat': 1, 'and': 1, 'hat': 1}
```

### Step 2 — Sets and comprehensions

```python
# set = unordered collection of UNIQUE items, fast membership tests
seen = {1, 2, 3, 3}
print(seen)                     # {1, 2, 3} — duplicate gone
print(2 in seen)                # True — O(1), unlike a list's O(n)

# comprehension = loop + filter + transform in one expression
nums = [1, 2, 3, 4, 5, 6]
squares = [n * n for n in nums]            # [1, 4, 9, 16, 25, 36]
evens = [n for n in nums if n % 2 == 0]    # [2, 4, 6]
sq_map = {n: n * n for n in nums}          # dict comprehension
unique_words = {w.lower() for w in "The cat and the CAT".split()}
print(unique_words)                        # {'the', 'cat', 'and'}
```

Comprehensions replace 4-line loops with 1 readable line — and they're idiomatic Python, not a gimmick.

### Step 3 — Reading and writing files

```python
# `with` closes the file automatically, even on error
with open("notes.txt", "w") as f:       # "w" = write (truncates!), "a" = append
    f.write("line one\n")
    f.write("line two\n")

with open("notes.txt") as f:            # default mode is read
    for line in f:                      # memory-friendly: line by line
        print(line.rstrip())            # rstrip() removes the trailing \n

with open("notes.txt") as f:
    content = f.read()                  # or read everything at once
    lines = content.splitlines()
```

Rule: prefer iterating over the file object to `read()` — a 10 GB log would otherwise land in RAM in full.

### Step 4 — Error handling with try/except

```python
def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"config {path} missing, using defaults")
        return ""
    except PermissionError:
        print(f"no permission to read {path}")
        raise                                # re-raise: this one we can't fix

# multiple exceptions, and `finally` always runs
try:
    value = int("abc")
except ValueError as e:
    print(f"bad number: {e}")
finally:
    print("cleanup happens here, error or not")
```

Catching `Exception` bare is a smell: be specific, handle what you can fix, let the rest crash loudly.

### Step 5 — Tying it together: a real mini-tool

```python
# wordfreq.py — count word frequencies in a text file
import sys

def count_words(path):
    counts = {}
    with open(path) as f:
        for line in f:
            for word in line.lower().split():
                counts[word] = counts.get(word, 0) + 1
    return counts

def main():
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"usage: python3 {sys.argv[0]} <file>")
    counts = count_words(path)
    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    for word, n in top:
        print(f"{n:5}  {word}")

if __name__ == "__main__":
    main()
```

New pieces here: `sys.argv` (command-line arguments), `sorted(..., key=lambda ...)` (sort by value), `if __name__ == "__main__"` (run main only when executed, not imported). Run: `python3 wordfreq.py notes.txt`.

## Quick Exercises

**Ex 1 — Word frequency.** Create a text file (any article, ~20 lines) and run `wordfreq.py` on it. Then modify it to show the 10 most frequent words.

<details><summary>Answer</summary>

```bash
python3 wordfreq.py article.txt
```
Change the slice:

```python
top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:10]
```
`sorted` on `.items()` sorts pairs; `key=lambda kv: kv[1]` sorts by the count; `reverse=True` makes it descending.

</details>

**Ex 2 — Dict to CSV.** Write a script that reads a file where each line is `name,age` (create 3 lines yourself) and prints them as a sorted dict, oldest first.

<details><summary>Answer</summary>

```python
people = {}
with open("people.txt") as f:
    for line in f:
        name, age = line.strip().split(",")
        people[name] = int(age)

for name, age in sorted(people.items(), key=lambda kv: kv[1], reverse=True):
    print(f"{name} is {age}")
```
`split(",")` returns two values — unpacking gives them names. `int()` converts the string age so sorting is numeric.

</details>

**Ex 3 — Crash-proof it.** Run your Ex 2 script with a missing filename as its argument. It should print a friendly message, not a traceback.

<details><summary>Answer</summary>

```python
import sys

try:
    path = sys.argv[1]
except IndexError:
    sys.exit("usage: python3 people.py <file>")

try:
    with open(path) as f:
        for line in f:
            name, age = line.strip().split(",")
            print(name, age)
except FileNotFoundError:
    sys.exit(f"error: file '{path}' not found")
```

</details>

**Ex 4 — Set surgery.** Two log files each list usernames, one per line. Print the names present in both, and the names only in the first.

<details><summary>Answer</summary>

```python
with open("log1.txt") as f:
    a = {line.strip() for line in f}
with open("log2.txt") as f:
    b = {line.strip() for line in f}

print("in both:  ", a & b)     # intersection
print("only in 1:", a - b)     # difference
```
This is why sets exist: `a & b` on lists would be slow and duplicates would pollute the result.

</details>

**Ex 5 — Comprehension bootcamp.** In one line each, from `nums = list(range(1, 21))`: (a) all multiples of 3, (b) their squares as a dict, (c) the odd numbers as a set.

<details><summary>Answer</summary>

```python
nums = list(range(1, 21))
mult3   = [n for n in nums if n % 3 == 0]
squares = {n: n * n for n in mult3}
odds    = {n for n in nums if n % 2 == 1}
```
Three bracket types, three collection types: list, dict, set.

</details>

---

# Part 2 — NixOS: Services & Flakes

## Core Concepts

Issue 1 used NixOS as a package manager with a config file. The real power is one level up: everything running on your machine — SSH, a web server, a timer, a database — is a *declared option* in one place. Write the declaration, rebuild, done: the service is configured, started, enabled at boot, and will survive reinstall because the whole state lives in your file. Flakes add the missing ingredient for teams: pinning *exact* versions of everything so two machines (or two rebuilds a year apart) produce identical systems.

## E-Learning Knowledge

### Step 1 — Options: the vocabulary of configuration.nix

NixOS exposes thousands of options; each is a documented knob.

```nix
# /etc/nixos/configuration.nix
{ config, pkgs, ... }:
{
  # a service toggle: enables + starts the OpenSSH server at boot
  services.openssh = {
    enable = true;
    settings.PasswordAuthentication = false;   # key-only login
  };

  # programs get their own options too
  programs.git.enable = true;

  # users are options as well — everything in one file
  users.users.mister = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];   # wheel = sudo access
  };
}
```

```bash
# discover options yourself (name contains "ssh"):
# https://search.nixos.org/options — the official option search
sudo nixos-rebuild switch
```

The mental shift: you never "configure nginx by hand and hope." You set `services.<name>.*` options and the NixOS modules translate them into config files, systemd units, and firewall rules — consistently, every rebuild.

### Step 2 — Declarative services: a real web server

```nix
services.nginx = {
  enable = true;
  virtualHosts."myapp.local" = {
    root = "/srv/myapp";
    locations."/".index = "index.html";
  };
};
```

```bash
sudo mkdir -p /srv/myapp && echo "<h1>hello</h1>" | sudo tee /srv/myapp/index.html
sudo nixos-rebuild switch
curl http://myapp.local   # or http://localhost with Host header
```

Compare with Debian (Issue 2): there you installed nginx, hand-edited `/etc/nginx/sites-available/...`, symlinked into `sites-enabled`, and hoped you remembered every step. Here, the five-line declaration *is* the whole setup — and deleting it cleanly removes the server.

### Step 3 — Custom services and timers: your own code as a service

You can wrap your own script as a systemd service without leaving configuration.nix:

```nix
systemd.services.my-backup = {
  description = "Nightly home backup";
  serviceConfig = {
    Type = "oneshot";
    ExecStart = "/home/mister/scripts/backup.sh";
  };
};

systemd.timers.my-backup = {
  wantedBy = [ "timers.target" ];
  timerConfig = {
    OnCalendar = "*-*-* 03:00:00";   # every night at 3 AM
    Persistent = true;               # run late if the machine was off
  };
};
```

```bash
sudo nixos-rebuild switch
systemctl list-timers               # your timer is listed and scheduled
journalctl -u my-backup -e          # logs, same as any Debian service
```

This is where Python from this issue meets NixOS: write your `wordfreq`-style script, point `ExecStart` at it, and it becomes a scheduled, monitored system job.

### Step 4 — Generations management (beyond the basics)

```bash
nix-env --list-generations --profile /nix/var/nix/profiles/system
sudo nix-env --profile /nix/var/nix/profiles/system --delete-generations 5 6
sudo nix-collect-garbage -d    # free disk space from old store paths
nixos-version                  # which exact revision you're on
```

Old generations are your safety net; garbage collection is how you pay for them in disk space. Keep a few, prune the ancient ones.

### Step 5 — Flakes: pinning the whole world

A flake is a `flake.nix` that declares your system *and* pins every input to an exact commit recorded in `flake.lock`.

```nix
# /etc/nixos/flake.nix
{
  description = "My NixOS machine";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";  # pinned channel

  outputs = { self, nixpkgs }: {
    nixosConfigurations.mymachine =
      nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [ ./configuration.nix ];   # your existing config still works
      };
  };
}
```

```bash
cd /etc/nixos
sudo nixos-rebuild switch --flake .#mymachine
```

From now on, `nixos-rebuild switch --flake .` builds against the *locked* nixpkgs, not whatever is newest. Upgrade deliberately:

```bash
nix flake update          # bump the lock file
sudo nixos-rebuild switch --flake .
```

This is reproducibility: the same `flake.nix` + `flake.lock` in git reproduce the same system on any machine, any year.

## Quick Exercises

**Ex 1 — Enable a service the declarative way.** Enable the OpenSSH server with password login disabled, rebuild, then verify from within the machine.

<details><summary>Answer</summary>

```nix
services.openssh = {
  enable = true;
  settings.PasswordAuthentication = false;
};
```

```bash
sudo nixos-rebuild switch
systemctl status sshd      # active (running)
```
One declaration replaced: install package, edit `sshd_config`, `systemctl enable --now sshd`.

</details>

**Ex 2 — Read a NixOS option.** Pick a service you use (e.g. `services.syncthing`), find it on search.nixos.org/options, and change one of its settings. Rebuild and check the generated config file appeared.

<details><summary>Answer</summary>

Example with syncthing:

```nix
services.syncthing = {
  enable = true;
  user = "mister";
};
```

```bash
sudo nixos-rebuild switch
ls ~/.config/syncthing/    # NixOS module generated the config for you
```
The general skill: search the option name, read its type and default, set it, rebuild, verify the artifact the module produced.

</details>

**Ex 3 — Schedule a Python script.** Take your `wordfreq.py` (or any script), make it print to a log, and run it nightly at 3 AM via a NixOS timer.

<details><summary>Answer</summary>

```nix
systemd.services.wordfreq = {
  serviceConfig = {
    Type = "oneshot";
    ExecStart = "${pkgs.python3}/bin/python3 /home/mister/wordfreq.py";
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
```
Note `${pkgs.python3}` — Nix interpolates the exact store path of the interpreter, so the service never depends on whatever Python happens to be in PATH.

</details>

**Ex 4 — Rollback drill.** Make a small change (add a package), rebuild, confirm it works — then roll back to the previous generation and confirm it's gone. Note the exact commands.

<details><summary>Answer</summary>

```bash
# add pkgs.htop to environment.systemPackages, then:
sudo nixos-rebuild switch      # generation N+1, htop present
htop --version

# roll back:
sudo nixos-rebuild switch --rollback
htop --version                 # command not found — gone
```
Alternatively reboot and pick the older entry in the boot menu. Deleting a line from `configuration.nix` plus a rebuild achieves the same forward instead of backward.

</details>

**Ex 5 — Flakerize.** Create `/etc/nixos/flake.nix` from the Step 5 template (adjust hostname via `hostname`), run `sudo nixos-rebuild switch --flake .#<hostname>`, and verify the lock file exists.

<details><summary>Answer</summary>

```bash
hostname                        # e.g. "mymachine"
cd /etc/nixos
# create flake.nix as in Step 5, with modules = [ ./configuration.nix ];
sudo nixos-rebuild switch --flake .#mymachine
cat flake.lock | head -20       # pinned revisions with hashes
```
From now on, `nixos-rebuild switch --flake .` is reproducible; `nix flake update` is your deliberate upgrade button.

</details>

---

## Next Issue Preview

**Issue 5 (Week B) — Rust deeper + Debian deeper:** Rust collections (`Vec`, `HashMap`), `Result` and the `?` operator (proper error handling, mirroring today's Python `try/except`), and on Debian: user management, cron, and security hardening basics. See you next Monday! 🚀
