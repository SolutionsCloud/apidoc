.. _config-page:

Config's File Format
====================

ApiDoc can be used with arguments in the command line or with a config file containing the list of options (or both arguments and config file)

The format of the config file can be either `YAML` or `JSON`, the extension of the file must be respectively `.yaml` (or `.yml`) or `.json`

Usage
-----

To use ApiDoc with a config file call the following arguments :

.. code-block:: console

    $ apidoc -c ./path-to-config.yaml

Sample
------

This is a minimalistic sample of a config file

.. code-block:: yaml

    input:
      locations:
        - ./sources/one.yml
    output:
      location: ./output/sample.html

Here is a basic sample of a config file

.. code-block:: yaml

    input:
      locations:
        - ./sources
        - ./sources2/one.yml
      arguments:
        url: api.sfr.com
    filter:
      versions:
        excludes:
          - v2
    output:
      location: ./output/sample.html
      componants: local
      template: default

.. _config-page-input:

input
-----

The section input defines where the source files are located. It contains three sub sections `locations` `validate` and `arguments`. The first subsection contains a list of directories or files and the third a list of arguments (or variables) which will be used by the source files (see :ref:`source-page-variable`). The validate flag define if the sources files should be validate by the json schema validator.
As for config files, the extensions of source files must be `.yaml` (or `.yml`) or `.json`. When a directory is specified in the `locations` subsection, all the source files (with a valid extension) contained in the directory (or in a sub directory) will be merged into a single virtual source file which will be used to generate the documentation (see :ref:`source-page`).
A config file must reference at least one input source file.

This is a full sample of the section input


.. code-block:: yaml

    input:
      locations:
        - ./project/api-sources
        - ../common-api/sources
        - ./project/api-v2-source/demo.yaml
        - ./project/api-v2-source/common.yaml
      validate: False
      arguments:
        url: api.sfr.com
        defaultVersion: v1

filter
------

The section filter provides a way to exclude or include versions and/or category in the rendered documentation. This section contains two sub sections : `versions` and `categories` which both contain two subsections `includes` and `excludes`. To include a specifique list of versions (or categories) and ignoring the others, specify these versions (or categories) in the `includes` subsection. To ignore a specific list of versions (or categories) and including the others, specify these versions (or categories) in the `exclude`subsection.
If the `filter` section is missing (or empty), all versions and sections will be displayed.
If the `versions` (or `categories`) subsection is missing (or empty), all versions (or categories) will be displayed.
If the `includes` subsection is missing (or empty), all but excluded versions (or categories) will be displayed.
If the `excludes` subsection  is missing (or empty), no versions (or categories) will be removed.

The excluded versions (and categories) will be removed at the end of the rendering process. If a displayed version (or category) extends an ignored version (or category), this version will be displayed normally.

Here is a full sample of a section filter


.. code-block:: yaml

    filter:
      versions:
        includes:
          - v1.0
          - v2.0
      categories:
        excludes:
          - Experiment
          - Draft

    filter:
      versions:
        excludes:
          - v3.0
      categories:
        include:
          - Authentication
          - Common

output
------

The section describes the format and the location of the rendered documentation. It contains three subsections: `location`, `template` and `componants`.
The `location` subsection defines the relative (or absolute) path to the file where ApiDoc will generate the documentation.
When the value is `stdout` the rendered result will be display on the standard output of the console. (Beware of using this mode with the command `analyse-watch`)
The `template` subsection defines the relative (or absolute) path to the template used to render the documentation. ApiDoc uses the template engine Jinja, for a full documentation `see the official site <http://jinja.pocoo.org/>`_.
When the value is `default` ApiDoc will use the default template.
The `componants` subsection defines where the assets (css, javascripts, images, fonts) are stored. The possible values are:

* `local`: The files are stored in the same folder as the output
* `embedded`: The files are embedded in the generated documentation
* `remote`: the generated documentation will reference remote assets using CDN or public repositories
* `without`: The files are not generated in documentation

The `layout` subsection defines the layout used by default template. The possible values are:

* `default`: Standard layout with header
* `content-only`: Layout without headers

This is a full sample of the section ouput

.. code-block:: yaml

    output:
      location: ./project/documentation.html
      componants: ./project/template/custom.html
      template: default
      layout: default