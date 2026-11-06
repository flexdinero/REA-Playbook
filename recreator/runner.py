"""Explicit trusted-local or pinned-image execution, never an implicit sandbox."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

from .storage import check, inside, sha, SuiteError


def minimal_environment():
    allowed = {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "TMPDIR", "HOME", "USERPROFILE",
               "LANG", "LC_ALL", "COMSPEC", "PATHEXT"}
    return {key: value for key, value in os.environ.items() if key.upper() in allowed}


def run_profile(repo, profile, *, trusted_local=False, sandbox_image=None):
    root = Path(repo).resolve()
    cwd = inside(root, profile["cwd"])
    check(cwd.is_dir(), "command cwd does not exist")
    argv = profile["argv"]
    check(isinstance(argv, list) and argv and all(isinstance(part, str) and part for part in argv), "argv must be a nonempty string array")
    timeout = profile["timeout_seconds"]
    check(type(timeout) is int and 1 <= timeout <= 300, "timeout must be 1..300 seconds")
    cleanup = None
    if sandbox_image:
        check(re.fullmatch(r"[A-Za-z0-9./:_-]+@sha256:[0-9a-f]{64}", sandbox_image), "sandbox image must be digest-pinned")
        check(shutil.which("docker"), "Docker CLI unavailable")
        # Owned-container cleanup survives a client timeout; no pulls or network egress.
        temporary = tempfile.TemporaryDirectory(prefix="recreator-container-")
        cidfile = Path(temporary.name) / "id"
        command = ["docker", "run", "--rm", "--pull=never", "--network=none", "--read-only",
                   "--cap-drop=ALL", "--security-opt=no-new-privileges", "--pids-limit=64",
                   "--memory=512m", "--cpus=1", "--user=65534:65534", "--cidfile", str(cidfile),
                   "--mount", f"type=bind,src={root},dst=/workspace,readonly",
                   "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m", "--workdir",
                   "/workspace/" + Path(profile["cwd"]).as_posix(), sandbox_image, *argv]
        def cleanup():
            try:
                identity = cidfile.read_text().strip() if cidfile.exists() else ""
                if re.fullmatch(r"[0-9a-f]{64}", identity):
                    subprocess.run(["docker", "rm", "-f", identity], capture_output=True, timeout=20, check=False)
            finally:
                temporary.cleanup()
    else:
        check(trusted_local, "execution requires explicit --trusted-local for owned code or a digest-pinned sandbox image")
        executable = shutil.which(argv[0])
        check(executable is not None, "configured executable unavailable")
        check(Path(executable).suffix.lower() not in {".bat", ".cmd"}, "batch launchers are not supported; use the underlying runtime directly")
        command = [executable, *argv[1:]]
    started = time.monotonic()
    try:
        with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            try:
                result = subprocess.run(command, cwd=cwd, env=minimal_environment(), stdin=subprocess.DEVNULL,
                                        stdout=out, stderr=err, timeout=timeout, check=False, shell=False,
                                        **({"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}))
                exit_code, timed_out = result.returncode, False
            except subprocess.TimeoutExpired:
                exit_code, timed_out = None, True
            out.seek(0); err.seek(0)
            stdout = out.read(2 * 1024 * 1024 + 1)
            stderr = err.read(2 * 1024 * 1024 + 1)
    finally:
        if cleanup:
            cleanup()
    return {"argv": argv, "cwd": profile["cwd"], "backend": "docker" if sandbox_image else "trusted-local",
            "exit_code": exit_code, "timed_out": timed_out,
            "duration_ms": round((time.monotonic() - started) * 1000),
            "stdout": stdout[:2 * 1024 * 1024].decode("utf-8", errors="replace"),
            "stderr": stderr[:2 * 1024 * 1024].decode("utf-8", errors="replace"),
            "output_truncated": len(stdout) > 2 * 1024 * 1024 or len(stderr) > 2 * 1024 * 1024,
            "passed": exit_code == 0 and not timed_out}
