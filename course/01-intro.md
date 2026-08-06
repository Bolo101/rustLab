## Understanding Variables in Rust

Welcome to this lesson on variables in the Rust programming language. We'll explore how Rust handles variables, including their mutability, how types are determined, the concept of shadowing, the use of constants, and various methods for printing variable values to the console.

## Variables and Mutability in Rust

One of the core safety features of Rust is its handling of variable mutability.

**Default Immutability**
By default, variables in Rust are immutable. This means that once a value is bound to a variable name, you cannot change that value. Attempting to reassign an immutable variable will result in a compile-time error.

Consider this example:
```rust
// let x = 1;
// x = 2; // Error: cannot assign twice to immutable variable `x`
```
If you were to uncomment and compile this code, the Rust compiler would prevent you from changing the value of `x`.

**Enabling Mutability with `mut`**
To declare a variable that can be changed, you must explicitly use the `mut` keyword before the variable name during its declaration.

Let's look at how to make a variable mutable:
```rust
fn main() {
    // Variables
    // - Immutable by default
    // - Use mut keyword to make it mutable
    let mut x = 1; // x is declared as mutable
    println!("The initial value of x is: {}", x);
    x += 1;        // The value of x can be changed
    println!("The new value of x is: {}", x); // Now x is 2
}
```
In this snippet, `x` is declared as mutable using `let mut x = 1;`. We can then successfully change its value, for instance, by incrementing it. This explicit approach to mutability is a key difference from many other programming languages where variables are often mutable by default.

## Type Inference

Rust is a statically-typed language. This means that the type of every variable must be known by the compiler at compile time. However, Rust also features powerful type inference. In many cases, you don't need to explicitly state the type of a variable because the compiler can infer it from the value assigned and how it's used.

**Default Integer Type**
When you assign an integer value without specifying a type, Rust defaults to `i32` (a 32-bit signed integer).

Observe the following declarations:
```rust
fn main() {
    // Type inference
    let y: i32 = -1; // Explicitly typed as i32
    let z = -1;       // Type is inferred by Rust as i32

    println!("y is: {}, z is: {}", y, z);
    // These two lines of code are essentially the same in terms of the resulting type for z.
}
```
Here, `y` is explicitly annotated as an `i32`. For `z`, no type is specified, so Rust infers it as `i32` because `-1` is an integer literal.

## Shadowing

Rust allows you to declare a new variable with the same name as a previously declared variable. This concept is known as "shadowing." The new variable "shadows" the previous one, meaning any subsequent use of that variable name will refer to the new variable until it goes out of scope or is shadowed again.

Shadowing is distinct from marking a variable as `mut`:
*   When you shadow a variable, you are effectively creating an entirely new variable. The previous variable still exists but is no longer accessible by that name in the current scope.
*   Crucially, shadowing allows you to change the type of the variable, which is not possible with `mut`. A mutable variable can change its value, but not its type.

Here's an example demonstrating shadowing, including a type change:
```rust
fn main() {
    // Shadowing
    let x: i32 = 1;
    println!("x is: {}", x); // x is 1 (i32)

    let x: i32 = 2;    // x is shadowed. It's now a new variable also named x, with value 2 (i32)
    println!("x is now: {}", x);

    let x: bool = true; // x is shadowed again. It's now a new variable of type bool with value true
    println!("x is finally: {}", x); // x is true (bool)
}
```
In this code, `x` is first an `i32` with value `1`, then shadowed by another `i32` with value `2`, and finally shadowed by a `bool` with value `true`.

## Type Placeholder for Inference

In some situations, particularly with more complex types or generic programming, the Rust compiler might require a type annotation, but you might want Rust to infer the specific type. For this, you can use an underscore `_` as a type placeholder. This tells the compiler, "I know a type is needed here, please figure it out."

```rust
fn main() {
    // Type placeholder
    let x: _ = 1234; // Rust will infer the type (i32 in this case)
    println!("x with type placeholder is: {}", x);
}
```
This can be handy when a type is verbose or obvious from the context, allowing you to let the compiler do the work. For `1234`, Rust infers `i32`.

