# Tech Learning Newsletter — Issue 5: Going Deeper

*Level: Intermediate → Advanced. Builds on Issues 1–4.*

---

## 🦀 Rust — Lifetimes & Smart Pointers

### Core Concepts
- **Lifetimes** describe how long references remain valid. They don't change how long data lives — they tell the compiler enough to prove safety.
- **Smart pointers** heap-allocate and own data: `Box<T>`, `Rc<T>`, `RefCell<T>`.

### E-Learning Knowledge (step by step)
1. **Explicit lifetimes** are needed when a function returns a reference and the compiler can't infer which input it comes from:
   ```rust
   fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {
       if a.len() > b.len() { a } else { b }
   }
   ```
   `'a` means: the returned reference is valid only as long as *both* inputs are.
2. **`Box<T>`** — single ownership on the heap. Use it for recursive types or large values:
   ```rust
   enum List { Cons(i32, Box<List>), Nil }
   ```
3. **`Rc<T>`** — reference counting for multiple owners (single-threaded):
   ```rust
   use std::rc::Rc;
   let shared = Rc::new(String::from("hello"));
   let a = Rc::clone(&shared); // cheap, bumps count
   ```
4. **`RefCell<T>`** — interior mutability: borrow rules checked at *runtime*. Combine as `Rc<RefCell<T>>` for shared, mutable state.
5. Rule of thumb: `Box` for ownership, `Rc` for sharing, `RefCell` for mutation — never all three unless you truly need them.

### Quick Exercises
1. Why does this fail, and fix it:
   ```rust
   fn first(s: &str) -> &str {
       let parts: Vec<&str> = s.split(' ').collect();
       parts[0]
   }
   ```
2. Which pointer for a tree node with two children sharing one parent-held child value?
3. What does `Rc::strong_count(&shared)` return after two clones?

<details><summary>Answers</summary>

1. It fails because `parts` (the `Vec`) is dropped at the end of the function, so the returned reference would dangle. Fix: return `String` or restructure so the data outlives the reference — e.g. `s.split(' ').next()` borrows directly from `s`, which works.
2. `Box<T>` for child ownership; `Rc<T>` only where multiple owners genuinely exist.
3. 3 — the original plus two clones.
</details>

---

## 🐍 Python — Decorators, Generators & Context Managers

### Core Concepts
- **Decorators** wrap functions to add behavior without modifying them.
- **Generators** produce values lazily, one at a time, keeping memory usage flat.
- **Context managers** (`with`) guarantee setup/teardown.

### E-Learning Knowledge (step by step)
1. **Decorators** are functions taking a function and returning a new one:
   ```python
   import functools, time
   def timed(fn):
       @functools.wraps(fn)
       def wrapper(*args, **kwargs):
           start = time.perf_counter()
           result = fn(*args, **kwargs)
           print(f"{fn.__name__} took {time.perf_counter() - start:.3f}s")
           return result
       return wrapper

   @timed
   def slow_sum(n): return sum(range(n))
   ```
   `@functools.wraps` preserves the original name and docstring.
2. **Generators** use `yield` instead of `return`:
   ```python
   def fib():
       a, b = 0, 1
       while True:
           yield a
           a, b = b, a + b
   # next(fib()), or for x in itertools.islice(fib(), 10): ...
   ```
   Ideal for reading huge files line by line or infinite sequences.
3. **Generator expressions** mirror list comprehensions with parentheses:
   `total = sum(len(line) for line in open("big.txt"))`
4. **Context managers**: write your own with a class (`__enter__`/`__exit__`) or `contextlib.contextmanager`:
   ```python
   from contextlib import contextmanager
   @contextmanager
   def timer():
       start = time.perf_counter()
       yield
       print(f"{time.perf_counter() - start:.3f}s")
   ```

### Quick Exercises
1. Write a decorator `@logged` that prints the arguments before calling the function.
2. What does this print, and why?
   ```python
   def gen():
       yield 1
       yield 2
   g = gen()
   print(sum(g), sum(g))
   ```
3. Convert `data = [x*x for x in range(10_000_000)]` to a memory-friendlier version.

<details><summary>Answers</summary>

1.
```python
def logged(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__} with {args} {kwargs}")
        return fn(*args, **kwargs)
    return wrapper
```
2. `3 0` — a generator is exhausted after one full pass; the second `sum()` iterates an empty generator.
3. Use a generator expression: `data = (x*x for x in range(10_000_000))` — values are computed on demand instead of storing 10 million ints.
</details>

---

## 🐧 Debian — Containers, Automation & Monitoring

### Core Concepts
- **Docker/Podman** package applications with their dependencies.
- **Systemd timers** are the modern replacement for cron, with logging via journald.
- **Performance monitoring** tools help find bottlenecks before they cause outages.

