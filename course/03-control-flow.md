## Mastering Conditional Logic: Basic `if/else` Statements in Rust

Conditional statements are fundamental to programming, allowing your code to make decisions and execute different paths based on specific criteria. In Rust, the `if/else` construct provides this capability, enabling you to control the flow of execution in your programs.

**The Core Concept**

`if/else` statements evaluate a condition. If the condition is true, a specific block of code is executed. If it's false, an optional `else if` condition can be checked, or an optional `else` block can be executed as a default fallback.

**Syntax**

The structure of an `if/else` statement in Rust is as follows:

```rust
if condition {
    // Code to execute if condition is true
} else if another_condition {
    // Code to execute if another_condition is true
} else {
    // Code to execute if all preceding conditions are false
}
```

**Illustrative Example**

Let's consider a practical example where we check the value of an unsigned 32-bit integer `x`:

```rust
// examples/if_else.rs
#![allow(unused)] // Attribute to allow unused code/variables

fn main() {
    let x: u32 = 10; // Declare an unsigned 32-bit integer x with value 10

    if x > 0 {
        println!("x > 0");
    } else if x < 0 {
        // For a u32, x < 0 will always be false.
        println!("x < 0");
    } else {
        println!("x = 0");
    }
}
```

**Dissecting the Example**

1.  We declare a variable `x` of type `u32` (an unsigned 32-bit integer) and initialize it to `10`. Unsigned integers can only hold non-negative values.
2.  The first condition `if x > 0` (evaluating `10 > 0`) is `true`.
3.  Consequently, the code inside this `if` block, `println!("x > 0");`, is executed, and "x > 0" is printed to the console.
4.  Since the first condition was met, the subsequent `else if` and `else` blocks are skipped entirely.

**A Note on Types and Compiler Warnings:** In this example, `x` is a `u32`. Because `u32` represents unsigned integers (0 and positive values), the condition `x < 0` can never be true. The Rust compiler is intelligent enough to recognize this and will typically issue a warning, such as "warning: comparison is useless due to type limits". This indicates that the `else if x < 0` branch is logically unreachable with a `u32` type.

## Leveraging `if/else` as Expressions in Rust

A particularly powerful and idiomatic feature in Rust is that `if/else` constructs are expressions, not just statements. This means they can evaluate to a value, which can then be directly assigned to a variable. This capability often leads to more concise and readable code.

**The Concept: Returning Values from `if/else`**

You can use an `if/else` block to determine the value assigned to a variable. A critical rule here is that *all branches* of the `if/else` expression (i.e., the `if` block, any `else if` blocks, and the `else` block) must return a value of the *same type*. If the types are inconsistent, the compiler will raise an error.

**Syntax for `if/else` Expressions**

When using `if/else` to assign a value, the syntax is as follows:

```rust
let variable_name = if condition {
    value_if_true // Note: No semicolon here
} else if another_condition {
    value_if_another_true // No semicolon here
} else {
    value_if_false // No semicolon here
}; // Semicolon here, for the 'let' statement
```

Observe the absence of semicolons after the values (`value_if_true`, etc.) within each block when the block is intended to return that value. The semicolon appears only at the end of the entire `let` statement.

**Example: Assigning a Value Conditionally**

Let's modify our previous example. We'll keep the variable `x` (a `u32`) and use an `if/else` expression to assign a value to a new variable `z` (an `i32` - a signed 32-bit integer) based on `x`'s value.

```rust
// examples/if_else.rs
#![allow(unused)]

fn main() {
    let x: u32 = 10;

    // This is the original if-else from the previous example.
    // It's included here to match the video's progression but can be removed
    // if only the expression-based assignment is needed.
    if x > 0 {
        println!("x > 0 (from basic if-else, first check)");
    } else if x < 0 {
        println!("x < 0 (from basic if-else, first check)");
    } else {
        println!("x = 0 (from basic if-else, first check)");
    }

    // if-else as an expression
    let z: i32 = if x > 0 {
        println!("x > 0 (evaluating for z assignment)"); // This line also executes
        1  // Value returned for z if x > 0
    } else if x < 0 {
        println!("x < 0 (evaluating for z assignment)");
        -1 // Value returned for z if x < 0
    } else {
        println!("x = 0 (evaluating for z assignment)");
        0  // Value returned for z if x is 0
    }; // Semicolon for the `let z` statement

    println!("z = {}", z);
}
```

