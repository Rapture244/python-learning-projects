#!/usr/bin/env python3
"""Analysis and manipulation project for a JSON file of individuals.

Objective:
    Load a JSON file of individuals, enrich the data with new computed
    fields, produce statistical analyses, export the results to CSV, and
    clean up the temporary files generated along the way.

Modules used:
    math, datetime, os, glob, string, random, csv, json

Structure:
    - Task 1  : Load & save JSON
    - Task 2  : Add the 'taille' field
    - Task 3  : Add the 'imc' field
    - Task 4  : Add the 'pays_naissance' field
    - Task 5  : Age analysis
    - Task 6  : BMI analysis
    - Task 7  : Random selection (underweight)
    - Task 8  : CSV export
    - Task 9  : Search by country
    - Task 10 : Cleanup of temporary files

Usage:
    python main.py

Note:
    The source file must be located at: data/individus.json
"""

# ruff: noqa: T201, TRY003
# pyright: reportAny=false, reportExplicitAny=false

from __future__ import annotations

import csv
import json
from pathlib import Path
import random
from typing import Any

# =============================================================================
# Task 1 : Load & save JSON
# =============================================================================


def load_json(filename: str | Path) -> list[Any] | dict[str, Any]:
    """Loads a JSON file and returns its content.

    Args:
        filename (str | Path): Path to the JSON file.

    Returns:
        list[Any] | dict[str, Any]: Content of the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path: Path = Path(filename).resolve()

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open(encoding="utf-8") as file:
        return json.load(fp=file)


def save_to_json(
    data: list[Any] | dict[str, Any],
    filename: str | Path,
    *,
    overwrite: bool,
) -> None:
    """Saves a data structure to a JSON file.

    Args:
        data (list[Any] | dict[str, Any]): Data to save.
        filename (str | Path): Path to the destination JSON file.
        overwrite (bool): If True, overwrites an existing file. If False, raises an error.

    Raises:
        FileNotFoundError: If the destination directory does not exist.
        FileExistsError: If the file already exists and overwrite=False.
        ValueError: If the data contains non-ASCII characters.

    Returns:
        None
    """
    path: Path = Path(filename).resolve()

    if not path.parent.exists():
        raise FileNotFoundError(f"Directory does not exist: {path.parent}")

    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {path}")

    raw: str = json.dumps(obj=data, ensure_ascii=False)
    if not raw.isascii():
        raise ValueError(f"Data contains non-ASCII characters: {path}")

    with path.open(mode="w", encoding="utf-8") as file:
        json.dump(obj=data, fp=file, indent=4, ensure_ascii=True)


# =============================================================================
# Task 2 : Add the 'taille' field
# =============================================================================


def add_taille(individus: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Adds a 'taille' field (meters) to each individual, randomly generated between 1.50 and 2.00, rounded to 2 decimals.

    Args:
        individus (list[dict[str, Any]]): List of dictionaries representing the individuals.

    Returns:
        list[dict[str, Any]]: Updated list with the 'taille' field.
    """
    for individu in individus:
        taille: float = round(number=random.uniform(a=1.50, b=2.00), ndigits=2)
        individu["taille"] = taille
    return individus


# =============================================================================
# Task 3 : Add the 'imc' field
# =============================================================================


def calculate_imc(poids: float, taille: float) -> float:
    """Calculates BMI from weight and height.

    Formula: BMI = poids / (taille ** 2)

    Args:
        poids (float): Weight in kilograms.
        taille (float): Height in meters.

    Returns:
        float: BMI rounded to 2 decimals.
    """
    return round(number=poids / (taille**2), ndigits=2)


