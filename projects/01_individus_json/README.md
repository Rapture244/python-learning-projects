# Individuals JSON Analysis — Exercise

## Objective

Load a JSON dataset of individuals, enrich each record with computed fields, run statistical analysis, export to CSV, and clean up the files generated along the way. Ten tasks, in order — each one builds on the previous one's output.

## Setup

Source data lives at `data/individus.json`, relative to your script's own location (use `Path(__file__).parent`, not the current working directory — the script should run the same regardless of where it's launched from).

Each record has: `nom`, `prenom`, `age`, `poids`, `ville_naissance`, `date_naissance`.

## Tasks

### Task 1 — Load & save JSON
Write `load_json(filename)` — loads a JSON file, returns its content. Raise `FileNotFoundError` if the file doesn't exist.
Write `save_to_json(data, filename, *, overwrite)` — saves data to JSON. Raise `FileNotFoundError` if the destination folder doesn't exist, `FileExistsError` if the file already exists and `overwrite=False`.

### Task 2 — Add `taille`
Write `add_taille(individus)` — adds a `taille` field (meters) to each individual, random between `1.50` and `2.00`, rounded to 2 decimals.

### Task 3 — Add `imc`
Write `calculate_imc(poids, taille)` — `IMC = poids / taille²`, rounded to 2 decimals.
Write `add_imc(individus)` — applies it to every individual. Raise `KeyError` if either `poids` or `taille` is missing on a record.

### Task 4 — Add `pays_naissance`
Print the unique `ville_naissance` values in your dataset first, so you know what to map. Build a `ville → pays` lookup for those cities. Write `add_pays_naissance(individus)` — any city not in your lookup falls back to `"Inconnu"` rather than raising.

### Task 5 — Age statistics
Write `analyze_ages(individus)` — returns a dict with mean age, minimum age, maximum age, and count of individuals over 50. Raise `KeyError` if a record is missing `age`.

### Task 6 — BMI statistics
Write `analyze_imc(individus)` — categorize each individual into `maigreur` (BMI < 18.5), `poids_normal` (18.5 ≤ BMI < 25), or `surpoids` (BMI ≥ 25), and return counts per category. Raise `KeyError` if a record is missing `imc`.

### Task 7 — Random selection
Write `select_random_sous_poids(individus, nb=3)` — randomly picks `nb` individuals with `imc < 18.5`. Raise `ValueError` if fewer than `nb` are eligible.

### Task 8 — CSV export
Write `export_to_csv(data, filename, *, overwrite)` — exports the full dataset to CSV.

### Task 9 — Search by country
Write `search_by_country(individus, pays_list)` — for each country in `pays_list`, find matching individuals, print a count, and return a `{pays: [individus]}` dict. Raise `KeyError` if `pays_naissance` is missing on a record.

### Task 10 — Cleanup
Write `clean_temp_files(data_dir)` — deletes every generated `.json` *and* `.csv` file in `data_dir` except the original source file. Print the names of whatever gets deleted.

---

## Correction — Design Notes

Once it's built and running end to end, here's what the reference solution does and why — worth comparing against your own version.

- **`overwrite` is keyword-only** on `save_to_json()` and `export_to_csv()` (`*, overwrite: bool`). Anything that can destroy an existing file forces the caller to type `overwrite=True` explicitly — no accidental overwrite from a stray positional argument.
- **ASCII is enforced, not assumed**: the reference `save_to_json()` builds the JSON string once, checks `raw.isascii()`, and raises `ValueError` if it isn't — catching an accented character before it's silently written to disk, not after.
- **Errors are specific, not generic**: `FileNotFoundError`, `FileExistsError`, `KeyError`, `ValueError` — each one tells you exactly what went wrong, rather than a bare crash or a single catch-all exception.
- **`Path(__file__).parent.resolve()`** anchors the data folder to the script's own location, not the current working directory.
- **`;` as the CSV delimiter**, not `,` — the French/European convention, since `,` is the decimal separator there and would clash with a plain comma-separated file.
- **The city lookup is a plain dict, not a database** — anything unmapped falls back to `"Inconnu"` rather than halting the whole pipeline over one unknown city.
- **Tasks run sequentially, not independently** — task 3 needs task 2's output, task 5 needs task 4's, and so on. If you want to test one task in isolation, load an intermediate JSON file rather than starting from the raw source.

> [!NOTE]  
> This is a starter exercise, so it deliberately keeps things simple: `print()` is used throughout instead of `logging`. Later projects in this repo will introduce `logging` once the basics are solid.
