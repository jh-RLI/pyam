import io
import os
import subprocess
import sys
import tempfile
import pytest

from conftest import here

try:
    import nbformat
    jupyter_installed = True
except:
    jupyter_installed = False

jupyter_reason = 'requires Jupyter Notebook to be installed'

try:
    pandoc_installed = subprocess.call(['which', 'pandoc']) == 0
except:
    pandoc_installed = False

pandoc_reason = 'requires Pandoc to be installed'

tut_path = os.path.join(here, '..', 'doc', 'source', 'tutorials')

# taken from the execellent example here:
# https://blog.thedataincubator.com/2016/06/testing-jupyter-notebooks/


def _notebook_run(path, kernel=None, capsys=None):
    """Execute a notebook via nbconvert and collect output.
    :returns (parsed nb object, execution errors)
    """
    major_version = sys.version_info[0]
    kernel = kernel or 'python{}'.format(major_version)
    dirname, __ = os.path.split(path)
    os.chdir(dirname)
    fname = os.path.join(here, 'test.ipynb')
    args = [
        "jupyter", "nbconvert", "--to", "notebook", "--execute",
        "--ExecutePreprocessor.timeout=60",
        "--ExecutePreprocessor.kernel_name={}".format(kernel),
        "--output", fname, path]
    subprocess.check_call(args)

    nb = nbformat.read(io.open(fname, encoding='utf-8'),
                       nbformat.current_nbformat)

    errors = [
        output for cell in nb.cells if "outputs" in cell
        for output in cell["outputs"] if output.output_type == "error"
    ]

    os.remove(fname)

    return nb, errors


@pytest.mark.skipif(not jupyter_installed, reason=jupyter_reason)
@pytest.mark.skipif(not pandoc_installed, reason=pandoc_reason)
def test_pyam_first_steps(capsys):
    fname = os.path.join(tut_path, 'pyam_first_steps.ipynb')
    nb, errors = _notebook_run(fname, capsys=capsys)
    assert errors == []
    assert os.path.exists(os.path.join(tut_path, 'tutorial_export.xlsx'))
    assert os.path.exists(os.path.join(tut_path, 'tutorial_metadata.xlsx'))


@pytest.mark.skipif(not jupyter_installed, reason=jupyter_reason)
@pytest.mark.skipif(not pandoc_installed, reason=pandoc_reason)
def test_checking_databases():
    fname = os.path.join(tut_path, 'checking_databases.ipynb')
    nb, errors = _notebook_run(fname)
    assert errors == []


@pytest.mark.skipif(not jupyter_installed, reason=jupyter_reason)
@pytest.mark.skipif(not pandoc_installed, reason=pandoc_reason)
def test_pyam_logo():
    fname = os.path.join(tut_path, 'pyam_logo.ipynb')
    nb, errors = _notebook_run(fname)
    assert errors == []


@pytest.mark.skipif(not jupyter_installed, reason=jupyter_reason)
@pytest.mark.skipif(not pandoc_installed, reason=pandoc_reason)
def test_iiasa_dbs():
    fname = os.path.join(tut_path, 'iiasa_dbs.ipynb')
    nb, errors = _notebook_run(fname)
    assert errors == []


@pytest.mark.skipif(not jupyter_installed, reason=jupyter_reason)
@pytest.mark.skipif(not pandoc_installed, reason=pandoc_reason)
def test_ipcc_colors():
    fname = os.path.join(tut_path, 'ipcc_colors.ipynb')
    nb, errors = _notebook_run(fname)
    assert errors == []