**Understanding the Expression**

1.  A new variable `z` of type `i32` (a signed integer, which can be positive, negative, or zero) is declared.
2.  The `if/else` block on the right-hand side of the `=` determines the value for `z`.
3.  Since `x` is `10`, the `x > 0` condition is true.
4.  The first block is evaluated:
    *   `println!("x > 0 (evaluating for z assignment)");` executes, printing its message.
    *   Then, the value `1` is the last expression in this block. Because it doesn't have a semicolon, it becomes the value that this block yields.
5.  This yielded value `1` is assigned to `z`.
6.  Finally, `println!("z = {}", z);` will output "z = 1".

The console output, following the video, would show the `println!` from the first basic `if/else` and then the `println!` from within the `if/else` expression block before showing the final `z` value.

**Crucial Points on Semicolons and Return Values:**

*   **Implicit Return from Blocks:** The values `1`, `-1`, and `0` at the end of their respective blocks do *not* have semicolons. This is critical. In Rust, the last expression in a block, if not followed by a semicolon, is the value that the block evaluates to. If a semicolon were added (e.g., `1;`), `1` would become a statement, and the block would implicitly return `()` (the unit type). This would cause a type mismatch error because `z` expects an `i32`, not `()`.
*   **Semicolon for `let` Statement:** The entire `if/else` expression, when used in an assignment, is part of a `let` statement. Therefore, a semicolon is required at the very end (after the closing brace `}` of the final `else` block) to terminate the `let z = ...;` statement.
*   **Avoid the `return` Keyword Here:** It's vital *not* to use the `return` keyword (e.g., `return 1;`) inside these blocks if your goal is for the `if/else` expression to yield a value for the assignment. Using `return 1;` would attempt to return `1` from the entire `main` function (or whatever function this code is in), not just from the `if` block to the `z` variable. This would likely lead to a type error if the function's return type doesn't match. To have the block yield a value for the expression, simply state the value as the last expression in the block without a trailing semicolon.

## Key Considerations and Best Practices for Rust `if/else`

To use `if/else` effectively and idiomatically in Rust, keep these important concepts and syntax rules in mind:

**1. `if/else` is an Expression**
Unlike in some other languages where `if/else` is purely a statement for control flow, in Rust, it's an expression. This means it evaluates to a value, allowing for elegant assignments like `let result = if condition { val_a } else { val_b };`.

**2. Implicit Return from Blocks**
The last expression in any Rust block (a sequence of code enclosed in `{}`) is implicitly returned as the value of that block, *provided it does not end with a semicolon*. This is the mechanism that allows `if/else` branches to yield values.

**3. Type Consistency Across Branches**
When using `if/else` as an expression to assign a value, all possible branches (the `if` block, all `else if` blocks, and the `else` block) must evaluate to values of the *same type*. If they don't, the Rust compiler will report a type mismatch error. For example, you cannot have one branch return an integer and another return a string if you're trying to assign the result to a single variable.

**4. Semicolon Placement is Crucial**
*   **Omit semicolons** on the value-producing expression at the end of a block if that block is part of an `if/else` expression used to yield a value (e.g., `1` not `1;` inside the block).
*   **Include a semicolon** at the end of a `let` statement, even if that statement uses an `if/else` expression for assignment (e.g., `let result = if condition { value_a } else { value_b };`).

**5. No Parentheses Around Conditions**
Rust's `if` conditions do not require being enclosed in parentheses. You should write `if x > 0` instead of `if (x > 0)`. While parentheses can be used for grouping complex logical operations within the condition itself (e.g., `if (x > 0 && y < 10) || z == 0`), they are not needed to merely wrap the entire condition.

**6. Curly Braces are Mandatory**
The blocks of code associated with `if`, `else if`, and `else` must *always* be enclosed in curly braces `{}`. This is true even if the block contains only a single line of code. This rule enhances clarity and helps prevent common bugs found in languages that allow optional braces.

```rust
// Correct:
if x > 5 {
    println!("x is greater than 5");
}

// Also correct (single line, but braces still required):
if x < 0 { println!("x is negative"); }

// Incorrect (will not compile):
// if x > 5 println!("x is greater than 5");
```

