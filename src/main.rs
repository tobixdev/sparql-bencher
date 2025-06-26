// src/main.rs

mod subsystems;
mod benchmark;

use clap::{Parser, Subcommand};
use benchmark::prepare_benchmark;
use benchmark::run_benchmark;

#[derive(Parser)]
#[command(name = "rdf-fusion-bench", about = "RDF Fusion Bench CLI")] 
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Prepare benchmark data
    Prepare {
        #[arg(long, default_value_t = 100_000)]
        dataset_size: usize,
    },
    /// Run benchmark
    Run {
        #[arg(long)]
        system: String,
        #[arg(long, default_value_t = 100_000)]
        dataset_size: usize,
        #[arg(long, default_value_t = 16)]
        parallelism: usize,
    },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Prepare { dataset_size } => {
            prepare_benchmark(dataset_size);
        }
        Commands::Run { system, dataset_size, parallelism } => {
            run_benchmark(&system, dataset_size, parallelism);
        }
    }
}
