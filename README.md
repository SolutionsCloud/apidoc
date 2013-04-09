ApiDoc
======

Summary
-------

ApiDoc is a documentation generator designe for API built with Python.
It's developed by Jérémy Derussé and [SFR](http://www.sfrbusinessteam.fr).

ApiDoc actually consists of a command line interface, maintained in a single repository and actually not documented.
By using this application you automatically require all of the necessary modules dependencies which are:

For core application

* PyYAML==3.10
* Jinja2==2.6
* pyinotify==0.9.4


For developpers who wants works on apidoc

* behave==1.2.2
* coverage==3.6
* mock==1.0.1
* nose==1.2.1
* distribute==0.6.28


Installation
------------

The fastest way to get started is by using the command line tool

```shell
sudo apt-get install python3 python3-setuptools
python3 setup.py install
```

For fast yaml file parsing, install libyaml (see http://pyyaml.org/wiki/PyYAML)


For developpers, it's strongly recommended to use `virtualenv`

```shell
pip install -r requirements-dev.txt
```



Running Tests
-------------

Two set of tests are imlpemented. Behaviours Test with `behave` and UnitTests with `unittest`

BehavioursTest

```shell
behave tests/features
```

UnitTess

```shell
nosetests --with-coverage --cover-package=apidoc --cover-package=util --cover-erase --cover-html
```


Using the Application
-------------

The application analyse provide a way to check configuration files

```shell
bin/analyse -h
```

The application analyse build the full documentation

```shell
bin/build -h
```

Generate documentation from a source file

```shell
bin/build -f ./example/source_simple/simple.yml
```

Split sources in multiple files

```shell
bin/build -f ./example/source_multiple/one.yml ./example/source_multiple/two.yml
```

Generate documentation from files contained in a directory

```shell
bin/build -d ./example/source_multiple/
```

Generate documentation with options definied in a config file

```shell
bin/build -c ./example/config/config.yaml
```

Mix everything

```shell
bin/build -c ./config.yaml -d ./folder1/ ./folder2/ -f /folder3/file.yaml /folder3/file.json
```

TODO
----

* RunMode: The user can run the methods through his browser
* Diff: Provide a diff file between versions
* Variable: Some parts of the sources can refered to variables defined in the source file or injected when the document is builded
