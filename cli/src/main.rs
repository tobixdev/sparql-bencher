#![allow(clippy::print_stderr, clippy::cast_precision_loss, clippy::use_debug)]
use crate::cli::{Args, Command};
use anyhow::{bail, Context};
use clap::Parser;
use rdf_fusion::io::{RdfFormat, RdfParser, RdfSerializer};
use rdf_fusion::model::{GraphName, NamedNode};
use rdf_fusion::store::Store;
use rdf_fusion_web::ServerConfig;
use std::ffi::OsStr;
use std::fs::File;
use std::io::{self, stdin, stdout, BufWriter, Read, Write};
use std::path::Path;
use std::str;

mod cli;

#[tokio::main]
pub async fn main() -> anyhow::Result<()> {
}