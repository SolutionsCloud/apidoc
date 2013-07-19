ApiDoc
======

[![Build Status](https://travis-ci.org/SFR-BT/apidoc.png?branch=master)](https://travis-ci.org/SFR-BT/apidoc) [![Coverage Status](https://coveralls.io/repos/SFR-BT/apidoc/badge.png)](https://coveralls.io/r/SFR-BT/apidoc)


![Screenshot](/docs/source/_static/screenshot_sample.png)

Summary
-------

ApiDoc is a documentation generator designe for API built with Python.
It's developed by Jérémy Derussé and [SFR](http://www.sfrbusinessteam.fr).

ApiDoc actually consists of a command line interface, maintained in a single repository.
By using this application you automatically require all of the necessary modules dependencies which are:

For core application

* PyYAML
* Jinja2
* JsonSchema

For developers who want to contribute code to ApiDoc

* behave
* coverage
* mock
* nose


Installation for users
----------------------

The fastest way to get started is by using the command line tool

    $ sudo apt-get install python3-pip
    $ pip3 install apidoc


The config parser script depends on PyYAML which links with LibYAML, which brings a performance boost to the PyYAML parser. However, installing LibYAML is optional but recommended. On Mac OS X, you can use homebrew to install LibYAML:

    brew install libyaml

On Linux, use your favorite package manager to install LibYAML. Here's how you do it on Debian/Ubuntu:

    sudo apt-get install libyaml-dev

On Windows, please install PyYAML using the binaries they provide


Installation for contributors
-----------------------------

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

    $ behave tests/features


UnitTess

    $ nosetests --with-coverage --cover-package=apidoc --cover-package=util --cover-erase --cover-html


Using the Application
-------------

The application analyse provide a way to check configuration files

    $ apidoc-analyse -h


The application build the full documentation

    $ apidoc-render -h


The application build the full documentation each time a source file or a template file is modificated

    $ apidoc-watch -h


Generate documentation from a source file

    $ apidoc-render -f ./example/source_simple/simple.yml


Split sources in multiple files

    $ apidoc-render -f ./example/source_multiple/one.yml ./example/source_multiple/two.yml


Generate documentation from files contained in a directory

    $ apidoc-render -d ./example/source_multiple/


Generate documentation with options definied in a config file

    $ apidoc-render -c ./example/config/config.yaml


Mix everything

    $ apidoc-render -c ./config.yaml -d ./folder1/ ./folder2/ -f /folder3/file.yaml /folder3/file.json


Todo
----

* RunMode: The end user can run the methods through his browser
* Simplify Sources: When the API have only one version or only one section, The keys version and section could be ommited in sources files
* Allow extension everywhere (will replace references)
* Using different version of source's schema
* Method templating: Methods are based on template who define what's will be used in the description. Ie. Json-rpc template will simplify request_body/response_body and provide a real errors cases
* Multiple responses: Provide a way for a request to have differents responses (like inheritances, or simplfyed/advanced responses....)
* Some methods does not reply always in json (in oAuth process for example)
* Reduce embedded size
    * Reduce (or eliminate) jquery
    * Minimize CSS and javascripts files


Licenses
--------

ApiDoc uses the following projects:

[Twitter Bootstrap](http://twitter.github.com/bootstrap)

[Jquery](http://jquery.org/)

[Icon Minia](http://dribbble.com/shots/598215-Icon-Minia-139-Vector-Icons)

[Entypo](http://www.entypo.com/)

[IcoMoon](http://keyamoon.com/icomoon/)



See Full Documentation
----------------------

[Documentation index](docs/source/index.rst)

[Installation guide](docs/source/install.rst)

[How to use the application](docs/source/usage.rst)

[Config's file format](docs/source/config.rst)

[Source's file format](docs/source/source.rst)

[Todo list](docs/source/todo.rst)