## Constants

Constants are values that are bound to a name and are guaranteed not to change. They differ from immutable variables in several key ways.

*   **Declaration**: Constants are declared using the `const` keyword instead of `let`.
*   **Type Annotation**: The type of a constant **must** always be explicitly annotated.
*   **Scope**: Constants can be declared in any scope, including the global scope (outside of any function).
*   **Naming Convention**: By convention, constant names are written in `UPPER_SNAKE_CASE` (e.g., `MAX_POINTS`).
*   **Value**: The value of a constant must be a constant expression, meaning it must be determinable at compile time. It cannot be the result of a function call or anything else computed at runtime.

Here's an example of a constant:
```rust
// This can be outside fn main()
// // Constants
const NUM: u32 = 1; // NUM is a constant of type u32 with value 1

fn main() {
    println!("The constant NUM is: {}", NUM);
}
```

**Key Differences Between Constants (`const`) and Immutable Variables (`let`)**:
*   Immutable variables declared with `let` are still variables. Their value is set at runtime (when the `let` statement is executed) and stored in memory. Even though they can't be changed after initialization, they behave like runtime values.
*   Constants declared with `const` are not just immutable; their values are effectively inlined into the compiled code wherever they are used. They are resolved at compile time. You cannot use `mut` with `const`.

## Printing Variables with the `println!` Macro

Rust provides the versatile `println!` macro for printing text and variable values to the console. It uses a format string as its first argument, followed by any values to be interpolated.

Here are several ways to use `println!`:

**1. Basic Placeholders**
Use empty curly braces `{}` as placeholders in the format string. The variables to be printed are passed as subsequent arguments to `println!`, and they fill the placeholders in order.

```rust
fn main() {
    let x = 1;
    let name = "Alice";
    println!("x is {}, and name is {}", x, name); // Output: x is 1, and name is Alice
}
```

**2. Inline Variable Names (Rust 2021+ Edition)**
You can directly include the variable name within the curly braces. This can make the `println!` statement more readable, especially when printing many variables.

```rust
fn main() {
    let x = 1;
    let y = 10;
    // Inline
    println!("x is {x} and y is {y}"); // Output: x is 1 and y is 10
}
```

**3. Positional Arguments**
You can use numbers inside the curly braces (e.g., `{0}`, `{1}`) to refer to the arguments passed to `println!` by their position (0-indexed). This allows you to reuse arguments or change their order in the output.

```rust
fn main() {
    let x = 1;
    // Positional arguments
    println!("{0} + {0} = {1}", x, x + x); // Output: 1 + 1 = 2
    println!("The second argument is {1}, the first is {0}", x, x + x); // Output: The second argument is 2, the first is 1
}
```
Here, `{0}` refers to the first argument after the format string (`x`), and `{1}` refers to the second argument (`x + x`).

**4. Debug Printing**
For more detailed output, especially for complex types (like structs or enums) or when debugging, you can use the debug formatting specifier:
*   `{:?}`: This requests a debug representation of the variable.
*   `{:#?}`: This requests a "pretty" debug print, which formats the output in a more human-readable way, often with indentation and newlines for complex structures.

```rust
fn main() {
    let x = 1;
    let point = (10, 20); // A tuple

    // Debug
    println!("DEBUG simple: x is {:?}", x);    // Output: DEBUG simple: x is 1
    println!("DEBUG pretty simple: x is {:#?}", x);   // Output: DEBUG pretty simple: x is 1 (for simple types, similar to :?)

    println!("DEBUG tuple: point is {:?}", point); // Output: DEBUG tuple: point is (10, 20)
    println!("DEBUG pretty tuple: point is {:#?}", point);
    // Output for pretty tuple:
    // DEBUG pretty tuple: point is (
    //     10,
    //     20,
    // )
}
```
Debug printing is incredibly useful for inspecting the state of your data. Most standard library types and types you define (if you derive `Debug`) can be printed this way.

