use clap::{Parser, Subcommand};
use std::path::PathBuf;

#[derive(Parser)]
#[command(about, version, name = "rdf-fusion")]
/// RdfFusion command line toolkit and SPARQL HTTP server
pub struct Args {}

#[derive(Subcommand)]
pub enum Command {}
