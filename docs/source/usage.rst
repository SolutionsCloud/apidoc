Usage of ApiDoc
===============

Main commands
-------------

`apidoc-analyse` provides a way to check configuration files

.. code-block:: console

   $ apidoc-analyse -h


`apidoc-render` builds the full documentation

.. code-block:: console

   $ apidoc-render -h


`apidoc-watch` build the full documentation each time a source file or a template file is modified

.. code-block:: console

   $ apidoc-watch -h


Generics Arguments
------------------

To generate documentation from a given source file:

.. code-block:: console

   $ apidoc-render -f ./example/source_simple/simple.yml

see page :ref:`source-page`


To generate documentation from split sources in multiple files:

.. code-block:: console

   $ apidoc-render -f ./example/source_multiple/one.yml ./example/source_multiple/two.yml

see page :ref:`source-page`


To generate documentation from the files contained in a given directory:

.. code-block:: console

   $ apidoc-render -d ./example/source_multiple/

see page :ref:`source-page`


To generate documentation with options defined in a given config file:

.. code-block:: console

   $ apidoc-render -c ./example/config/config.yaml

see page :ref:`config-page`


Combining those options:

.. code-block:: console

   $ apidoc-render -c ./config.yaml -d ./folder1/ ./folder2/ -f /folder3/file.yaml /folder3/file.json