This lesson covered the fundamentals of variables in Rust: their default immutability, the `mut` keyword, type inference, shadowing, constants, and various ways to print them using `println!`. These concepts are foundational to writing any Rust program.

## Getting Started with Functions in Rust

Functions are fundamental building blocks in Rust, allowing you to encapsulate logic, promote code reuse, and structure your programs effectively. This lesson provides a comprehensive introduction to defining, calling, and understanding the nuances of functions in Rust.

## Declaring Functions in Rust

In Rust, functions are declared using the `fn` keyword. The basic syntax involves the function name, a list of parameters enclosed in parentheses, and an optional return type.

**Syntax:**

```rust
fn function_name(param1: Type1, param2: Type2) -> ReturnType {
    // function body: statements and/or expressions
}
```

Let's illustrate this with a simple example. We'll create a function named `add` that takes two unsigned 32-bit integers (`u32`) as input and returns their sum, also as a `u32`.

```rust
fn add(x: u32, y: u32) -> u32 {
    return x + y;
}
```

Let's break down this `add` function:
*   `fn add`: This declares a function named `add`.
*   `(x: u32, y: u32)`: This defines two parameters: `x` of type `u32`, and `y` also of type `u32`. Type annotations for parameters are mandatory in Rust.
*   `-> u32`: This specifies that the function `add` will return a value of type `u32`.
*   `{ return x + y; }`: This is the function body. Here, `x + y` calculates the sum, and the `return` keyword explicitly sends this sum back to the caller. Note the semicolon at the end of the `return` statement.

## Mastering Return Values

Rust offers flexibility in how functions return values. You can use an explicit `return` statement or leverage Rust's expression-based nature for implicit returns.

### Explicit Return

As seen in our initial `add` function, the `return` keyword explicitly designates the value to be returned. A semicolon must follow the `return` statement.

For clarity, let's rename our first version of `add` to `add_with_return`:

```rust
fn add_with_return(x: u32, y: u32) -> u32 {
    return x + y;
}
```

### Implicit Return

Rust is an expression-based language, which means most things evaluate to a value. If the last line of a function body is an expression (without a trailing semicolon), its value is automatically returned. The `return` keyword is not needed in this case.

Let's refactor our `add` function to use an implicit return:

```rust
fn add(x: u32, y: u32) -> u32 {
    x + y // No semicolon; this expression's value is returned
}
```

**Important Note:** Only the *final expression* in a function block can be an implicit return. Any preceding lines of code within the function must be statements, typically ending with a semicolon.

Consider this modified `add` function:

