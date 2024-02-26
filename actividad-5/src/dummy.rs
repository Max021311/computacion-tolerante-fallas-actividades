
fn main () {
    proctitle::set_title("dummy-process");
    loop {
        std::thread::sleep(std::time::Duration::from_secs(5));
        println!("Five seconds elapsed")
    }
}