**7. The `return` Keyword's Behavior**
Be very mindful of the `return` keyword. If you use `return some_value;` inside an `if/else` *expression* that's part of an assignment (like `let z = if ...`), it will cause the entire enclosing function (e.g., `main`) to attempt to return `some_value`. It does *not* just yield `some_value` for the `if/else` expression itself. To make an `if/else` block yield a value for the expression, ensure that value is the last item in the block and that it does not have a semicolon.

## Understanding Rust's Basic `loop`: Infinite Iteration and Control

In Rust, the most fundamental way to create a repetitive block of code is with the `loop` keyword. By default, this construct creates an infinite loop, continuously executing the code within its block.

Consider this initial example:
```rust
fn main() {
    loop {
        println!("loop");
    }
}
```
If you compile and run this program, it will print "loop" to your terminal indefinitely. You'll need to manually stop it, typically using Ctrl+C.

While infinite loops have their uses (e.g., in servers or embedded systems waiting for events), most practical scenarios require loops that eventually terminate. To achieve this with the `loop` keyword, we introduce a counter and a `break` statement. The `break` keyword immediately exits the current loop.

Let's see how to control a `loop`:
```rust
fn main() {
    let mut i = 0; // Declare a mutable counter, initialized to 0
    loop {
        println!("loop {}", i); // Print the current value of the counter
        i += 1; // Increment the counter

        if i > 5 { // Condition to exit the loop
            break;     // Execute break to exit the loop
        }
    }
    // Execution continues here after the loop breaks
    println!("Loop finished.");
}
```
In this revised example:
*   `let mut i = 0;`: We declare a variable `i` and mark it as `mut` (mutable) because its value will change within the loop.
*   `i += 1;`: In each iteration, we increment `i`.
*   `if i > 5 { break; }`: This is our termination condition. When `i` becomes 6 (i.e., `i > 5` is true), the `break` statement is executed, and the loop stops.

The output of this controlled loop will be:
```
loop 0
loop 1
loop 2
loop 3
loop 4
loop 5
Loop finished.
```
The loop executes for `i` values from 0 up to and including 5. Once `i` is 5, "loop 5" is printed, `i` increments to 6, the condition `i > 5` becomes true, and the loop terminates.

## Conditional Execution: Mastering the `while` Loop in Rust

Another common way to control loop execution is with a `while` loop. A `while` loop continues to execute its block of code as long as a specified boolean condition remains true. The condition is checked *before* each iteration.

Here's an example that achieves the same outcome as our previous controlled `loop`:
```rust
fn main() {
    let mut i = 0; // Re-initialize or use a new counter
    while i <= 5 { // Loop continues as long as i is less than or equal to 5
        println!("while loop {}", i);
        i += 1; // Increment the counter
    }
    println!("While loop finished.");
}
```
The `while i <= 5` line dictates that the loop will run as long as `i` is less than or equal to 5. Once `i` becomes 6, the condition `6 <= 5` evaluates to false, and the loop terminates.

The output will be:
```
while loop 0
while loop 1
while loop 2
while loop 3
while loop 4
while loop 5
While loop finished.
```

## Effortless Iteration: Exploring `for` Loops and Ranges in Rust

Rust's `for` loop is particularly well-suited for iterating over a sequence of items, such as a range of numbers or the elements within a collection. It's often considered more idiomatic and safer than manual index management with `loop` or `while` for these tasks.

To iterate a specific number of times, you can use a `for` loop with a range:
```rust
fn main() {
    for i in 0..6 { // Iterates from 0 up to (but not including) 6
        println!("for loop {}", i);
    }
    println!("For loop (exclusive range) finished.");

    // For an inclusive range (0 to 5 inclusive):
    for i in 0..=5 {
        println!("for loop inclusive {}", i);
    }
    println!("For loop (inclusive range) finished.");
}
```
*   `0..6`: This creates a range that starts at 0 and goes up to, but does not include, 6. So, it includes the numbers 0, 1, 2, 3, 4, and 5.
*   `0..=5`: This syntax creates an inclusive range, meaning it includes 0, 1, 2, 3, 4, and 5.

