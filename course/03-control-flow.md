# Rust Programming: Control Flow and Loops

## Table of Contents
1. [Conditional Expressions](#conditional-expressions)
2. [Loops](#loops)
3. [Pattern Matching](#pattern-matching)
4. [If Let](#if-let)

---

## Conditional Expressions

### Basic If/Else Syntax

```rust
let number = 6;

if number < 5 {
    println!("condition was true");
} else {
    println!("condition was false");
}
```

### If as Expression Returning Values

In Rust, `if/else` is an expression that can return values, but both branches must return the same type:

```rust
let condition = true;
let number = if condition { 5 } else { 6 };

println!("The value of number is: {}", number);
```

**Important Rules:**
- Both branches must return the same type
- Don't use semicolon after the expression if you want it to return a value
- The type consistency is enforced at compile time

---

## Loops

### 1. Infinite Loop

```rust
loop {
    println!("again!");
    break; // Use break to exit the loop
}
```

### Returning Values from Loop

The `loop` expression can return values:

```rust
let mut counter = 0;

let result = loop {
    counter += 1;

    if counter == 10 {
        break counter * 2;
    }
};

println!("The result is {}", result);
```

### 2. While Loop

```rust
let mut number = 3;

while number != 0 {
    println!("{}!", number);
    number -= 1;
}

println!("LIFTOFF!!!");
```

### 3. For Loop with Ranges

#### Using Range Patterns

```rust
// Exclusive range (1..5 = 1, 2, 3, 4)
for i in 1..5 {
    println!("{}!", i);
}

// Inclusive range (1..=5 = 1, 2, 3, 4, 5)
for i in 1..=5 {
    println!("{}!", i);
}
```

#### Iterating Over Collections

```rust
let a = [10, 20, 30, 40, 50];

for element in a {
    println!("the value is: {}", element);
}
```

### Iteration: Indexing vs. Direct Access

#### Method 1: Index-Based Iteration

```rust
let v = vec![1, 2, 3];

for i in 0..v.len() {
    println!("{}", v[i]);
}
```

**Characteristics:**
- Uses numeric indices to access elements
- Explicit control over iteration position
- Can access elements out of order if needed
- **Performance**: Same as direct iteration in most cases, but with slightly more complex code

#### Method 2: Direct Iteration (Idiomatic Rust)

```rust
let v = vec![1, 2, 3];

for element in v {
    println!("{}", element);
}
```

**Why Direct Iteration is Preferred:**
- **Readability**: More expressive and clearer intent - "for each element"
- **Safety**: No risk of index out-of-bounds errors
- **Simplicity**: Less boilerplate, more concise
- **Idiomatic**: Follows Rust community conventions and best practices
- **Performance**: Compiler optimizations make it equally efficient
- **Ownership**: Works naturally with Rust's ownership system

#### Method 3: Borrowing with .iter()

```rust
let v = vec![1, 2, 3];

for element in v.iter() {
    println!("{}", element);
}
```

**When to Use .iter():**
- **Multiple iterations**: Need to iterate over the same vector multiple times
- **Preserve ownership**: Want to keep the vector intact after iteration
- **Immutable access**: Only need to read elements, not modify them

**Key Differences:**
- `into_iter()` (implicit in direct iteration): Takes ownership - the vector is consumed
- `.iter()`: Borrows references - the vector remains available for further use
- Index-based: Can be less safe and more verbose, but offers explicit index control

### Iteration Guidelines

**Use Index-Based When:**
- You need the actual index value during iteration
- You need to access elements out of order
- You're working with APIs that require indices

**Use Direct Iteration When:**
- You simply need to process each element in sequence
- You want idiomatic, readable Rust code
- You're working with standard collection iteration patterns

**Use .iter() When:**
- You need to iterate multiple times over the same collection
- You want to preserve the collection for later use
- You only need immutable access to elements

---

## Pattern Matching

### Basic Match Expression

```rust
let number = 3;

match number {
    1 => println!("One"),
    2 => println!("Two"),
    3 => println!("Three"),
    _ => println!("Other"),
}
```

### Exhaustiveness Requirement

`match` must handle all possible values. Use `_` as a wildcard for remaining cases:

```rust
let number = 7;

match number {
    1 => println!("One"),
    _ => println!("Not one"),
}
```

**Why This Rule Exists:**
- **Safety**: Prevents runtime crashes from unhandled cases
- **Clarity**: Forces explicit consideration of all possibilities
- **Maintainability**: Code must be updated when new cases are added
- **Documentation**: Serves as self-documenting code showing intended behavior

### Matching Ranges

```rust
let number = 5;

match number {
    1..=5 => println!("Between 1 and 5"),
    _ => println!("Other"),
}
```

### Binding with @

```rust
let age = 25;

match age {
    0 => println!("Just born"),
    n @ 1..=12 => println!("Child of age {}", n),
    n @ 13..=19 => println!("Teenager of age {}", n),
    n => println!("Adult of age {}", n),
}
```

### Handling Option Type

```rust
let some_value = Some(5);

match some_value {
    Some(x) => println!("Got value: {}", x),
    None => println!("No value"),
}
```

### Handling Result Type

```rust
let result: Result<i32, &str> = Ok(100);

match result {
    Ok(value) => println!("Success: {}", value),
    Err(error) => println!("Error: {}", error),
}
```

---

## If Let: Concise Pattern Matching

### When to Use If Let

Use `if let` when you only care about one pattern and want to ignore others:

```rust
let some_value = Some(5);

if let Some(x) = some_value {
    println!("Got value: {}", x);
} else {
    println!("No value");
}
```

### Comparison with Match

**Match approach:**
```rust
match some_value {
    Some(x) => println!("Got value: {}", x),
    _ => println!("No value"),
}
```

**If let approach (more concise for single pattern):**
```rust
if let Some(x) = some_value {
    println!("Got value: {}", x);
}
```

**Why Use If Let:**
- **Conciseness**: Reduces boilerplate when only one pattern matters
- **Readability**: Clearer intent - "if this pattern matches, do X"
- **Maintainability**: Easier to add additional patterns later if needed
- **Idiomatic**: Preferred pattern for single-case matching in Rust

**When to Stick with Match:**
- Multiple patterns need different handling
- You need the compiler's exhaustiveness checking
- All cases are equally important

### Practical Example

```rust
let mut optional_value = Some(0);

while let Some(i) = optional_value {
    if i > 5 {
        optional_value = None;
    } else {
        println!("i is {:?}", i);
        optional_value = Some(i + 1);
    }
}
```

---

## Key Takeaways

1. **If/Else Expressions**: Can return values but require type consistency across all branches
2. **Loop Types**: Use `loop` for infinite loops with optional return values, `while` for conditional loops, `for` for iteration
3. **Iteration Patterns**: Direct iteration is idiomatic Rust, but all methods have their use cases
4. **Match**: Must be exhaustive, supports ranges, binding with `@`, and handles `Option`/`Result` types elegantly
5. **If Let**: Concise alternative to `match` when you only care about one specific pattern
6. **Ownership**: Be mindful of ownership during iteration - use `.iter()` to borrow instead of consume
7. **Best Practices**: Follow Rust idioms for readability and safety, but understand when alternatives are appropriate