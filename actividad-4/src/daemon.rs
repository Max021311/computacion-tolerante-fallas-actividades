
use daemonize::Daemonize;
use std::fs::File;
use std::net::{TcpStream, TcpListener};
use std::io::Write;
use std::thread;
use std::time;

fn invoke_daemon () {
    let stdout = File::create("/tmp/daemon.out").expect("Failed at create daemon.out");
    let stderr = File::create("/tmp/daemon.err").expect("Failed at create daemon.err");

    let daemon = Daemonize::new()
        .pid_file("/tmp/daemon.pid")
        .stdout(stdout)
        .stderr(stderr);

    match daemon.start() {
        Ok(_) => {
            listener()
        },
        Err(e) => {
            eprintln!("Error {}", e);
        }
    };
}

fn main () {
    invoke_daemon()
}

fn listener () {
    let listener = TcpListener::bind("127.0.0.1:7878").expect("Failed at init server");
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                println!("New connection: {}", stream.peer_addr().unwrap());
                thread::spawn(|| handle_connection(stream));
            },
            Err(e) => eprintln!("Error: {}", e)
        }
    }
    drop(listener)
}

fn handle_connection (mut stream: TcpStream) {
    for i in 6..11 {
        thread::sleep(time::Duration::from_millis(1000));
        let buffer = std::format!("Hello from daemon {}", i);
        print!("{}", buffer);
        stream.write(buffer.as_bytes()).unwrap();
    }
}
