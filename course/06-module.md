# Rust Modules and Project Organization Summary

## 1. Defining and Accessing Basic Modules

Modules are a fundamental feature in Rust for organizing code into logical units. They enable you to group related functionality, control the visibility of items (encapsulation), and create distinct namespaces to prevent naming conflicts.

### Creating a Module

To better organize code, you can move functions into a new module:

```rust
#![allow(unused)]

mod my { // Defines the module 'my'
    fn print() {
        println!("rust");
    }
}

fn main() {
    // How do we call print() now that it's in the 'my' module?
}
```

### Controlling Visibility with the `pub` Keyword

To make `print()` accessible from outside `mod my`, we must declare it as public using the `pub` keyword.

```rust
#![allow(unused)]

mod my {
    pub fn print() { // 'pub' makes this function public
        println!("rust");
    }

    // This function remains private to 'mod my'
    fn private_print() {
        println!("private");
    }
}

fn main() {
    my::print(); // Now this works
    // my::private_print(); // This would cause a compile-time error
}
```

### Calling Functions from Modules

To call a function defined within a module from outside that module, you must prefix the function name with the module name and the `::` path separator.

```rust
fn main() {
    my::print(); // Accessing print() from the my module
}
```

**Key Points:**
- All items within a module are private by default
- The `pub` keyword makes items accessible from outside their defining module
- The `::` operator is used to navigate module hierarchies

---

## 2. Structuring Code with Nested Modules

Modules can be nested within other modules, allowing for more granular organization.

### Creating Nested Modules

Let's create a new module `a` inside our existing `mod my`:

```rust
#![allow(unused)]

mod my {
    pub fn print() {
        println!("rust");
    }

    fn private_print() {
        println!("private");
    }

    // Nested module 'a'
    pub mod a {
        pub fn print() {
            println!("a");
        }
    }
}

fn main() {
    my::print();
    my::a::print(); // To call this, 'mod a' and 'a::print()' must both be public
}
```

### Visibility for Nested Modules

For the call `my::a::print()` to work from `main()`:
1. The nested module `a` itself must be declared `pub` within `mod my` (i.e., `pub mod a`).
2. The function `print()` within `mod a` must also be declared `pub` (i.e., `pub fn print()`).

Output:
```
rust
a
```

---

## 3. Encapsulating Data with Structs in Modules

Structs, like functions, can be defined within modules. Their visibility, and the visibility of their fields, follows similar rules.

### Defining Structs in Modules

```rust
mod my {
    pub mod a {
        pub struct S {
            id: u32,
            name: String,
        }
    }
}
```

### Visibility of Struct Fields

Even if a struct itself is declared `pub`, its fields are private by default. To access or initialize struct fields from outside the module where the struct is defined, the individual fields must also be marked `pub`.

```rust
mod my {
    pub mod a {
        pub struct S {
            pub id: u32,     // Public field
            pub name: String, // Public field
        }
    }
}

fn main() {
    my::print();
    my::a::print();

    let s = my::a::S {
        id: 0,
        name: "rust".to_string(),
    };
    println!("Struct S: id = {}, name = {}", s.id, s.name);
}
```

If you tried to initialize `s` while `name` (or `id`) was not `pub`, you would encounter a compile-time error like `field 'name' of struct 'S' is private`.

### The Builder Pattern for Structs with Private Fields

A common and robust pattern for initializing structs, especially when you want to control how fields are set or keep some fields private, is to provide a public constructor function.

```rust
mod my {
    pub mod a {
        pub struct S {
            pub id: u32,  // 'id' is public
            name: String, // 'name' is private
        }

        // Public constructor function for S
        pub fn build_s(id: u32, initial_name: &str) -> S {
            S {
                id, // Shorthand for id: id
                name: initial_name.to_string(), // Can access private 'name' here
            }
        }
    }
}

fn main() {
    // Initialize 's' using the public 'build_s' function
    let s_instance = my::a::build_s(1, "hello_private_field");
    println!("Struct S built: id = {}", s_instance.id);
    // We cannot directly access s_instance.name here as it's private.
}
```

