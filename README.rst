ApiDoc
======

.. image:: https://travis-ci.org/SolutionsCloud/apidoc.png?branch=master
        :target: https://travis-ci.org/SolutionsCloud/apidoc
.. image:: https://coveralls.io/repos/SolutionsCloud/apidoc/badge.png
        :target: https://coveralls.io/r/SolutionsCloud/apidoc
.. image:: https://pypip.in/v/ApiDoc/badge.png
        :target: https://preview-pypi.python.org/project/ApiDoc
.. image:: https://pypip.in/d/ApiDoc/badge.png
        :target: https://preview-pypi.python.org/project/ApiDoc
.. image:: https://requires.io/github/SolutionsCloud/apidoc/requirements.png?branch=develop
        :target: https://requires.io/github/SolutionsCloud/apidoc/requirements/?branch=develop

Summary
-------

`ApiDoc <http://solutionscloud.github.io/apidoc>`_ is a documentation generator designe for API built with Python and given by `SFR Business Team <http://www.sfrbusinessteam.fr>`_.

.. image:: https://raw.github.com/SolutionsCloud/apidoc/master/docs/source/_static/screenshot_sample.png

* Demo: http://solutionscloud.github.io/apidoc/demo
* Home Page: http://solutionscloud.github.io/apidoc
* Documentation: http://apidoc.rtfd.org
* Bug Tracker: https://github.com/SolutionsCloud/apidoc/issues
* GitHub: https://github.com/SolutionsCloud/apidoc
* PyPI: https://preview-pypi.python.org/project/ApiDoc
* License: GPLv3+


Installation
------------

The fastest way to get started is by using the command line tool

.. code-block:: console

    $ sudo apt-get install python3-pip
    $ pip3 install apidoc

If the package python3-pip does not exists

.. code-block:: console

   $ sudo apt-get install python3-setuptools
   $ sudo easy_install3 pip
   $ sudo pip3-2 install apidoc


Try it
------

You can download a sample file and try to render it documentation

.. code-block:: console

    $ mkdir apidoc
    $ cd apidoc
    $ wget https://raw.github.com/SolutionsCloud/apidoc/master/example/demo/source.yml
    $ apidoc -i source.yml -o output/index.html
    $ firefox output/index.html
