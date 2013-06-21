Feature: Source config extension

    Scenario: extends
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
              v2:
                extends: v1
            """
         When a source_factory load this file
         Then the root contains "1" methods
          And the changes status of method "a" is "new" for the version "v1"
          And the changes status of method "a" is "none" for the version "v2"

    Scenario: change a value in a extension
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
              v2:
                extends: v1
                methods:
                  a:
                    uri: /c
            """
         When a source_factory load this file
         Then the root contains "1" methods
          And the changes status of method "a" is "new" for the version "v1"
          And the changes status of method "a" is "updated" for the version "v2"

    Scenario: removed a method from an extension
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
              v2:
                extends: v1
                methods:
                  a:
                    removed: true
            """
         When a source_factory load this file
         Then the root contains "1" methods
          And the changes status of method "a" is "new" for the version "v1"
          And the changes status of method "a" is "deleted" for the version "v2"

    Scenario: extends multiple sources
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
              v2:
                methods:
                  a:
                    uri: /
                  b:
                    uri: /
              v3:
                extends:
                  - v1
                  - v2
            """
         When a source_factory load this file
         Then the root contains "2" methods
          And the changes status of method "a" is "new" for the version "v1"
          And the changes status of method "b" is "new" for the version "v2"
          And the changes status of method "a" is "none" for the version "v3"
          And the changes status of method "b" is "none" for the version "v3"

    Scenario: break inheritance in extension
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
              v2:
                extends: v1
                methods:
                  inherit: false
            """
         When a source_factory load this file
         Then the root contains "1" methods
          And the changes status of method "a" is "new" for the version "v1"
          And the changes status of method "a" is "deleted" for the version "v2"

    Scenario: do not break self inheritance in extension
       Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
              v2:
                extends: v1
                inherit: false
            """
         When a source_factory load this file
         Then the root contains "1" methods
          And the changes status of method "a" is "new" for the version "v1"
          And the changes status of method "a" is "none" for the version "v2"