This approach works because the `build_s` function is part of `mod a` and therefore has permission to access and initialize the private fields of `struct S`.

---

## 4. Navigating Parent Scopes with the `super` Keyword

The `super` keyword is a special path qualifier that allows you to refer to the parent module's scope. This is particularly useful for accessing items in sibling modules or items defined in the parent module from within a child module.

### Accessing Sibling Modules

Imagine we have two sibling modules, `foo` and `my`, at the same level:

```rust
mod foo {
    pub fn print() {
        println!("foo");
    }
}

mod my {
    // To call foo::print() from within 'my', we need to bring 'foo' into scope.
    // 'super' refers to the parent scope of 'my'.
    use super::foo;

    pub fn print_message_from_foo() {
        foo::print(); // Now callable because 'foo' is in scope via 'use super::foo;'
    }

    pub mod a {
        // ...
    }
}

fn main() {
    my::print_message_from_foo();
}
```

### Using `super` from a Deeper Nested Module

If we want to call `foo::print()` from within `mod a` (which is nested inside `mod my`), we need to use `super` twice:

```
// File/Crate Root
//  |- mod foo
//  |- mod my
//     |- pub mod a
//        |- // To access 'foo' from here:
//        // 'super' goes from 'a' to 'my'.
//        // 'super::super' goes from 'a' to 'my', then from 'my' to the File/Crate Root.
```

Here's the code:

```rust
mod foo {
    pub fn print() {
        println!("foo");
    }
}

mod my {
    pub fn print() {
        println!("rust");
    }

    pub mod a {
        // First 'super' accesses 'my' module's scope.
        // Second 'super' accesses the crate root scope (parent of 'my').
        use super::super::foo;

        pub fn print() {
            println!("a");
        }

        pub fn print_message_from_foo_via_a() {
            foo::print(); // Calls foo::print() from the crate root
        }
    }
}

fn main() {
    my::print();
    my::a::print();
    my::a::print_message_from_foo_via_a();
}
```

Output:
```
rust
a
foo
```

---

## 5. Core Principles for Effective Module Usage in Rust

To effectively use modules in Rust, keep these key principles in mind:

*   **Default Privacy:** All items within a module (functions, structs, enums, constants, and other modules) are private by default. They can only be accessed by code within the same module or its direct children.
*   **The `pub` Keyword:** Use `pub` to make an item public, meaning it can be accessed from outside its defining module. This applies to the module declaration itself if it's nested (`pub mod my_module`), as well as to functions (`pub fn my_func`), structs (`pub struct MyStruct`), and individual struct fields (`pub field_name: Type`).
*   **Path Separator `::`:** The double colon (`::`) is used to navigate module hierarchies and access items within modules (e.g., `my_module::my_sub_module::my_function()`).
*   **The `use` Keyword:** This keyword brings paths into the current scope, allowing you to refer to items by shorter names. It's often used with `self`, `super`, or crate names to create more convenient paths.
*   **The `super` Keyword:** `super` refers to the parent module of the current module. It can be chained (e.g., `super::super::`) to navigate multiple levels up the module hierarchy, enabling access to items in ancestor or sibling modules.
*   **Builder Pattern:** For structs, especially those with private fields or complex initialization logic, consider providing public constructor functions (often called `new` or following a builder pattern). This enhances encapsulation and provides a controlled interface for creating struct instances.

---

## 6. Structuring Your Rust Project: From Single File to Organized Modules

This lesson guides you through refactoring a Rust project from a single file into a well-organized structure using multiple files and directories for your modules.

### Initial State: All Code in `examples/mods.rs`

We begin with a scenario where all our module definitions (`foo` and `my`) and the `main` function reside in a single file:

```rust
// examples/mods.rs
#![allow(unused)]

mod foo {
    pub fn print() {
        println!("foo");
    }
}

mod my {
    use super::foo;

    pub fn print() {
        println!("rust");
    }

    fn private_print() {
        a::print();
        println!("private");
    }

    pub mod a {
        use super::super::foo;

        pub fn print_foo() {
            foo::print();
        }

        pub fn print() {
            println!("a");
        }

        pub struct S {
            pub id: u32,
            name: String,
        }

        pub fn build(id: u32) -> S {
            S {
                id,
                name: "".to_string(),
            }
        }
    }
}

fn main() {
    my::print();
    my::a::print();
    let s = my::a::build(1);
    my::a::print_foo();
}
```