```rust
fn add(x: u32, y: u32) -> u32 {
    println!("Calculating sum for x = {}", x); // This is a statement
    println!("And y = {}", y);                 // This is also a statement
    x + y                                     // This is an expression, its value is returned
}
```
Here, the `println!` macro calls are statements (they perform an action but don't evaluate to the value we want to return from `add`). The final line `x + y` is an expression, and its result becomes the return value of the `add` function.

### Returning Multiple Values

Functions in Rust can return multiple values by using a tuple as the return type. A tuple is a collection of values of different types, grouped together.

Let's modify our `add` function to return both the sum (a `u32`) and a boolean flag (`bool`):

```rust
fn add_multiple(x: u32, y: u32) -> (u32, bool) {
    return (x + y, true); // Returns a tuple containing the sum and 'true'
}
```
The return type `-> (u32, bool)` indicates that the function will return a tuple where the first element is a `u32` and the second is a `bool`.

### Functions Without Explicit Returns (The Unit Type)

If a function doesn't explicitly return a value, it implicitly returns the "unit type," denoted as `()`. The unit type is an empty tuple and essentially signifies "no meaningful value." You can omit `-> ()` from the function signature if it doesn't return anything.

Here's an example of a `print_message` function that takes a `String` and prints it to the console. It performs an action but doesn't return any specific data.

```rust
fn print_message(s: String) { // Implicitly returns ()
    // In Rust 2021 edition and later, "{s}" uses s as an implicit named argument.
    // This line prints the content of the string 's' five times, concatenated.
    println!("{s}{s}{s}{s}{s}");
}
```

## Understanding Function Parameters

Parameters are the inputs to your functions. They are defined within the parentheses after the function name, with each parameter specified as `name: Type`. Type annotations for all function parameters are mandatory.

### Type Conversion for Arguments

When calling a function, the arguments you pass must match the types of the parameters defined in the function signature. Sometimes, this requires explicit type conversion.

Our `print_message` function, for example, expects a parameter `s` of type `String`. However, string literals in Rust (e.g., `"🐸"`) are of type `&str` (a string slice, which is a reference to string data).

To pass a string literal like `"🐸"` to `print_message`, we must convert it from `&str` to `String`. A common way to do this is by using the `.to_string()` method:

```rust
// Assuming print_message function is defined as above
// print_message("🐸"); // This would cause a type error

print_message("🐸".to_string()); // Correct: "🐸" (&str) is converted to String
```
The distinction between `String` (an owned, heap-allocated string) and `&str` (a string slice) is a key concept in Rust's ownership system, which will be explored in more detail in future lessons.

## Calling Functions

Once a function is defined, you can call (or invoke) it by using its name followed by parentheses. If the function expects arguments, you provide them inside the parentheses.

If a function returns a value, you can assign this value to a variable using a `let` binding.

Let's see how to call our previously defined functions within a `main` function, which is the entry point for Rust programs.

```rust
// This attribute can be placed at the top of a file
// to suppress compiler warnings for unused code, useful during development.
#![allow(unused)]

fn add(x: u32, y: u32) -> u32 {
    x + y
}

fn print_message(s: String) {
    println!("{s}{s}{s}{s}{s}");
}

fn main() {
    let x = 1;
    let y = 2;

    // Calling the 'add' function (which uses implicit return)
    // and storing its result in 'z'.
    let z = add(x, y);
    println!("{} + {} = {}", x, y, z); // Expected output: 1 + 2 = 3

    // Calling the 'print_message' function
    print_message("🐸".to_string()); // Expected output: 🐸🐸🐸🐸🐸
}
```

## Running Your Rust Code

To compile and run your Rust code, you typically use Cargo, Rust's build system and package manager. If your code is in a file named `func.rs` within an `examples` directory of your Cargo project, you would run it from your terminal using:

```bash
cargo run --example func
```

## Key Takeaways: Rust Functions at a Glance

Let's summarize the core concepts covered in this lesson:

*   **`fn` Keyword:** Used to declare all functions in Rust.
*   **Type Annotations:** Mandatory for function parameters and return values. They ensure type safety.
*   **`return` Keyword:** Can be used for explicit returns. A statement using `return` must end with a semicolon.
*   **Implicit Returns:** If the last line of a function is an expression (no semicolon), its value is automatically returned.
*   **Semicolons:** Differentiate statements (which end with `;`) from expressions (which often don't end with `;` if they are intended as the return value of a block or function).
*   **Tuples:** Used to enable functions to return multiple values.
*   **Unit Type `()`:** The implicit return type of functions that don't explicitly return a value. It signifies "no value."
*   **Common Types:** We encountered `u32` (unsigned 32-bit integer), `bool` (boolean: `true` or `false`), `String` (owned string), and `&str` (string slice).
*   **`.to_string()` Method:** A common method for converting various types, like `&str`, into an owned `String`.
*   **`println!` Macro:** A versatile macro used for printing formatted output to the console.
*   **Rust 2021 Implicit Named Arguments:** In `println!` macros (and other formatting macros), if a variable `s` is in scope, `{s}` can be used as a shorthand for `{s = s}`. This is why `println!("{s}{s}{s}{s}{s}");` effectively prints the content of the variable `s` five times.
*   **`#![allow(unused)]`:** A crate-level attribute useful during development to suppress compiler warnings about unused code, variables, or functions.

Understanding functions is crucial for writing any non-trivial Rust program. By mastering their declaration, parameter handling, and return value mechanics, you'll be well-equipped to build robust and maintainable applications.