Quick Start
============

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

Run a sample demo
-----------------

.. code-block:: console

   $ mkdir apidoc
   $ cd apidoc
   $ wget https://raw.github.com/SFR-BT/apidoc/master/example/demo/source.yml
   $ apidoc-render -f source.yml -o output/index.html
   $ firefox output/index.html