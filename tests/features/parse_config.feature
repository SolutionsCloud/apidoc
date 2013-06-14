Feature: Config file parsing

    Scenario: Parse an empty file
        Given a "yaml" config file containing
            """
            ---
            """
         when a config_factory load this file
         then the object_config returned contains "None" for the attribute "input.directories"
          and the object_config returned contains "None" for the attribute "input.files"
          and the object_config returned contains "None" for the attribute "filter.versions.includes"
          and the object_config returned contains "None" for the attribute "filter.versions.excludes"
          and the object_config returned contains "None" for the attribute "filter.categories.includes"
          and the object_config returned contains "None" for the attribute "filter.categories.excludes"
          and the object_config returned contains "stdout" for the attribute "output.location"
          and the object_config returned contains "default" for the attribute "output.template"
          and the object_config returned contains "local" for the attribute "output.componants"


    Scenario: Parse a minimal file
        Given a "yaml" config file containing
            """
            input:
              files:
                - ./sources/one.yml
            """
         when a config_factory load this file
         then the object_config returned contains "None" for the attribute "input.directories"
          and the object_config returned contains the files "['sources/one.yml']" for the attribute "input.files"
          and the object_config returned contains "None" for the attribute "filter.versions.includes"
          and the object_config returned contains "None" for the attribute "filter.versions.excludes"
          and the object_config returned contains "None" for the attribute "filter.categories.includes"
          and the object_config returned contains "None" for the attribute "filter.categories.excludes"
          and the object_config returned contains "stdout" for the attribute "output.location"
          and the object_config returned contains "default" for the attribute "output.template"
          and the object_config returned contains "local" for the attribute "output.componants"


    Scenario: Parse a json file
        Given a "json" config file containing
            """
            {
              "input": {
                "files": [
                  "./sources/one.yml"
                ]
              }
            }
            """
         when a config_factory load this file
         then the object_config returned contains the files "['sources/one.yml']" for the attribute "input.files"


    Scenario: Parse a special file
        Given a "yaml" config file containing
            """
            output:
              componants: remote
            """
         when a config_factory load this file
         then the object_config returned contains "remote" for the attribute "output.componants"


    Scenario: Parse a file with wrong attributes
        Given a "yaml" config file containing
            """
            wrong:
              fail: True
            """
         when a config_factory load this file
         then the object_config returned contains "None" for the attribute "input.directories"
          and the object_config returned contains "None" for the attribute "input.files"
          and the object_config returned contains "None" for the attribute "filter.versions.includes"
          and the object_config returned contains "None" for the attribute "filter.versions.excludes"
          and the object_config returned contains "None" for the attribute "filter.categories.includes"
          and the object_config returned contains "None" for the attribute "filter.categories.excludes"
          and the object_config returned contains "stdout" for the attribute "output.location"
          and the object_config returned contains "default" for the attribute "output.template"
          and the object_config returned contains "local" for the attribute "output.componants"


    Scenario: Parse a full file
        Given a "yaml" config file containing
            """
            input:
              directories:
                - ./sources
                - ./sources/sub
              files:
                - ./sources/one.yml
                - ./sources/two.yml
            filter:
              versions:
                includes:
                  - v1.0
                  - v1.1
                excludes:
                  - v2.0
                  - v2.1
              categories:
                includes:
                  - s1
                  - s2
                excludes:
                  - s3
                  - s4
              methods:
                includes:
                  - m1
                  - m2
                excludes:
                  - m3
                  - m4
            output:
              location: sample.html
              template: template/my.html
              componants: embedded
            """
         when a config_factory load this file
         then the object_config returned contains the files "['sources', 'sources/sub']" for the attribute "input.directories"
          and the object_config returned contains the files "['sources/one.yml', 'sources/two.yml']" for the attribute "input.files"
          and the object_config returned contains "['v1.0', 'v1.1']" for the attribute "filter.versions.includes"
          and the object_config returned contains "['v2.0', 'v2.1']" for the attribute "filter.versions.excludes"
          and the object_config returned contains "['s1', 's2']" for the attribute "filter.categories.includes"
          and the object_config returned contains "['s3', 's4']" for the attribute "filter.categories.excludes"
          and the object_config returned contains the file "sample.html" for the attribute "output.location"
          and the object_config returned contains the file "template/my.html" for the attribute "output.template"
          and the object_config returned contains "embedded" for the attribute "output.componants"
