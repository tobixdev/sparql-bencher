use std::fmt::{Display, Formatter};

/// Contains the configuration for the BSBM benchmarks.
///
/// Use-case-specific configurations are not part of this struct.
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub struct BsbmConfiguration {
    /// The total number of products.
    number_of_products: usize,
}

impl BsbmConfiguration {
    /// Creates a postfix for the benchmarking directory based on the configuration.
    pub fn dir_name_postfix(&self) -> String {
        format!("{}", self.number_of_products)
    }
}

impl Display for BsbmConfiguration {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "products={}", self.number_of_products)
    }
}
