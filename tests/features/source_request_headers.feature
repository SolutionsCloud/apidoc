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

    Scenario: parameter sample for string
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    request_headers:
                      b:
                        type: string
                      c:
                        type: number
                      d:
                        type: bool
                      e:
                        type: const
                        value: str
                      f:
                        type: none
                      g:
                        type: the_type
                      h:
                        type: reference
                        reference: the_reference
                      i:
                        type: object
                        primary:
                          j:
                            type: string
                      k:
                        type: array
                        items:
                          type: string
                      l:
                        type: dynamic
                        items:
                          type: string

                reference:
                  the_reference:
                    type: string
                types:
                  the_type:
                    primary: string
            """
         When a source_factory load this file
         Then the "request_headers" of method "a" contains a sample "my_b" for parameter "b" for the version "v1"
         Then the "request_headers" of method "a" contains a sample "123" for parameter "c" for the version "v1"
         Then the "request_headers" of method "a" contains a sample "True" for parameter "d" for the version "v1"
         Then the "request_headers" of method "a" contains a sample "my_the_type" for parameter "g" for the version "v1"
         Then the "request_headers" of method "a" contains a sample "my_h" for parameter "h" for the version "v1"
         Then the "request_headers" of method "a" contains a sample "my_i" for parameter "i" for the version "v1"
         Then the "request_headers" of method "a" contains a sample "my_k" for parameter "k" for the version "v1"
         Then the "request_headers" of method "a" contains a sample "{'key2': 'sample', 'key1': 'my_l'}" for parameter "l" for the version "v1"
