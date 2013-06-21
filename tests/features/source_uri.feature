Feature: Source config URI manipulation

    Scenario: uri in method
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /a
            """
         When a source_factory load this file
         Then the "full_uri" of method "a" is "/a" for the version "v1"
          And the "absolute_uri" of method "a" is "/a" for the version "v1"

    Scenario: When an URI is specified in version, it will be used to compose the uris of methods
        Given a "yaml" source file containing
            """
            versions:
              v1:
                uri: /a
                methods:
                  a:
                    uri: /b
            """
         When a source_factory load this file
         Then the "full_uri" of method "a" is "/a/b" for the version "v1"
          And the "absolute_uri" of method "a" is "/a/b" for the version "v1"

    Scenario: When an URI is specified in versions, it will be used to compose the full_uri of methods
        Given a "yaml" source file containing
            """
            configuration:
              uri: /a
            versions:
              v1:
                uri: /b
                methods:
                  a:
                    uri: /c
            """
         When a source_factory load this file
         Then the "full_uri" of method "a" is "/a/b/c" for the version "v1"
          And the "absolute_uri" of method "a" is "/b/c" for the version "v1"

    Scenario: When an URI is not specified in version, the uris of method will ommited it
        Given a "yaml" source file containing
            """
            configuration:
              uri: /a
            versions:
              v1:
                methods:
                  a:
                    uri: /b
            """
         When a source_factory load this file
         Then the "full_uri" of method "a" is "/a/b" for the version "v1"
          And the "absolute_uri" of method "a" is "/b" for the version "v1"
