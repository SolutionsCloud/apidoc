ApiDoc
======

.. image:: https://travis-ci.org/SolutionsCloud/apidoc.png?branch=master
        :target: https://travis-ci.org/SolutionsCloud/apidoc
.. image:: https://coveralls.io/repos/SolutionsCloud/apidoc/badge.png
        :target: https://coveralls.io/r/SolutionsCloud/apidoc
.. image:: https://pypip.in/v/ApiDoc/badge.png
        :target: https://crate.io/packages/ApiDoc
.. image:: https://pypip.in/d/ApiDoc/badge.png
        :target: https://crate.io/packages/ApiDoc

Summary
-------

`ApiDoc <http://solutionscloud.github.io/apidoc>`_ is a documentation generator designe for API built with Python.

.. image:: https://raw.github.com/SolutionsCloud/apidoc/master/docs/source/_static/screenshot_sample.png

It's developed by `Jérémy Derussé <http://github.com/jeremy-derusse>`_ and `SFR Business Team <http://www.sfrbusinessteam.fr>`_.

`Full documentation available on ReadTheDocs. <http://apidoc.rtfd.org>`_

`Demo available on http://solutionscloud.github.io/apidoc/demo <http://solutionscloud.github.io/apidoc/demo>`_



Installation
------------

The fastest way to get started is by using the command line tool

.. code-block:: console

    $ sudo apt-get install python3-pip
    $ pip3 install apidoc


The config parser script depends on PyYAML which links with LibYAML, which brings a performance boost to the PyYAML parser. However, installing LibYAML is optional but recommended. On Mac OS X, you can use homebrew to install LibYAML:


.. code-block:: console

    $ brew install libyaml

On Linux, use your favorite package manager to install LibYAML. Here's how you do it on Debian/Ubuntu:


.. code-block:: console

    $ sudo apt-get install libyaml-dev

On Windows, please install PyYAML using the binaries they provide


Try it
------

You can download a sample file and try to render it documentation

.. code-block:: console

    $ mkdir apidoc
    $ cd apidoc
    $ wget https://raw.github.com/SolutionsCloud/apidoc/master/example/demo/source.yml
    $ apidoc-render -f source.yml -o output/index.html
    $ firefox output/index.html
