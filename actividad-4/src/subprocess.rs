use std::process::Command;
use std::thread;
use std::time;

pub fn main () {
    println!("=== Subprocess ===");
    println!("Main process: print every number in range from 1 to 5 every second.");
    println!("Subprocess: print every number in range from 6 to 10 every second.");
    let mut child = Command::new("sh")
        .arg("-c")
        .arg("for i in $(seq 6 10); do echo Hello from subprocess $i; sleep 1; done")
        .spawn()
        .expect("Failed to execute the subprocess");

    for i in 1..6 {
        println!("Hello from main process {}", i);
        thread::sleep(time::Duration::from_millis(1000));
    }
    let _ = child.wait().expect("Failed to wait subprocess");
}
