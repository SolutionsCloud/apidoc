Usage of ApiDoc
===============

Main commands
-------------

`apidoc` builds the full documentation

.. code-block:: console

    $ apidoc -h


Generics Arguments
------------------

To generate documentation from a given source file:

.. code-block:: console

    $ apidoc -f ./example/source_simple/simple.yml

see page :ref:`source-page`


To generate documentation from split sources in multiple files:

.. code-block:: console

    $ apidoc -f ./example/source_multiple/one.yml ./example/source_multiple/two.yml

see page :ref:`source-page`


To generate documentation from the files contained in a given directory:

.. code-block:: console

    $ apidoc -d ./example/source_multiple/

see page :ref:`source-page`


To generate documentation with options defined in a given config file:

.. code-block:: console

    $ apidoc -c ./example/config/config.yaml

see page :ref:`config-page`


Combining those options:

.. code-block:: console

    $ apidoc -c ./config.yaml -d ./folder1/ ./folder2/ -f /folder3/file.yaml /folder3/file.json


Analyse the sources files without buiilding the documentation:

.. code-block:: console

    $ apidoc -f ./example/source_simple/simple.yml -y


Render automaticly the documentation each time a file is changed:

.. code-block:: console

    $ apidoc -f ./example/source_simple/simple.yml -w


Display less logging informations

.. code-block:: console

    $ apidoc -f ./example/source_simple/simple.yml -q
    $ apidoc -f ./example/source_simple/simple.yml -qq


Display traceback (for advanced users)

.. code-block:: console

    $ apidoc -f ./example/source_simple/simple.yml -t

