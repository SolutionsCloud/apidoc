Feature: Source config URI manipulation

    Scenario: Response code definition
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_codes:
                    - code: 200
                      message: OK
            """
         When a source_factory load this file
         Then the "response_codes" of method "a" contains a "200" for the version "v1"

    Scenario: Response code definition ordered by code
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_codes:
                    - code: 404
                      message: Not found
                    - code: 200
                      message: OK
            """
         When a source_factory load this file
         Then the "response_codes" of method "a" contains in order "200" then "404" for the version "v1"

    Scenario: Response code definition use default message
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    code: 300
                    response_codes:
                    - code: 200
                    - code: 300
            """
         When a source_factory load this file
         Then the "message" of response_codes "200" of method "a" for the version "v1" is "OK"
         Then the "message" of response_codes "300" of method "a" for the version "v1" is "Multiple Choices"
