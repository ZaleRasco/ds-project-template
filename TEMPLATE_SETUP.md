# New project setup

One-time steps after creating a project from this template. Delete this file
when you're done.

1. **Create the repo.** On GitHub, use **Use this template**, or:
   `gh repo create <new-name> --private --template <owner>/ds-project-template --clone`
2. **Name the project.** In `pyproject.toml`, set `name` and `description`. The
   import name stays `tools`.
3. **Relock and install:** `uv lock && uv sync`
4. **Describe the project:** fill in `## Project` in `AGENTS.md` and rewrite
   the README intro. Keep the setup sections.
5. **Configure your editor** using the [README setup instructions](README.md#setup).
   For R or collaborators without uv, see [optional setup](README.md#optional-setup).
6. **Check the environment:** `uv run python scripts/check_env.py`
7. **Delete this file**, remove its link from the README, and commit.
