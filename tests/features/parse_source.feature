Feature: Source config parsing

    Scenario: Parse an empty file
        Given a "yaml" source file containing
            """
            configuration:
              title: a
            """
         When a source_factory load this file
         Then the root contains "0" versions
          And the root contains "0" method's categories
          And the root contains "0" type's categories
          And the root contains "0" methods
          And the root contains "0" types

    Scenario: common file with method
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    category: b
            """
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "1" method's categories
          And the root contains "1" methods

    Scenario: common directory
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    category: b
            """
         When a source_factory load the directory containing this file
         Then the root contains "1" versions
          And the root contains "1" method's categories
          And the root contains "1" methods

    Scenario: Use a default method category
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
            """
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "1" method's categories
          And the root contains "1" methods

    Scenario: Share the same method category
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    category: b
                  c:
                    category: b
            """
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "1" method's categories
          And the root contains "2" methods

    Scenario: Common file with type
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    request_headers:
                      b:
                        type: a
                types:
                  a:
                    category: b
                    item:
                      type: string
            """
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "1" type's categories
          And the root contains "1" types

    Scenario: Use default type category
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    request_headers:
                      b:
                        type: a
                types:
                  a:
                    item:
                      type: string
            """
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "1" type's categories
          And the root contains "1" types

    Scenario: Share the same type category
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    request_headers:
                      b:
                        type: a
                      c:
                        type: c
                types:
                  a:
                    category: b
                    item:
                      type: string
                  c:
                    category: b
                    item:
                      type: string
            """
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "1" type's categories
          And the root contains "2" types

    Scenario: Ignore unused types
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
                types:
                  a:
                    category: b
                    item:
                      type: string
            """
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "0" type's categories
          And the root contains "0" types

    Scenario: Ignore undisplayed category
        Given a "yaml" source file containing
            """
            categories:
              a:
                display: false
            versions:
              v1:
                methods:
                  B:
                    category: a
            """
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "0" method's categories
          And the root contains "0" methods

    Scenario: Split files
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_codes:
                    - code: 200
            """
          And a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_codes:
                    - code: 300
                  b:
                    url /
            """
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "1" method's categories
          And the root contains "2" methods

 Scenario: extends
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
              v2:
                methods:
                  b:
                    uri: /
            """
         When a source_factory load this file
         Then the root contains "2" versions
          And the root contains "2" methods

    Scenario: multiVersionning of descriptions
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    description: b
              v2:
                methods:
                  a:
                    description: c
            """
         When a source_factory load this file
         Then the root contains "1" methods
          And the "description" of method "a" is "b" for the version "v1"
          And the "description" of method "a" is "c" for the version "v2"

    Scenario: Using argument
        Given a "yaml" source file containing
            """
            configuration:
              title: My ${name}
            """
          And a configuration with the argument "name" equals to "doc"
         When a source_factory load this file
         Then the title of the root is "My doc"

    Scenario: common file with method
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    category: b
            """
          And a configuration filtering the "versions" "v1" by "excludes"
         When a source_factory load this file
         Then the root contains "0" versions
          And the root contains "0" method's categories
          And the root contains "0" methods

    Scenario: common file with method
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    category: b
              v2:
                extends: v1
              v3:
                extends: v1
            """
          And a configuration filtering the "versions" "v1" by "includes"
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "1" method's categories
          And the root contains "1" methods

    Scenario: common file with method
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    category: b
            """
          And a configuration filtering the "categories" "b" by "excludes"
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "0" method's categories
          And the root contains "0" methods

    Scenario: common file with method
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    category: b
                  c:
                    category: d
                  e:
                    category: f
            """
          And a configuration filtering the "categories" "b" by "includes"
         When a source_factory load this file
         Then the root contains "1" versions
          And the root contains "1" method's categories
          And the root contains "1" methods