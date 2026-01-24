use std::env;
use std::net::IpAddr;

#[allow(unused)]
struct Arguments {
    flag: String,
    ipaddr: IpAddr,
    threads: u16,
}
#[allow(unused)]
fn main() {
    let args: Vec<String> = env::args().collect();
    let program = args[0].clone();

    for i in &args {
        println!("{}", i);
    }

    println!("{:?}", args);
}
