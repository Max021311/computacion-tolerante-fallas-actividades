use tokio::runtime::Builder;
use tokio::time;
use std::ops::Range;

async fn print_range_in_interval (
    range: Range<i32>,
    duration: time::Duration,
    task_id: i32
) {
    for i in range {
        let _ = time::sleep(duration).await;
        println!("Task {} say {}", task_id, i)
    }
}

pub fn main () {
    println!("=== Concurrency ===");
    println!("Task 1: print every number in range from 1 to 5 every second.");
    println!("Task 2: print every number in range from 6 to 10 every second.");
    println!(
        "Only one task can run in the thread but the current task yield the control to the next task while wait the interval.",
    );
    println!(
        "This avoid some task can block the process while wait an external resource.",
    );
    println!();
    let rt = Builder::new_current_thread()
        .enable_time()
        .build()
        .unwrap();
    let duration = time::Duration::from_millis(1000);
    let _ = rt.block_on(async {
        let _ = tokio::join!(
            print_range_in_interval(1..6, duration, 1),
            print_range_in_interval(6..11, duration, 2),
        );
    });
}
