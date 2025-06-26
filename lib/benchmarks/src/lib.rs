pub mod bsbm;
mod benchmark_suite_id;

pub use benchmark_suite_id::BenchmarkSuiteId;

/// Represents a benchmark.
pub trait SparqlBench {
    /// Returns the [BenchmarkSuiteId] of the benchmark.
    fn name(&self) -> BenchmarkSuiteId;
}
