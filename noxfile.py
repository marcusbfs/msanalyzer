"""Nox sessions."""
import subprocess
import sys
from textwrap import dedent

import nox

try:
    from nox_poetry import Session, session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message))


package = "msanalyzer"
python_versions = ["3.9", "3.8", "3.7"]
nox.options.sessions = (
    "format",
    "tests",
)

all_test = ["tests"]
all_src = ["src"]
all_scripts = ["noxfile.py"]
all_code = all_src + all_scripts + all_test


@session(python=False, reuse_venv=True)
def format(session: Session) -> None:
    """Format code."""
    session.run(
        "autoflake",
        "-i",
        "--remove-unused-variables",
        "--remove-all-unused-imports",
        "-r",
        *all_code,
        external=True,
    )
    session.run("isort", *all_code, external=True)
    session.run("black", *all_code, external=True)


@session(python=False, reuse_venv=True)
def safety(session: Session) -> None:
    """Perform safety checks"""
    session.run("bandit", "-r", *all_src, external=True)


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["src", "tests", "docs/conf.py"]
    session.install(".")
    session.install("mypy", "pytest")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install("pytest", "pytest-sugar")
    session.run("pytest", *session.posargs)


@session(python=False)
def build(session: Session) -> None:
    """Build the wheels and tar.gz"""
    subprocess.call(["poetry", "build"], shell=True)


@session(python=False)
def version(session: Session) -> None:
    """Bump version number"""
    args = session.posargs
    if not args:
        print("Use one of the following arg: major, minor, patch")
        return
    session.run("bump2version", *args, external=True)
