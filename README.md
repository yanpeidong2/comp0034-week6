# COMP0034 2023 Week 6 starter code and activities

## Activities

- [Weekly coding activities](/activities/activities.md)
- [Getting started with coursework 2](/activities/coursework_getting_started.md)
- [Optional activity: Blueprints](/activities/blueprints.md)
- [Optional activity: Configuring Flask from a Python class](/activities/configuration.md)

## Setup

Two options are provided for setup.

This assumes you have already created a copy of the code in your own GitHub account and cloned it to your computer for use in your IDE (VS Code, PyCharm etc).

To date you have used then following approach. This can still be used:

### 1. venv + pip

- Create and activate a virtual environment
- Install the dependencies `pip install -r requirements.txt`
- Install the code you will develop `pip install -e .`

The experience has varied between students as there are inconsistent behaviours with imports when using this approach.

### 2. poetry

This is an alternative approach for managing packaging and dependencies in Python. It is **hoped** this may address some of the inconsistency with package imports experienced by students. This has not been proven to be the case however as it only just being introduced in the teaching materials this week.

#### 2.1 Install poetry (once only in the base Python environment)

If you have never used poetry then need to first install it. You only need this once, you won't need to repeat it for the rest of this course. You install it in the base python installation and NOT in a venv.

You must have a version of Python that is 3.7 or greater.

The documentation recommends:

```
# Windows powershell

(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -

# Mac / Linux shell
curl https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
```

The check it is installed by running the following, and you should get a version number returned:

```
poetry --version
```

If the version of poetry is not returned from the second command then you need add it to your PATH. See the [poetry installation documentation](https://python-poetry.org/docs/#installing-with-pipx).

#### 2.2 Setup the project environment using poetry

In the VS Code/PyCharm terminal in the project code directory: `poetry env list`. There should not be any output from this command.

Create a vitual environment using Python 3 (must be 3.7 or later): `poetry env use python3`

You should see a message indicating that the virtual environment is being created.

As long as you’re inside your project folder, Poetry will now use the virtual environment associated with it.

Now type: `poetry install` to install the dependencies for the project. The dependencies are listed in a file called `pyproject.toml`.

If you type `poetry show` you should see the packages that have been installed.

#### 2.3 Install your own project code

Now install your code in 'editable' mode by running `pip install -e .`

## Further information

If you want to add packages not listed in `pyproject.toml` then you can use a command similar to pip: `poetry add requests` would install the `requests` package.

[RealPython poetry tutorial](https://realpython.com/dependency-management-python-poetry/).

[Guide here to using VS Code with poetry]()<https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1)>

[Python poetry pyproject.toml keywords](https://python-poetry.org/docs/pyproject/)
