# Rust Programming Core Concepts Summary

## 1. Scalar Data Types

### Integers - Whole Numbers

**Signed Integers (i8, i16, i32, i64, i128)**
- Can hold both positive and negative values
- Range: `-(2^(n-1))` to `2^(n-1) - 1`
- `i32` is the default when no type is specified

```rust
let i0: i8 = -1;      // Range: -128 to 127
let i1: i16 = 2;      // Range: -32,768 to 32,767
let i2: i32 = 3;      // Range: -2,147,483,648 to 2,147,483,647
let i3: i64 = -4;     // Range: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
let i4: i128 = 5;     // A very large range
```

**Unsigned Integers (u8, u16, u32, u64, u128)**
- Can only hold non-negative values (zero and positive)
- Range: `0` to `2^n - 1`

```rust
let u0: u8 = 1;       // Range: 0 to 255
let u1: u16 = 2;      // Range: 0 to 65,535
let u2: u32 = 3;      // Range: 0 to 4,294,967,295
let u3: u64 = 4;      // Range: 0 to 18,446,744,073,709,551,615
let u4: u128 = 5;     // A very large range, up to 2^128 - 1
```

**Architecture-Dependent Integers**
- `isize`: signed integer matching pointer size
- `usize`: unsigned integer matching pointer size
- `usize` is used for indexing collections

```rust
let i5: isize = -6; // Will be i32 or i64
let u5: usize = 6;  // Will be u32 or u64
```

### Floating-Point Numbers

- `f32`: single-precision (32 bits)
- `f64`: double-precision (64 bits) - **default**
- Follow IEEE 754 standard

```rust
let f0: f32 = 0.01;
let f1: f64 = 0.02; // f64 is the default if not specified
```

### Boolean Type

- `bool` type with only two values: `true` or `false`
- Occupies one byte in memory

```rust
let b: bool = true;
let is_active: bool = false;
```

### Character Type

- `char` represents a single Unicode Scalar Value
- Uses single quotes `'` for character literals
- Four bytes in size
- Can hold accented letters, emojis, and global language characters

```rust
let c: char = 'c';
let z: char = 'ℤ';
let heart: char = '❤';
let e: char = '🦀'; // Emojis are valid char values
```

### Type Conversion with `as`

- Rust requires explicit type conversion using `as` keyword
- No implicit conversions between primitive types
- Converting between signed and unsigned can reinterpret bit patterns

```rust
let i: i32 = -1;
let u: u32 = i as u32; // Explicit conversion from i32 to u32
// Result: (-1) as u32 = (4294967295)
```

### Numeric Type Limits

- Use `MIN` and `MAX` constants to find type bounds

```rust
let i_max: i32 = i32::MAX;
let u_min: u32 = u32::MIN;
// i32 max: 2147483647
// u32 min: 0
```

## 2. Integer Overflow Handling

### Default Behavior: Debug vs Release Mode

**Debug Mode** (default during development):
- Panics on overflow to catch bugs early
- Example: `u32::MAX + 1` causes panic

```rust
let mut x = u32::MAX;
println!("Initial x: {}", x);
x += 1; // Panics in debug mode
```

**Release Mode** (`--release` flag):
- Wraps around using two's complement
- `u32::MAX + 1` becomes `0`

```rust
let mut x = u32::MAX;
println!("Initial x: {}", x);
x += 1; // Wraps to 0 in release mode
println!("u32 max: {}, x after increment: {}", u32::MAX, x);
```

### Explicit Overflow Methods

**`checked_add`** - Returns `Option<T>`:
- `Some(result)` if no overflow
- `None` if overflow occurs

```rust
let result_overflow = u32::checked_add(u32::MAX, 1);
println!("checked_add(u32::MAX, 1): {:?}", result_overflow); // None

let result_valid = u32::checked_add(3, 1);
println!("checked_add(3, 1): {:?}", result_valid); // Some(4)
```

**`wrapping_add`** - Always wraps:
- Explicit wrapping behavior regardless of compilation mode
- Returns the result directly

