use crate::environment::RdfFusionBenchContext;
use crate::prepare::requirement::ArchiveType;
use crate::prepare::FileDownloadAction;
use anyhow::{bail, Context};
use bzip2::read::MultiBzDecoder;
use reqwest::Url;
use sparql_bencher_common::SparqlBencherContext;
use std::fs::File;
use std::io::{Cursor, Read};
use std::path::{Path, PathBuf};
use std::{fs, path};

/// Represents an action that is applied to a downloaded file.
pub struct FileDownloadRequirement {
    /// The URL that can be used to download the file.
    pub url: Url,
    /// The file name of the resulting file.
    pub file_name: PathBuf,
    /// An optional action that is applied to the downloaded file.
    pub action: Option<FileDownloadAction>,
}

/// Represents an action that is applied to a downloaded file.
pub enum FileDownloadAction {
    /// Unpacks a file after it has been downloaded.
    Unpack(ArchiveType),
}

/// Represents the type of archive.
pub enum ArchiveType {
    /// A .bz2 archive.
    Bz2,
    /// A .zip archive.
    Zip,
}

impl Requirement for FileDownloadRequirement {
    fn prepare(&self, ctx: &SparqlBencherContext) -> anyhow::Result<()> {
        prepare_file_download(
            &ctx.rdf_fusion_bench_context,
            self.url.clone(),
            self.file_name.clone(),
            self.action.clone(),
        )
    }

    fn check(&self, ctx: &SparqlBencherContext) -> anyhow::Result<()> {
        let file_path = ctx.join_data_dir(file_name)?;
        if !file_path.exists() {
            bail!(
                "{:?} does not exist ({:?})",
                &file_path,
                &path::absolute(&file_path)
            );
        }
        Ok(())
    }
}


/// Downloads a file from the given url and executes a possible `action` afterward
/// (e.g., Extract Archive).
pub async fn prepare_file_download(
    env: &RdfFusionBenchContext,
    url: Url,
    file_name: PathBuf,
    action: Option<FileDownloadAction>,
) -> anyhow::Result<()> {
    println!("Downloading file '{url}' ...");
    let file_path = env
        .join_data_dir(&file_name)
        .context("Cant join data dir with file name")?;
    if file_path.exists() {
        if file_path.is_dir() {
            fs::remove_dir_all(&file_path)
                .context("Cannot remove existing directory in prepare_file_download")?;
        } else {
            fs::remove_file(&file_path)
                .context("Cannot remove existing file in prepare_file_download")?;
        }
    }

    let response = reqwest::Client::new()
        .get(url.clone())
        .send()
        .await
        .with_context(|| format!("Could not send request to download file '{url}'"))?;
    if !response.status().is_success() {
        bail!(
            "Response code for file '{url}' was not OK. Actual: {}",
            response.status()
        )
    }

    let parent_file = file_path.parent().context("Cannot create parent dir")?;
    fs::create_dir_all(parent_file).context("Cannot create parent dir for file")?;
    fs::write(&file_path, &response.bytes().await?).context("Can't write response to file")?;
    println!("File downloaded.");

    match action {
        None => {}
        Some(FileDownloadAction::Unpack(archive_type)) => {
            println!("Unpacking file ...");
            match archive_type {
                ArchiveType::Bz2 => {
                    let mut buf = Vec::new();
                    MultiBzDecoder::new(File::open(&file_path)?).read_to_end(&mut buf)?;
                    fs::write(&file_path, &buf)?;
                }
                ArchiveType::Zip => {
                    let archive = fs::read(&file_path).context("Cannot read zip file")?;
                    fs::remove_file(&file_path).context("Cannot remove existing .zip file")?;
                    zip_extract::extract(Cursor::new(archive), &file_path, true)
                        .context("Cannot extract zip file")?;
                }
            }
            println!("File unpacked.");
        }
    }

    Ok(())
}