The output for the first `for` loop (`0..6`):
```
for loop 0
for loop 1
for loop 2
for loop 3
for loop 4
for loop 5
For loop (exclusive range) finished.
```
And for the second `for` loop (`0..=5`):
```
for loop inclusive 0
for loop inclusive 1
for loop inclusive 2
for loop inclusive 3
for loop inclusive 4
for loop inclusive 5
For loop (inclusive range) finished.
```
Both produce the same sequence of numbers in this specific case.

## Iterating Over Arrays in Rust: Indexing vs. Direct Access

Arrays in Rust are fixed-size collections of elements of the same type. `for` loops provide convenient ways to iterate through them.

First, let's declare an array:
```rust
let arr = [10, 20, 30, 40, 50];
```

**Method 1: Index-based `for` loop**

You can iterate over an array using its indices, similar to how you might in other languages.
```rust
fn main() {
    let arr = [1, 2, 3, 4, 5];
    let n: usize = arr.len(); // Get the length of the array.

    for i in 0..n { // Iterate from index 0 to n-1
        println!("arr index: {}, value: {}", i, arr[i]); // Access element by index
    }
}
```
*   `arr.len()`: This method returns the number of elements in the array.
*   `let n: usize`: The length of an array (and indices) in Rust is of type `usize`. This type is platform-dependent and large enough to represent the size of any collection in memory.
*   `arr[i]`: This syntax accesses the element at index `i` in the array.

The output will be:
```
arr index: 0, value: 1
arr index: 1, value: 2
arr index: 2, value: 3
arr index: 3, value: 4
arr index: 4, value: 5
```

**Method 2: Direct Iteration over Elements (More Idiomatic Rust)**

A more Rusty and often preferred way to iterate over an array is to directly access its elements:
```rust
fn main() {
    let arr = [1, 2, 3, 4, 5];

    for element_value in arr { // Iterates directly over the values in 'arr'
        println!("arr value: {}", element_value);
    }
}
```
This loop iterates through each element of `arr`, assigning its value to `element_value` in each iteration. For arrays containing simple types (like integers) that implement the `Copy` trait, this iteration behaves as if it's working on copies of the elements, and the original array remains usable.

The output for this method:
```
arr value: 1
arr value: 2
arr value: 3
arr value: 4
arr value: 5
```
This direct iteration is generally less error-prone as it avoids manual index management and potential off-by-one errors.

## Working with Vectors: Rust's `for` Loop, Ownership, and `iter()`

Vectors (`Vec<T>`) are dynamically-sized, growable collections in Rust, akin to arrays that can change their size. Iterating over vectors introduces an important Rust concept: ownership.

Let's declare a vector:
```rust
let v = vec![10, 20, 30, 40, 50];
```

**Direct Iteration and Ownership**

If you iterate over a vector directly using a `for` loop like this:
```rust
fn main() {
    let v = vec![10, 20, 30, 40, 50];

    // First loop:
    for n_val in v { // This loop takes ownership of 'v'
        println!("vec {}", n_val);
    }

    // Attempting to use 'v' again will cause a compile-time error:
    // println!("Vector length after loop: {}", v.len()); // ERROR: value used here after move
    // for n_val in v { // ERROR: value used here after move
    //     println!("vec again {}", n_val);
    // }
}
```
When you write `for n_val in v`, Rust implicitly calls a method called `into_iter()` on the vector `v`. The `into_iter()` method consumes the vector, taking ownership of it. This means that after the loop finishes, the vector `v` is no longer valid in the current scope; it has been "moved" into the loop and dropped (its memory deallocated) when the loop concludes. Any attempt to use `v` after this loop will result in a compile-time "value used here after move" error, a key safety feature of Rust preventing use-after-free bugs.

The output of the first (and only successful) loop:
```
vec 10
vec 20
vec 30
vec 40
vec 50
```

**Iterating Multiple Times using `.iter()` (Borrowing)**

If you need to iterate over a vector multiple times, or use the vector after the loop, you must borrow it instead of letting the loop consume it. This is done using the `.iter()` method.
```rust
fn main() {
    let v = vec![10, 20, 30, 40, 50];

    // First loop using .iter()
    for n_val_ref in v.iter() { // '.iter()' borrows 'v'
        println!("vec ref {}", n_val_ref); // n_val_ref is a reference (e.g., &i32)
    }

    // Second loop using .iter() - this is now allowed because 'v' was only borrowed
    for n_val_ref in v.iter() {
        println!("vec ref again {}", n_val_ref);
    }

    println!("Vector is still valid, length: {}", v.len());
}
```
*   `v.iter()`: This method returns an iterator that yields *references* to the elements in the vector (e.g., `&i32` if `v` contains `i32`). The original vector `v` is only borrowed for the duration of the loop and remains valid and owned by its original scope.
*   Because `n_val_ref` is a reference, if you need the actual value, you might need to dereference it (e.g., `*n_val_ref`), though `println!` often handles this automatically for display purposes.