```rust
let result_wrap = u32::wrapping_add(u32::MAX, 1);
println!("wrapping_add(u32::MAX, 1): {}", result_wrap); // 0

let result_valid = u32::wrapping_add(3, 1);
println!("wrapping_add(3, 1): {}", result_valid); // 4
```

## 3. Tuples

### Characteristics
- **Fixed size**: Cannot change after declaration
- **Mixed types**: Elements can be different types
- **Known at compile time**: Size and types must be determined at compilation

### Creating Tuples

```rust
let t: (bool, char, u32) = (true, 'a', 1);
```

### Accessing Elements
- Use dot notation with zero-based indices

```rust
println!("{}, {}, {}", t.0, t.1, t.2); // true, a, 1
```

### Empty Tuple (Unit Type)
- `()` represents the unit type
- Similar to `void` in other languages
- Used for functions that don't return meaningful values

```rust
let t = (); // Type is ()
```

### Nested Tuples
- Tuples can contain other tuples

```rust
let nested = (('a', 1.23), (true, 1u32, -1i32), ());
println!("nested.0.1: {}", (nested.0).1); // 1.23
```

### Destructuring
- Break tuple apart into separate variables

```rust
let t: (bool, char, u32) = (true, 'a', 1);
let (a, b, c) = t;
println!("a = {}, b = {}, c = {}", a, b, c); // a = true, b = a, c = 1
```

### Partial Destructuring
- Use `_` to ignore values

```rust
let t: (bool, char, u32) = (true, 'a', 1);
let (_, b, _) = t; // Only capture the second element
```

### Functions Returning Multiple Values
- Functions can return tuples to return multiple values

```rust
fn return_many() -> (u32, bool) {
    (1u32, true)
}

let (num_value, bool_value) = return_many();
```

## 4. Arrays vs Slices

### Arrays
- **Fixed length** known at compile time
- Type signature: `[T; N]` where T is element type and N is length
- Efficient stack allocation

```rust
let arr: [u32; 3] = [1, 2, 3];
println!("arr[0]: {}", arr[0]); // 1
```

### Mutable Arrays
- Use `mut` keyword to allow modification

```rust
let mut arr: [u32; 3] = [1, 2, 3];
arr[1] = 99;
// println!("{:?}", arr); // [1, 99, 3]
```

### Array Initialization with Default Value
- `[value; count]` creates array with repeated values

```rust
let arr: [u32; 10] = [0; 10];
// println!("arr: {:?}", arr); // [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

### Slices
- **Dynamic length** determined at runtime
- References to contiguous sequences in collections
- Type: `&[T]` for immutable slices
- Syntax: `&array[start_index..end_index]` (start inclusive, end exclusive)

```rust
let nums: [i32; 10] = [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5];
let s: &[i32] = &nums[0..3]; // First 3 elements: [-1, 1, -2]
let s: &[i32] = &nums[7..10]; // Last 3 elements: [4, -5, 5]
let s: &[i32] = &nums[3..7]; // Middle 4 elements: [2, -3, 3, -4]
// println!("mid 4: {:?}", s); // mid 4: [2, -3, 3, -4]
```

### Slice Syntax Shorthands
- `&array[..end_index]` - from beginning to end_index
- `&array[start_index..]` - from start_index to end
- `&array[..]` - entire array

```rust
let s: &[i32] = &nums[..3]; // Same as &nums[0..3]
let s: &[i32] = &nums[7..]; // Same as &nums[7..10]
```

## 5. Strings: `String` vs `&str`

### `String` (Owned)
- **Heap-allocated** and owned data
- **Growable and modifiable**
- Used when ownership or modification is needed

```rust
let msg: String = String::from("Hello Rust");
let msg: String = "Hello Rust".to_string();
let length: usize = msg.len(); // 10 (number of bytes)
```

### `&str` (String Slice)
- **Borrowed reference** to UTF-8 bytes
- **Immutable**
- Used for read-only access
- String literals are `&'static str`

