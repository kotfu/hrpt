#
#
"""Development related tasks to be run with 'invoke'"""

import contextlib
import os
import pathlib
import shutil

import invoke


# shared function
def rmrf(items, verbose=True):
    "Silently remove a list of directories or files"
    if isinstance(items, (str, pathlib.PosixPath)):
        items = [items]

    for item in items:
        if verbose:
            print(f"Removing {item}")
        shutil.rmtree(item, ignore_errors=True)
        # rmtree doesn't remove bare files
        with contextlib.suppress(FileNotFoundError):
            os.remove(item)


# create namespaces
namespace = invoke.Collection()
namespace_clean = invoke.Collection("clean")
namespace.add_collection(namespace_clean, "clean")

namespace_check = invoke.Collection("check")
namespace.add_collection(namespace_check, "check")


@invoke.task(name="ruff")
def ruff_lint(context):
    "Check code quality using ruff"
    context.run("ruff check *.py tests src", echo=True)


namespace_check.add_task(ruff_lint)


@invoke.task(name="format")
def format_check(context):
    """Check if code is properly formatted using ruff"""
    context.run("ruff format --check *.py tests src", echo=True)


namespace_check.add_task(format_check)


@invoke.task(name="format")
def formatt(context):
    """Format code using ruff"""
    context.run("ruff format *.py tests src", echo=True)


namespace.add_task(formatt)


#####
#
# build and distribute
#
#####
DISTDIR = pathlib.Path("dist")


@invoke.task
def dist_clean(context):
    "Remove the dist directory"
    rmrf(DISTDIR)


namespace_clean.add_task(dist_clean, "dist")


@invoke.task
def eggs_clean(context):
    "Remove egg directories"
    dirs = set()
    dirs.add(".eggs")
    for _, _, files in os.walk(os.curdir):
        for file in files:
            if file.endswith(".egg"):
                dirs.add(file)
    rmrf(dirs)


namespace_clean.add_task(eggs_clean, "eggs")


@invoke.task
def bytecode_clean(context):
    "Remove __pycache__ directories and *.pyc files"
    dirs = set()
    for dirpath, _, files in os.walk(os.curdir):
        if dirpath == "__pycache__":
            dirs.add(dirpath)
        for file in files:
            if file.endswith(".pyc"):
                dirs.add(os.path.join(dirpath, file))
    print("Removing __pycache__ directories and .pyc files")
    rmrf(dirs, verbose=False)


namespace_clean.add_task(bytecode_clean, "bytecode")


@invoke.task(pre=list(namespace_clean.tasks.values()), default=True)
def clean_all(context):
    "Clean everything"


namespace_clean.add_task(clean_all, "all")


@invoke.task(pre=[clean_all])
def build(context):
    "Create a source distribution"
    context.run("python -m build")


namespace.add_task(build)


@invoke.task(pre=[build])
def twine(context):
    "Check for rendering errors in README.rst"
    context.run("twine check dist/*")


namespace_check.add_task(twine)


@invoke.task(pre=[build, twine])
def pypi(context):
    "Build and upload a distribution to pypi"
    context.run("twine upload dist/*")


namespace.add_task(pypi)


@invoke.task(pre=[build, twine])
def testpypi(context):
    "Build and upload a distribution to https://test.pypi.org"
    context.run("twine upload -r testpypi dist/*")


namespace.add_task(testpypi)

# we don't need pytest here because tox will run pytest for us
checktasks = []
for task in list(namespace_check.tasks.values()):
    if task.name != "pytest":
        checktasks.append(task)


@invoke.task(pre=checktasks, default=True)
def check_all(context):
    "Run this before you commit or submit a pull request"


namespace_check.add_task(check_all, "all")