### E-Learning Knowledge (step by step)
1. **Run a first container** (Podman needs no daemon and no root):
   ```bash
   sudo apt install podman
   podman run --rm -p 8080:80 docker.io/library/nginx
   # visit http://localhost:8080, then Ctrl+C; --rm cleans up
   ```
2. **Build your own image** with a `Dockerfile`/`Containerfile`:
   ```dockerfile
   FROM debian:bookworm-slim
   RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*
   COPY app.py /app/app.py
   CMD ["python3", "/app/app.py"]
   ```
   Build & run: `podman build -t myapp .` then `podman run --rm myapp`.
3. **Systemd timers** instead of cron:
   ```ini
   # /etc/systemd/system/backup.timer
   [Timer]
   OnCalendar=*-*-* 03:00:00
   Persistent=true
   [Install]
   WantedBy=timers.target
   ```
   Enable with `systemctl enable --now backup.timer`, verify with `systemctl list-timers`. `Persistent=true` runs missed jobs after downtime — cron won't.
4. **Monitoring essentials**:
   - `htop` — interactive process view.
   - `vmstat 1`, `iostat -x 1` — CPU/memory and disk I/O over time.
   - `journalctl -u <service> --since "1 hour ago"` — service logs.
   - `dmesg | tail` — kernel messages (disk errors, OOM kills).

### Quick Exercises
1. Command to see which timer runs next and when?
2. In a `Containerfile`, why combine `apt-get update && apt-get install ...` in a single `RUN`?
3. A service silently died overnight — which two commands show why?

<details><summary>Answers</summary>

1. `systemctl list-timers --all` (shows `NEXT` and `LAST` columns).
2. Each `RUN` is a cached layer; splitting them leaves the stale `update` cache layer baked in and grows the image.
3. `systemctl status <service>` (state, exit code) and `journalctl -u <service> --since yesterday` (logs around the failure); `dmesg | tail` if an OOM kill is suspected.
</details>

---

## ❄️ NixOS — Modules, Options & Multi-Config Setups

### Core Concepts
- **Modules** are the building blocks of `configuration.nix` — everything is a module merging into one configuration.
- **Options** define the interface a module exposes; `config` sets values.
- **One config file, many machines**: share a base and specialize per host.

### E-Learning Knowledge (step by step)
1. **Write your own module** in the flake style:
   ```nix
   # mymodule.nix
   { config, lib, ... }: {
     options.services.myapp.enable = lib.mkEnableOption "my app";

     config = lib.mkIf config.services.myapp.enable {
       systemd.services.myapp = {
         description = "My App";
         wantedBy = [ "multi-user.target" ];
         serviceConfig.ExecStart = "${pkgs.myapp}/bin/myapp";
       };
     };
   }
   ```
   `mkIf` makes the whole config block conditional on your option.
2. **Layering**: `mkDefault` gives a low-priority value; user config can override it without errors. Use it inside modules, plain values in your own `configuration.nix`.
3. **Shared base, per-host specialization**:
   ```nix
   # common.nix — locale, users, ssh, base packages
   # hosts/laptop.nix = { imports = [ ../common.nix ]; ... laptop-specific bits }
   # hosts/server.nix = { imports = [ ../common.nix ]; ... server-specific bits }
   ```
4. **Safe iteration workflow**:
   - `nixos-rebuild build` — builds only, catches errors without switching.
   - `nixos-rebuild test` — switches the running system without adding a boot entry.
   - `nixos-rebuild switch --rollback` — go back if something breaks.
   - `nixos-rebuild list-generations` — see the full history.

### Quick Exercises
1. What's the difference between `nixos-rebuild switch` and `nixos-rebuild test`?
2. Why use `mkDefault` in a module instead of a plain value?
3. What does `lib.mkEnableOption` create?

<details><summary>Answers</summary>

1. `switch` activates the config **and** adds a boot entry (persistent); `test` activates it in the running system only — ideal for trying things out without committing a boot generation.
2. A plain value in a module can conflict with user settings; `mkDefault` yields so the user's `configuration.nix` overrides it cleanly instead of producing a merge conflict.
3. A boolean option `services.myapp.enable` (default `false`) with a friendly description used in error messages.
</details>

---

## 📌 Recap & What's Next
- **Rust**: lifetimes + the `Box`/`Rc`/`RefCell` trio.
- **Python**: decorators, generators, context managers.
- **Debian**: containers, systemd timers, monitoring.
- **NixOS**: writing modules, options, and multi-host setups.

Issue 6 will push into the advanced tier: async Rust (`async/await`, `tokio`), Python concurrency (`asyncio`), Debian performance tuning, and NixOS networking/declarative services.
