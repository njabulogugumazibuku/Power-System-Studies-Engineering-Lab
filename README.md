# Power System Studies Engineering Lab

An educational Python project for learning, implementing, and testing power-system studies through small, reproducible engineering examples.

The repository combines power-system theory with software development practices: clear input data, modular calculations, automated tests, and documented assumptions. It is intended for engineers and students who want to understand both the calculations and how to implement them in Python.

> **Status:** Educational project under active development. Do not use its results for operational, planning, protection, or other real-world engineering decisions without independent engineering validation.

## What you can do here

- Explore a small power-system network defined in CSV files.
- Load and validate the network model using Python.
- Develop and test power-system calculations incrementally.
- Learn through worked examples, unit tests, and documented assumptions.
- Extend the project with additional studies as the model matures.

## Repository guide

| Location | What it is for |
|---|---|
| `01_system_model/` | Network input data in CSV format and related system-model assets. |
| `src/power_system/` | Python package containing the network model, input/output functions, calculations, and validation logic. |
| `tests/` | Automated tests for calculations, data loading, and model validation. |
| `docs/` | Engineering reference material, worked calculations, data definitions, verification guidance, and recorded decisions. |
| `pyproject.toml` | Python project metadata, package configuration, and test configuration. |

The network input files are maintained separately from the calculation code. This makes it easier to inspect the input data and understand which values a calculation uses.

### Where should I start?

- **New to the repository?** Start here, then inspect `01_system_model/` and `01_system_model/load_model.py`.
- **Want to understand the engineering assumptions?** Read `docs/study_basis.md`.
- **Need to interpret the CSV columns?** Read `docs/data_dictionary.md`.
- **Want to follow a calculation by hand?** Read `docs/worked_examples.md`.
- **Want to understand how the model is checked?** Read `docs/verification_checklist.md` and explore `tests/`.
- **Want to understand why a modelling choice was made?** Read `docs/engineering_decisions.md`.

Some files may be added as the project develops. If a path listed above is not yet present in the current branch, use the files that are available and treat the relevant documentation as planned or in progress.

## Prerequisites

You will need:

- **Git** to clone the repository.
- **Python 3.10 or later**.
- **pip**, included with standard Python installations, to install the project and its development tools.
- A terminal and a code editor. VS Code or another Python-capable editor is suitable.

The project uses a `src/` package layout and is configured through `pyproject.toml`. The test suite uses `pytest`.

No database or external power-system simulation application is required for the basic Python workflow described below.

## Setup

### 1. Clone the repository

Replace `<repository-url>` with the clone URL shown on the repository's GitHub page.

```bash
git clone <repository-url>
cd power-system-studies-engineering-lab
```

If you already have the repository locally, change into its root directory instead.

### 2. Create a virtual environment

A virtual environment keeps this project's Python packages separate from other Python projects.

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

If your system does not have the required Python version, install Python 3.10 or later before continuing.

### 3. Install the project

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

The editable install makes the package importable from the development checkout without repeatedly reinstalling it after every source-code change.

### 4. Install the test tool

If `pytest` is not already installed in the virtual environment, install it:

```bash
python -m pip install pytest
```

The repository's `pyproject.toml` configures pytest to look for tests in `tests/` and adds `src/` to the Python import path.

> **Dependency note:** If the project later declares development dependencies or an optional development extra in `pyproject.toml`, prefer installing those declared dependencies rather than maintaining a separate manual list.

## Run the project

Run commands from the **repository root**, unless a command says otherwise.

### Load and inspect the network model

The repository includes a script for loading the CSV-based model:

```bash
python 01_system_model/load_model.py
```

This script should load the network data and print a model summary. If it fails, check that you are in the repository root, that the expected CSV files are present, and that the package has been installed in the active virtual environment.

### Run the automated tests

Run the full test suite:

```bash
python -m pytest
```

For a more detailed report:

```bash
python -m pytest -v
```

Run a single test file when working on a particular feature:

```bash
python -m pytest tests/test_csv_loader.py
```

Test filenames and available test modules may evolve as the project grows. Use `pytest --collect-only -q` to see which tests pytest currently discovers.

### Deactivate the virtual environment

When you are finished:

```bash
deactivate
```

To return to the project later, open a terminal in the repository and activate `.venv` again.

## Typical development workflow

1. **Understand the problem.** Read the relevant engineering notes and identify the inputs and assumptions.
2. **Inspect the network data.** Check the relevant CSV rows and units before writing calculations.
3. **Implement one small calculation.** Keep engineering logic in the Python package rather than duplicating it in scripts.
4. **Write or update tests.** Cover normal results, boundary conditions, and invalid inputs where appropriate.
5. **Run the tests.** Use `python -m pytest` before committing.
6. **Document meaningful changes.** Update the relevant document in `docs/` when assumptions, equations, supported data fields, or model behaviour change.

A useful learning loop for this repository is:

**Learn → derive by hand → implement → test → interpret → document.**

## Working with Git

Check the current working tree:

```bash
git status
```

Review the changes:

```bash
git diff
```

Stage and commit a change:

```bash
git add <path-to-file>
git commit -m "Describe the change"
```

Push your branch to GitHub using the branch and remote configured for your checkout:

```bash
git push
```

Before committing, make sure you have not accidentally staged virtual-environment files, caches, generated outputs, or unrelated changes.

## Troubleshooting

### `ModuleNotFoundError: No module named 'power_system'`

- Confirm that the virtual environment is active.
- From the repository root, run `python -m pip install -e .`.
- Check that you are using the same Python interpreter for installation and execution.

### `pytest` is not found

Run:

```bash
python -m pip install pytest
python -m pytest
```

Using `python -m pytest` helps ensure pytest runs with the active Python interpreter.

### The CSV loader cannot find a file

- Run the script from the repository root.
- Confirm that the expected CSV files exist under `01_system_model/`.
- Check the file names and required column names.
- Read the error message before changing paths or data.

### Tests fail after a change

- Read the first failing test and its assertion or traceback.
- Determine whether the failure is caused by the code, input data, or an outdated test expectation.
- Avoid changing a test simply to make it pass unless the expected behaviour itself has been shown to be incorrect.

## Project scope and limitations

This is a learning and software-engineering project. Its calculations and model capabilities are limited to what is implemented and tested in the current codebase. A documented future feature should not be assumed to be implemented.

Do not use the model as a substitute for validated utility-grade software, approved study procedures, or review by a suitably qualified engineer.

## Contributing

Contributions that improve correctness, readability, tests, or learning value are welcome.

Before proposing a change:

- Keep calculations small and explainable.
- State units and assumptions explicitly.
- Add tests for new behaviour.
- Keep example values distinguishable from actual network inputs.
- Update the relevant engineering documentation when needed.
- Avoid committing secrets, local environment files, virtual environments, or generated caches.

## License

No license is specified here. Check the repository for a `LICENSE` file before reusing, modifying, or redistributing the code.
