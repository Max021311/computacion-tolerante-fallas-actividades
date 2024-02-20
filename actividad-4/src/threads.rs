
use std::thread;
use std::time;

pub fn main () {
    println!("=== Multi threading ===");
    println!("Main thread: print every number in range from 1 to 5 every second.");
    println!("Second thread: print every number in range from 6 to 10 every second.");
    println!();
    let handle = thread::spawn(|| {
        for i in 6..11 {
            println!("Hello from second thread {}", i);
            thread::sleep(time::Duration::from_millis(1000));
        }
    });
    for i in 1..6 {
        println!("Hello from main thread {}", i);
        thread::sleep(time::Duration::from_millis(1000));
    }
    handle.join().unwrap();
}
