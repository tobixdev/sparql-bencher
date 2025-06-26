use std::path::PathBuf;

/// The main context for a `sparql-bencher` execution
pub struct SparqlBencherContext {
    /// The path to the data dir.
    data_dir: PathBuf,
    /// The path to the main results directory.
    results_dir: PathBuf,
}
