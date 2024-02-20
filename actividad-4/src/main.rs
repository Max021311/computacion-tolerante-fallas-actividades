mod concurrency;
mod threads;
mod subprocess;

use std::io::{Read};
use std::time;
use std::net::TcpStream;
use std::thread;

fn main() {
    let start = time::Instant::now();
    daemon_test();
    println!("Elapsed time {}ms", start.elapsed().as_millis());
    println!();

    let start = time::Instant::now();
    threads::main();
    println!("Elapsed time {}ms", start.elapsed().as_millis());
    println!();

    let start = time::Instant::now();
    concurrency::main();
    println!("Elapsed time {}ms", start.elapsed().as_millis());
    println!();

    let start = time::Instant::now();
    subprocess::main();
    println!("Elapsed time {}ms", start.elapsed().as_millis());
    println!();

}

fn daemon_test () {
    println!("=== Daemon ===");
    let handle = thread::spawn(|| {
        match  TcpStream::connect("localhost:7878") {
            Ok(mut stream) => {
                let mut buffer = [0 as u8; 50];
                loop {
                    let size = stream.read(&mut buffer).expect("Failed at read");
                    if size == 0 { break }
                    let res = std::str::from_utf8(&buffer).expect("Fail at parse vec");
                    println!("{}", res);
                }

            },
            Err(e) => { eprintln!("Error: {}", e) }
        };
    });

    for i in 1..6 {
        println!("Hello from main process {}", i);
        thread::sleep(time::Duration::from_millis(1000));
    }

    handle.join().unwrap();
}