```rust
let s: &str = "Hello World"; // String literal
let msg: String = String::from("Hello Rust");
let s: &str = &msg; // Reference to entire String
let s: &str = &msg[0..5]; // Slice: "Hello"
```

### Conversions Between Types

**`&str` to `String`:**
```rust
let s_slice: &str = "Hello World";
let owned_string_v1: String = s_slice.to_string();
let owned_string_v2: String = String::from(s_slice);
```

**`&String` to `&str` (Deref Coercion):**
```rust
fn print_message(s: &str) {
    println!("{}", s);
}

let msg_string: String = String::from("Hello from String");
print_message(&msg_string); // Automatically coerces &String to &str

let s_literal: &str = "Hello from literal";
print_message(s_literal);
```

### String Modification and Construction

**Appending to `String`:**
```rust
let mut msg: String = String::from("Hello Rust");
msg += " World"; // Appends " World"
// Alternatively: msg.push_str(" World");
println!("{}", msg); // Hello Rust World
```

**String Interpolation with `format!`:**
```rust
let name = "Rust";
let version = 1.76;
let emoji = "🦀";

let s: String = format!("Learning {} version {} is fun! {}", name, version, emoji);
println!("{}", s); // Learning Rust version 1.76 is fun! 🦀
```

## 6. Enums

### Defining Custom Enums
- List all possible values (variants)
- Can be simple, tuple-like, or struct-like

```rust
enum Command {
    Play,                      // Simple variant
    Stop,                      // Simple variant
    Skip(u32),                 // Tuple-like variant
    Back(u32),                 // Tuple-like variant
    Resize {                   // Struct-like variant
        width: u32,
        height: u32,
    },
}
```

### Creating Enum Instances

```rust
let cmd: Command = Command::Play;
let cmd: Command = Command::Skip(10); // Skip to timestamp 10
let cmd: Command = Command::Resize { width: 100, height: 50 };
```

### Deriving Traits

**Debug Trait** - enables printing:
```rust
#[derive(Debug)]
enum Command {
    Play,
    Stop,
    Skip(u32),
    Back(u32),
    Resize { width: u32, height: u32 },
}

fn main() {
    let cmd: Command = Command::Resize { width: 100, height: 50 };
    println!("{:?}", cmd); // Resize { width: 100, height: 50 }
}
```

**PartialEq Trait** - enables comparison:
```rust
#[derive(Debug, PartialEq)]
enum Command {
    Play,
    Stop,
    Skip(u32),
    Back(u32),
    Resize { width: u32, height: u32 },
}

fn main() {
    let cmd0: Command = Command::Play;
    let cmd1: Command = Command::Skip(10);
    println!("cmd0 == cmd1: {}", cmd0 == cmd1); // false

    let cmd_skip1: Command = Command::Skip(10);
    let cmd_skip2: Command = Command::Skip(10);
    println!("cmd_skip1 == cmd_skip2: {}", cmd_skip1 == cmd_skip2); // true
}
```

### Standard Library Enums

**`Option<T>`** - represents optional values:
```rust
enum Option<T> {
    Some(T), // Value present
    None,    // Value absent
}

let x: Option<i32> = Some(5);
let y: Option<i32> = None;
let z: Option<f64> = Some(3.14);
let name: Option<String> = None;
```

**`Result<T, E>`** - represents success/failure:
```rust
enum Result<T, E> {
    Ok(T),   // Success with value
    Err(E),  // Failure with error
}

let x: Result<i32, String> = Ok(100);
let y: Result<i32, String> = Err("Failed to parse".to_string());
```

## 7. Structs

### Types of Structs

**Named-Field Structs:**
```rust
struct Point {
    x: i32,
    y: i32,
}
```

**Tuple Structs:**
```rust
struct Point3D(i32, i32, i32);
```

**Unit-like Structs:**
```rust
struct Empty;
```

**Nested Structs:**
```rust
struct Circle {
    radius: u32,
    center: Point, // Nested struct
}
```

### Creating Struct Instances

