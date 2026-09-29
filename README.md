# Data science project template

A starting point for data science projects: Python managed by
[uv](https://docs.astral.sh/uv/), Jupyter notebooks, a shared `tools`
package importable from any notebook, and optional R notebooks via IRkernel.

**Starting a new project from this template?** Follow
[TEMPLATE_SETUP.md](TEMPLATE_SETUP.md), then delete it.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/). uv installs
  the right Python version for you.

## Setup

Joining an existing project? Clone the team's repo; only the project creator
uses the template. Skip this step if you already have a local copy:

```sh
git clone <project-repo-url> <project-folder>
cd <project-folder>
```

From the project root:

```sh
uv sync                                   # create .venv and install everything
uv run python scripts/check_env.py        # confirm the environment is correct
```

`uv sync` also installs `src/tools/` in editable mode, so any notebook can
`from tools import ...` and changes to the code are picked up after a kernel
restart.

### VS Code

Open the project folder, then open a notebook, click **Select Kernel** and
choose the project's `.venv` environment. For Python scripts, choose the same
environment with **Python: Select Interpreter** if needed.

## Layout

| Path | Contents |
| --- | --- |
| `data/raw/` | Original inputs. Never modified. |
| `data/processed/` | Derived data. |
| `notebooks/` | Exploratory and final analysis notebooks, tracked in Git. |
| `src/tools/` | Reusable functions imported by notebooks and scripts as `tools`. |
| `scripts/` | Standalone scripts, such as `check_env.py`. |
| `reports/` | Reports, slides, and HTML exports, tracked in Git. |

Empty folders contain `.gitkeep` placeholders so they are included when cloning.

Put commands you run in `scripts/` and reusable functions you import in
`src/tools/`. Scripts can call those functions.

Keep exploration in `notebooks/`, including unsuccessful approaches that
explain your decisions. Keep final notebooks there too, and final deliverables
in `reports/`; commit the exact versions you share or submit.

## Everyday commands

Run Python and Jupyter through uv (`uv run python ...`, `uv run jupyter ...`).
Manage dependencies with `uv add <package>` so `pyproject.toml` and `uv.lock`
stay in sync; avoid installing directly with pip in the uv-managed environment.

After pulling changes to `pyproject.toml` or `uv.lock`, run `uv sync` and
restart any running notebook kernels.

Export a notebook to HTML with:

```sh
uv run jupyter nbconvert --to html --output-dir reports <notebook>.ipynb
```

## Group work

A shared repo is its own project. Personal repos are optional; if you keep one,
place it alongside the shared repo and open each in its own VS Code window.

Keep team notebooks, reusable code, and data-loading instructions in the shared
repo, including exploratory work. Use a personal repo for private notes and
separate analyses. The shared project should run without access to anyone's
personal repo.

Coordinate notebook ownership to reduce conflicts, agree on who assembles the
final analysis, and put reusable functions in `src/tools/`. Organize notebooks
by task when useful, for example `notebooks/customer-segmentation/exploration.ipynb`.

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

### Alternative for collaborators without uv

Collaborators who use pip or conda can install from an exported requirements
file. The project still manages dependencies through uv; someone with uv
generates the file and shares it (don't commit it; regenerate it when
dependencies change):

```sh
uv export --no-hashes > requirements.txt
```

From the project root, with Python 3.13:

```sh
python3.13 -m venv .venv
source .venv/bin/activate                 # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Or with conda:

```sh
conda create -n my-project python=3.13
conda activate my-project
pip install -r requirements.txt
```

The export includes `-e .`, so pip also installs `tools`. Select this environment
as the notebook kernel. Run `python scripts/check_env.py` in the activated
environment; it will warn that the environment isn't uv-managed.
