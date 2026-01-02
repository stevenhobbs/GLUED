## Environment Setup (Pipenv and Conda)
This repository uses:
 - Pipenv for the main analysis, GLUED.py
 - Conda for Pymer4 and R dependencies used in GLUED_LMM.py

## Optional
 - `pyenv` to pin Python 3.11.11
 - `direnv` auto load env vars from .envrc when cd'ing into the repo.
 - .envrc sets `PIPENV_VENV_IN_PROJECT=1` to create the Pipenv venv locally in `./.venv`

## Optional direnv setup:
1. Install direnv:
    `brew install direnv`
2. Enable direnv in shell
    `echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc`
    `source ~/.zshrc`

## Optional (pyenv)
1. `pyenv install 3.11.11`
2. `pyenv local 3.11.11`
3. `direnv allow`

## Main environment
3. Create Pipenv environment
    `pipenv --python "$(pyenv which python)"` OR `pipenv --python 3.11`
    `pipenv install`
4. Create Conda environment
    `conda env create -f envs/pymer4/environment.yml`

## Data
Three data files are available at https://github.com/cbshuang/cbds-take-home/tree/main:
 - Countries GDP 1960-2020.csv
 - enrollments.csv
 - enrollments_schema.csv