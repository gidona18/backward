backward - *A Backward-Chaining Inference Engine*
=================================================

A small programming language that can deduce new information when given a set of rules and facts.

|made-with-python| |PyPI-package-version| |PyPI-license| |PyPI-python-versions| |travis-ci| |PyPI-downloads-month|

Installation
------------

``pip install backward``

Usage
-----

.. code:: python


   >>> from backward import Backward
   
   >>> ctx = Backward()
   >>> ctx.evaluate("a => b")
   >>> ctx.evaluate("b => c")
   >>> ctx.evaluate("= a")  # a is true
   >>> ctx.evaluate("a b c")  # are b and c true?
   [True, True, True]

You can also call ``python -m backward`` from your shell to enter an interactive REPL.

Contributing
------------
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
.. |PyPI-downloads-month| image:: https://img.shields.io/pypi/dm/backward.svg
   :target: https://pypi.python.org/pypi/backward/
.. |PyPI-package-version| image:: https://img.shields.io/pypi/v/backward.svg
   :target: https://pypi.python.org/pypi/backward/
.. |PyPI-license| image:: https://img.shields.io/pypi/l/backward.svg
   :target: https://pypi.python.org/pypi/backward/
.. |PyPI-python-versions| image:: https://img.shields.io/pypi/pyversions/backward.svg
   :target: https://pypi.python.org/pypi/backward/
.. |travis-ci| image:: https://travis-ci.com/jellowfish/backward.svg?branch=master
   :target: https://travis-ci.com/jellowfish/backward