The output will be:
```
vec ref 10
vec ref 20
vec ref 30
vec ref 40
vec ref 50
vec ref again 10
vec ref again 20
vec ref again 30
vec ref again 40
vec ref 50
Vector is still valid, length: 5
```
Understanding the distinction between `into_iter()` (takes ownership) and `iter()` (borrows) is crucial for working effectively with collections in Rust. If you need to modify the elements within the loop, you would use `.iter_mut()`, which provides mutable references.

## Powerful Loops: Returning Values from `loop` Expressions in Rust

In Rust, many constructs are expressions, meaning they evaluate to a value. This includes the basic `loop` construct. You can use a `loop` to compute a value and return it, which can then be assigned to a variable.

The value to be returned from the loop is specified after the `break` keyword.
```rust
fn main() {
    let mut i = 0;
    let result_string: &str = loop { // The loop expression is assigned to 'result_string'
        println!("loop computation {}", i);
        i += 1;
        if i > 5 {
            break "loop computation ends here"; // Return this string literal
        }
    }; // Note the semicolon: `let ... = loop { ... };` is a statement.

    println!("Loop returned: {}", result_string);
}
```
Key points in this example:
*   `let result_string: &str = loop { ... };`: The entire `loop { ... }` block is an expression. Its resulting value is assigned to `result_string`.
*   The type of `result_string` is explicitly annotated as `&str` (a string slice reference) because the loop is set up to return a string literal. Rust can often infer this, but explicit annotation is good practice here.
*   `break "loop computation ends here";`: When `i` exceeds 5, the loop terminates. The `break` statement not only exits the loop but also provides the value `"loop computation ends here"`, which becomes the result of the entire `loop` expression.
*   Semicolon: Since `let result_string = ...;` is a statement, the `loop` block (when used as an expression in an assignment) must be followed by a semicolon.

The output of this code will be:
```
loop computation 0
loop computation 1
loop computation 2
loop computation 3
loop computation 4
loop computation 5
Loop returned: loop computation ends here
```
This ability for `loop` to return values allows for concise and expressive code, especially when a loop's primary purpose is to compute a result that's needed afterwards. Remember that only the `loop` keyword supports returning values with `break`; `while` and `for` loops do not directly return values in this manner (they evaluate to `()`, the unit type).

## Mastering Rust's `match` Control Flow

In Rust, control flow is not just about `if/else` statements and loops. One of the most powerful and frequently used constructs is the `match` keyword. While it may look like a `switch` statement from other languages, `match` is a far more capable expression that enables robust pattern matching, ensuring you handle every possible case, which is a cornerstone of Rust's safety guarantees.

### Basic `match` Syntax

At its core, `match` allows you to compare a value against a series of patterns. When it finds a matching pattern, it executes the code associated with that pattern. Each pattern and its associated code is called an "arm."

Let's look at a basic example. Here, we want to perform a different action based on the value of an integer `x`.

```rust
fn main() {
    let x = 1;

    match x {
        1 => println!("one"),
        2 => println!("two"),
        3 => println!("three"),
    }
}
```

In this snippet, we are matching on the value of `x`. The `match` expression checks each arm in order. Since `x` is `1`, it matches the first arm, `1 => println!("one")`, and the program prints "one".

### The Rule of Exhaustiveness

If you try to compile the code above as-is, you will encounter a compiler error. This is because `match` in Rust must be **exhaustive**. This means you must provide an arm for every possible value that the type can hold. Our variable `x` is an `i32` (a 32-bit integer), but we've only handled the values 1, 2, and 3.

The compiler will stop you with a helpful message:

```
error[E0004]: non-exhaustive patterns: `i32::MIN..=0_i32` and `4_i32..=i32::MAX` not covered
 --> src/main.rs:5:11
  |
5 |     match x {
  |           ^ patterns `i32::MIN..=0_i32` and `4_i32..=i32::MAX` not covered
```

