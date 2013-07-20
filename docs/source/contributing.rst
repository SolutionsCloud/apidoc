Contributing
============

Installation
------------

The safest way to install ApiDoc for contributors is to use virtualenvs

.. code-block:: console

   $ sudo apt-get install git python3 python3-setuptools python3-pip
   $ sudo pip install virtualenv
   $ virtualenv -p /usr/bin/python3 vitualenvs/apidoc
   $ source vitualenvs/apidoc/bin/activate
   $ git clone https://github.com/SFR-BT/apidoc.git
   $ cd apidoc
   $ pip install -r requirements.txt


Generating self documentation
-----------------------------

You can build and display

.. code-block:: console

    $ cd docs
    $ make html
    $ firefox ./build/html/index.html


Running Tests
-------------

Two set of tests are imlpemented. Behaviours Test with `behave` and UnitTests with `unittest`

BehavioursTest

.. code-block:: console

   $ behave tests/features


UnitTess


.. code-block:: console

   $ nosetests

WithCoverage


.. code-block:: console

   $ nosetests --with-coverage --cover-package=apidoc --cover-package=util --cover-erase --cover-html --cover-branch --cover-html-dir=tests/cover/unit
   $ coverage run --branch `which behave` tests/features/; coverage html --include=apidoc* -d tests/cover/features
   $ coverage run --branch `which behave` tests/features/; coverage run --append --branch `which nosetests`; coverage html --include=apidoc* -d tests/cover/unified
