A little process manager with the following capabilities:
- List PID, name and status of processes (Allow usage of PID or process name).
- Kill processes by name or PID

# How to run?

1. Run the process manager
  ```bash
  cargo run --bin proc-manager -- <command> [<arg>]
  ```
2. Run the dummy process
  ```bash
  cargo run --bin dummy-process
  ```

## Requirements

- cargo
- rust

## How to scan

### All processes
```bash
cargo run --bin proc-manager -- scan
```

![Scan](./assets/scan.png "Scan")

### Processes by name
```bash
cargo run --bin proc-manager -- scan dummy-process
```

![Scan by name](assets/scan-by-name.png "Scan by name")

### Process by pid
```bash
cargo run --bin proc-manager -- scan 123
````

![Scan by pid](assets/scan-by-pid.png "Scan by pid")

### How to kill
### Processes by name
```bash
cargo run --bin proc-manager -- kill dummy-process
```

![Kill by name](assets/kill-by-name.png "Kill by name")

### Process by pid
```bash
cargo run --bin proc-manager -- kill 123
````

![Kill by pid](assets/kill-by-pid.png "Kill by pid")
