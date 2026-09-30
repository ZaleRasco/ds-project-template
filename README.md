# Data science project template

A starting point for data science projects, with Python managed by
[uv](https://docs.astral.sh/uv/), Jupyter notebooks, a shared `tools`
package importable from any notebook, and optional R notebooks.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/), which will also install
  the right Python version for you.

## Setup

- **Starting a new project from this template** → Follow
[TEMPLATE_SETUP.md](TEMPLATE_SETUP.md), then delete it.

- **Joining an existing project** → Simply clone the team's repo into a folder of your choice.

After you have a local project on your machine, run the following from the project root:

```sh
uv sync                                   # create .venv and install everything
uv run python scripts/check_env.py        # confirm the environment is correct
```

Lastly, in VSCode, create or open a notebook in the `/notebooks` folder and click **Select Kernel**.
Choose the project's `.venv` environment. For Python scripts, choose the same
environment with **Python: Select Interpreter** if needed.

## Layout

| Path | Contents |
| --- | --- |
| `data/raw/` | Holds original inputs, which should not be modified|
| `data/processed/` | Derived and transformed data|
| `notebooks/` | Exploratory and final analysis notebooks|
| `src/tools/` | Reusable functions imported with `from tools import ...`|
| `scripts/` | Standalone scripts such as `check_env.py`|
| `reports/` | Reports, slides, and HTML exports|

Empty folders contain `.gitkeep` placeholders so they are included when cloning.

Put standalone commands in `scripts/`, and reusable functions you will import later in
`src/tools/`. Scripts and notebooks can import those functions using `from tools import ...`.

## Group work

Coordinate and assign notebook ownership to reduce merge conflicts. 
Agree ahead of time on who will assemble and export the final analysis.

A shared repo is its own project. Personal repos are optional; if you keep one,
place the folder alongside (separate from) the shared repo and open each in its own VS Code window. 

## uv Reminders

Run Python or Jupyter in terminal through uv (`uv run python ...` or `uv run jupyter ...`).
Manage dependencies with `uv add <package>` so `pyproject.toml` and `uv.lock`
stay in sync; avoid installing directly with pip in the uv-managed environment.

After pulling any changes to `pyproject.toml` or `uv.lock`, run `uv sync` and
restart any running notebook kernels.

To export a notebook to HTML, use:

```sh
uv run jupyter nbconvert --to html --output-dir reports <notebook>.ipynb
```

## Optional setup

### R notebooks

Install [R](https://cran.r-project.org/), then install IRkernel and register it
once per machine. Running registration through `uv run` puts the project's
Jupyter on the PATH, which `installspec()` needs:

```sh
Rscript -e 'install.packages("IRkernel", repos = "https://cloud.r-project.org")'
uv run Rscript -e 'IRkernel::installspec()'
```

Then have `check_env.py` check for R: in `pyproject.toml`, under
`[tool.envcheck]`, switch to the commented-out `kernels` and `r_packages` lines.
Select the R kernel when opening an R notebook.
