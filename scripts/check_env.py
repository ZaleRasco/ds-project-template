"""Check that a project's Python environment is the one it should be.

Standard library only, so it runs under any Python 3.11+ and reports on the
interpreter that runs it. From the project root:

    uv run python scripts/check_env.py            # uv projects
    .venv/bin/python scripts/check_env.py         # any venv
    uv run python scripts/check_env.py --strict   # warnings also fail

Levels: FAIL = will break work, WARN = departs from convention, INFO = context.
Exit code is 1 on any FAIL (or any WARN with --strict).

Optional per-project checks, in pyproject.toml:

    [tool.envcheck]
    kernels = ["python3", "ir"]                   # Jupyter kernels that must exist
    r_packages = ["IRkernel", "car"]              # R packages that must load
"""

import argparse
import re
import shutil
import subprocess
import sys
import tomllib
from importlib import metadata
from pathlib import Path

try:  # optional: enables version checks; presence is still checked without it
    from packaging.requirements import Requirement
    from packaging.specifiers import SpecifierSet
except ImportError:
    Requirement = SpecifierSet = None

counts = {"FAIL": 0, "WARN": 0}


def say(level: str, msg: str) -> None:
    counts[level] = counts.get(level, 0) + 1
    print(f"  {level:<4}  {msg}")


def find_project(start: Path) -> Path | None:
    for d in (start, *start.parents):
        if (d / "pyproject.toml").is_file():
            return d
    return None


def env_kind(prefix: Path) -> str:
    if (prefix / "conda-meta").is_dir():
        return "conda"
    cfg = prefix / "pyvenv.cfg"
    if cfg.is_file():
        return "uv" if re.search(r"^uv\s*=", cfg.read_text(), re.MULTILINE) else "venv"
    return "system"


def check_interpreter(root: Path, project: dict) -> bool:
    print("Interpreter")
    prefix = Path(sys.prefix).resolve()
    kind = env_kind(prefix)
    version = ".".join(map(str, sys.version_info[:3]))
    say("INFO", f"Python {version} ({kind}) at {prefix}")

    if kind == "system":
        say("FAIL", "not in a virtual environment; run through the project's env")
        return False
    if kind != "uv":
        say("WARN", f"environment is {kind}, not uv-managed")
    if prefix != (root / ".venv").resolve():
        say("WARN", f"environment is not this project's .venv ({root / '.venv'})")

    pinned = root / ".python-version"
    if pinned.is_file():
        want = pinned.read_text().strip()
        if not version.startswith(want):
            say("WARN", f"Python {version} doesn't match .python-version ({want})")
    spec = project.get("requires-python")
    if spec and SpecifierSet:
        ok = version in SpecifierSet(spec)
    elif spec and (m := re.fullmatch(r">=\s*(\d+)\.(\d+)", spec.strip())):
        ok = sys.version_info[:2] >= (int(m[1]), int(m[2]))  # common case, no packaging
    else:
        ok = True
    if not ok:
        say("FAIL", f"Python {version} doesn't satisfy requires-python {spec}")
    return True


def check_dependencies(project: dict) -> None:
    deps = project.get("dependencies", [])
    print(f"Dependencies ({len(deps)} declared)")
    if Requirement is None:
        say("INFO", "'packaging' not installed: checking presence only, not versions")
    for line in deps:
        if Requirement:
            req = Requirement(line)
            if req.marker and not req.marker.evaluate():
                continue
            name, spec = req.name, req.specifier
        else:
            name, spec = re.match(r"[A-Za-z0-9._-]+", line).group(), None
        try:
            have = metadata.version(name)
        except metadata.PackageNotFoundError:
            say("FAIL", f"{name} is not installed")
            continue
        if spec and have not in spec:
            say("FAIL", f"{name} {have} doesn't satisfy {spec}")
        else:
            say("INFO", f"{name} {have}")


def check_kernels(wanted: list[str]) -> None:
    print("Jupyter kernels")
    try:
        from jupyter_client.kernelspec import KernelSpecManager
    except ImportError:
        say("FAIL", "jupyter_client is not installed in this environment")
        return
    found = KernelSpecManager().find_kernel_specs()
    for k in wanted:
        if k in found:
            say("INFO", f"{k} kernel")
        else:
            say("FAIL", f"{k} kernel not registered")


def check_r(packages: list[str]) -> None:
    print("R")
    rscript = shutil.which("Rscript")
    if not rscript:
        say("FAIL", "Rscript not on PATH")
        return
    names = ", ".join(f'"{p}"' for p in packages)
    code = (
        f"cat(R.version$major, R.version$minor, '\\n'); for (p in c({names})) "
        "cat(p, requireNamespace(p, quietly = TRUE), '\\n')"
    )
    try:
        out = subprocess.run(
            [rscript, "-e", code],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,  # a failed package load shows up as FALSE in the output
        ).stdout.splitlines()
    except subprocess.SubprocessError as exc:
        say("FAIL", f"Rscript failed: {exc}")
        return
    if out:
        say("INFO", f"R {'.'.join(out[0].split())} at {rscript}")
    loaded = dict(line.split()[:2] for line in out[1:] if len(line.split()) >= 2)
    for p in packages:
        if loaded.get(p) == "TRUE":
            say("INFO", f"R package {p}")
        else:
            say("FAIL", f"R package {p} won't load")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument(
        "--project",
        type=Path,
        default=Path.cwd(),
        help="where to look for pyproject.toml",
    )
    args = ap.parse_args()

    root = find_project(args.project.resolve())
    if root is None:
        print(f"No pyproject.toml at or above {args.project.resolve()}")
        return 1
    data = tomllib.loads((root / "pyproject.toml").read_text())
    project = data.get("project", {})
    extra = data.get("tool", {}).get("envcheck", {})
    print(f"Project: {project.get('name', root.name)} ({root})\n")

    if check_interpreter(root, project):
        check_dependencies(project)
        if extra.get("kernels"):
            check_kernels(extra["kernels"])
    else:
        print(
            "  (skipping package and kernel checks: they'd describe the wrong Python)"
        )
    if extra.get("r_packages"):
        check_r(extra["r_packages"])

    fails, warns = counts["FAIL"], counts["WARN"]
    print(f"\n{fails} failure(s), {warns} warning(s)")
    return 1 if fails or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
