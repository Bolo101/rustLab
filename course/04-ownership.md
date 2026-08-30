# Rust Memory Management: Stack, Heap, Ownership, and Borrowing

## Table of Contents
1. [Stack and Heap Memory](#stack-and-heap-memory)
2. [Ownership Rules](#ownership-rules)
3. [The Copy Trait](#the-copy-trait)
4. [Borrowing and References](#borrowing-and-references)

---

## Stack and Heap Memory

### The Stack: Fast and Fixed

The stack is a region of memory used for storing data whose size is fixed and known at compile time.

**Data Types Stored on Stack:**
- Primitive types: `u32`, `i32`, `bool`, `char`, floating-point numbers
- Fixed-size arrays with known compile-time length
- Tuples with all fixed-size, stack-allocated elements

**Performance Characteristics:**
- **Very fast** allocation and deallocation
- Uses simple pointer manipulation (push/pop)
- No searching for free memory space needed
- Direct access to data

**Storage Mechanism:**
- Operates on **LIFO (Last In, First Out)** principle
- Data is added (pushed) to the top and removed (popped) from the top
- Example: A stack of plates where you add/remove from the top

### The Heap: Flexible but Slower

The heap is a region of memory used for storing data whose size is unknown at compile time or might change during execution.

**Data Types Primarily Stored on Heap:**
- `String`: Growable, mutable, UTF-8 encoded text
- `Vec<T>`: Growable vectors/lists
- Data explicitly allocated using `Box<T>` smart pointer

**Performance Characteristics:**
- **Slower allocation**: Allocator must find suitable empty space
- **Slower access**: Requires indirection via pointer stored on stack
- **Bookkeeping overhead**: Memory management and tracking

**Memory Safety:**
- Rust's ownership and borrowing rules primarily manage heap-allocated data
- Prevents dangling pointers, double frees, and memory leaks
- No garbage collector needed

### Practical Code Examples

#### Stack Examples
```rust
fn main() {
    // i32 variable (stack-allocated)
    let x: i32 = 1;
    // Fixed size (32 bits), known at compile time

    // Fixed-size array (stack-allocated)
    let arr: [i32; 10] = [1; 10];
    // Total size known at compile time (10 * 4 bytes)
}
```

#### Heap Examples
```rust
fn main() {
    // String (heap-allocated data, stack-allocated metadata)
    let mut s: String = "hello".to_string();
    s += " world";
    // Actual text on heap; String struct (pointer, length, capacity) on stack

    // Vector (heap-allocated elements, stack-allocated metadata)
    let mut v = vec![];
    v.push(0);
    v.push(0);
    // Elements on heap; Vec struct (pointer, length, capacity) on stack

    // Explicit heap allocation
    let boxed_num = Box::new(1i32);
    // Normally stack-allocated i32 forced onto heap
    // Box<i32> pointer stored on stack, actual value on heap
}
```

### Stack vs. Heap Comparison

| Feature | Stack | Heap |
|---------|-------|------|
| **Data Size** | Fixed, known at compile time | Dynamic, unknown or changeable |
| **Allocation** | Very fast (push/pop) | Slower (finds space, bookkeeping) |
| **Access** | Very fast (direct) | Slower (indirect via pointer) |
| **Organization** | LIFO structure | Less organized, managed by allocator |
| **Management** | Automatic by compiler | Managed by Rust's ownership system |
| **Typical Data** | Primitives, fixed-size arrays | `String` data, `Vec<T>` elements, `Box<T>` data |

**Why This Matters:**
- **Performance**: Stack operations are significantly faster
- **Safety**: Heap data requires careful ownership management
- **Flexibility**: Heap allows dynamic sizing and growth
- **Idiomatic Rust**: Understanding memory allocation helps write efficient code

---

## Ownership Rules

### Rule 1: Each Value Has an Owner

Every piece of data in Rust is owned by a variable.

```rust
let s = String::from("rust");  // s owns the string "rust"
let i = 1;                      // i owns the value 1
```

### Rule 2: Only One Owner at a Time

Any given value can only have a single owner. For complex types like `String`, ownership is **moved** when assigned.

```rust
let s = String::from("dog");    // s owns "dog"
let s1 = s;                     // Ownership moves to s1, s is invalid
let s2 = s1;                    // Ownership moves to s2, s1 is invalid

println!("{}", s2);             // Works: s2 is current owner
// println!("{}", s);           // ERROR: s was moved
```

**Compilation Error:**
```
error[E0382]: borrow of moved value: `s`
  --> examples/ownership.rs:20:20
   |
13 |     let s = String::from("dog");
   |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
14 |     let s1 = s;
   |              - value moved here
...
20 |     println!("{}", s);
   |                    ^ value borrowed here after move
```

**Why This Rule Exists:**
- **Memory Safety**: Prevents double free errors
- **Resource Management**: Clear responsibility for cleanup
- **Predictability**: No shared mutable state by default
- **Performance**: Enables efficient memory management

### Rule 3: When Owner Goes Out of Scope, Value is Dropped

"Dropped" means memory is deallocated and cleanup occurs automatically.

#### Example: Function Takes Ownership
```rust
fn take_ownership(some_string: String) {
    println!("Inside take_ownership: {}", some_string);
} // some_string goes out of scope, String data is dropped

fn main() {
    let s = String::from("cat");  // s owns "cat"
    take_ownership(s);            // Ownership moves into function
    // s is now invalid
    // println!("{}", s);          // ERROR: borrow of moved value
}
```

**Why This Rule Exists:**
- **Automatic Cleanup**: No manual memory management needed
- **Resource Safety**: Guarantees resources are released
- **Memory Safety**: Prevents memory leaks and dangling pointers
- **Deterministic**: Memory is freed at predictable points

---

## The Copy Trait: An Exception to Ownership Moves

Types that implement the `Copy` trait are copied rather than moved when assigned or passed to functions.

### Copy Trait Examples

#### Stack-Allocated Copy Types
```rust
// i32 implements Copy
let i = 1;
let i1 = i;   // Value is copied, both i and i1 are valid
let i2 = i1;  // Value is copied again

println!("i = {}, i1 = {}, i2 = {}", i, i1, i2);
// All variables remain valid and hold their own copies
```

#### Copy Types Passed to Functions
```rust
fn process_copy(value: i32) {
    println!("Inside process_copy: {}", value);
} // value (the copy) is dropped here

fn main() {
    let i = 1;
    process_copy(i);           // A copy is passed to the function
    println!("After process_copy, i = {}", i);  // i is still valid
}
```

### Types That Implement Copy

- **All integer types**: `i32`, `u64`, `i8`, `u8`, etc.
- **Boolean type**: `bool`
- **Floating-point types**: `f32`, `f64`
- **Character type**: `char`
- **Tuples**: If all elements implement `Copy`

### Types That Don't Implement Copy

- **`String`**: Manages heap-allocated data
- **`Vec<T>`**: Growable collections
- **Any type with heap-allocated data**: Complex data structures

**Why String Doesn't Implement Copy:**
- **Heap allocation**: Copying would require deep copying all heap data
- **Performance**: Deep copying would be expensive for large strings
- **Semantics**: Move semantics are more appropriate for owned data
- **Safety**: Prevents accidental expensive operations

**Why Copy Types Are Stack-Allocated:**
- **Fixed size**: Known at compile time
- **Simple copying**: Bitwise copy is sufficient
- **No heap data**: No complex memory management needed
- **Performance**: Very fast to copy

---

## Borrowing and References

### What is Borrowing?

Borrowing allows temporary use of a value without taking ownership. It's achieved through **references**.

### Types of References

#### 1. Immutable References (`&T`)

Allow reading data but not modifying it.

**Rule:** You can have **any number of immutable references** simultaneously.

```rust
let s = String::from("rust");
let s1 = &s;   // s1 is an immutable reference to s
let s2 = &s;   // s2 is another immutable reference to s
let s3 = s2;   // s3 is also an immutable reference

// All references provide read-only access
println!("s: {}, s1: {}, s2: {}, s3: {}", s, s1, s2, s3);
```

**Multiple Immutable References:**
```rust
let s = String::from("rust");
let r1 = &s;  // OK
let r2 = &s;  // OK
let r3 = &s;  // OK - unlimited immutable references
```

#### 2. Mutable References (`&mut T`)

Allow both reading and writing data. Original data must be declared `mut`.

**Rule:** You can have **only one mutable reference** at a time.

```rust
let mut s = String::from("rust");
let s1 = &mut s;  // s1 is a mutable reference to s
s1.push_str(" 🦀");  // Can modify s through s1

println!("{}", s);  // s has been modified
```

**Non-Lexical Lifetimes (NLL):**
```rust
let mut s = String::from("rust");
let s1 = &mut s;
s1.push_str(" 🦀");  // Last use of s1's borrow

// s1's borrow has ended, can create new mutable reference
let s2 = &mut s;
s2.push_str("🦀");

println!("{}", s);  // "rust 🦀🦀"
```

#### 3. Mixing Immutable and Mutable References

**Rule:** You cannot have both types active simultaneously for the same data.

```rust
// This will NOT compile
let mut s = String::from("rust");
let s1 = &s;      // Immutable borrow 1
let s2 = &s;      // Immutable borrow 2
// let s3 = &mut s;  // ERROR: Cannot borrow as mutable while already borrowed as immutable

println!("s1: {}", s1);  // s1's borrow is active here
```

### Preventing Dangling References

**Fundamental Safety Rule:** A reference must **never outlive** the data it refers to.

#### Example: Ownership Move Creates Dangling Reference
```rust
// This will NOT compile
let s_outer = String::from("rust");
let s1_ref = &s_outer;

{
    let s2_inner_owner = s_outer;  // Ownership moves
} // s2_inner_owner dropped, String data deallocated

// ERROR: s1_ref now references dropped data
// println!("s1_ref: {}", s1_ref);
```

#### Example: Function Returns Dangling Reference
```rust
// This function will NOT compile
// fn dangle(s: String) -> &String {
//     &s  // Returns reference to data that will be dropped
// } // s is dropped here

fn main() {
    let my_string = String::from("hello");
    // let reference_to_nothing = dangle(my_string);  // Would be problematic
}
```

### Applying Borrowing: Solving Ownership Transfer Problems

#### Original Problem: Ownership Transfer
```rust
fn take(s: String) {
    println!("take {}", s);
}

fn main() {
    let s = String::from("rust");
    take(s);  // Ownership moves, s becomes invalid
    // println!("{}", s);  // ERROR: s was moved
}
```

#### Solution: Borrowing Instead
```rust
fn borrow_string(s_ref: &String) {  // Takes immutable reference
    println!("borrow {}", s_ref);
}

fn main() {
    let original_s = String::from("rust");  // original_s owns the data
    borrow_string(&original_s);  // Pass reference, ownership stays

    println!("{}", original_s);  // original_s is still valid
}
```

#### Mutable Borrowing for Modification
```rust
fn modify_string(s_ref: &mut String) {  // Takes mutable reference
    s_ref.push_str(" is awesome!");
    println!("modified in function: {}", s_ref);
}

fn main() {
    let mut modifiable_s = String::from("Rust");
    modify_string(&mut modifiable_s);  // Pass mutable reference

    println!("after function: {}", modifiable_s);  // Changes reflected
}
```

### Key Borrowing Principles

- **Temporary Access**: Borrowing allows temporary use without ownership transfer
- **No Ownership Move**: Creating references doesn't transfer ownership
- **Reference Types**: Immutable (`&T`) for read-only, mutable (`&mut T`) for read-write
- **Mutual Exclusion**: Either many immutable OR one mutable reference, never both
- **Lifetime Safety**: References must never outlive their data

### Why Borrowing Rules Exist

**Memory Safety:**
- Prevents data races in concurrent code
- Eliminates dangling pointers
- Ensures memory is not freed while in use

**Performance:**
- Zero-cost abstractions
- No runtime overhead for checking
- Compiler optimization opportunities

**Correctness:**
- Compile-time guarantees
- Clear ownership semantics
- Predictable program behavior

---

## Key Takeaways

### Stack vs. Heap
- **Stack**: Fast, fixed-size, compile-time known, LIFO organization
- **Heap**: Slower, dynamic size, runtime allocation, needs ownership management
- **Performance**: Understanding allocation helps write efficient code

### Ownership System
1. **Each value has an owner** - Clear responsibility
2. **Only one owner at a time** - Prevents conflicts and memory issues
3. **Dropped when out of scope** - Automatic cleanup

### Copy Trait
- **Stack types implement Copy** - Simple, fast bitwise copying
- **Heap types don't implement Copy** - Would require expensive deep copying
- **Move semantics** - More appropriate for owned data

### Borrowing
- **References enable temporary access** - Without ownership transfer
- **Immutable references** - Unlimited concurrent read access
- **Mutable references** - Exclusive write access
- **Lifetime safety** - References cannot outlive their data

### Why This Matters
- **Memory Safety**: No garbage collector, yet no memory errors
- **Performance**: Efficient memory management with zero runtime overhead
- **Concurrency**: Prevents data races at compile time
- **Idiomatic Rust**: Understanding these concepts is essential for writing good Rust code