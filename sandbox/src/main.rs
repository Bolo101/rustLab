fn double_parsed(text: &str) -> Result<i32, String> {
    let n = text.trim().parse::<i32>().map_err(|e| e.to_string())?;
    Ok(n * 2)
}

fn main() {
    println!(
        "Value double of {} is {:?}",
        "42".to_string(),
        double_parsed("42")
    );
}
