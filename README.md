# UDA Final Project – MPC Text Mining

This repository contains the code and notebooks for a text‑mining analysis of Bank of England Monetary Policy Committee (MPC) minutes.

The main goal is to turn the wording of MPC minutes into simple numerical indicators that can be related to interest‑rate decisions and asset price moves.

## Files and Folders

- `UDA_pipeline.ipynb` – main notebook that loads the data, preprocesses text and runs the analysis.
- `data/` – input data files and any saved intermediate outputs (not tracked in version control by default).
- `Images/` – figures exported from the notebook (for the report).
- `scripts/` – small helper scripts used by the notebook, if any.
- `requirements.txt` – list of Python packages needed to run the notebook.
- `CentralBankRoBERTa/` – cloned repository with the CentralBankRoBERTa model code (used inside the notebook).

## Quick Start

1. Open a terminal in this folder.
3. Install dependencies

```powershell
pip install -r requirements.txt
```

4. Open `UDA_pipeline.ipynb` in Jupyter or VS Code and run the cells from top to bottom.

All of the project logic (data loading, preprocessing and modelling) is contained in that notebook.