---

## 7. Step 1: Moving Modules to a Library Crate (`lib.rs`)

Our first step is to separate the module logic into a library crate.

### Create `src/lib.rs`

In your project's `src` directory, create a new file named `lib.rs`. This file serves as the root of a new library crate.

Project structure:
```
src/
├── lib.rs  <-- New file
└── main.rs
examples/
└── mods.rs
```

### Move Module Code to `lib.rs`

Cut the `mod foo { ... }` and `mod my { ... }` blocks from `examples/mods.rs` and paste them into `src/lib.rs`.

### Make Modules Public in `lib.rs`

For these modules to be accessible from outside the library, they must be declared `pub`:

```rust
// src/lib.rs
#![allow(unused)]

pub mod foo {
    pub fn print() {
        println!("foo");
    }
}

pub mod my {
    pub fn print() {
        println!("rust");
    }

    fn private_print() {
        a::print();
        println!("private");
    }

    pub mod a {
        use crate::foo;

        pub fn print_foo() {
            foo::print();
        }

        pub fn print() {
            println!("a");
        }

        pub struct S {
            pub id: u32,
            name: String,
        }

        pub fn build(id: u32) -> S {
            S {
                id,
                name: "".to_string(),
            }
        }
    }
}
```

### Importing Modules into `examples/mods.rs`

The `examples/mods.rs` file now needs to import the modules from our newly created library.

Check your `Cargo.toml` file:
```toml
[package]
name = "hello_rust" // This is your package name
version = "0.1.0"
edition = "2024"
```

Update `examples/mods.rs`:
```rust
// examples/mods.rs
use hello_rust::my; // Imports 'my' module from the 'hello_rust' crate

fn main() {
    my::print();
    my::a::print();
    let s = my::a::build(1);
    my::a::print_foo();
}
```

### Running the Example

Execute your example using `cargo run --example mods`.

---

## 8. Step 2: Splitting Top-Level Modules in `lib.rs` into Separate Files

The next step is to split the `foo` and `my` modules into their own dedicated files.

### Create `src/foo.rs` and `src/my.rs`

Create two new files in the `src` directory: `foo.rs` and `my.rs`.

File structure:
```
src/
├── foo.rs   <-- New file
├── lib.rs
├── main.rs
└── my.rs    <-- New file
```

### Update `src/lib.rs`

Modify `src/lib.rs` to declare these modules:

```rust
// src/lib.rs
#![allow(unused)]

pub mod foo; // Rust looks for src/foo.rs or src/foo/mod.rs
pub mod my;  // Rust looks for src/my.rs or src/my/mod.rs
```

### Content of `src/foo.rs`

Move the content of the original `mod foo { ... }` block into `src/foo.rs`:

```rust
// src/foo.rs
pub fn print() {
    println!("foo");
}
```

### Content of `src/my.rs`

Move the content of the original `mod my { ... }` block into `src/my.rs`:

```rust
// src/my.rs

pub fn print() {
    println!("rust");
}

fn private_print() {
    a::print();
    println!("private");
}

pub mod a {
    use crate::foo;

    pub fn print_foo() {
        foo::print();
    }

    pub fn print() {
        println!("a");
    }

    pub struct S {
        pub id: u32,
        name: String,
    }

    pub fn build(id: u32) -> S {
        S {
            id,
            name: "".to_string(),
        }
    }
}
```

---

## 9. Step 3: Organizing Nested Modules (`my::a`) with Directories

The `my` module contains a nested module `a`. We can further organize this by giving `my` its own directory.

### Create Directory `src/my/`

Inside the `src` directory, create a new directory named `my`.

### Create `src/my/mod.rs` and `src/my/a.rs`

*   `src/my/mod.rs`: This file will now represent the `my` module itself.
*   `src/my/a.rs`: This file will contain the code for the `a` submodule.

