Feature: Source config URI manipulation

    Scenario: Headers definition
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    request_headers:
                      content-type:
                        type: string
            """
         When a source_factory load this file
         Then the "request_headers" of method "a" contains a "content-type" for the version "v1"

    Scenario: parameter in ui are ordered by name
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    request_headers:
                      p1:
                        type: string
                      p2:
                        type: string
            """
         When a source_factory load this file
         Then the "request_headers" of method "a" contains in order "p1" then "p2" for the version "v1"
