# Agent instructions

## Project
<!-- One or two lines: what this project is and anything agents should know. -->

## Environment
- Python is managed by uv. Dependencies are declared in `pyproject.toml` (exact
  versions in `uv.lock`). Check `pyproject.toml` before suggesting any install.
- If something is missing, propose `uv add <pkg>` and wait for approval.
  Never use `pip install`.
- Run tools through uv: `uv run python ...`, `uv run jupyter ...`.
- Shared code lives in the `tools` package (`src/tools/`), installed in
  editable mode. Import it with `from tools import ...`.
- R notebooks (if any) use the IRkernel. Agents can edit R notebooks but can't
  run cells in a live R session; to execute one, use
  `uv run jupyter nbconvert --to notebook --execute --inplace <notebook>.ipynb`.
- Export notebooks to HTML with
  `uv run jupyter nbconvert --to html --output-dir reports <notebook>.ipynb`.
- If the environment seems broken, run `uv run python scripts/check_env.py`.

## Conventions
- Before large edits to a notebook, remind the user to commit first.
- Use LaTeX in notebook markdown cells for math.

## Layout
- `data/raw/`: original inputs, never modified. Derived data goes in `data/processed/`.
- `notebooks/`: tracked exploratory and final analysis notebooks.
- `scripts/`: standalone commands such as `check_env.py`.
- `src/tools/`: shared, importable functions.
- `reports/`: tracked reports, slides, and HTML exports.