File structure:
```
src/
├── foo.rs
├── lib.rs
├── main.rs
└── my/         <-- New directory
    ├── a.rs    <-- New file (for submodule a)
    └── mod.rs  <-- New file (for module my)
```

Delete the previous `src/my.rs` file.

### Content of `src/my/a.rs`

Move the code that was inside the `pub mod a { ... }` block into `src/my/a.rs`:

```rust
// src/my/a.rs

use crate::foo;

pub fn print_foo() {
    foo::print();
}

pub fn print() {
    println!("a");
}

pub struct S {
    pub id: u32,
    name: String,
}

pub fn build(id: u32) -> S {
    S {
        id,
        name: "".to_string(),
    }
}
```

### Content of `src/my/mod.rs`

This file defines the `my` module. It must declare its public submodule `a`:

```rust
// src/my/mod.rs

// Declare the submodule 'a'. Rust will look for src/my/a.rs or src/my/a/mod.rs.
pub mod a;

// Items directly part of the 'my' module
pub fn print() {
    println!("rust");
}

fn private_print() {
    a::print();
    println!("private");
}
```

---

## 10. Key Concepts for Rust Module Organization

*   **`lib.rs` (or `main.rs` for binaries):** This is the crate root. Modules defined or declared here form the top level of your crate's module tree.
*   **Module Declaration:**
    *   `mod my_module;` tells Rust to look for the contents of `my_module` in:
        1.  `src/my_module.rs` (for a module without submodules)
        2.  `src/my_module/mod.rs` (if `my_module` has its own submodules organized in the `my_module/` directory)
*   **`mod.rs`:** A special filename. When you have a directory representing a module (e.g., `src/my/`), the file `src/my/mod.rs` contains the code for the `my` module itself, including declarations of its submodules.
*   **`pub` Keyword:** Crucial for visibility. Use `pub` to make modules, functions, structs, enums, traits, and struct fields accessible from outside their defining module.
*   **`use` Statement:**
    *   To bring items into scope from the *same crate*: `use crate::module_name::item_name;` or `use crate::module_name;`
    *   To bring items into scope from an *external crate*: `use external_crate_name::module_name::item_name;`
*   **`super` Keyword:**
    *   Refers to the parent module. For example, in `src/my/a.rs`, `super` refers to the `my` module.
    *   `super::super::item` would go two levels up.
    *   While `super` is useful for relative paths, `crate::path::to::item` is often clearer and more resilient to refactoring.
*   **Package Name:** Found in `Cargo.toml` under `[package].name`. This is the name used when your library is a dependency for another crate.

---

## 11. Final Achieved File Structure

After these steps, your project's relevant files will be structured as follows:

```
.
├── Cargo.toml
├── examples/
│   └── mods.rs
└── src/
    ├── foo.rs          // Contains the public 'foo' module's code
    ├── lib.rs          // Crate root for the library; declares 'pub mod foo;' and 'pub mod my;'
    ├── main.rs         // (Potentially the root of a binary crate)
    └── my/             // Directory representing the 'my' module
        ├── a.rs        // Contains the public 'my::a' submodule's code
        └── mod.rs      // Contains code for 'my' module itself, declares 'pub mod a;'
```

This structured approach significantly improves code organization. Each module and submodule has a distinct location in the file system, making the codebase easier to navigate, understand, and maintain, particularly as it scales in size and complexity.

---

## Summary

Rust modules provide a powerful system for organizing code:

1. **Basic Modules**: Use `mod` to define modules and `pub` for visibility
2. **Nested Modules**: Modules can contain other modules for hierarchical organization
3. **Struct Encapsulation**: Control visibility of structs and their fields
4. **Path Navigation**: Use `::` for path separation and `super` for parent access
5. **Project Structure**: Move from single files to organized library crates
6. **File Organization**: Split modules into separate files and directories
7. **Visibility Control**: Default privacy with explicit `pub` declarations
8. **Builder Pattern**: Use constructor functions for controlled struct initialization

By understanding and applying these concepts, you can write well-organized, maintainable, and robust Rust applications where code is neatly compartmentalized and access is carefully controlled.