use crate::bsbm::BsbmConfiguration;
use std::fmt::{Display, Formatter};

/// An enum with variants for all supported benchmark suites.
///
/// The id should incoroporate relevant configurations. For example, a benchmark with 10 triples
/// should be different from a benchmark with 100 triples, even if the executed queries are the
/// same.
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub enum BenchmarkSuiteId {
    /// The BSBM benchmark suite
    Bsbm(BsbmConfiguration),
}

impl BenchmarkSuiteId {
    /// Returns a directory name for the benchmark.
    pub fn dir_name(&self) -> String {
        match self {
            BenchmarkSuiteId::Bsbm(configuration) => {
                format!("bsbm-{}", configuration.dir_name_postfix())
            }
        }
    }
}

impl Display for BenchmarkSuiteId {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            BenchmarkSuiteId::Bsbm(configuration) => write!(f, "BSBM: {configuration}"),
        }
    }
}
