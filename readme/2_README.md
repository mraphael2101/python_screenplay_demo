pre-requisites
 - pip install selenium
 - pip install pytest
 - pip install pytest-html
 - pip install requests
 - pip install jsonpath


Pytest configuration rules
- Test files can have just function for classes
- If class, then '__init__()' should not exist
- Functions must start with 'test_*'
- Class names must start with 'Test' and methods with 'test_' e.g.
    Class TestFooBar(object):
        def test_verify_something():

- To run the test:
$ pytest <options>
$ pytest <options> /path/to/test/filesc
$ python -m pytest <options> /path/to/test/files 
$ pytest -m regression
$ pytest -m "smoke or regression" ./tests
$ pytest -m "not prod" ./tests

- In Pytest, to handle setup and teardown we use the concept of fixtures 
  (otherwise known as hooks in different frameworks)