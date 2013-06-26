Feature: Source config Body manipulation
#
#    Scenario: Type enum
#        Given a "yaml" source file containing
#            """
#            versions:
#              v1:
#                methods:
#                  a:
#                    response_body:
#                      type: b
#                types:
#                  b:
#                    description: c
#                    item:
#                      type: enum
#                      values:
#                      - e
#                      - f
#
#            """
#         When a source_factory load this file
#         Then the response body of method "a" is a "type" for the version "v1"
#
#    Scenario: Type referened
#        Given a "yaml" source file containing
#            """
#            versions:
#              v1:
#                methods:
#                  a:
#                    response_body:
#                      type: b
#                types:
#                  b:
#                    description: c
#                    item:
#                      type: reference
#                      reference: d
#                references:
#                  d:
#                    type: string
#
#            """
#         When a source_factory load this file
#         Then the response body of method "a" is a "type" for the version "v1"
#
#    Scenario: Reference typed
#        Given a "yaml" source file containing
#            """
#            versions:
#              v1:
#                methods:
#                  a:
#                    response_body:
#                      reference: d
#                types:
#                  b:
#                    description: c
#                    item:
#                      type: reference
#                      reference: d
#                references:
#                  d:
#                    type: b
#
#            """
#         When a source_factory load this file
#         Then the response body of method "a" is a "type" for the version "v1"