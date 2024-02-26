use sysinfo::{System, Pid};

use std::str::FromStr;

fn scan (sys: & mut System, args: &[String]) {
    let len = args.len();
    match len {
        0 => {
            sys.refresh_processes();
            for (pid, process) in sys.processes() {
                println!("PID: {}\t Name: {}\t Status: {}\t", pid, process.name(), process.status());
            }
        },
        1 => {
            let arg = args[0].as_str();
            if is_number(arg) {
                let pid = Pid::from_str(arg).unwrap();
                sys.refresh_process(pid);
                if let Some(process) = sys.process(pid) {
                    println!(
                        "PID: {}\t Name: {}\t Status: {}\t",
                        process.pid(),
                        process.name(),
                        process.status()
                    );
                }
            } else {
                sys.refresh_processes();
                for process in sys.processes_by_name(arg) {
                    println!(
                        "PID: {}\t Name: {}\t Status: {}\t",
                        process.pid(),
                        process.name(),
                        process.status()
                    );
                }
            }
        },
        _ => {
            panic!("Scan command require one or zero arguments");
        }
    }
}

fn is_number (string: &str) -> bool {
    let numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    for c in string.chars() {
        if !numbers.contains(&c) {
            return false
        }
    }
    true
}

fn kill (sys: & mut System, args: &[String]) {
    let len = args.len();
    match len {
        1 => {
            let arg = args[0].as_str();
            if is_number(arg) {
                let pid = Pid::from_str(arg).unwrap();
                sys.refresh_process(pid);
                if let Some(process) = sys.process(pid) {
                    process.kill();
                }
            } else {
                sys.refresh_processes();
                for process in sys.processes_by_name(arg) {
                    process.kill();
                }
            }
        },
        _ => {
            panic!("Kill command require one argument");
        }
    }
}

fn help () {
    println!("Unknow command.\n");
    println!("scan [<pid_or_process_name>]");
    println!("kill <pid_or_process_name>");
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        help();
        return;
    }
    let command = args[1].as_str();
    let subargs = &args[2..];

    let mut sys = System::new_all();
    match command {
        "scan" => { scan(& mut sys, subargs) },
        "kill" => { kill(& mut sys, subargs) },
        _ => { help() }
    }
}
