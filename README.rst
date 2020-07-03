backward - *A Backward-Chaining Inference Engine*
=================================================

A simple programming language and inference engine powered by backward chaining.
When given rules and facts, it will deduce new information.

|made-with-python| |PyPI-package-version| |PyPI-license| |PyPI-python-versions| |travis-ci| |PyPI-downloads-month|

Installation
------------

``pip install backward``

Usage
-----

.. code:: python

   >>> from backward import Backward
   
   >>> ctx = Backward()
   >>> _ = ctx.evaluate("a => b")
   >>> _ = ctx.evaluate("b => c")
   >>> _ = ctx.evaluate("= a")  # a is true
   >>> ctx.evaluate("a b c")  # are b and c true?
   [True, True, True]

You can also type ``python -m backward`` into your shell to enter an interactive REPL.

Syntax
------

::

   C => E          # C implies E
   A & B & C => D  # A and B and C implies D
   A | B => C      # A or B implies C
   A & !B => F     # A and not B implies F
   C | !G => H     # C or not G implies H
   V ^ W => X      # V xor W implies X
   A & B => Y & Z  # A and B implies Y and Z

   = A B G         # Initial facts : A, B and G are true. All others are false.
   G V X           # What are G, V and X ?

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
.. |travis-ci| image:: https://travis-ci.com/gidona18/backward.svg?branch=master
   :target: https://travis-ci.com/gidona18/backward
