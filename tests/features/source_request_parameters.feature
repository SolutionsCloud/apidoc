Feature: Source config URI manipulation

    Scenario: parameter in uri of method
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /a/{param}
                    request_parameters:
                      param:
                        type: string
            """
         When a source_factory load this file
         Then the "request_parameters" of method "a" contains a "param" for the version "v1"

    Scenario: parameter missing are hidden
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /a
                    request_parameters:
                      param:
                        type: string
            """
         When a source_factory load this file
         Then the "request_parameters" of method "a" does not contains a "param" for the version "v1"

    Scenario: parameter in uri of version
        Given a "yaml" source file containing
            """
            versions:
              v1:
                uri : /{version}
                methods:
                  a:
                    uri: /a
                    request_parameters:
                      version:
                        type: string
            """
         When a source_factory load this file
         Then the "request_parameters" of method "a" contains a "version" for the version "v1"

    Scenario: parameter in uri of configuration
        Given a "yaml" source file containing
            """
            configuration:
              uri: /{host}
            versions:
              v1:
                methods:
                  a:
                    uri: /a
                    request_parameters:
                      host:
                        type: string
            """
         When a source_factory load this file
         Then the "request_parameters" of method "a" contains a "host" for the version "v1"

    Scenario: parameter are ordered by position in uri
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /a/{p2}/{p1}
                    request_parameters:
                      p1:
                        type: string
                      p2:
                        type: string
            """
         When a source_factory load this file
         Then the "request_parameters" of method "a" contains in order "p2" then "p1" for the version "v1"
