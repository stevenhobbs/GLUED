## Environment Setup (Pipenv)
This repository uses:
 - `pyenv` to pin the Python version
 - `pipenv` for dependenceis
 - `direnv` to auto-load `PIPENV_VENV_IN_PROJECT=1`, which keeps the virtual environment localy in `./.venv`

## One-time steps (machine setup):
1. Install Python 3.11.11
    `pyenv install 3.11.11`
2. Install direnv:
    `brew install direnv`
3. Update .zshrc
    `echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc`
    `source ~/.zshrc`

## Project setup
1. Pin the python version within the repository
    `pyenv local 3.11.11`
2. Allow direnv within the repository
    `direnv allow`
5. Create environment
    `pipenv --python "$(pyenv which python)"`
    `pipenv install`