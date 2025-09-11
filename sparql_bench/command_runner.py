import subprocess
import shlex
from pathlib import Path


class CommandRunner:
    def __init__(self, log_path="work/command.log"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def run(self, command, **kwargs):
        """
        Run a shell command, log it, and return the result.
        Args:
            command (str or list): The command to execute.
            **kwargs: Passed to subprocess.run
        Returns:
            subprocess.CompletedProcess
        """
        if isinstance(command, list):
            cmd_str = shlex.join(command)
        else:
            cmd_str = command
        self._log_command(cmd_str)
        result = subprocess.run(command, **kwargs)
        return result

    def _log_command(self, cmd_str):
        with self.log_path.open("a") as f:
            f.write(cmd_str + "\n")