To satisfy the compiler and make our code robust, we need a way to handle all other possible values. This is done using the special wildcard pattern `_`, which acts as a catch-all.

```rust
fn main() {
    let x = 5; // Changed to demonstrate the catch-all

    match x {
        1 => println!("one"),
        2 => println!("two"),
        3 => println!("three"),
        // The wildcard `_` handles all other possible values.
        _ => println!("others"),
    }
}
```

Now, if `x` is any value other than 1, 2, or 3, the final arm will execute, printing "others". This exhaustiveness check is a key feature that prevents bugs by forcing you to consider all outcomes.

### Advanced Pattern Matching

The power of `match` extends beyond simple value checks. You can match against multiple values, ranges, and even bind the matched value to a new variable for use within the arm's expression.

#### Matching Multiple Values and Ranges

You can make a single arm handle several patterns by using the `|` (OR) operator. To match against a continuous sequence of values, you can use the inclusive range syntax `..=`.

```rust
fn main() {
    let x = 7;

    match x {
        // This arm matches if x is 1, 2, OR 3.
        1 | 2 | 3 => println!("1, 2, or 3"),
        // This arm matches any number from 4 to 10, inclusive.
        4..=10 => println!("4 to 9"),
        _ => println!("others"),
    }
}
```

In this example, since `x` is `7`, it falls into the `4..=10` range, and the program will print "4 to 9".

#### Binding Matched Values with `@`

Sometimes you want to match against a range but also need to use the specific value that was matched. You can bind the value to a variable using the `@` symbol.

```rust
fn main() {
    let x = 10;
    match x {
        // 'i' will be bound to the value of x if it's in the range 1..=10.
        i @ 1..=10 => println!("1 to 10: found {}", i),
        _ => println!("others"),
    }
}
```

Here, `x` matches the range `1..=10`. The value of `x` (which is 10) is bound to the variable `i`, which we can then use in our `println!` macro. The output will be: `1 to 10: found 10`.

### Common Use Cases: Handling `Option` and `Result`

The most idiomatic and powerful use of `match` is for handling enums, especially the standard library's `Option<T>` and `Result<T, E>` types. `match` forces you to handle every variant of the enum, making your code safer.

#### Matching `Option<T>`

An `Option` can either be `Some(value)`, containing a value, or `None`, indicating the absence of a value. `match` is the perfect tool for safely unwrapping it.

```rust
fn process_optional(x: Option<i32>) {
    match x {
        // If x is Some, the inner value is bound to `val`.
        Some(val) => println!("Option contains the value: {val}"),
        // Handles the case where x is None.
        None => println!("Option is None"),
    }
}

fn main() {
    process_optional(Some(9));
    process_optional(None);
}
```

#### Matching `Result<T, E>`

Similarly, a `Result` represents either success, `Ok(value)`, or failure, `Err(error)`. Using `match` is the canonical way to handle both outcomes explicitly.

```rust
fn process_result(res: Result<i32, String>) {
    match res {
        // Handles the success case and binds the value to `val`.
        Ok(val) => println!("Success! The value is {val}"),
        // Handles the error case and binds the error to `err`.
        Err(err) => println!("Error: {err}"),
    }
}

fn main() {
    process_result(Ok(123));
    process_result(Err("failed to process data".to_string()));
}
```

### Using `match` as an Expression

In Rust, most control flow constructs are expressions, meaning they evaluate to a value. This is true for `match` as well. You can use a `match` block to determine the value of a variable. The value returned is the result of the expression from the arm that executes.

This is extremely useful for transforming data or providing default values.

```rust
fn main() {
    let x: Option<i32> = Some(9);
    // let x: Option<i32> = None; // Try uncommenting this line

    // The result of the match block is assigned to `z`.
    let z: i32 = match x {
        Some(val) => val, // If Some, return the inner value.
        None      => 0,   // If None, return a default value of 0.
    };

    println!("The value of z is: {z}");
}
```

If `x` is `Some(9)`, the first arm executes, and the expression `val` (which is 9) is returned and assigned to `z`. If `x` were `None`, the second arm would execute, returning `0`. This pattern provides a clean and safe way to get a value out of an `Option`, with a fallback for the `None` case.
