use anyhow::{bail, Context};
use std::path::Path;
use std::process::Command;

struct RunCommandRequirement {
    /// The working directory.
    workdir: PathBuf,
    /// The program to run.
    program: String,
    /// The args for the program.
    args: Vec<String>,
    /// A checking function that can be used to check if the requirement is fulfilled.
    check_requirement: Box<dyn Fn() -> anyhow::Result<bool>>,
}

impl Requirement for RunCommandRequirement {
    fn prepare(&self, ctx: &SparqlBencherContext) -> anyhow::Result<()> {
        println!("Working directory: {}", self.workdir.display());
        println!("Executing command: {} {}", self.program, args.join(" "));
        let mut cmd = Command::new(self.program);
        cmd.args(args).current_dir(self.workdir);

        let status = cmd
            .status()
            .context(format!("Failed to execute command '{program}'."))?;

        if !status.success() {
            let exit_code = status.code().unwrap_or(-1);
            bail!("Command `{}` failed with exit code {}", self.program, exit_code);
        }

        println!("Command executed successfully.");
        Ok(())
    }

    fn check(&self, ctx: &SparqlBencherContext) -> anyhow::Result<()> {
        todo!("Implement check for RunCommandRequirement");
    }
}