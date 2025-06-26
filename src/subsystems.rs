// src/subsystems.rs

pub trait Subsystem {
    fn run(&self, dataset_size: usize, parallelism: usize);
}

pub struct Jena;
impl Subsystem for Jena {
    fn run(&self, dataset_size: usize, parallelism: usize) {
        println!("[Jena] Running with dataset_size={} parallelism={}", dataset_size, parallelism);
        // TODO: Implement Jena-specific logic
    }
}

pub struct Oxigraph;
impl Subsystem for Oxigraph {
    fn run(&self, dataset_size: usize, parallelism: usize) {
        println!("[Oxigraph] Running with dataset_size={} parallelism={}", dataset_size, parallelism);
        // TODO: Implement Oxigraph-specific logic
    }
}

pub struct Rdf4j;
impl Subsystem for Rdf4j {
    fn run(&self, dataset_size: usize, parallelism: usize) {
        println!("[RDF4J] Running with dataset_size={} parallelism={}", dataset_size, parallelism);
        // TODO: Implement RDF4J-specific logic
    }
}

pub fn get_subsystem(name: &str) -> Option<Box<dyn Subsystem>> {
    match name.to_lowercase().as_str() {
        "jena" => Some(Box::new(Jena)),
        "oxigraph" => Some(Box::new(Oxigraph)),
        "rdf4j" => Some(Box::new(Rdf4j)),
        _ => None,
    }
}