def add_imc(individus: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Adds an 'imc' field to each individual using calculate_imc().

    Args:
        individus (list[dict[str, Any]]): List of dictionaries representing the individuals.
        Each individual must have the 'poids' and 'taille' fields.

    Returns:
        list[dict[str, Any]]: Updated list with the 'imc' field.

    Raises:
        KeyError: If an individual is missing the 'poids' or 'taille' fields.
    """
    for individu in individus:
        if "poids" not in individu or "taille" not in individu:
            raise KeyError(f"Missing 'poids' or 'taille' for individu: {individu}")

        imc: float = calculate_imc(poids=individu["poids"], taille=individu["taille"])
        individu["imc"] = imc

    return individus


# =============================================================================
# Task 4 : Add the 'pays_naissance' field
# =============================================================================
def print_ville_naissance(individus: list[dict[str, Any]]) -> None:
    """Prints the set of unique birth cities present in the data.

    Args:
        individus (list[dict[str, Any]]): List of dictionaries representing the individuals.

    Returns:
        None
    """
    print({individu["ville_naissance"] for individu in individus})


def add_pays_naissance(individus: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Adds a 'pays_naissance' field to each individual based on their birth city.

    An internal dictionary maps each known city to its country.
    If the city is not in the dictionary, the country will be "Inconnu".

    Args:
        individus (list[dict[str, Any]]): List of dictionaries representing the individuals.
        Each individual must have a 'ville_naissance' field.

    Returns:
        list[dict[str, Any]]: Updated list with the 'pays_naissance' field.
    """
    ville_to_pays: dict[str, str] = {
        "Paris": "France",
        "Londres": "Royaume-Uni",
        "Berlin": "Allemagne",
        "Lisbonne": "Portugal",
        "Moscou": "Russie",
        "Tokyo": "Japon",
        "New York": "Etats-Unis",
        "Rio": "Bresil",
        "Sydney": "Australie",
    }

    for individu in individus:
        ville: str = individu["ville_naissance"]
        individu["pays_naissance"] = ville_to_pays.get(ville, "Inconnu")

    return individus


# =============================================================================
# Task 5 : Age analysis
# =============================================================================


def analyze_ages(individus: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculates statistics on the ages of the individuals.

    Expected statistics:
        - age_moyen       : average age (rounded to 2 decimals)
        - age_minimum     : lowest age
        - age_maximum     : highest age
        - plus_de_50_ans  : number of people over 50 years old

    Args:
        individus (list[dict[str, Any]]): List of dictionaries representing the individuals.
        Each individual must have an 'age' field.

    Returns:
        dict[str, Any]: Dictionary containing the four statistics above.

    Raises:
        KeyError: If an individual is missing the 'age' field.
    """
    sum_age: int = 0
    count_age: int = 0
    age_min: float = float("inf")
    age_max: float = float("-inf")
    count_over_50: int = 0

    for individu in individus:
        if "age" not in individu:
            raise KeyError(f"Missing 'age' for individu: {individu}")

        age: int = individu["age"]

        sum_age += age
        count_age += 1
        age_min = min(age_min, age)
        age_max = max(age_max, age)
        if age > 50:
            count_over_50 += 1

    return {
        "age_moyen": round(number=sum_age / count_age, ndigits=2),
        "age_minimum": age_min,
        "age_maximum": age_max,
        "plus_de_50_ans": count_over_50,
    }


# =============================================================================
# Task 6 : BMI analysis
# =============================================================================


def analyze_imc(individus: list[dict[str, Any]]) -> dict[str, int]:
    """Categorizes individuals by BMI and returns the count per category.

    Categories:
        - maigreur     : BMI < 18.5
        - poids_normal : 18.5 <= BMI < 25
        - surpoids     : BMI >= 25

    Args:
        individus (list[dict[str, Any]]): List of dictionaries representing the individuals.
        Each individual must have an 'imc' field.

    Returns:
        dict[str, int]: Dictionary { category: number of individuals }.

    Raises:
        KeyError: If an individual is missing the 'imc' field.
        ValueError: If a BMI doesn't match any known category.
    """
    maigreur: int = 0
    poids_normal: int = 0
    surpoids: int = 0

    for individu in individus:
        if "imc" not in individu:
            raise KeyError(f"Missing 'imc' for individu: {individu}")

        imc: float = individu["imc"]

        if imc < 18.5:
            maigreur += 1
        elif 18.5 <= imc < 25:
            poids_normal += 1
        elif imc >= 25:
            surpoids += 1
        else:
            raise ValueError(f"Unexpected IMC value: {imc}")

    return {"maigreur": maigreur, "poids_normal": poids_normal, "surpoids": surpoids}


# =============================================================================
# Task 7 : Random selection (underweight)
# =============================================================================


def select_random_sous_poids(
    individus: list[dict[str, Any]],
    nb: int = 3,
) -> list[dict[str, Any]]:
    """Randomly selects a number of individuals with a BMI strictly below 18.5.

    Args:
        individus (list[dict[str, Any]]): List of dictionaries representing the individuals.
        nb (int): Number of individuals to select. Default: 3.

    Returns:
        list[dict[str, Any]]: List of selected individuals.

    Raises:
        ValueError: If the number of eligible individuals is less than nb.
    """
    eligibles: list[dict[str, Any]] = [individu for individu in individus if individu["imc"] < 18.5]

    if len(eligibles) < nb:
        raise ValueError(f"Not enough eligible individuals; found {len(eligibles)}, need {nb}")

    return random.sample(population=eligibles, k=nb)


# =============================================================================
# Task 8 : CSV export
# =============================================================================


def export_to_csv(
    data: list[dict[str, Any]],
    filename: str | Path,
    *,
    overwrite: bool,
) -> None:
    """Exports the list of individuals to a CSV file.

    The columns correspond to the keys of the first dictionary in the list.

    Args:
        data (list[dict[str, Any]]): List of dictionaries representing the individuals.
        filename (str | Path): Path to the destination CSV file.
        overwrite (bool): If True, overwrites an existing file. If False, raises an error.

    Returns:
        None

    Raises:
        FileNotFoundError: If the destination directory does not exist.
        FileExistsError: If the file already exists and overwrite=False.
    """
    path: Path = Path(filename).resolve()

    if not path.parent.exists():
        raise FileNotFoundError(f"Directory does not exists: {path}")

    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {path}")

    fieldnames: list[str] = list(data[0].keys())

    with path.open(mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(f=file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rowdicts=data)


# =============================================================================
# Task 9 : Search by country
# =============================================================================


def search_by_country(
    individus: list[dict[str, Any]],
    pays_list: list[str],
) -> dict[str, list[dict[str, Any]]]:
    """Searches for individuals born in each of the countries in the list and prints the results.

    Args:
        individus (list[dict[str, Any]]): List of dictionaries representing the individuals.
        Each individual must have a 'pays_naissance' field.
        pays_list (list[str]): List of strings representing the countries to search for.

    Returns:
        dict[str, list[dict[str, Any]]]: Dictionary { country: list of individuals from that country }.

    Raises:
        KeyError: If an individual is missing the 'pays_naissance' field.
    """
    resultats: dict[str, list[dict[str, Any]]] = {}

    for pays in pays_list:
        individus_du_pays: list[dict[str, Any]] = []

        for individu in individus:
            if "pays_naissance" not in individu:
                raise KeyError(f"Missing 'pays_naissance' for individu: {individu}")

            if individu["pays_naissance"] == pays:
                individus_du_pays.append(individu)

        print(f"{pays} : {len(individus_du_pays)} individu(s)")
        resultats[pays] = individus_du_pays

    return resultats


# =============================================================================
# Task 10 : Cleanup of temporary files
# =============================================================================


def clean_temp_files(data_dir: Path) -> None:
    """Deletes all temporary JSON and CSV files in data_dir, except 'individus.json'.

    Prints the list of deleted files for verification.

    Args:
        data_dir (Path): Folder containing the files to clean up.

    Returns:
        None
    """
    temp_files: list[Path] = [
        file
        for file in list(data_dir.glob("*.json")) + list(data_dir.glob("*.csv"))
        if file.name != "individus.json"
    ]

    if not temp_files:
        print("Aucun fichier temporaire à supprimer")
        return

    print("Fichiers temporaires supprimés :")
    for file in temp_files:
        file.unlink()
        print(f"- {file.name}")


# =============================================================================
# Main entry point
# =============================================================================

if __name__ == "__main__":
    script_dir: Path = Path(__file__).parent.resolve()
    data_dir: Path = script_dir / "data"

    # --- Task 1 : Loading ---
    individus = load_json(filename=data_dir / "individus.json")
    if not isinstance(individus, list):
        raise TypeError(f"Expected a list of individuals, got {type(individus).__name__}")
    print(f"Données chargées avec succès. Nombre d'individus : {len(individus)}")

    # --- Task 2 : Height ---
    individus_with_taille = add_taille(individus)
    save_to_json(
        data=individus_with_taille,
        filename=data_dir / "individus_with_tailles.json",
        overwrite=True,
    )
    print("Champ 'taille' ajouté et sauvegardé dans 'individus_with_taille.json'.")

    # --- Task 3 : BMI ---
    individus_with_imc = add_imc(individus_with_taille)
    save_to_json(
        data=individus_with_imc,
        filename=data_dir / "individus_with_imc.json",
        overwrite=True,
    )
    print("Champ 'imc' ajouté et sauvegardé dans 'individus_with_imc.json'.")

    # --- Task 4 : Country of birth ---
    print_ville_naissance(individus_with_imc)

    individus_with_pays = add_pays_naissance(individus_with_imc)
    save_to_json(
        data=individus_with_pays,
        filename=data_dir / "individus_with_pays.json",
        overwrite=True,
    )
    print("Champ 'pays_naissance' ajouté et sauvegardé dans 'individus_with_pays.json'.")

    # --- Task 5 : Age analysis ---
    stats_ages = analyze_ages(individus_with_pays)

    print("\nStatistiques sur les âges :")
    for key, value in stats_ages.items():
        print(f"  - {key.replace('_', ' ').capitalize()} : {value}")

    save_to_json(data=stats_ages, filename=data_dir / "stats_ages.json", overwrite=True)
    print("Statistiques sauvegardées dans 'stats_ages.json'.")

    # --- Task 6 : BMI analysis ---
    stats_imc = analyze_imc(individus_with_pays)
    print("\nStatistiques sur les IMC :")
    for key, value in stats_imc.items():
        print(f"  - {key.replace('_', ' ').capitalize()} : {value}")
    save_to_json(data=stats_imc, filename=data_dir / "stats_imc.json", overwrite=True)
    print("Statistiques sauvegardées dans 'stats_imc.json'.")

    # --- Task 7 : Random selection ---
    selection = select_random_sous_poids(individus_with_pays, nb=3)
    print("\n3 individus sous-poids sélectionnés aléatoirement :")
    for ind in selection:
        print(f"  - {ind}")
    save_to_json(data=selection, filename=data_dir / "selection_sous_poids.json", overwrite=True)
    print("Sélection sauvegardée dans 'selection_sous_poids.json'.")

    # --- Task 8 : CSV export ---
    export_to_csv(
        data=individus_with_pays,
        filename=data_dir / "individus_complets.csv",
        overwrite=True,
    )
    print("\nDonnées exportées dans 'individus_complets.csv'.")

    # --- Task 9 : Search by country ---
    pays_a_rechercher = ["France", "Portugal", "Inconnu"]  # à adapter selon vos données
    resultats_par_pays = search_by_country(
        individus=individus_with_pays, pays_list=pays_a_rechercher
    )

    for pays, individus_du_pays in resultats_par_pays.items():
        save_to_json(
            data=individus_du_pays,
            filename=data_dir / f"individus_par_pays_{pays}.json",
            overwrite=True,
        )

    # --- Task 10 : Cleanup ---
    clean_temp_files(data_dir=data_dir)
