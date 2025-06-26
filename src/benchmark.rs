// src/benchmark.rs

use crate::subsystems::{get_subsystem, Subsystem};

pub fn prepare_benchmark(dataset_size: usize) {
    println!("Preparing benchmark data with dataset size: {}", dataset_size);
    // TODO: Implement actual data preparation logic
}

pub fn run_benchmark(system: &str, dataset_size: usize, parallelism: usize) {
    println!("Running benchmark for system: {}", system);
    println!("Dataset size: {} | Parallelism: {}", dataset_size, parallelism);
    if let Some(subsystem) = get_subsystem(system) {
        subsystem.run(dataset_size, parallelism);
    } else {
        eprintln!("Unknown system: {}", system);
    }
}
