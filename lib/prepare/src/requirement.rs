use reqwest::Url;
use std::path::PathBuf;

/// The implementation of a requirement.
pub trait Requirement {
    /// Prepares the requirement in the given context.
    fn prepare(&self, ctx: &SparqlBencherContext) -> anyhow::Result<()>;

    /// Checks the requirement in the given context.
    /// 
    /// Returns `Ok(())` if the requirement is fulfilled, otherwise an error with a descriptive message.
    fn check(&self, ctx: &SparqlBencherContext) -> anyhow::Result<()>;

    /// Ensures that the requirement is fulfilled in the given context.
    /// 
    /// If the requirement is already fulfilled (see [Self::check]), this method does not prepare.
    fn ensure(&self, ctx: &SparqlBencherContext) -> anyhow::Result<()> {
        if self.check(ctx).is_ok() {
            Ok(())
        } else {
            self.prepare(ctx)
        }
    }
}

/// Defines a requirement of preparing for a benchmark.
pub enum PrepRequirement {
    /// Requires that a file is downloaded at a given (relative) path.
    FileDownload(FileDownloadRequirement),
    /// Runs a command.
    RunCommand(RunCommandRequirement),
}

impl Requirement for PrepRequirement {
    fn prepare(&self, ctx: &SparqlBencherContext) -> anyhow::Result<()> {
        match self {
            PrepRequirement::FileDownload(req) => req.prepare(ctx),
            PrepRequirement::RunCommand(req) => req.prepare(ctx),
        }
    }

    fn check(&self, ctx: &SparqlBencherContext) -> anyhow::Result<()> {
        match self {
            PrepRequirement::FileDownload(req) => req.check(ctx),
            PrepRequirement::RunCommand(req) => req.check(ctx),
        }
    }
}