```rust
let p = Point { x: 1, y: 1 };
let p3d = Point3D(-1, 0, -1);
let empty_instance = Empty;
let circle_instance = Circle {
    radius: 1,
    center: Point { x: 0, y: 0 },
};
```

### Debug Printing
```rust
#[derive(Debug)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 1, y: 1 };
    println!("{:?}", p); // Point { x: 1, y: 1 }
    println!("{:#?}", p); // Pretty-printed
}
```

### Accessing Fields

```rust
let p = Point { x: 1, y: 1 };
println!("x: {}, y: {}", p.x, p.y); // x: 1, y: 1

let p3d = Point3D(-1, 0, -1);
println!("point 3D: ({}, {}, {})", p3d.0, p3d.1, p3d.2); // point 3D: (-1, 0, -1)
```

### Field Init Shorthand
```rust
let x: i32 = 1;
let y: i32 = 1;
let p_short = Point { x, y }; // Short for Point { x: x, y: y }
```

### Struct Update Syntax
```rust
let p0 = Point { x: 1, y: 2 };
let p1 = Point { x: 5, ..p0 }; // x = 5, y copied from p0
```

### Modifying Fields
```rust
let mut p_update = Point { x: 1, y: 1 };
p_update.x += 1;
p_update.y = 99;
```

## 8. Vectors

### Creating Vectors

**Empty vector:**
```rust
let mut v: Vec<i32> = Vec::new();
```

**Adding elements:**
```rust
let mut v: Vec<i32> = Vec::new();
v.push(1);
v.push(2);
v.push(3);
```

**With initial values:**
```rust
let v = vec![1, 2, 3]; // Rust infers Vec<i32>
let v: Vec<i8> = vec![1, 2, 3]; // Explicit type
let v = vec![1u8, 2, 3]; // Type suffix inference
```

**Repeating values:**
```rust
let v: Vec<i8> = vec![0i8; 100]; // 100 zeros
```

### Accessing Elements

**Index notation (unsafe):**
```rust
let v: Vec<i8> = vec![10, 20, 30];
println!("Element at index 1: {}", v[1]); // 20
// v[1000] would panic
```

**`get()` method (safe):**
```rust
let v: Vec<i8> = vec![0i8; 100];
println!("v.get(1): {:?}", v.get(1)); // Some(0)
println!("v.get(1000): {:?}", v.get(1000)); // None
```

### Updating Elements
```rust
let mut v: Vec<i8> = vec![1, 2, 3];
v[0] = 99;
```

### Removing Elements with `pop()`
```rust
let mut v: Vec<i8> = vec![1, 2, 3];
let x1: Option<i8> = v.pop(); // Some(3)
let x2: Option<i8> = v.pop(); // Some(2)
let x3: Option<i8> = v.pop(); // Some(1)
let x4: Option<i8> = v.pop(); // None (empty vector)
```

### Slices from Vectors
```rust
let v = vec![1, 2, 3, 4, 5];
let s: &[i32] = &v[1..4]; // [2, 3, 4]
```

## 9. HashMaps

### Importing and Initializing
```rust
use std::collections::HashMap;

let mut scores: HashMap<String, u32> = HashMap::new();
```

### Inserting Key-Value Pairs
```rust
scores.insert("red".to_string(), 100);
scores.insert("blue".to_string(), 200);
```

### Displaying Contents
```rust
println!("{:#?}", scores);
// {
//     "red": 100,
//     "blue": 200,
// }
```

### Retrieving Values
```rust
let score: Option<&u32> = scores.get("red");
println!("Red score: {:?}", score); // Some(100)

let score: Option<&u32> = scores.get("green");
println!("Green score: {:?}", score); // None
```

### Updating Values with `entry` and `or_insert`
```rust
// Insert "black" with 0 if not exists, then add 100
let score: &mut u32 = scores.entry("black".to_string()).or_insert(0);
*score += 100; // Black score: Some(100)

// Update existing "blue" from 200 to 300
let score: &mut u32 = scores.entry("blue".to_string()).or_insert(0);
*score += 100; // Blue score: Some(300)
```
