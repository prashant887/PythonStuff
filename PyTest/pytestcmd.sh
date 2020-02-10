pytest
pytest --help
pytest test_funs.py
pytest -v test_funs.py
pytest -v
pytest -v test_funs.py::test_add_strings
pytest -v test_funs.py -k "add"
pytest -v test_funs.py -k "add or strings"
pytest -v test_funs.py -k "add and strings"
pytest -v test_funs.py -m number
pytest -v test_funs.py -m strings
pytest -v test_funs.py -x
pytest -v test_funs.py -x --disable-warnings
pytest -v test_funs.py -x --disable-warnings --maxfail=2
pytest -v test_funs.py -x --disable-warnings --maxfail=5
pytest -v test_funs.py -x --disable-warnings --maxfail=5 -s
pytest -v test_funs.py -x --disable-warnings --maxfail=5  -s
pytest -v test_funs.py --disable-warnings --maxfail=5  -s
pytest -v test_funs.py --disable-warnings
pytest -v test_funs.py --disable-warnings -s
