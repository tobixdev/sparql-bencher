/// Identifies the engine and its configuration used for a benchmark.
pub enum Engine {
    /// [RDF Fusion](https://github.com/tobixdev/rdf-fusion) engine.
    RdfFusion(RdfFusionConfiguration),
}