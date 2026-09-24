fn stats(v: &Vec<i32>) -> Option<(i32, i32)> {
    if v.is_empty() {
        return None;
    };
    let max = *v.iter().max().unwrap();
    let min = *v.iter().min().unwrap();
    Some((max, min))
}

fn main() {
    let m: Vec<i32> = vec![1, 2, 3, 4];
    println!("Stats {:?}", stats(&m))
}
