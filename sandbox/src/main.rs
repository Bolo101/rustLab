use std::collections::HashMap;

fn main() {
    let mut counts: HashMap<char, i32> = HashMap::new();
    for c in "mississipi".chars() {
        *counts.entry(c).or_insert(0) += 1;
    }
    println!("{:?}", counts)
}
