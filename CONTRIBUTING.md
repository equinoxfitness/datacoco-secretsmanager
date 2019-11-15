# Contributing Guidelines

Thank you for contributing to datacoco_secretsmanager!
  
## Local development setup

datacoco-secretsmanager requires Python 3.6+

```
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt

```

Please install [pre-commit](https://pre-commit.com) git hooks to use [Black](https://black.readthedocs.io/en/stable/) autoformatting and flake8 PEP8 validations by running:

```
pre-commit install

```

## Tests
Run [tox](https://tox.readthedocs.io/en/latest/) to validate tests are working

```
tox
```

To run tox for multiple Python 3 versions, you can use  [pyenv](https://github.com/pyenv/pyenv) to install and manage different Python versions locally

If you see an error indicating a missing Python version, ie:
`SKIPPED: InterpreterNotFound: python3.7`

- See if you have the version specified: `pyenv versions`
- If not, install it: `pyenv install 3.7.0`
- Make available to your local directory: `pyenv local 3.7.0`
- Run `tox` again