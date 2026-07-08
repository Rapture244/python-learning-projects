# Python Learning Projects

A small collection of independent Python projects where I apply and learn core programming concepts, from beginner basics to advanced topics. Each project follows the Zen of Python: simple, readable, explicit code, using type hints and logging throughout, built as a foundation for real software engineering and programmer critical thinking.

## 🚀 Getting Started

Clone the repo with `git clone` (not a ZIP download — versioning relies on git tags, which a ZIP doesn't include):

```shell
git clone https://github.com/Rapture244/python-learning-projects.git
cd python-learning-projects
```

Then install with whichever tool you use:

```shell
# uv (recommended)
uv sync
 
# pip
pip install -e .
 
# poetry
poetry install
```

## 📂 Projects

| # | Project | What it does | Concepts practiced | Links |
|---|---------|---------------|----------------------|-------|
| 01 | **Individuals JSON Analysis** | Loads a JSON dataset of individuals, enriches each record with computed fields (height, BMI, country of birth), runs statistical analysis (age stats, BMI categories), exports the result to CSV, and cleans up generated files. | `pathlib`, JSON I/O, type hints, docstrings, CSV export, basic statistics, error handling | [README](projects/01_individus_json/README.md) |

> [!NOTE]  
> Each project expects its input data in a `data/` folder next to its script (e.g. `projects/01_individus_json/data/individus.json`). Adjust the path if your local layout differs.
