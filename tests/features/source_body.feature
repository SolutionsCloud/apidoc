Feature: Source config Body manipulation

    Scenario: Response body None
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
            """
         When a source_factory load this file
         Then the "response_body" of method "a" is "null" for the version "v1"
          And the "request_body" of method "a" is "null" for the version "v1"

    Scenario: Body as string
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: string
                      optional: false
            """
         When a source_factory load this file
         Then the response body of method "a" is a "string" for the version "v1"
          And the response body sample of method "a" is "my_response" for the version "v1"

    Scenario: Body as enum
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: enum
                      values:
                      - A
                      - B
                      optional: false
            """
         When a source_factory load this file
         Then the response body of method "a" is a "enum" for the version "v1"
          And the response body sample of method "a" is "A" for the version "v1"

    Scenario: Body as number
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: number
            """
         When a source_factory load this file
         Then the response body of method "a" is a "number" for the version "v1"
          And the response body sample of method "a" is "123" for the version "v1"

    Scenario: Body as bool
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: bool
                  b:
                    response_body:
                      type: bool
                      sample: yes

            """
         When a source_factory load this file
         Then the response body of method "a" is a "bool" for the version "v1"
          And the response body sample of method "a" is "True" for the version "v1"
          And the response body sample of method "b" is "True" for the version "v1"

    Scenario: Body as none
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: none
            """
         When a source_factory load this file
         Then the response body of method "a" is a "none" for the version "v1"

    Scenario: Body as object
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: object
                      properties:
                        a:
                          type: string
              v2:
                methods:
                  a:
                    response_body:
                      type: object
                      properties:
                        a:
                          type: string
                        b:
                          type: number
            """
         When a source_factory load this file
         Then the response body of method "a" is a "object" for the version "v1"
          And the response body as object of method "a" contains a "a" for the version "v1"
          And the response body as object of method "a" contains a "b" for the version "v2"

    Scenario: Body as array
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: array
                      sample_count: 4
                      items:
                        type: string
              v2:
                methods:
                  a:
                    response_body:
                      type: array
                      items:
                        type: number
            """
         When a source_factory load this file
         Then the response body of method "a" is a "array" for the version "v1"
          And the response body sample of method "a" is "4" for the version "v1"

    Scenario: Body as dynamic
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: dynamic
                      items:
                        type: string
              v2:
                methods:
                  a:
                    response_body:
                      type: dynamic
                      items:
                        type: string
                      sample:
                        foo: bar
            """
         When a source_factory load this file
         Then the response body of method "a" is a "dynamic" for the version "v1"
          And the response body sample of method "a" is "{'key2': 'sample', 'key1': 'my_response'}" for the version "v1"
          And the response body sample of method "a" is "{'foo': 'bar'}" for the version "v2"

    Scenario: Body as const
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: const
                      value: b
                  b:
                    response_body:
                      type: const
                      const_type: number
                      value: 123
            """
         When a source_factory load this file
         Then the response body of method "a" is a "const" for the version "v1"
          And the response body sample of method "a" is "b" for the version "v1"
         Then the response body of method "b" is a "const" for the version "v1"
          And the response body sample of method "b" is "123" for the version "v1"

    Scenario: Body as reference
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: reference
                      reference: b
                references:
                  b:
                    type: string
            """
         When a source_factory load this file
         Then the response body of method "a" is a "string" for the version "v1"
          And the response body sample of method "a" is "my_response" for the version "v1"

    Scenario: Body as type
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    response_body:
                      type: b
                types:
                  b:
                    item:
                      type: string
                      sample: c
            """
         When a source_factory load this file
         Then the response body of method "a" is a "type" for the version "v1"
          And the response body sample of method "a" is "c" for the version "v1"

