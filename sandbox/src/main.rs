use std::io;

fn main() {
    println!("Welcome to Rust!");
    
    // Reading user input
    println!("Please enter your name:");
    let mut name = String::new();
    io::stdin()
        .read_line(&mut name)
        .expect("Failed to read line");
    
    let name = name.trim(); // Remove newline
    println!("Nice to meet you, {}!", name);
    
    // Basic arithmetic
    let a = 10;
    let b = 3;
    println!("{} + {} = {}", a, b, a + b);
    println!("{} - {} = {}", a, b, a - b);
    println!("{} * {} = {}", a, b, a * b);
    println!("{} / {} = {}", a, b, a / b);
    println!("{} % {} = {}", a, b, a % b);
}
