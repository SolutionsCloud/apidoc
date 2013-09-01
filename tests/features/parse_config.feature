Feature: Config file parsing

    Scenario: Parse an empty file
        Given a "yaml" config file containing
            """
            ---
            """
         When a config_factory load this file
         Then the object_config returned contains "None" for the attribute "input.locations"
          And the object_config returned contains "None" for the attribute "filter.versions.includes"
          And the object_config returned contains "None" for the attribute "filter.versions.excludes"
          And the object_config returned contains "None" for the attribute "filter.categories.includes"
          And the object_config returned contains "None" for the attribute "filter.categories.excludes"
          And the object_config returned contains "stdout" for the attribute "output.location"
          And the object_config returned contains "default" for the attribute "output.template"
          And the object_config returned contains "local" for the attribute "output.componants"


    Scenario: Parse a minimal file
        Given a "yaml" config file containing
            """
            input:
              locations:
                - ./sources/one.yml
            """
         When a config_factory load this file
         Then the object_config returned contains the files "['sources/one.yml']" for the attribute "input.locations"
          And the object_config returned contains "None" for the attribute "filter.versions.includes"
          And the object_config returned contains "None" for the attribute "filter.versions.excludes"
          And the object_config returned contains "None" for the attribute "filter.categories.includes"
          And the object_config returned contains "None" for the attribute "filter.categories.excludes"
          And the object_config returned contains "stdout" for the attribute "output.location"
          And the object_config returned contains "default" for the attribute "output.template"
          And the object_config returned contains "local" for the attribute "output.componants"


    Scenario: Parse a json file
        Given a "json" config file containing
            """
            {
              "input": {
                "locations": [
                  "./sources/one.yml"
                ]
              }
            }
            """
         When a config_factory load this file
         Then the object_config returned contains the files "['sources/one.yml']" for the attribute "input.locations"


    Scenario: Parse a special file
        Given a "yaml" config file containing
            """
            output:
              componants: remote
            """
         When a config_factory load this file
         Then the object_config returned contains "remote" for the attribute "output.componants"


    Scenario: Parse a file with wrong attributes
        Given a "yaml" config file containing
            """
            wrong:
              fail: True
            """
         When a config_factory load this file
         Then the object_config returned contains "None" for the attribute "input.locations"
          And the object_config returned contains "None" for the attribute "filter.versions.includes"
          And the object_config returned contains "None" for the attribute "filter.versions.excludes"
          And the object_config returned contains "None" for the attribute "filter.categories.includes"
          And the object_config returned contains "None" for the attribute "filter.categories.excludes"
          And the object_config returned contains "stdout" for the attribute "output.location"
          And the object_config returned contains "default" for the attribute "output.template"
          And the object_config returned contains "local" for the attribute "output.componants"


    Scenario: Parse a full file
        Given a "yaml" config file containing
            """
            input:
              locations:
                - ./sources
                - ./sources/sub
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
         When a config_factory load this file
         Then the object_config returned contains the files "['sources', 'sources/sub', 'sources/one.yml', 'sources/two.yml']" for the attribute "input.locations"
          And the object_config returned contains "['v1.0', 'v1.1']" for the attribute "filter.versions.includes"
          And the object_config returned contains "['v2.0', 'v2.1']" for the attribute "filter.versions.excludes"
          And the object_config returned contains "['s1', 's2']" for the attribute "filter.categories.includes"
          And the object_config returned contains "['s3', 's4']" for the attribute "filter.categories.excludes"
          And the object_config returned contains the file "sample.html" for the attribute "output.location"
          And the object_config returned contains the file "template/my.html" for the attribute "output.template"
          And the object_config returned contains "embedded" for the attribute "output.componants"
